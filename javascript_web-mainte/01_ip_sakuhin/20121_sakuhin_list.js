var SakuhinListController = function() {
};
SakuhinListController.prototype = new AbstractController();

/**
 * IP一覧画面の主処理
 */
SakuhinListController.prototype.execute = function() {
    var self = this;

    return $.Deferred().resolve().promise();
};

/**
 * メニュー選択処理
 */
SakuhinListController.prototype.selectedMenu = function() {
    return '.sakuhin-list';
};

/**
 * イベント登録処理
 */
SakuhinListController.prototype.bindEvent = function() {
    var self = this;

    // 新規登録ボタン
    $('.create-button').on('click', function() {
        window.location.href = '/admin_app/sakuhin_create/';
    });

    // 更新履歴DLエリアのイベント設定
    NoticeTableUtil.setDLArea();

    // 更新履歴CSVダウンロード
    NoticeTableUtil.downloadTableCsv('m_sakuhin', '作品マスタ');

    // IPマスタCSVダウンロード
    self.downloadCsv();

    // 作品マスタ一覧生成
    self.selectSakuhinList().fail(function(){
        $('#errorMsg').show();
        return $.Deferred().resolve().promise();
    });

    //return $.Deferred().resolve().promise();
};

/**
 * 作品マスタ検索 (ajaxで作品一覧検索結果を取得)
 */
SakuhinListController.prototype.selectSakuhinList = function() {
    var self = this;
    var param = {
          'sakuhin-list' : 'sakuhin-list'
      };
    return AjaxUtil.get('/admin_app/sakuhin_list/', param).then(function(xhr, status) {
        var promise = $.Deferred();
        if(status == 'success'){
            var result = JSON.parse(xhr.responseText);
            self.createSakuhinList(result);
            return promise.resolve();
        }else{
            return promise.reject();
        }
    });
        
}

/**
 * IP一覧生成<br>
 * jQGridを使用して表を描画する。
 */
SakuhinListController.prototype.createSakuhinList = function(result) {
    var self = this;

    // 一覧データが10以下の場合は高さ自動調整
    var height = 'auto';
    if (result.length >= 10) {
        height = 450;
    }

    if ($('#gbox_list-grid').is(':visible')) {
        $('#list-grid').jqGrid('clearGridData').trigger('reloadGrid');
        $('#list-grid').jqGrid('setGridParam', {
            data : result,
        }).trigger('reloadGrid');
    }
    // グリッド生成
    var colModel = self.createColModel();
    var option = {
        colNames : colModel.name,
        colModel : colModel.model,
        data : result,
        width : $('#list').width(),
        height : height,
        pager : '#pager',
        loadComplete : self.gridBtnEvent,
        pgbuttons : false,
        pginput : false,
        viewrecords : true,
        rowList : result.length,
        rowNum : result.length
        
    };
    GridUtil.renderNormalGrid('#list-grid', option, true);
};

/**
 * jQGrid用のカラム定義
 */
