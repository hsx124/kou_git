var MangaListController = function() {
};
MangaListController.prototype = new AbstractController();

/**
 * メニュー選択処理
 */
MangaListController.prototype.selectedMenu = function() {
    return '.manga-list';
};

/**
 * イベント登録処理
 */
MangaListController.prototype.bindEvent = function() {
    var self = this;

    // 新規登録ボタン
    $('.create-button').on('click', function() {
        window.location.href = '/admin_app/manga_create/';
    });

    // 更新履歴DLエリアのイベント設定
    NoticeTableUtil.setDLArea();

    // 更新履歴CSVダウンロード
    NoticeTableUtil.downloadTableCsv('m_manga_title', 'マンガ情報');

    // CSVダウンロード
    self.downloadCsv();

    // マンガタイトル基本マスタ一覧生成
    self.selectMangaList();

    return $.Deferred().resolve().promise();
};


/**
 * マンガタイトル基本マスタ検索 (ajaxでマンガ一覧検索結果を取得)
 */
MangaListController.prototype.selectMangaList = function() {
    var self = this;
    var param = {
        'manga' : 'manga-list'
    };
    AjaxUtil.get('/admin_app/manga_list/', param, function(data) {
        self.searchResultCallback(data);
    });
}

/**
 * ajaxでマンガ一覧検索結果を処理
 */
MangaListController.prototype.searchResultCallback = function(data) {
    var self = this;
    var result = JSON.parse(data.toString());

    // データエスケープ処理
    Escape.escapeHtml(result);

    // マンガタイトル基本マスタ一覧の表を描画
    self.createMangaList(result);
}

/**
 * マンガタイトル基本マスタ一覧の表を描画する
 */
MangaListController.prototype.createMangaList = function(result) {
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
MangaListController.prototype.createColModel = function() {
    var width = $('#list').width();

    var modelArray = [];
    modelArray.push(
        GridUtil.createColModel({
            name: 'manga_title_name',
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
                    '<button type="button" class="grid-btn-update" data-manga-code="' + rdt.manga_title_code + '">' + '編集' +'</button>'
                    + '<button type="button" class="grid-btn-delete" data-manga-name="' + rdt.manga_title_name
                    + '" data-manga-code="' + rdt.manga_title_code + '" data-row-id="' + opt.rowId + '">' + '削除' + '</button>'
                    );
                },
            sortable: false
        })
    );
    return {
        model: modelArray,
        name: ['マンガタイトル名', '連載開始年月','掲載媒体','出版社','最終更新者', '最終更新日時', 'データ操作']
    };
};

/**
 * jQGrid用のボタンイベント定義
 */
MangaListController.prototype.gridBtnEvent = function(data) {
    var self = this;
    $('.grid-btn-delete, .grid-btn-update').button();

    // 編集ボタンをクリックし、編集画面へ遷移する
    $('.grid-btn-update').on('click', function() {
        var button = $(this);
        // マンガコードを取得
        var mangaCode = button.attr('data-manga-code');
        // マンガ編集画面へ遷移
        window.location.href = '/admin_app/manga_update?mangac=' + mangaCode;
    });

    $('.grid-btn-delete').off('click');
    // 削除ボタンをクリックし、削除処理を行う
    $('.grid-btn-delete').on('click', function() {
        var button = $(this);
        $('#delete-manga-code').text(button.attr('data-manga-code'));
        $('#delete-manga-name').text(button.attr('data-manga-name'));
        var modal = $('#delete-confirm-dialog');

        // 削除キャンセル処理
        $('.cancel-botton').on('click', function() {
            modal.dialog('close');
            $('.delete-button').off('click');
        });

        // ajaxで、削除処理を行う
        $('.delete-button').on('click', function() {
            var param = {
                'delete-manga-code' : $('#delete-manga-code').text(),
                'delete-manga-name' : $('#delete-manga-name').text(),
            };
            AjaxUtil.post('/admin_app/manga_list/', param, function(data) {

                var result = JSON.parse(data.toString());

                if(result.is_error){
                    // 削除メッセージ表示
                    MsgUtil.showStatusMsg('#list', $('#delete-manga-name').text() , '既に削除');
                }else{
                    // 削除メッセージ表示
                    MsgUtil.showStatusMsg('#list', $('#delete-manga-name').text() , '削除');
                }

                // データエスケープ処理
                Escape.escapeHtml(result.manga_list);

                // マンガタイトル基本マスタ一覧の表を再描画
                MangaListController.prototype.createMangaList(result.manga_list);

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
MangaListController.prototype.downloadCsv = function() {
    var self = this;

    // CSVダウンロード全件
    $('#csv-all').click(function() {
        AjaxUtil.get('/admin_app/manga_list/csv_download/', {}, function(data) {
            var fileName = 'マンガタイトル情報_全件.csv';
            FileUtil.outputCsv(data, fileName);
        });
    });
}

$(function() {
    var controller = new MangaListController();
    controller.init();
});
