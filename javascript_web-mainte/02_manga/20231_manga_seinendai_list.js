var MangaSeinendaiListController = function() {};
MangaSeinendaiListController.prototype = new AbstractController();

/**
 * メニュー選択処理
 */
MangaSeinendaiListController.prototype.selectedMenu = function() {
    return '.manga-seinendai-list';
};
/**
 * イベント登録処理
 */
MangaSeinendaiListController.prototype.bindEvent = function() {
    var self = this;

    // 更新履歴DLエリアのイベント設定
    NoticeTableUtil.setDLArea();

    // 更新履歴CSVダウンロード
    NoticeTableUtil.downloadTableCsv('m_seinendai', '性年代情報');

    // CSVダウンロード
    self.downloadCsv();

    // マンガタイトル基本マスタ一覧生成
    self.selectMangaSeinendaiList();

    
    return $.Deferred().resolve().promise();
};

/**
 * 性年代基本マスタ検索 (ajaxで性年代情報一覧検索結果を取得)
 */
MangaSeinendaiListController.prototype.selectMangaSeinendaiList = function() {
    var self = this;
    var param = {
        'seinendai' : 'seinendai-list'
    };
    AjaxUtil.get('/admin_app/manga_seinendai_list/', param, function(data) {
        self.searchResultCallback(data);
    });
}

/**
 * ajaxで性年代一覧検索結果を処理
 */
MangaSeinendaiListController.prototype.searchResultCallback = function(data) {
    var self = this;
    var result = JSON.parse(data.toString());

    // データエスケープ処理
    Escape.escapeHtml(result);

    // マンガタイトル基本マスタ一覧の表を描画
    self.createMangaSeinendaiList(result);
}

/**
 * 性年代マスタ一覧の表を描画する
 */
MangaSeinendaiListController.prototype.createMangaSeinendaiList = function(result) {
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
MangaSeinendaiListController.prototype.createColModel = function() {
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
            name: 'total_cnt',
            width: width * 0.1,
            align: 'left',
            formatter : function(val){
                if(val == -1){
                    return '-';
                } else{
                    return val;
                }
            }
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'male_cnt',
            width: width * 0.1,
            align: 'left',
            formatter : function(val){
                if(val == '-1'){
                    return '-';
                } else{
                    return val;
                }
            }
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'female_cnt',
            width: width * 0.1,
            align: 'left',
            formatter : function(val){
                if(val == '-1'){
                    return '-';
                } else{
                    return val;
                }
            }
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'update_user',
            width: width * 0.1,
            align: 'left',
            formatter : function(val){
                if(val == undefined){
                    return '-';
                } else{
                    return val;
                }
            }
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'update_time',
            width: width * 0.1,
            align: 'left',
            formatter: function(val, opt, rdt) {
                if(val){
                    var tmp = new Date(val);
                    var year = tmp.getFullYear();
                    var month = ('0' + (tmp.getMonth() + 1)).slice(-2);
                    var date = ('0' + (tmp.getDate() + 1)).slice(-2);
                    return year + '/' + month + '/' + date;
                }else{
                    return '-';
                }
            },
        })
    );  
    modelArray.push(
        GridUtil.createColModel({
            title: false,
            name: 'operation',
            width: width * 0.07,
            align: 'center',
            formatter: function(val, opt, rdt) {
                if(rdt.seinendai_code == 'no-code'){
                    return ('<button type="button" class="grid-btn-create" data-seinendai-code="' + rdt.manga_title_code + '">新規登録</button>');
                } else {
                    return (
                        '<button type="button" class="grid-btn-update" data-seinendai-code="' + rdt.manga_title_code + '">' + '編集' +'</button>'
                        + '<button type="button" class="grid-btn-delete" data-seinendai-code="'+ rdt.seinendai_code +'" data-manga-name="' + rdt.manga_title_name
                        + '" data-manga-title-code="' + rdt.manga_title_code + '" data-row-id="' + opt.rowId + '">' + '削除' + '</button>'
                        );
                }
            },
            sortable: false
        })
    );
    return {
        model: modelArray,
        name: ['マンガタイトル名', '総人数','男性総人数','女性総人数','最終更新者', '最終更新日時', 'データ操作']
    };
};

/**
 * jQGrid用のボタンイベント定義
 */
MangaSeinendaiListController.prototype.gridBtnEvent = function(data) {
    var self = this;
    $('.grid-btn-delete, .grid-btn-update , .grid-btn-create').button();

    // 編集ボタンをクリックし、編集画面へ遷移する
    $('.grid-btn-update').on('click', function() {
        var button = $(this);
        // マンガコードを取得
        var mangaCode = button.attr('data-seinendai-code');
        // 編集画面へ遷移
        window.location.href = '/admin_app/manga_seinendai_update?mangac=' + mangaCode;
    });

    // 新規登録ボタン
    $('.grid-btn-create').on('click', function() {
        var button = $(this);
        // マンガコードを取得
        var mangaCode = button.attr('data-seinendai-code');
        // 新規登録画面に遷移
        window.location.href = '/admin_app/manga_seinendai_create?mangac=' + mangaCode;
    });

    $('.grid-btn-delete').off('click');
    // 削除ボタンをクリックし、削除処理を行う
    $('.grid-btn-delete').on('click', function() {
        var button = $(this);
        $('#delete-manga-code').text(button.attr('data-manga-title-code'));
        $('#delete-manga-code').val(button.attr('data-seinendai-code'));
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
                'delete-manga-code' : $('#delete-manga-code').val(),
                'delete-manga-name' : $('#delete-manga-name').text(),
            };
            AjaxUtil.post('/admin_app/manga_seinendai_list/', param, function(data) {

                var result = JSON.parse(data.toString());

                if(result.is_error){
                    // 削除メッセージ表示
                    MsgUtil.showStatusMsg('#list', $('#delete-manga-name').text() , '既に削除');
                }else{
                    // 削除メッセージ表示
                    MsgUtil.showStatusMsg('#list', $('#delete-manga-name').text() , '削除');
                }

                // データエスケープ処理
                Escape.escapeHtml(result.manga_seinendai_list);

                // 性年代情報一覧の表を再描画
                MangaSeinendaiListController.prototype.createMangaSeinendaiList(result.manga_seinendai_list);

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
MangaSeinendaiListController.prototype.downloadCsv = function() {
    var self = this;

    // CSVダウンロード全件
    $('#csv-all').click(function() {
        AjaxUtil.get('/admin_app/manga_seinendai_list/csv_download/', {}, function(data) {
            var fileName = '性年代情報_全件.csv';
            FileUtil.outputCsv(data, fileName);
        });
    });
}

$(function() {
    var controller = new MangaSeinendaiListController();
    controller.init();
});