SakuhinListController.prototype.createColModel = function() {
    var width = $('#list').width();

    var modelArray = [];
    modelArray.push(GridUtil.createColModel({
        name : 'sakuhin_code',
        width : width * 0.07
    }));
    modelArray.push(GridUtil.createColModel({
        name : 'sakuhin_name',
        width : width * 0.12
    }));
    modelArray.push(GridUtil.createColModel({
        name : 'overview',
        align : 'center',
        width : width * 0.1,
        formatter : GridUtil.formatMaruBatsu,
    }));
    modelArray.push(GridUtil.createColModel({
        name : 'keyvisual_file_name',
        align : 'center',
        width : width * 0.1,
        formatter : GridUtil.formatMaruBatsu,
    }));
    modelArray.push(GridUtil.createColModel({
        name : 'keyword',
        width : width * 0.2
    }));
    modelArray.push(GridUtil.createColModel({
        name : 'release_date',
        formatter : 'date',
        formatoptions : {
            srcformat : 'ISO8601Long',
            newformat : 'Y/m'
        }
    }));
    modelArray.push(GridUtil.createColModel({
        name : 'update_user',
        width : width * 0.1
    }));
    modelArray.push(GridUtil.createColModel({
        name : 'update_date',
        formatter : 'date',
        formatoptions : {
            srcformat : 'ISO8601Long',
            newformat : 'Y/m/d'
        }
    }));
    modelArray.push(GridUtil.createColModel({
        title : false,
        name : 'operation',
        width : width * 0.12,
        align : 'center',
        formatter : function(val, opt, rdt) {
            return ('<button type="button" class="grid-btn-update" data-sakuhin-code="' + rdt.sakuhin_code + '">' + '編集' + '</button>' + '<button type="button" class="grid-btn-delete" data-sakuhin-name="' + rdt.sakuhin_name + '" data-sakuhin-code="' + rdt.sakuhin_code + '" data-row-id="' + opt.rowId
                    + '">' + '削除' + '</button>');
        },
        sortable : false
    }));
    return {
        model : modelArray,
        name : [ '作品コード', '作品名', 'あらすじ', 'キービジュアル', 'キーワード', '展開開始年月日', '最終更新者', '最終更新日時', 'データ操作' ]
    };
};

/**
 * jQGrid用のボタンイベント定義
 */
SakuhinListController.prototype.gridBtnEvent = function(data) {
    var local = data;
    $('.grid-btn-delete, .grid-btn-update').button();
    $('.grid-btn-update').on('click', function() {
        var button = $(this);
        var sakuhincode = button.attr('data-sakuhin-code');

        window.location.href = '/admin_app/sakuhin_update?sakuhinc=' + sakuhincode;
    });
    $('.grid-btn-delete').off('click');
    $('.grid-btn-delete').on('click', function() {
        var button = $(this);
        $('#delete-sakuhin-code').text(button.attr('data-sakuhin-code'));
        $('#delete-sakuhin-name').text(button.attr('data-sakuhin-name'));

        var modal = $('#delete-confirm-dialog');
        $('.cancel-botton').on('click', function() {
            modal.dialog('close');
            $('.delete-button').off('click');
        });
        $('.delete-button').on('click', function() {

            var param = {
                'delete-sakuhincode' : $('#delete-sakuhin-code').text(),
                'delete-sakuhinname' : $('#delete-sakuhin-name').text(),
            };
            AjaxUtil.post('/admin_app/sakuhin_list/', param).then(function(xhr,status)  {
                if(status == 'success'){
                    var result = JSON.parse(xhr.responseText);
                    if(result.is_error){
                        // 削除メッセージ表示
                        MsgUtil.showStatusMsg('#list', $('#delete-sakuhin-name').text() , '既に削除');
                    }else{
                        // 削除メッセージ表示
                        MsgUtil.showStatusMsg('#list', $('#delete-sakuhin-name').text() , '削除');
                    }
                

                // データエスケープ処理
                Escape.escapeHtml(result.sakuhin_list);

                // グリッド描画
                SakuhinListController.prototype.createSakuhinList(result.sakuhin_list);
            }
            }).then(function(){
                modal.dialog('close');
            });
            $('.delete-button').off('click');
        });

        modal.dialog({
            modal : true,
            width : '500px'
        });
    });
};

/**
 * CSVダウンロードイベント追加
 */
SakuhinListController.prototype.downloadCsv = function() {

    var self = this;

    // CSVダウンロード全件
    $('#csv-all').click(function() {
        AjaxUtil.get('/admin_app/sakuhin_list/csv_download/', {}, function(data) {
            var fileName = '作品マスタ_全件.csv';
            FileUtil.outputCsv(data, fileName);
        });
    });
}
$(function() {
    var controller = new SakuhinListController();
    controller.init();
});
