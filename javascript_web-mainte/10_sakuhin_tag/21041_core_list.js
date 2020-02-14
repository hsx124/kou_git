var CoreListController = function() {};
CoreListController.prototype = new AbstractController();

/**
 * メニュー選択処理
 */
CoreListController.prototype.selectedMenu = function() {
    return '.core-list';
};

/**
 * イベント登録処理
 */
CoreListController.prototype.bindEvent = function() {
    var self = this;

    // 新規登録ボタン
    $('.create-button').on('click', function() {
        window.location.href = '/admin_app/core_create/';
    });

    // 更新履歴DLエリアのイベント設定
    NoticeTableUtil.setDLArea();

    // 更新履歴CSVダウンロード
    NoticeTableUtil.downloadTableCsv('m_core', 'コア情報');

    // CSVダウンロード
    self.downloadCsv();

    // コアマスタ一覧生成
    self.selectCoreList();

    return $.Deferred().resolve().promise();
};

/**
 * コアマスタ検索 (ajaxでコア一覧検索結果を取得)
 */
CoreListController.prototype.selectCoreList = function() {
    var self = this;
    var param = {
        'core' : 'core-list'
    };
    AjaxUtil.get('/admin_app/core_list/', param, function(data) {
        self.searchResultCallback(data);
    });
}

/**
 * ajaxでコア一覧検索結果を処理
 */
CoreListController.prototype.searchResultCallback = function(data) {
    var self = this;
    var result = JSON.parse(data.toString());

    // データエスケープ処理
    Escape.escapeHtml(result);

    // コアマスタ一覧の表を描画
    self.createCoreList(result);
}

/**
 * コアマスタ一覧の表を描画する
 */
CoreListController.prototype.createCoreList = function(result) {
    var self = this;

    // 一覧データが10以下の場合は高さ自動調整
    var height = 'auto';
    if (result.length >= 10) {
        height = 450;
    }
    // グリッドを再描画
    if ($('#gbox_list-grid').is(':visible')) {
        $('#list-grid').jqGrid('clearGridData').trigger('reloadGrid');
        $('#list-grid').jqGrid('setGridHeight', height).trigger('reloadGrid');
        $('#list-grid').jqGrid('setGridParam', {
            data : result,
        }).trigger('reloadGrid');
    }else{
        // グリッド生成
        var colModel = self.createColModel();
        var option = {
            colNames: colModel.name,
            colModel: colModel.model,
            data: result,
            width: $('#list').width(),
            height : height,
            pager: '#pager',
            loadComplete: self.gridBtnEvent,
            pgbuttons : false,
            pginput : false,
            viewrecords : true,
            rowList : result.length,
            rowNum : result.length
        };
        // グリッドを描画
        GridUtil.renderNormalGrid('#list-grid', option, true);
    }
};

/**
 * jQGrid用のカラム定義
 */
CoreListController.prototype.createColModel = function() {
    var width = $('#list').width();

    var modelArray = [];
    modelArray.push(
        GridUtil.createColModel({
            name: 'core_code',
            width: width * 0.2
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'core_name',
            width: width * 0.2,
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'update_user',
            width: width * 0.1,
            align: 'left',
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'update_time',
            width: width * 0.1,
            align: 'left',
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
            width: width * 0.07,
            align: 'center',
            formatter: function(val, opt, rdt) {
                return (
                    '<button type="button" class="grid-btn-update" data-core-code="' + rdt.core_code + '">' + '編集' +'</button>'
                    + '<button type="button" class="grid-btn-delete" data-core-name="' + rdt.core_name
                    + '" data-core-code="' + rdt.core_code + '" data-row-id="' + opt.rowId + '">' + '削除' + '</button>'
                    );
                },
            sortable: false
        })
    );
    return {
        model: modelArray,
        name: ['コアコード','コア名','最終更新者', '最終更新日時', 'データ操作']
    };
};

/**
 * jQGrid用のボタンイベント定義
 */
CoreListController.prototype.gridBtnEvent = function(data) {
    var self = this;
    $('.grid-btn-delete, .grid-btn-update').button();

    // 編集ボタンをクリックし、編集画面へ遷移する
    $('.grid-btn-update').on('click', function() {
        var button = $(this);
        // コアコードを取得
        var coreCode = button.attr('data-core-code');
        // コア編集画面へ遷移
        window.location.href = '/admin_app/core_update?corec=' + coreCode;
    });

    $('.grid-btn-delete').off('click');
    // 削除ボタンをクリックし、削除処理を行う
    $('.grid-btn-delete').on('click', function() {
        var button = $(this);
        $('#delete-core-code').text(button.attr('data-core-code'));
        $('#delete-core-name').text(button.attr('data-core-name'));
        var modal = $('#delete-confirm-dialog');

        // 削除キャンセル処理
        $('.cancel-botton').on('click', function() {
            modal.dialog('close');
            $('.delete-button').off('click');
        });

        // ajaxで、削除処理を行う
        $('.delete-button').on('click', function() {
            var param = {
                'delete-core-code' : $('#delete-core-code').text(),
                'delete-core-name' : $('#delete-core-name').text(),
            };
            AjaxUtil.post('/admin_app/core_list/', param, function(data) {

                var result = JSON.parse(data.toString());

                if(result.is_error){
                    // 削除メッセージ表示
                    MsgUtil.showStatusMsg('#list', $('#delete-core-name').text() , '既に削除');
                }else{
                    // 削除メッセージ表示
                    MsgUtil.showStatusMsg('#list', $('#delete-core-name').text() , '削除');
                }

                // データエスケープ処理
                Escape.escapeHtml(result.core_list);

                // コアマスタ一覧の表を再描画
                CoreListController.prototype.createCoreList(result.core_list);

            });
            modal.dialog('close');

            $('.delete-button').off('click');
        });

        modal.dialog({
            modal: true,
            width: '600px'
        });
    });
};

/**
 * CSVダウンロードイベント追加
 */
CoreListController.prototype.downloadCsv = function() {
    var self = this;

    // CSVダウンロード全件
    $('#csv-all').click(function() {
        AjaxUtil.get('/admin_app/core_list/csv_download/', {}, function(data) {
            var fileName = 'コア情報_全件.csv';
            FileUtil.outputCsv(data, fileName);
        });
    });
}

$(function() {
    var controller = new CoreListController();
    controller.init();
});
