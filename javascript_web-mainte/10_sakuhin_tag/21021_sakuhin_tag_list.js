var SakuhinTagListController = function() {};
SakuhinTagListController.prototype = new AbstractController();

/**
 * タグマスタ一覧画面の主処理
 */
SakuhinTagListController.prototype.execute = function() {
    var self = this;

    return $.Deferred()
        .resolve()
        .promise();
};

/**
 * メニュー選択処理
 */
SakuhinTagListController.prototype.selectedMenu = function() {
    return '.tag-list';
};
/**
 * イベント登録処理
 */
SakuhinTagListController.prototype.bindEvent = function() {
    var self = this;

    // 新規登録ボタン
    $('.create-button').on('click', function() {
        window.location.href = '/admin_app/sakuhin_tag_create/';
    });

    //プルダウン選択時処理
    $('select[name=filter-category]').on('selectmenuchange', function() {
        // セレクトボックスのValを取得する
        var selectVal = $('#filter-category-select').val();
        // セレクトボックスが全件の場合
        var param = {
            'search-category-code' : selectVal
        }

        AjaxUtil.get('/admin_app/sakuhin_tag_list/', param, function(data) {
            var result = JSON.parse(data.toString());
            // グリッド描画
            self.createSakuhinTagList(result);
            
        });
    });

    //初期表示
    var param = {
        'search-category-code' : 'all-category'
    }
    AjaxUtil.get('/admin_app/sakuhin_tag_list/', param, function(data) {
        var result = JSON.parse(data.toString());
        // グリッド描画
        self.createSakuhinTagList(result);
        
    });

    // 更新履歴DLエリアのイベント設定
    NoticeTableUtil.setDLArea();

    // 更新履歴CSVダウンロード
    NoticeTableUtil.downloadTableCsv('m_sakuhin_tag', 'タグ情報');

    // タグマスタCSVダウンロード
    self.downloadCsv();

    return $.Deferred()
        .resolve()
        .promise();
};

/**
 * 作品タグ一覧生成
 * jQGridを使用して表を描画する。
 */
SakuhinTagListController.prototype.createSakuhinTagList = function(result) {
    var self = this;
    var height = 'auto';
    // 一覧データが10以下の場合は高さ自動調整
    if (result.length >= 10) {
         height = 450;
        }
    if ($('#gbox_list-grid').is(':visible')) {
        $('#list-grid').jqGrid('clearGridData').trigger('reloadGrid');
        $('#list-grid').jqGrid('setGridHeight', height).trigger('reloadGrid');
        $('#list-grid').jqGrid('setGridParam', {
            data : result,
        }).trigger('reloadGrid');
    }
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
        viewrecords : true,
        rowList : result.length,
        rowNum : result.length
    };
    GridUtil.renderNormalGrid('#list-grid', option, true);
};

/**
 * jQGrid用のカラム定義
 */
SakuhinTagListController.prototype.createColModel = function() {
    var width = $('#list').width();

    var modelArray = [];
    modelArray.push(
        GridUtil.createColModel({
            name: 'sakuhin_tag_code',
            width: width * 0.07
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'sakuhin_tag_category_name',
            width: width * 0.12
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'sakuhin_tag_name',
            width: width * 0.12
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
            width: width * 0.1
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
                    '<button type="button" class="grid-btn-update" data-tag-code="' +
                    rdt.sakuhin_tag_code +
                    '">' +
                    '編集' +
                    '</button>' +
                    '<button type="button" class="grid-btn-delete" data-tag-name="' +
                    rdt.sakuhin_tag_name +
                    '" data-tag-code="' +
                    rdt.sakuhin_tag_code +
                    '" data-row-id="' +
                    opt.rowId +
                    '">' +
                    '削除' +
                    '</button>'
                );
            },
            sortable: false
        })
    );
    return {
        model: modelArray,
        name: ['タグコード', 'タグカテゴリ名', 'タグ名','最終更新者', '最終更新日時', 'データ操作']
    };
};

/**
 * jQGrid用のボタンイベント定義
 */
SakuhinTagListController.prototype.gridBtnEvent = function(data) {
    var self = this;
    $('.grid-btn-delete, .grid-btn-update').button();
    $('.grid-btn-update').on('click', function() {
        var button = $(this);
        var tagcode = button.attr('data-tag-code');
 
        window.location.href = '/admin_app/sakuhin_tag_update?tagc=' + tagcode;
    });
    $('.grid-btn-delete').off('click');
    // 削除ボタンをクリックし、削除処理を行い
    $('.grid-btn-delete').on('click', function() {
        var button = $(this);
        $('#delete-tag-code').text(button.attr('data-tag-code'));
        $('#delete-tag-name').text(button.attr('data-tag-name'));
        var modal = $('#delete-confirm-dialog');
 
         // 削除キャンセル処理
        $('.cancel-botton').on('click', function() {
            modal.dialog('close');
            $('.delete-button').off('click');
        });
 
        // ajax削除処理
        $('.delete-button').on('click', function() {
             // セレクトボックスのValを取得する
            var selectVal = $('#filter-category-select').val();

            var param = {
                'delete-tag-code' : $('#delete-tag-code').text(),
                'delete-tag-name' : $('#delete-tag-name').text(),
                'search-category-code' : selectVal
            };

            AjaxUtil.post('/admin_app/sakuhin_tag_list/', param, function(data) {
 
                var result = JSON.parse(data.toString());
                
                // グリッドを再描画
                SakuhinTagListController.prototype.createSakuhinTagList(result.sakuhin_list);
                if(result.is_error){
                    // 削除メッセージ表示
                    MsgUtil.showStatusMsg('#list', $('#delete-tag-name').text() , '既に削除');
                }else{
                    // 削除メッセージ表示
                    MsgUtil.showStatusMsg('#list', $('#delete-tag-name').text() , '削除');
                }
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
SakuhinTagListController.prototype.downloadCsv = function() {

    var self = this;

    // CSVダウンロード全件
    $('#csv-all').click(function() {
        AjaxUtil.get('/admin_app/sakuhin_tag_list/csv_download/', {}, function(data) {
            var fileName = 'タグ情報_全件.csv';
            FileUtil.outputCsv(data, fileName);
        });
    });
}
$(function() {
    var controller = new SakuhinTagListController();
    controller.init();
});
