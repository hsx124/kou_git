var NovelHeibaiListController = function() {};
NovelHeibaiListController.prototype = new AbstractController();

/**
 * メニュー選択処理
 */
NovelHeibaiListController.prototype.selectedMenu = function() {
    return '.novel-heibai-list';
};
/**
 * イベント登録処理
 */
NovelHeibaiListController.prototype.bindEvent = function() {
    var self = this;

    // 更新履歴DLエリアのイベント設定
    NoticeTableUtil.setDLArea();

    // 更新履歴CSVダウンロード
    NoticeTableUtil.downloadTableCsv('m_heibai(novel)', '小説併売情報');

    // CSVダウンロード
    self.downloadCsv();

    // 小説タイトル基本マスタ一覧生成
    self.selectNovelHeibaiList();

    return $.Deferred().resolve().promise();
};

/**
 * 併売基本マスタ検索 (ajaxで併売情報一覧検索結果を取得)
 */
NovelHeibaiListController.prototype.selectNovelHeibaiList = function() {
    var self = this;
    var param = {
        'heibai' : 'heibai-list'
    };
    AjaxUtil.get('/admin_app/novel_heibai_list/', param, function(data) {
        self.searchResultCallback(data);
    });
}

/**
 * ajaxで併売一覧検索結果を処理
 */
NovelHeibaiListController.prototype.searchResultCallback = function(data) {
    var self = this;
    var result = JSON.parse(data.toString());

    // データエスケープ処理
    Escape.escapeHtml(result);

    // 小説タイトル基本マスタ一覧の表を描画
    self.createNovelHeibaiList(result);
}

/**
 * 併売マスタ一覧の表を描画する
 */
NovelHeibaiListController.prototype.createNovelHeibaiList = function(result) {
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
NovelHeibaiListController.prototype.createColModel = function() {
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
            name: 'heibai_name_1',
            width: width * 0.1,
            align: 'left',
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'heibai_name_2',
            width: width * 0.1,
            align: 'left',
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'heibai_name_3',
            width: width * 0.1,
            align: 'left',
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'heibai_name_4',
            width: width * 0.1,
            align: 'left',
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'heibai_name_5',
            width: width * 0.1,
            align: 'left',
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'update_user',
            width: width * 0.1,
            align: 'left',
            formatter : function(val){
                if(val == undefined){
                    return 'ー';
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
                    return 'ー';
                }
            },
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            title: false,
            name: 'operation',
            width: width * 0.1,
            align: 'center',
            formatter: function(val, opt, rdt) {
                if(rdt.heibai_code == 'no-code'){
                    return ('<button type="button" class="grid-btn-create" data-heibai-code="' + rdt.novel_title_code + '">新規登録</button>');
                } else {
                    return (
                        '<button type="button" class="grid-btn-update" data-heibai-code="' + rdt.novel_title_code + '">' + '編集' +'</button>'
                        + '<button type="button" class="grid-btn-delete" data-heibai-code="'+ rdt.heibai_code +'" data-novel-name="' + rdt.novel_title_name
                        + '" data-novel-title-code="' + rdt.novel_title_code + '" data-row-id="' + opt.rowId + '">' + '削除' + '</button>'
                        );
                }
            },
            sortable: false
        })
    );
    return {
        model: modelArray,
        name: ['小説タイトル名', '併売名1', '併売名2', '併売名3', '併売名4', '併売名5','最終更新者', '最終更新日時', 'データ操作']
    };
};

/**
 * jQGrid用のボタンイベント定義
 */
NovelHeibaiListController.prototype.gridBtnEvent = function(data) {
    var self = this;
    $('.grid-btn-delete, .grid-btn-update , .grid-btn-create').button();

    // 編集ボタンをクリックし、編集画面へ遷移する
    $('.grid-btn-update').on('click', function() {
        var button = $(this);
        // 小説タイトルコードを取得
        var novelCode = button.attr('data-heibai-code');
        // 編集画面へ遷移
        window.location.href = '/admin_app/novel_heibai_update?novelc=' + novelCode;
    });

    // 新規登録ボタン
    $('.grid-btn-create').on('click', function() {
        var button = $(this);
        // 小説タイトルコードを取得
        var novelCode = button.attr('data-heibai-code');
        // 新規登録画面に遷移
        window.location.href = '/admin_app/novel_heibai_create?novelc=' + novelCode;
    });

    $('.grid-btn-delete').off('click');
    // 削除ボタンをクリックし、削除処理を行う
    $('.grid-btn-delete').on('click', function() {
        var button = $(this);
        $('#delete-novel-code').text(button.attr('data-novel-title-code'));
        $('#delete-novel-code').val(button.attr('data-heibai-code'));
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
                'delete-novel-code' : $('#delete-novel-code').val(),
                'delete-novel-name' : $('#delete-novel-name').text(),
            };
            AjaxUtil.post('/admin_app/novel_heibai_list/', param, function(data) {

                var result = JSON.parse(data.toString());

                if(result.is_error){
                    // 削除メッセージ表示
                    MsgUtil.showStatusMsg('#list', $('#delete-novel-name').text() , '既に削除');
                }else{
                    // 削除メッセージ表示
                    MsgUtil.showStatusMsg('#list', $('#delete-novel-name').text() , '削除');
                }

                // データエスケープ処理
                Escape.escapeHtml(result.novel_heibai_list);

                // 併売情報一覧の表を再描画
                NovelHeibaiListController.prototype.createNovelHeibaiList(result.novel_heibai_list);

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
NovelHeibaiListController.prototype.downloadCsv = function() {
    var self = this;

    // CSVダウンロード全件
    $('#csv-all').click(function() {
        AjaxUtil.get('/admin_app/novel_heibai_list/csv_download/', {}, function(data) {
            var fileName = '小説併売情報_全件.csv';
            FileUtil.outputCsv(data, fileName);
        });
    });
}

$(function() {
    var controller = new NovelHeibaiListController();
    controller.init();
});
