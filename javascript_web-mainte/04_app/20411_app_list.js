var AppListController = function() {};
AppListController.prototype = new AbstractController();

/**
 * アプリマスタ一覧画面の主処理
 */
AppListController.prototype.execute = function() {
    var self = this;

    return $.Deferred()
        .resolve()
        .promise();
};

/**
 * メニュー選択処理
 */
AppListController.prototype.selectedMenu = function() {
    return '.app-list';
};

/**
 * イベント登録処理
 */
AppListController.prototype.bindEvent = function() {
    var self = this;

    // 新規登録ボタン
    $('.create-button').on('click', function() {
        var ipcode = $('input[name="ip-list"]:checked').val()
        window.location.href = '/admin_app/app_create?ipc=' + ipcode;
    });

    // 更新履歴DLエリアのイベント設定
    NoticeTableUtil.setDLArea();

    // 更新履歴CSVダウンロード
    NoticeTableUtil.downloadTableCsv('m_mobile_app', 'アプリマスタ');

    // IPコード検索
    self.searchIpbyIpCode();

    // IP名検索
    self.searchIpbyIpName();

    // CSVダウンロード
    self.downloadCsv();

    return $.Deferred()
        .resolve()
        .promise();
};

/**
 * アプリ一覧生成<br>
 * jQGridを使用して表を描画する。
 */
AppListController.prototype.createAppList = function(djangoObj) {
    var self = this;

    if ($('#gbox_list-grid').is(':visible')) {
        $('#list-grid').jqGrid('clearGridData').trigger('reloadGrid');
        $('#list-grid').jqGrid('setGridParam', {
            data : djangoObj,
        }).trigger('reloadGrid');

    } else {
        var colModel = self.createColModel();
        var option = {
            colNames : colModel.name,
            colModel : colModel.model,
            data : djangoObj,
            width : $('#list').width(),
            pager : '#pager',
            loadComplete : self.gridBtnEvent
        };
        // グリッド生成
        GridUtil.renderNormalGrid('#list-grid', option, true);
    }
};

/**
 * jQGrid用のカラム定義
 */
AppListController.prototype.createColModel = function() {
    var width = $('#list').width();

    var modelArray = [];
    modelArray.push(
        GridUtil.createColModel({
            name: 'app_name',
            width: width * 0.23
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'app_id_android',
            width: width * 0.08,
            align: 'center',
            formatter: GridUtil.formatMaruBatsu,
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'app_id_ios',
            width: width * 0.08,
            align: 'center',
            formatter: GridUtil.formatMaruBatsu,
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'distributor_name',
            width: width * 0.15
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'start_date',
            width: width * 0.08,
            formatter : 'date',
            formatoptions : {
                srcformat : 'Y-m-d',
                newformat : 'Y/m/d'
            }
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'end_date',
            width: width * 0.08,
            formatter : 'date',
            formatoptions : {
                srcformat : 'Y-m-d',
                newformat : 'Y/m/d'
            }
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'update_user',
            width: width * 0.08
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'update_date',
            width: width * 0.07,
            formatter : 'date',
            formatoptions : {
                srcformat : 'ISO8601Long',
                newformat : 'Y/m/d'
            }
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            title: false,
            name: 'operation',
            width: width * 0.1,
            align: 'center',
            formatter: function(val, opt, rdt) {
                return (
                    '<button type="button" class="grid-btn-update" data-ip-code="' +rdt.ip_code +'" data-app-name="' + rdt.app_name + '">' +'編集' +'</button>'
                    + '</button>' + '<button type="button" class="grid-btn-delete" data-ip-code="' + rdt.ip_code + '" data-app-name="' + rdt.app_name + '"data-row-id="' + opt.rowId + '">' + '削除' + '</button>'
                );
            },
            sortable: false
        })
    );
    return {
        model: modelArray,
        name: ['アプリ名', 'Android', 'iOS', '販売元', 'サービス開始年月日', 'サービス終了年月日', '最終更新者', '最終更新日時', 'データ操作']
    };
};

/**
 * jQGrid用のボタンイベント定義
 */
AppListController.prototype.gridBtnEvent = function(data) {
    var local = data;

    // 編集ボタン
    $('.grid-btn-update').button();
    $('.grid-btn-update').on('click', function() {
        var button = $(this);
        var ipCode = button.attr('data-ip-code');
        var appName = button.attr('data-app-name');

        window.location.href = '/admin_app/app_update?ipc='+ipCode + '&app_name=' + appName;
    });

    // 削除ボタン
    $('.grid-btn-delete').button();
    $('.grid-btn-delete').off('click');
    $('.grid-btn-delete').on('click', function() {
        var button = $(this);
        var rowId = button.attr('data-row-id');
        $('#delete-app').text(button.attr('data-app-name'));

        var modal = $('#delete-confirm-dialog');
        $('.cancel-botton').on('click', function() {
            modal.dialog('close');
            $('.delete-button').off('click');
        });
        $('.delete-button').on('click', function() {
            var param = {
                'reload-ipcode' : $("input[name='ip-list']:checked").val(),
                'delete-app' : $('#delete-app').text(),
            };
            AjaxUtil.post('/admin_app/app_list/', param, function(data) {
                var result = JSON.parse(data.toString());

                // グリッド描画
                AppListController.prototype.createAppList(result);

                // 削除メッセージ表示
                MsgUtil.showStatusMsg('#grid-area', $('#delete-app').text() , '削除');
            });
            modal.dialog('close');

            $('.delete-button').off('click');
        });
        modal.dialog({
            modal: true,
            width: '600px'
        });
    });
}


