//////////////////////////////////////////////////////////
// 画面制御を行う抽象コントローラクラス
//////////////////////////////////////////////////////////
var AbstractController = function() {
};
AbstractController.prototype = {
    /**
     * 初期処理
     */
    init : function() {
        var self = this;

        window.onerror = function(e) {
            // 予期せぬエラー
            self.createErrMsg(e);
        };

        // Google Analytics用の設定
        self.ga();

        // ヘッダー描画処理
        self.createHeader().then(function() {
            // メニュー描画処理
            return self.createMenu();
        }).then(function() {
            // フッター描画
            return self.createFooter();
        }).then(function() {
            // 画面の主処理
            return self.execute();
        }).then(function() {
            // レイアウト設定
            self.setLayout();
            // イベント登録
            return self.bindEvent();
        }).fail(function(errorInfo) {
            // 処理中にrejectされた時の処理
            self.createErrMsg(errorInfo);
        });
    },

    /**
     * Google Analytics用の設定
     */
    ga : function() {
        // tag:グローバル変数
        if (tag) {
            (function(i, s, o, g, r, a, m) {
                i['GoogleAnalyticsObject'] = r;
                i[r] = i[r] || function() {
                    (i[r].q = i[r].q || []).push(arguments)
                }, i[r].l = 1 * new Date();
                a = s.createElement(o), m = s.getElementsByTagName(o)[0];
                a.async = 1;
                a.src = g;
                m.parentNode.insertBefore(a, m)
            })(window, document, 'script', '//www.google-analytics.com/analytics.js', 'ga');

            ga('create', tag);
            ga('send', 'pageview');
        }

        $(document).ajaxSuccess(function(event, xhr, settings) {
            if (tag) {
                var url = location.pathname;
                var param = settings.data
                ga('send', 'pageview', url + '?' + param);
            }
        });
    },

    /**
     * ヘッダー描画処理
     */
    createHeader : function() {
        var promise = $.Deferred();
        $('#header').ready(function() {
            promise.resolve();
            $(".contents").css("display", "block");
        });
        return promise.promise();
    },

    /**
     * メニューバー描画処理
     */
    createMenu : function() {
        var self = this;
        var promise = $.Deferred();

        $('#header').ready(function() {

            var selector = self.selectedMenu();
            if (selector) {
                $(self.selectedMenu()).addClass('selected');
            }

            $(".search").hover(function() {
                $("ul.child").stop().slideDown();
            }, function() {
                $("ul.child").stop().slideUp();
            });

            promise.resolve();
        });
        return promise.promise();
    },

    /**
     * 画面レイアウト設定
     */
    setLayout : function() {
        TextfollowUtil.execute('keyword_search_icon');
        $('#contents').css('display', 'table-cell');
        $('#body').css('display', 'table');
    },

    /**
     * フッター描画処理
     */
    createFooter : function() {
        var promise = $.Deferred();
        var footer = '<div class="boder"></div>';
        $('#footer').append(footer).ready(function() {
            promise.resolve();
        });
        return promise.promise();
    },

    /**
     * エラーメッセージ描画処理
     */
    createErrMsg : function(errorObject) {
        $('#contents').css('display', 'table-cell');
        $('#body').css('display', 'table');

        // コンテンツ欄を削除
        $('.contents').empty();

        var errorInfo;
        if (errorObject instanceof TypeError) {
            errorInfo = new ErrorInfo(errorObject);
        } else if (errorObject instanceof ErrorInfo) {
            errorInfo = errorObject;
        } else {
            errorInfo = new ErrorInfo();
            if (errorObject) {
                errorInfo.setMsgDetail('' + errorObject);
            }
        }

        var msg = errorInfo.msg;
        var msgDetail = errorInfo.msgDetail;
        var errMsgArea = $('<div class="error-msg"></div>');
        errMsgArea.append(msg);
        errMsgArea.append('<br>');
        errMsgArea.append('エラー詳細：' + msgDetail);
        $('.contents').append(errMsgArea);
    },

    /**
     * 画面の主処理<br>
     * 継承して処理を実装する
     */
    execute : function() {
        return $.Deferred().resolve().promise();
    },

    /**
     * メニュー選択処理<br>
     * 継承して処理を実装する
     */
    selectedMenu : function() {
        return null;
    },
    /**
     * イベント登録処理<br>
     * 継承して処理を実装する
     */
    bindEvent : function() {
        return $.Deferred().resolve().promise();
    }
};

// ////////////////////////////////////////////////////////
// エラー情報
// ////////////////////////////////////////////////////////
var ErrorInfo = function(e) {
    if (e) {
        this.exception = e;
        this.msgDetail = e.message;
    } else {
        this.exception = null;
        this.msgDetail = '';
    }
    this.msg = '予期せぬエラーが発生しました。';
};
ErrorInfo.prototype = {
    /**
     * エラーメッセージ設定
     */
    setMsg : function(msg) {
        this.msg = msg;
    },
    /**
     * エラーメッセージ詳細設定
     */
    setMsgDetail : function(msgDetail) {
        this.msgDetail = msgDetail;
    }
};

/**
 * 非同期通信を行うユーティリティクラス
 */
var AjaxUtil = {

    ajax : function(option) {
        $.ajax(option);
    },

    /**
     * GETメソッドを使用して非同期通信を行う<br>
     *
     * @param url
     *            非同期通信を行うURL
     * @param data
     *            送信データ
     * @param callback
     *            非道通信成功時のコールバック
     */
    get : function(url, data, callback) {

        var promise = $.Deferred();
        var token = AjaxUtil.getToken();

        if (AjaxUtil.check(token)) {

            data['csrfmiddlewaretoken'] = token;
            AjaxUtil.ajax({
                url : url,
                method : 'GET',
                data : data,
                timeout : 10000,
                dataType : 'text',
                success : callback,
                complete : function(xhr, status) {
                    promise.resolve(xhr, status);
                },
            })

            return promise.promise();
        } else {
            return promise.reject().promise();
        }
    },

    /**
     * POSTメソッドを使用して非同期通信を行う<br>
     *
     * @param url
     *            非同期通信を行うURL
     * @param data
     *            送信データ
     * @param callback
     *            非道通信成功時のコールバック
     */
    post : function(url, data, callback) {

        var promise = $.Deferred();
        var token = AjaxUtil.getToken();

        if (AjaxUtil.check(token)) {

            data['csrfmiddlewaretoken'] = token;
            AjaxUtil.ajax({
                url : url,
                method : 'POST',
                data : data,
                timeout : 10000,
                dataType : 'text',
                success : callback,
                complete : function(xhr, status) {
                    promise.resolve(xhr, status);
                },
            })

            return promise.promise();
        } else {
            return promise.reject().promise();
        }

    },

    check : function(token) {
        if (token === null || token === undefined || token === '') {
            console.log('CSRFトークンが画面に設定されていません。');
            console.log('非同期通信を中止します。');
            return false;
        } else {
            return true;
        }
    },

    getToken : function() {
        return $('[name=csrfmiddlewaretoken]').val();
    },
}

var TransitionUtil = {
    transition : function(url) {
        if (url.match(/static\/ipdds_app\/file/)) {
            window.open(url, '_blank');
        } else if (url.match(/ipdds/)) {
            window.location.href = url;
        } else {
            window.open(url, '_blank');
        }
    }
}