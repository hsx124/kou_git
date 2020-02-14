var PublisherListController = function() {};
PublisherListController.prototype = new AbstractController();

/**
 * メニュー選択処理
 */
PublisherListController.prototype.selectedMenu = function() {
    return '.publisher-list';
};

/**
 * イベント登録処理
 */
PublisherListController.prototype.bindEvent = function() {
    var self = this;

    // 新規登録ボタン
    $('.create-button').on('click', function() {
        window.location.href = '/admin_app/publisher_create/';
    });

    // 更新履歴DLエリアのイベント設定
    NoticeTableUtil.setDLArea();

    // 更新履歴CSVダウンロード
    NoticeTableUtil.downloadTableCsv('m_publisher', '出版社情報');

    // 出版社マスタCSVダウンロード
    self.downloadCsv();

    // 出版社マスタ一覧生成
    self.selectPublisherList();

    return $.Deferred().resolve().promise();
};

/**
 * 出版社マスタ検索 (ajaxで出版社一覧検索結果を取得)
 */
PublisherListController.prototype.selectPublisherList = function() {
    var self = this;
    var param = {
          'publisher' : 'publisher-list'
      };
    AjaxUtil.get('/admin_app/publisher_list/', param, function(data) {
        self.searchResultCallback(data);
    });
}

/**
 * ajaxで出版社一覧検索結果を処理
 */
PublisherListController.prototype.searchResultCallback = function(data) {
    var self = this;
    var result = JSON.parse(data.toString());

    // データエスケープ処理
    Escape.escapeHtml(result);
    // 出版社マスタ一覧の表を描画
    self.createPublisherList(result);
}

/**
 * 出版社マスタ一覧の表を描画する
 */
PublisherListController.prototype.createPublisherList = function(result) {
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
        // グリッドを初期描画
        GridUtil.renderNormalGrid('#list-grid', option, true);
    }
};

/**
 * jQGrid用のカラム定義
 */
PublisherListController.prototype.createColModel = function() {
    var width = $('#list').width();

    var modelArray = [];
    modelArray.push(
        GridUtil.createColModel({
            name: 'publisher_code',
            width: width * 0.1
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'publisher_name',
            width: width * 0.2
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'update_user',
            width: width * 0.1
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'update_time',
            width: width * 0.1,
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
                    '<button type="button" class="grid-btn-update" data-publisher-code="' + rdt.publisher_code + '">' + '編集' +'</button>'
                    + '<button type="button" class="grid-btn-delete" data-publisher-name="' + rdt.publisher_name 
                    + '" data-publisher-code="' + rdt.publisher_code + '" data-row-id="' + opt.rowId + '">' + '削除' + '</button>'
                );
            },
            sortable: false
        })
    );
    return {
        model: modelArray,
        name: ['出版社コード', '出版社名', '最終更新者', '最終更新日時', 'データ操作']
    };
};

/**
 * jQGrid用のボタンイベント定義
 */
PublisherListController.prototype.gridBtnEvent = function(data) {

    $('.grid-btn-delete, .grid-btn-update').button();

    // 編集ボタンをクリックし、編集画面へ遷移する
    $('.grid-btn-update').on('click', function() {
        var button = $(this);
        // 出版社コードを取得
        var publishercode = button.attr('data-publisher-code');
        // 出版社編集画面へ遷移
        window.location.href = '/admin_app/publisher_update?publisherc=' + publishercode;
    });

    $('.grid-btn-delete').off('click');
    // 削除ボタンをクリックし、削除処理を行う
    $('.grid-btn-delete').on('click', function() {
        var button = $(this);
        $('#delete-publisher-code').text(button.attr('data-publisher-code'));
        $('#delete-publisher-name').text(button.attr('data-publisher-name'));
        var modal = $('#delete-confirm-dialog');

        // 削除キャンセル処理
        $('.cancel-botton').on('click', function() {
            modal.dialog('close');
            $('.delete-button').off('click');
        });

        // ajaxで、削除処理を行う
        $('.delete-button').on('click', function() {
            var param = {
                'delete-publisher-code' : $('#delete-publisher-code').text(),
                'delete-publisher-name' : $('#delete-publisher-name').text(),
            };
            AjaxUtil.post('/admin_app/publisher_list/', param, function(data) {

                var result = JSON.parse(data.toString());

                if(result.is_error){
                    // 削除メッセージ表示
                    MsgUtil.showStatusMsg('#list', $('#delete-publisher-name').text() , '既に削除');
                }else{
                    // 削除メッセージ表示
                    MsgUtil.showStatusMsg('#list', $('#delete-publisher-name').text() , '削除');
                }

                // データエスケープ処理
                Escape.escapeHtml(result.publisherlist);
                // グリッドを再描画
                PublisherListController.prototype.createPublisherList(result.publisherlist);
               
            });
            modal.dialog('close');

            $('.delete-button').off('click');
        });

        modal.dialog({
            modal: true,
            width: '500px'
        });
    });
};

/**
 * CSVダウンロードイベント追加
 */
PublisherListController.prototype.downloadCsv = function() {
    var self = this;

    // CSVダウンロード全件
    $('#csv-all').click(function() {
        AjaxUtil.get('/admin_app/publisher_list/csv_download/', {}, function(data) {
            var fileName = '出版社情報_全件.csv';
            FileUtil.outputCsv(data, fileName);
        });
    });
}
$(function() {
    var controller = new PublisherListController();
    controller.init();
});
