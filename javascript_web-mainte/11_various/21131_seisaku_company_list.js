var SeisakuCompanyListController = function() {};
SeisakuCompanyListController.prototype = new AbstractController();

/**
 * メニュー選択処理
 */
SeisakuCompanyListController.prototype.selectedMenu = function() {
    return '.seisaku-company-list';
};

/**
 * イベント登録処理
 */
SeisakuCompanyListController.prototype.bindEvent = function() {
    var self = this;

    // 新規登録ボタン
    $('.create-button').on('click', function() {
        window.location.href = '/admin_app/seisaku_company_create/';
    });

    // 更新履歴DLエリアのイベント設定
    NoticeTableUtil.setDLArea();

    // 更新履歴CSVダウンロード
    NoticeTableUtil.downloadTableCsv('m_seisaku_company', '制作会社情報');

    // 制作会社マスタCSVダウンロード
    self.downloadCsv();

    // 制作会社マスタ一覧生成
    self.selectSeisakuCompanyList();

    return $.Deferred().resolve().promise();
};

/**
 * 制作会社マスタ検索 (ajaxで制作会社一覧検索結果を取得)
 */
SeisakuCompanyListController.prototype.selectSeisakuCompanyList = function() {
    var self = this;
    var param = {
          'seisaku-company' : 'seisaku-company-list'
      };
    AjaxUtil.get('/admin_app/seisaku_company_list/', param, function(data) {
        self.searchResultCallback(data);
    });
}

/**
 * ajaxで制作会社一覧検索結果を処理
 */
SeisakuCompanyListController.prototype.searchResultCallback = function(data) {
    var self = this;
    var result = JSON.parse(data.toString());

    // データエスケープ処理
    Escape.escapeHtml(result);
    // 制作会社マスタ一覧の表を描画
    self.createSeisakuCompanyList(result);
}

/**
 * 制作会社マスタ一覧の表を描画する
 */
SeisakuCompanyListController.prototype.createSeisakuCompanyList = function(result) {
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
SeisakuCompanyListController.prototype.createColModel = function() {
    var width = $('#list').width();

    var modelArray = [];
    modelArray.push(
        GridUtil.createColModel({
            name: 'seisaku_company_code',
            width: width * 0.1
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'seisaku_company_name',
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
                    '<button type="button" class="grid-btn-update" data-seisaku-company-code="' + rdt.seisaku_company_code + '">' + '編集' +'</button>'
                    + '<button type="button" class="grid-btn-delete" data-seisaku-company-name="' + rdt.seisaku_company_name 
                    + '" data-seisaku-company-code="' + rdt.seisaku_company_code + '" data-row-id="' + opt.rowId + '">' + '削除' + '</button>'
                );
            },
            sortable: false
        })
    );
    return {
        model: modelArray,
        name: ['制作会社コード', '制作会社名', '最終更新者', '最終更新日時', 'データ操作']
    };
};

/**
 * jQGrid用のボタンイベント定義
 */
SeisakuCompanyListController.prototype.gridBtnEvent = function(data) {

    $('.grid-btn-delete, .grid-btn-update').button();

    // 編集ボタンをクリックし、編集画面へ遷移する
    $('.grid-btn-update').on('click', function() {
        var button = $(this);
        // 制作会社コードを取得
        var seisakucompanycode = button.attr('data-seisaku-company-code');
        // 制作会社編集画面へ遷移
        window.location.href = '/admin_app/seisaku_company_update?seisakucompanyc=' + seisakucompanycode;
    });

    $('.grid-btn-delete').off('click');
    // 削除ボタンをクリックし、削除処理を行う
    $('.grid-btn-delete').on('click', function() {
        var button = $(this);
        $('#delete-seisaku-company-code').text(button.attr('data-seisaku-company-code'));
        $('#delete-seisaku-company-name').text(button.attr('data-seisaku-company-name'));
        var modal = $('#delete-confirm-dialog');

        // 削除キャンセル処理
        $('.cancel-botton').on('click', function() {
            modal.dialog('close');
            $('.delete-button').off('click');
        });

        // ajaxで、削除処理を行う
        $('.delete-button').on('click', function() {
            var param = {
                'delete-seisaku-company-code' : $('#delete-seisaku-company-code').text(),
                'delete-seisaku-company-name' : $('#delete-seisaku-company-name').text(),
            };
            AjaxUtil.post('/admin_app/seisaku_company_list/', param, function(data) {

                var result = JSON.parse(data.toString());

                if(result.is_error){
                    // 削除メッセージ表示
                    MsgUtil.showStatusMsg('#list', $('#delete-seisaku-company-name').text() , '既に削除');
                }else{
                    // 削除メッセージ表示
                    MsgUtil.showStatusMsg('#list', $('#delete-seisaku-company-name').text() , '削除');
                }

                // データエスケープ処理
                Escape.escapeHtml(result.seisakucompanylist);
                // グリッドを再描画
                SeisakuCompanyListController.prototype.createSeisakuCompanyList(result.seisakucompanylist);
               
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
SeisakuCompanyListController.prototype.downloadCsv = function() {
    var self = this;

    // CSVダウンロード全件
    $('#csv-all').click(function() {
        AjaxUtil.get('/admin_app/seisaku_company_list/csv_download/', {}, function(data) {
            var fileName = '制作会社情報_全件.csv';
            FileUtil.outputCsv(data, fileName);
        });
    });
}
$(function() {
    var controller = new SeisakuCompanyListController();
    controller.init();
});
