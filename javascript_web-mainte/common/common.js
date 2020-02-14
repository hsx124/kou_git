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
        // メニュー描画処理
        self.createMenu().then(function() {
            // フッター描画
            return self.createFooter();
        }).then(function() {
            // レイアウト設定
            self.setLayout();
            self.setJqueryUI();
            // 画面の主処理
            return self.execute();
        }).then(function() {
            // イベント登録
            return self.bindEvent();
        }).fail(function(errorInfo) {
            // 処理中にrejectされた時の処理
            self.createErrMsg(errorInfo);
        });
    },

    /**
     * メニュー描画処理
     */
    createMenu : function() {
        var self = this;
        var promise = $.Deferred();
        $('#menu').css({
            height : $(window).height() - 185
        });

        $('.sub-menu').hide();
        $('.main-menu').on('click', function() {
            var elem = $(this);
            var menu = elem.parent().find(".sub-menu");
            if (menu.is(":hidden")) {
                menu.slideDown('slow');
            } else {
                menu.slideUp('slow');
            }
        });

        var selector = self.selectedMenu();
        if (selector) {
            var selected = $(self.selectedMenu());
            selected.addClass('selected');
            selected.parent().show();

        }
        return promise.resolve();
    },

    /**
     * 画面レイアウト設定
     */
    setLayout : function() {
        $('#contents').css('display', 'table-cell');
        $('#body').css('display', 'table');
    },

    /**
     * jQueryUI設定
     */
    setJqueryUI : function() {
        $('input[type=text],textarea').addClass('ui-textfield ui-widget ui-widget-content ui-corner-all');
        $('.search-button').button();
        $('.dialog-button').button();
        $('input[type=radio]').checkboxradio();
        $('select').selectmenu();
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
                timeout : 300000,
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

// ////////////////////////////////////////////////////////
// ファイル操作ユーティリティクラス
// ////////////////////////////////////////////////////////
var FileUtil = {
    /**
     * CSV出力<br>
     */
    outputCsv : function(data, fileName) {
        var downloadData = new Blob([ data ], {
            type : 'text/csv'
        });

        // ファイルのダウンロードにはブラウザ毎に処理を分けます
        if (window.navigator.msSaveBlob) { // for IE
            window.navigator.msSaveBlob(downloadData, fileName);
        } else {
            var downloadUrl = (window.URL || window.webkitURL).createObjectURL(downloadData);
            var link = document.createElement('a');
            link.href = downloadUrl;
            link.download = fileName;
            link.click();
            (window.URL || window.webkitURL).revokeObjectURL(downloadUrl);
        }
    }
}
// ////////////////////////////////////////////////////////
// メッセージユーティリティクラス
// ////////////////////////////////////////////////////////
var MsgUtil = {
    /**
     * ステータスメッセージ表示<br>
     */
    showStatusMsg : function(prependId, targetName, status) {

        // 既に表示されているメッセージを削除
        $('#status-msg').remove();

        // Div生成
        var divStatusMsg = $('<div id="status-msg" class="status-msg"></div>');

        // 削除時色変更
        var color = 'orange'
        if ('削除' === status) {
            color = 'blue';
            divStatusMsg.addClass('delete-msg');
        }else if('既に削除' === status||'強制解除'){
            color = 'red';
            divStatusMsg.addClass('submit-error-msg');
        }

        divStatusMsg.append('<span class="ui-icon ui-icon-circle-check ui-icon-' + color + '"></span>');
        if('既に削除' === status||'強制解除'=== status){
            divStatusMsg.append('『<spanid="target-name">' + targetName + '</span>』は<span id="edit-status">' + status + '</span>されています。')
        }else{
            divStatusMsg.append('『<spanid="target-name">' + targetName + '</span>』を<span id="edit-status">' + status + '</span>しました。')
        }

        // 画面要素に付与。
        $(prependId).prepend(divStatusMsg);
    }
};

// ////////////////////////////////////////////////////////
// 一覧データエスケープ処理
// ////////////////////////////////////////////////////////
var Escape = {
    /**
     * データエスケープ処理を行う<br>
     *
     * @param result
     *            データエスケープ対象データList
     */
    escapeHtml : function (result) {
        result.forEach(function(obj, index){
            for(var key in obj){
                if(typeof obj[key] == 'string') {
                    obj[key] = obj[key].replace(/[&'`"<>]/g, function(match) {
                        return {
                        '&': '&amp;',
                        "'": '&#x27;',
                        '`': '&#x60;',
                        '"': '&quot;',
                        '<': '&lt;',
                        '>': '&gt;',
                        }[match]
                    });
                }

            };
        });
    },

    /**
     * データエスケープ処理を行う<br>
     *
     * @param result
     *            データエスケープ対象データ
     */
    escapeString : function (result) {
        return result.replace(/[&'`"<>]/g, function(match) {
            return {
            '&': '&amp;',
            "'": '&#x27;',
            '`': '&#x60;',
            '"': '&quot;',
            '<': '&lt;',
            '>': '&gt;',
            }[match]
        });
    }

};
