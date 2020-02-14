var StaffListController = function() {};
StaffListController.prototype = new AbstractController();

/**
 * スタッフ一覧画面の主処理
 */
StaffListController.prototype.execute = function() {
    var self = this;

    return $.Deferred()
        .resolve()
        .promise();
};

/**
 * メニュー選択処理
 */
StaffListController.prototype.selectedMenu = function() {
    return '.staff-list';
};

/**
 * イベント登録処理
 */
StaffListController.prototype.bindEvent = function() {
    var self = this;

    // 新規登録ボタン
    $('.create-button').on('click', function() {
        window.location.href = '/admin_app/staff_create/';
    });

    // 更新履歴DLエリアのイベント設定
    NoticeTableUtil.setDLArea();

    // 更新履歴CSVダウンロード
    NoticeTableUtil.downloadTableCsv('m_staff', 'スタッフ情報');

    // CSVダウンロード
    self.downloadCsv();

    // スタッフマスタ一覧生成
    self.selectStaffList();

    return $.Deferred().resolve().promise();
};

/**
 * スタッフマスタ検索 (ajaxでスタッフ一覧検索結果を取得)
 */
StaffListController.prototype.selectStaffList = function() {
    var self = this;
    var param = {
        'staff' : 'staff-list'
    };
    AjaxUtil.get('/admin_app/staff_list/', param, function(data) {
        self.searchResultCallback(data);
    });
}

/**
 * ajaxでスタッフ一覧検索結果を処理
 */
StaffListController.prototype.searchResultCallback = function(data) {
    var self = this;
    var result = JSON.parse(data.toString());

    // データエスケープ処理
    Escape.escapeHtml(result);

    // スタッフマスタ一覧の表を描画
    self.createStaffList(result);
}

/**
 * スタッフマスタ一覧の表を描画する
 */
StaffListController.prototype.createStaffList = function(result) {
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
            rowNum : result.length,
        };
        if(result.length >= 1000){
            option.rownumWidth = 40
        }
        // グリッドを描画
        GridUtil.renderNormalGrid('#list-grid', option, true);
    }
};

/**
 * jQGrid用のカラム定義
 */
StaffListController.prototype.createColModel = function() {
    var width = $('#list').width();

    var modelArray = [];
    modelArray.push(
        GridUtil.createColModel({
            name: 'staff_name',
            width: width * 0.10,
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'past_sakuhin',
            width: width * 0.15,
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'remarks',
            width: width * 0.15,
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
                    '<button type="button" class="grid-btn-update" data-staff-code="' + rdt.staff_code + '">' + '編集' +'</button>'
                    + '<button type="button" class="grid-btn-delete" data-staff-name="' + rdt.staff_name
                    + '" data-staff-code="' + rdt.staff_code + '" data-row-id="' + opt.rowId + '">' + '削除' + '</button>'
                    );
                },
            sortable: false
        })
    );
    return {
        model: modelArray,
        name: ['スタッフ名','過去作品','備考','最終更新者', '最終更新日時', 'データ操作']
    };
};

/**
 * jQGrid用のボタンイベント定義
 */
StaffListController.prototype.gridBtnEvent = function(data) {
    var self = this;
    $('.grid-btn-delete, .grid-btn-update').button();

    // 編集ボタンをクリックし、編集画面へ遷移する
    $('.grid-btn-update').on('click', function() {
        var button = $(this);
        // スタッフコードを取得
        var staffCode = button.attr('data-staff-code');
        // スタッフ編集画面へ遷移
        window.location.href = '/admin_app/staff_update?staffc=' + staffCode;
    });

    $('.grid-btn-delete').off('click');
    // 削除ボタンをクリックし、削除処理を行う
    $('.grid-btn-delete').on('click', function() {
        var button = $(this);
        $('#delete-staff-code').text(button.attr('data-staff-code'));
        $('#delete-staff-name').text(button.attr('data-staff-name'));
        var modal = $('#delete-confirm-dialog');

        // 削除キャンセル処理
        $('.cancel-botton').on('click', function() {
            modal.dialog('close');
            $('.delete-button').off('click');
        });

        // ajaxで、削除処理を行う
        $('.delete-button').on('click', function() {
            var param = {
                'delete-staff-code' : $('#delete-staff-code').text(),
                'delete-staff-name' : $('#delete-staff-name').text(),
            };
            AjaxUtil.post('/admin_app/staff_list/', param, function(data) {

                var result = JSON.parse(data.toString());

                if(result.is_error){
                    // 削除メッセージ表示
                    MsgUtil.showStatusMsg('#list', $('#delete-staff-name').text() , '既に削除');
                }else{
                    // 削除メッセージ表示
                    MsgUtil.showStatusMsg('#list', $('#delete-staff-name').text() , '削除');
                }

                // データエスケープ処理
                Escape.escapeHtml(result.staff_list);

                // スタッフマスタ一覧の表を再描画
                StaffListController.prototype.createStaffList(result.staff_list);

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
StaffListController.prototype.downloadCsv = function() {
    var self = this;

    // CSVダウンロード全件
    $('#csv-all').click(function() {
        AjaxUtil.get('/admin_app/staff_list/csv_download/', {}, function(data) {
            var fileName = 'スタッフ情報_全件.csv';
            FileUtil.outputCsv(data, fileName);
        });
    });
}


$(function() {
    var controller = new StaffListController();
    controller.init();
});
