var SakuhinTagCategoryListController = function() {};
SakuhinTagCategoryListController.prototype = new AbstractController();

/**
 * メニュー選択処理
 */
SakuhinTagCategoryListController.prototype.selectedMenu = function() {
    return '.tag-category-list';
};

/**
 * イベント登録処理
 */
SakuhinTagCategoryListController.prototype.bindEvent = function() {
    var self = this;

    // 新規登録ボタン
    $('.create-button').on('click', function() {
        window.location.href = '/admin_app/sakuhin_tag_category_create/';
    });

    // 更新履歴DLエリアのイベント設定
    NoticeTableUtil.setDLArea();

    // 更新履歴CSVダウンロード
    NoticeTableUtil.downloadTableCsv('m_sakuhin_tag_category', 'タグカテゴリ情報');

    // CSVダウンロード
    self.downloadCsv();

    // タグカテゴリマスタ一覧生成
    self.selectSakuhinTagCategoryList();

    return $.Deferred().resolve().promise();
};

/**
 * タグカテゴリマスタ検索 (ajaxでタグカテゴリ一覧検索結果を取得)
 */
SakuhinTagCategoryListController.prototype.selectSakuhinTagCategoryList = function() {
    var self = this;
    var param = {
        'sakuhin-tag-category' : 'sakuhin-tag-category-list'
    };
    AjaxUtil.get('/admin_app/sakuhin_tag_category_list/', param, function(data) {
        self.searchResultCallback(data);
    });
}

/**
 * ajaxでタグカテゴリ一覧検索結果を処理
 */
SakuhinTagCategoryListController.prototype.searchResultCallback = function(data) {
    var self = this;
    var result = JSON.parse(data.toString());

    // データエスケープ処理
    Escape.escapeHtml(result);

    // タグカテゴリマスタ一覧の表を描画
    self.createSakuhinTagCategoryList(result);
}

/**
 * タグカテゴリマスタ一覧の表を描画する
 */
SakuhinTagCategoryListController.prototype.createSakuhinTagCategoryList = function(result) {
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
SakuhinTagCategoryListController.prototype.createColModel = function() {
    var width = $('#list').width();

    var modelArray = [];
    modelArray.push(
        GridUtil.createColModel({
            name: 'sakuhin_tag_category_code',
            width: width * 0.2
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'sakuhin_tag_category_name',
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
                    '<button type="button" class="grid-btn-update" data-sakuhin-tag-category-code="' + rdt.sakuhin_tag_category_code + '">' + '編集' +'</button>'
                    + '<button type="button" class="grid-btn-delete" data-sakuhin-tag-category-name="' + rdt.sakuhin_tag_category_name
                    + '" data-sakuhin-tag-category-code="' + rdt.sakuhin_tag_category_code + '" data-row-id="' + opt.rowId + '">' + '削除' + '</button>'
                    );
                },
            sortable: false
        })
    );
    return {
        model: modelArray,
        name: ['タグカテゴリコード','タグカテゴリ名','最終更新者', '最終更新日時', 'データ操作']
    };
};

/**
 * jQGrid用のボタンイベント定義
 */
SakuhinTagCategoryListController.prototype.gridBtnEvent = function(data) {
    var self = this;
    $('.grid-btn-delete, .grid-btn-update').button();

    // 編集ボタンをクリックし、編集画面へ遷移する
    $('.grid-btn-update').on('click', function() {
        var button = $(this);
        // タグカテゴリコードを取得
        var sakuhinTagCode = button.attr('data-sakuhin-tag-category-code');
        // タグカテゴリ編集画面へ遷移
        window.location.href = '/admin_app/sakuhin_tag_category_update?sakuhin_tag_categoryc=' + sakuhinTagCode;
    });

    $('.grid-btn-delete').off('click');
    // 削除ボタンをクリックし、削除処理を行う
    $('.grid-btn-delete').on('click', function() {
        var button = $(this);
        $('#delete-sakuhin-tag-category-code').text(button.attr('data-sakuhin-tag-category-code'));
        $('#delete-sakuhin-tag-category-name').text(button.attr('data-sakuhin-tag-category-name'));
        var modal = $('#delete-confirm-dialog');

        // 削除キャンセル処理
        $('.cancel-botton').on('click', function() {
            modal.dialog('close');
            $('.delete-button').off('click');
        });

        // ajaxで、削除処理を行う
        $('.delete-button').on('click', function() {
            var param = {
                'delete-sakuhin-tag-category-code' : $('#delete-sakuhin-tag-category-code').text(),
                'delete-sakuhin-tag-category-name' : $('#delete-sakuhin-tag-category-name').text(),
            };
            AjaxUtil.post('/admin_app/sakuhin_tag_category_list/', param, function(data) {

                var result = JSON.parse(data.toString());

                if(result.is_error){
                    // 削除メッセージ表示
                    MsgUtil.showStatusMsg('#list', $('#delete-sakuhin-tag-category-name').text() , '既に削除');
                }else{
                    // 削除メッセージ表示
                    MsgUtil.showStatusMsg('#list', $('#delete-sakuhin-tag-category-name').text() , '削除');
                }

                // データエスケープ処理
                Escape.escapeHtml(result.sakuhin_tag_category_list);

                // タグカテゴリマスタ一覧の表を再描画
                SakuhinTagCategoryListController.prototype.createSakuhinTagCategoryList(result.sakuhin_tag_category_list);

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
SakuhinTagCategoryListController.prototype.downloadCsv = function() {
    var self = this;

    // CSVダウンロード全件
    $('#csv-all').click(function() {
        AjaxUtil.get('/admin_app/sakuhin_tag_category_list/csv_download/', {}, function(data) {
            var fileName = 'タグカテゴリ情報_全件.csv';
            FileUtil.outputCsv(data, fileName);
        });
    });
}

$(function() {
    var controller = new SakuhinTagCategoryListController();
    controller.init();
});
