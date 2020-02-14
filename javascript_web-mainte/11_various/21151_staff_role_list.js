var StaffRoleListController = function() {};
StaffRoleListController.prototype = new AbstractController();

/**
 * スタッフ役割一覧画面の主処理
 */
StaffRoleListController.prototype.execute = function() {
    var self = this;

    return $.Deferred()
        .resolve()
        .promise();
};

/**
 * メニュー選択処理
 */
StaffRoleListController.prototype.selectedMenu = function() {
    return '.staff-role-list';
};

/**
 * イベント登録処理
 */
StaffRoleListController.prototype.bindEvent = function() {
    var self = this;

    // 新規登録ボタン
    $('.create-button').on('click', function() {
        window.location.href = '/admin_app/staff_role_create';
    });

    // 更新履歴DLエリアのイベント設定
    NoticeTableUtil.setDLArea();

    // 更新履歴CSVダウンロード
    NoticeTableUtil.downloadTableCsv('m_staff_role', 'スタッフ役割情報');

    // CSVダウンロード
    self.downloadCsv();

    // スタッフ役割マスタ一覧生成
    self.selectStaffRoleList();

    return $.Deferred().resolve().promise();
};

/**
 * スタッフ役割マスタ検索 (ajaxでスタッフ役割一覧検索結果を取得)
 */
StaffRoleListController.prototype.selectStaffRoleList = function() {
    var self = this;
    var param = {
        'staff_role' : 'staff-role-list'
    };
    AjaxUtil.get('/admin_app/staff_role_list/', param, function(data) {
        self.searchResultCallback(data);
    });
}

/**
 * ajaxでスタッフ役割一覧検索結果を処理
 */
StaffRoleListController.prototype.searchResultCallback = function(data) {
    var self = this;
    var result = JSON.parse(data.toString());
    // データエスケープ処理
    Escape.escapeHtml(result);

    // スタッフ役割マスタ一覧の表を描画
    self.createStaffRoleList(result);
}

/**
 * スタッフ役割マスタ一覧の表を描画する
 */
StaffRoleListController.prototype.createStaffRoleList = function(result) {
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
StaffRoleListController.prototype.createColModel = function() {
    var width = $('#list').width();

    var modelArray = [];
    modelArray.push(
        GridUtil.createColModel({
            name: 'staff_role_code',
            width: width * 0.1,
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'staff_role_name',
            width: width * 0.3,
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
                    '<button type="button" class="grid-btn-update" data-staff-role-code="' + rdt.staff_role_code + '">' + '編集' +'</button>'
                    + '<button type="button" class="grid-btn-delete" data-staff-role-name="' + rdt.staff_role_name
                    + '" data-staff-role-code="' + rdt.staff_role_code + '" data-row-id="' + opt.rowId + '">' + '削除' + '</button>'
                    );
                },
            sortable: false
        })
    );
    return {
        model: modelArray,
        name: ['スタッフ役割コード','スタッフ役割名','最終更新者', '最終更新日時', 'データ操作']
    };
};

/**
 * jQGrid用のボタンイベント定義
 */
StaffRoleListController.prototype.gridBtnEvent = function(data) {
    var self = this;
    $('.grid-btn-delete, .grid-btn-update').button();

    // 編集ボタンをクリックし、編集画面へ遷移する
    $('.grid-btn-update').on('click', function() {
        var button = $(this);
        // スタッフ役割コードを取得
        var staffRoleCode = button.attr('data-staff-role-code');
        // スタッフ役割編集画面へ遷移
        window.location.href = '/admin_app/staff_role_update?staff_rolec=' + staffRoleCode;
    });

    $('.grid-btn-delete').off('click');
    // 削除ボタンをクリックし、削除処理を行う
    $('.grid-btn-delete').on('click', function() {
        var button = $(this);
        $('#delete-staff-role-code').text(button.attr('data-staff-role-code'));
        $('#delete-staff-role-name').text(button.attr('data-staff-role-name'));
        var modal = $('#delete-confirm-dialog');

        // 削除キャンセル処理
        $('.cancel-botton').on('click', function() {
            modal.dialog('close');
            $('.delete-button').off('click');
        });

        // ajaxで、削除処理を行う
        $('.delete-button').on('click', function() {
            var param = {
                'delete-staff-role-code' : $('#delete-staff-role-code').text(),
                'delete-staff-role-name' : $('#delete-staff-role-name').text(),
            };
            AjaxUtil.post('/admin_app/staff_role_list/', param, function(data) {

                var result = JSON.parse(data.toString());

                if(result.is_error){
                    // 削除メッセージ表示
                    MsgUtil.showStatusMsg('#list', $('#delete-staff-role-name').text() , '既に削除');
                }else{
                    // 削除メッセージ表示
                    MsgUtil.showStatusMsg('#list', $('#delete-staff-role-name').text() , '削除');
                }

                // データエスケープ処理
                Escape.escapeHtml(result.staff_role_list);

                // スタッフ役割マスタ一覧の表を再描画
                StaffRoleListController.prototype.createStaffRoleList(result.staff_role_list);

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
StaffRoleListController.prototype.downloadCsv = function() {
    var self = this;

    // CSVダウンロード全件
    $('#csv-all').click(function() {
        AjaxUtil.get('/admin_app/staff_role_list/csv_download/', {}, function(data) {
            var fileName = 'スタッフ役割情報_全件.csv';
            FileUtil.outputCsv(data, fileName);
        });
    });
}

$(function() {
    var controller = new StaffRoleListController();
    controller.init();
});