/**
 * IP検索時のコールバック処理
 *
 * @param data
 *            非同期通信結果
 */
AppListController.prototype.searchResultCallback = function(data) {
    var self = this;
    var result = JSON.parse(data.toString());

    // IP選択ボタン生成
    self.createIpSelect(result)

    // IP選択時にグリッド生成イベント付与
    self.createGrid()

    $('.ipname-result').slideDown('slow');

    // 検索結果表示位置までスクロール
    var position = $('.ipname-result').offset().top -300;
    $('html,body').animate({
        scrollTop : position}
        ,1000
    );
};
/**
 * IPコード検索<br>
 * ajaxでIPコード検索結果を取得
 */
AppListController.prototype.searchIpbyIpCode = function() {
    var self = this;

    // IPコード検索ボタン
    $('#search_ipcode_button').click(function(event) {

        // グリッド非表示
        $('.search-list').slideUp('slow');
        setTimeout(function() {
            $('#list-grid').GridUnload();
        }, 500);

        // エラーメッセージ削除
        $('.input-err').removeClass('input-err');
        $('.input-err-msg').remove();

        // 入力チェックエラーの場合、検索を行わない
        // if (!InputCheckUtil.checkIpCode()) {
        //     return;
        // }

        // IPコードの場合、コード決めうちなので10桁半角英数以外は拒否する。
        var param = {
            'input-ipcode' : $('#input-ipcode').val()
        };
        AjaxUtil.get('/admin_app/app_list/', param, function(data) {
            self.searchResultCallback(data);
        });
    });
}

/**
 * IP名検索<br>
 * ajaxでIP名検索結果を取得
 */
AppListController.prototype.searchIpbyIpName = function() {
    var self = this;
    // IPコード検索ボタン
    $('#search_ipname_button').click(function(event) {

        // グリッド非表示
        $('.search-list').slideUp('slow');
        setTimeout(function() {
            $('#list-grid').GridUnload();
        }, 500);

        // エラーメッセージ削除
        $('.input-err').removeClass('input-err');
        $('.input-err-msg').remove();

        // 入力チェックエラーの場合、検索を行わない
        if (!InputCheckUtil.checkIpName()) {
            return;
        }

        // IPコードの場合、コード決めうちなので10桁半角英数以外は拒否する。
        var param = {
            'input-ipname' : $('#input-ipname').val()
        };
        AjaxUtil.get('/admin_app/app_list/', param, function(data) {
            self.searchResultCallback(data);
        });
    })
}

/**
 * IP名選択（ラジオボタン）生成<br>
 */
AppListController.prototype.createIpSelect = function(data) {
    var self = this;

    // IP選択ボタン削除
    $('#ip-search-result').children().remove();

    // 検索件数が0件の場合、ラジオ生成しない
    if (data.length) {
        // ラジオボタン生成
        for (var i = 0; i < data.length; i++) {
            var $radio = $('<label for="radio' + i + '"></label>');
            $radio.text(data[i].ip_code + ':' + data[i].ip_name);
            $radio.append('<input type="radio" name="ip-list" id="radio' + i + '" value="' + data[i].ip_code + '">');
            $radio.append('<input type="hidden" id="' + data[i].ip_code + '" value="' + data[i].ip_name + '">');
            $('#ip-search-result').append($radio);
        }
        // ラジオボタンにjQueryUIのスタイルを適応
        self.setJqueryUI();

        // ラジオボタンを縦に配置
        $(".controlgroup-vertical").controlgroup({
            "direction" : "vertical"
        });
    } else {
        $('#ip-search-result').append('<div>検索条件に該当するIPが見つかりませんでした。</div>');
    }

}

/**
 * グリッド生成<br>
 */
AppListController.prototype.createGrid = function() {

    var self = this;
    // グリッド生成
    $('input[name="ip-list"]').on('change', function() {
        var param = {
            'ip-list' : $(this).val()
        };
        setTimeout(function() {
            AjaxUtil.get('/admin_app/app_list/', param, function(data) {
                var result = JSON.parse(data.toString());
                // グリッド描画
                self.createAppList(result);
                $('.search-list').slideDown('slow');

                // グリッド表示位置までスクロール
                var position = $('.search-list').offset().top -300;
                $('html,body').animate({
                    scrollTop : position}
                    ,1000
                );
            });
        }, 1000);

    });
}

/**
 * CSVダウンロードイベント追加
 */
AppListController.prototype.downloadCsv = function() {

    var self = this;

    // CSVダウンロード全件
    $('#csv-all').click(function() {
        AjaxUtil.get('/admin_app/app_list/csv_download/', {}, function(data) {
            var fileName = 'アプリマスタ_全件.csv';
            FileUtil.outputCsv(data, fileName);
        });
    });

    // CSVダウンロードIP毎
    $('#csv-ip').click(function() {

        var value = $('input[name="ip-list"]:checked').val();
        var param = {
            'ip-list' : value
        };
        AjaxUtil.get('/admin_app/app_list/csv_download/', param, function(data) {
            var ipName = $('#' + value).val();
            var fileName = 'アプリマスタ_' + ipName + '.csv';
            FileUtil.outputCsv(data, fileName);
        });
    });
}

$(function() {
    var controller = new AppListController();
    controller.init();
});
