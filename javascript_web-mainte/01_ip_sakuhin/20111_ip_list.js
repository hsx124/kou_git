var IpListController = function() {};
IpListController.prototype = new AbstractController();
/**
 * IPマスタ一覧画面の主処理
 */
IpListController.prototype.execute = function() {
    var self = this;
    
    // IPマスタ一覧生成
    return self.selectIpList().fail(function(){
        $('#errorMsg').show();
        return $.Deferred().resolve().promise();
    })
    
};
/**
 * メニュー選択処理
 */
IpListController.prototype.selectedMenu = function() {
    return '.ip-list';
};
/**
 * イベント登録処理
 */
IpListController.prototype.bindEvent = function() {
    var self = this;

    // 新規登録ボタン
    $('.create-button').on('click', function() {
        window.location.href = '/admin_app/ip_create/';
    });

    // 更新履歴DLエリアのイベント設定
    NoticeTableUtil.setDLArea();

    // 更新履歴CSVダウンロード
    NoticeTableUtil.downloadTableCsv('m_ip', 'IP情報');

    // IPマスタCSVダウンロード
    self.downloadCsv();


    return $.Deferred().resolve().promise();
};

/**
 * IPマスタ検索 (ajaxでIP一覧検索結果を取得)
 */
IpListController.prototype.selectIpList = function() {
    var self = this;
    var param = {
          'ip' : 'ip-list'
      };
    return AjaxUtil.get('/admin_app/ip_list/', param).then(function(xhr, status) {
        var promise = $.Deferred();
        if(status == 'success'){
            var result = JSON.parse(xhr.responseText);
            self.searchResultCallback(result);
            return promise.resolve();
        }else{
            return promise.reject();
        }
    });
}

/**
 * ajaxでIP一覧検索結果を処理
 */
IpListController.prototype.searchResultCallback = function(result) {
    var self = this;

    // データエスケープ処理
    Escape.escapeHtml(result);

    // IPマスタ一覧の表を描画
    self.createIpList(result);
}

/**
 * IPマスタ一覧の表を描画する
 */
IpListController.prototype.createIpList = function(result) {
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
IpListController.prototype.createColModel = function() {
    var width = $('#list').width();

    var modelArray = [];
    modelArray.push(
        GridUtil.createColModel({
            name: 'ip_code',
            width: width * 0.03
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'ip_name',
            width: width * 0.13,
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'ip_kana_name',
            width: width * 0.15,
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'ip_control_flg',        
            align : 'center',
            width : width * 0.04,
            formatter : GridUtil.formatMaruBatsu,
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
            width: width * 0.07,
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
                    '<button type="button" class="grid-btn-update" data-ip-code="' + rdt.ip_code + '">' + '編集' +'</button>'
                    + '<button type="button" class="grid-btn-delete" data-ip-name="' + rdt.ip_name 
                    + '" data-ip-code="' + rdt.ip_code + '" data-row-id="' + opt.rowId + '">' + '削除' + '</button>'
                );
            },
            sortable: false
        })
    );
    return {
        model: modelArray,
        name: ['IPコード', 'IP名', 'IPかな名', 'IP管理フラグ','最終更新者', '最終更新日時', 'データ操作']
    };
};

/**
 * jQGrid用のボタンイベント定義
 */
IpListController.prototype.gridBtnEvent = function(data) {

    $('.grid-btn-delete, .grid-btn-update').button();

    // 編集ボタンをクリックし、編集画面へ遷移する
    $('.grid-btn-update').on('click', function() {
        var button = $(this);
        // IPコードを取得
        var ipcode = button.attr('data-ip-code');
        // IP編集画面へ遷移
        window.location.href = '/admin_app/ip_update?ipc=' + ipcode;
    });

    $('.grid-btn-delete').off('click');
    // 削除ボタンをクリックし、削除処理を行う
    $('.grid-btn-delete').on('click', function() {
        var button = $(this);
        $('#delete-ip-code').text(button.attr('data-ip-code'));
        $('#delete-ip-name').text(button.attr('data-ip-name'));
        var modal = $('#delete-confirm-dialog');

        // 削除キャンセル処理
        $('.cancel-botton').on('click', function() {
            modal.dialog('close');
            $('.delete-button').off('click');
        });

        // ajaxで、削除処理を行う
        $('.delete-button').on('click', function() {
            var param = {
                'delete-ip-code' : $('#delete-ip-code').text(),
                'delete-ip-name' : $('#delete-ip-name').text(),
            };
            
            AjaxUtil.post('/admin_app/ip_list/', param).then(function(xhr, status) {
                if(status == 'success'){
                    var result = JSON.parse(xhr.responseText);
                    if(result.is_error){
                        // 削除メッセージ表示
                        MsgUtil.showStatusMsg('#list', $('#delete-ip-name').text() , '既に削除');
                    }else{
                         // 削除メッセージ表示
                         MsgUtil.showStatusMsg('#list', $('#delete-ip-name').text() , '削除');
                    }
                    // データエスケープ処理
                    Escape.escapeHtml(result.ip_list);
                    
                    // IPマスタ一覧の表を再描画
                    IpListController.prototype.createIpList(result.ip_list);
                    }
            }).then(function(){
                modal.dialog('close');
            });
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
IpListController.prototype.downloadCsv = function() {
    var self = this;
    
    // CSVダウンロード全件
    $('#csv-all').click(function() {
        AjaxUtil.get('/admin_app/ip_list/csv_download/', {}, function(data) {
            var fileName = 'IP情報_全件.csv';
            FileUtil.outputCsv(data, fileName);
        });
    });
}

$(function() {
    var controller = new IpListController();
    controller.init();
});