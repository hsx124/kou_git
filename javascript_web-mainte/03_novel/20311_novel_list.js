var NovelListController = function() {};
NovelListController.prototype = new AbstractController();

/**
 * メニュー選択処理
 */
NovelListController.prototype.selectedMenu = function() {
    return '.novel-list';
};

/**
 * イベント登録処理
 */
NovelListController.prototype.bindEvent = function() {
    var self = this;

    // 新規登録ボタン
    $('.create-button').on('click', function() {
        window.location.href = '/admin_app/novel_create/';
    });

    // 更新履歴DLエリアのイベント設定
    NoticeTableUtil.setDLArea();

    // 更新履歴CSVダウンロード
    NoticeTableUtil.downloadTableCsv('m_novel_title', '小説情報');

    // CSVダウンロード
    self.downloadCsv();

    // 小説タイトル基本マスタ一覧生成
    self.selectNovelList();

    return $.Deferred().resolve().promise();
};


/**
 * 小説タイトル基本マスタ検索 (ajaxで小説一覧検索結果を取得)
 */
NovelListController.prototype.selectNovelList = function() {
    var self = this;
    var param = {
        'novel' : 'novel-list'
    };
    AjaxUtil.get('/admin_app/novel_list/', param, function(data) {
        self.searchResultCallback(data);
    });
}

/**
 * ajaxで小説一覧検索結果を処理
 */
NovelListController.prototype.searchResultCallback = function(data) {
    var self = this;
    var result = JSON.parse(data.toString());

    // データエスケープ処理
    Escape.escapeHtml(result);

    // 小説タイトル基本マスタ一覧の表を描画
    self.createNovelList(result);
}

/**
 * 小説タイトル基本マスタ一覧の表を描画する
 */
NovelListController.prototype.createNovelList = function(result) {
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
NovelListController.prototype.createColModel = function() {
    var width = $('#list').width();

    var modelArray = [];
    modelArray.push(
        GridUtil.createColModel({
            name: 'novel_title_name',
            width: width * 0.2
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'rensai_start_yyyymm',
            width: width * 0.1,
            formatter : function(val) {
                if(val && val.length == 6){
                    return val.substring(0,4) + '/' + val.substring(4);
                } else if (val && val.length == 4) {
                    return val;
                } else {
                    return ' ';
                }
            }
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'media_name',
            width: width * 0.1,
            align: 'left',
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'publisher_name',
            width: width * 0.1,
            align: 'left',
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
                    '<button type="button" class="grid-btn-update" data-novel-code="' + rdt.novel_title_code + '">' + '編集' +'</button>'
                    + '<button type="button" class="grid-btn-delete" data-novel-name="' + rdt.novel_title_name
                    + '" data-novel-code="' + rdt.novel_title_code + '" data-row-id="' + opt.rowId + '">' + '削除' + '</button>'
                    );
                },
            sortable: false
        })
    );
    return {
        model: modelArray,
        name: ['小説タイトル名', '連載開始年月','掲載媒体','出版社','最終更新者', '最終更新日時', 'データ操作']
    };
};

/**
 * jQGrid用のボタンイベント定義
 */
NovelListController.prototype.gridBtnEvent = function(data) {
    var self = this;
    $('.grid-btn-delete, .grid-btn-update').button();

    // 編集ボタンをクリックし、編集画面へ遷移する
    $('.grid-btn-update').on('click', function() {
        var button = $(this);
        // 小説コードを取得
        var novelCode = button.attr('data-novel-code');
        // 小説編集画面へ遷移
        window.location.href = '/admin_app/novel_update?novelc=' + novelCode;
    });

    $('.grid-btn-delete').off('click');
    // 削除ボタンをクリックし、削除処理を行う
    $('.grid-btn-delete').on('click', function() {
        var button = $(this);
        $('#delete-novel-code').text(button.attr('data-novel-code'));
        $('#delete-novel-name').text(button.attr('data-novel-name'));
        var modal = $('#delete-confirm-dialog');

        // 削除キャンセル処理
        $('.cancel-botton').on('click', function() {
            modal.dialog('close');
            $('.delete-button').off('click');
        });

        // ajaxで、削除処理を行う
        $('.delete-button').on('click', function() {
            var param = {
                'delete-novel-code' : $('#delete-novel-code').text(),
                'delete-novel-name' : $('#delete-novel-name').text(),
            };
            AjaxUtil.post('/admin_app/novel_list/', param, function(data) {

                var result = JSON.parse(data.toString());

                if(result.is_error){
                    // 削除メッセージ表示
                    MsgUtil.showStatusMsg('#list', $('#delete-novel-name').text() , '既に削除');
                }else{
                    // 削除メッセージ表示
                    MsgUtil.showStatusMsg('#list', $('#delete-novel-name').text() , '削除');
                }

                // データエスケープ処理
                Escape.escapeHtml(result.novel_list);

                // 小説タイトル基本マスタ一覧の表を再描画
                NovelListController.prototype.createNovelList(result.novel_list);

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
NovelListController.prototype.downloadCsv = function() {
    var self = this;

    // CSVダウンロード全件
    $('#csv-all').click(function() {
        AjaxUtil.get('/admin_app/novel_list/csv_download/', {}, function(data) {
            var fileName = '小説タイトル情報_全件.csv';
            FileUtil.outputCsv(data, fileName);
        });
    });
}


$(function() {
    var controller = new NovelListController();
    controller.init();
});
