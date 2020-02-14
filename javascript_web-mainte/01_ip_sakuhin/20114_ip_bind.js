var IpBindController = function() {};
IpBindController.prototype = new AbstractController();

/**
 * メニュー選択処理
 */
IpBindController.prototype.selectedMenu = function() {
    return '.ip-bind';
};

/**
 * イベント登録処理
 */
IpBindController.prototype.bindEvent = function() {
    var self = this;
    //IP名検索のツールチープを追加
    TextfollowUtil.execute();

    // 更新履歴DLエリアのイベント設定
    NoticeTableUtil.setDLArea();

    // 更新履歴CSVダウンロード
    NoticeTableUtil.downloadTableCsv('m_ip_map', 'IP紐付け情報');

    // IP検索モーダル
    $('.search-ip').click(function () {
        self.selectIp();
    });

    // 関連作品追加モーダル
    $('.search-connection-sakuhin').click(function () {
        self.selectConnectionSakuhin();
    });

    // 作品検索モーダル
    $('.search-sakuhin').click(function () {
        self.selectSakuhin();
    });

    // 関連IP追加モーダル
    $('.search-connection-ip').click(function(){
        self.selectConnectionIp();
    });
    
    return $.Deferred().resolve().promise();
};

/**
 * IPマスタ検索 (ajaxでIPマスタ検索結果を取得)
 */
IpBindController.prototype.selectIp = function() {
    var self = this;

    // エラーメッセージ削除
    $('.input-err').removeClass('input-err');
    $('.input-err-msg').remove();

    // 入力チェックエラーの場合、検索を行わない
    if (!InputCheckUtil.checkInputValue('#input-ipname','IP名',100)) {
        return;
    }
    // IPデータ検索を行う
    self.selectIpByIpName();
}

/**
 * IPデータ検索を行う
 */
IpBindController.prototype.selectIpByIpName = function () {
    var self = this;
    // データ検索を行う
    var param = {
        'select-ip-modal' : 'select-ip-modal',
        'ip-name' : $('#input-ipname').val()
    };
    AjaxUtil.get('/admin_app/ip_bind/', param, function(data) {
        // 検索したIPデータ
        var result = JSON.parse(data.toString());
        if(result.length > 100){
            InputCheckUtil.showErrMsg('#input-ipname', '検索結果が100件以上のため、検索条件を絞って、もう一度検索してください。');
            return;
        }

        // IPマスタ一覧グリッドを描画
        self.createIpModalGrid(result);
        // IP一覧のモーダル定義
        var modal = $('#ip-dialog');
        var title = "IPを選択";
        // IP一覧のモーダル作成
        self.createModal(modal, title);
    });
}

/**
 * IP選択モーダルを作成
 */
IpBindController.prototype.createIpModalGrid = function (result) {
    var self = this;

    // 一覧データが10以下の場合は高さ自動調整
    var height = 'auto';
    if (result.length >= 10) {
        height = 450;
    }
    // グリッドを再描画
    $('#list-grid-ip').jqGrid('clearGridData');
    $("#list-grid-ip").jqGrid("GridUnload");
    // グリッド生成
    var colModel = self.createIpColModel('dialog');
    var option = {
        colNames: colModel.name,
        colModel: colModel.model,
        data: result,
        width: $('#ip-list').width(),
        height : height,
        pager: '#ip-pager',
        loadComplete: function(){self.selectIpBtn()},
        pgbuttons : false,
        pginput : false,
        viewrecords : true,
        rowList : result.length,
        rowNum : result.length
    };
    // グリッドを初期描画
    GridUtil.renderNormalGrid('#list-grid-ip', option, true);
};

/**
 * jQGrid用のカラム定義（IP選択モーダル用）
 */
IpBindController.prototype.createIpColModel = function (flg) {
    var width = 2200;
    if ("dialog" == flg) {
        var width = 1700;
    }

    var modelArray = [];
    modelArray.push(
        GridUtil.createColModel({
            name: 'ip_code',
            width: width * 0.1
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'ip_name',
            width: width * 0.15
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'ip_kana_name',
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
            formatter: function (val, opt, rdt) {
                if("dialog" == flg){
                    return "<button type='button' class='grid-btn-update grid-btn-selectip' data-ip-name='" 
                    + rdt.ip_name + "' data-ip-code='" + rdt.ip_code + "'>" + '選択' + '</button>';
                }else{
                    return "<button type='button' class='grid-btn-delete connection-ip-del-btn' data-ip-name='" 
                    + rdt.ip_name + "' data-ip-code='" + rdt.ip_code + "' data-ip-map-id='"+rdt.ip_map_id+"'>" + '紐付けを解除' + '</button>';
                }
            },
            sortable: false
        })
    );
    return {
        model: modelArray,
        name: ['IPコード', 'IP名', 'IPかな名', '最終更新者', '最終更新日時', '操作']
    };
};

/**
 * IP選択モーダルのイベントを設定する
 */
IpBindController.prototype.selectIpBtn = function () {
    var self = this;
    $('.grid-btn-selectip').button();
    $('.grid-btn-selectip').on('click', function () {

        var button = $(this);
        //選択IP名を設定
        $('.select-ip-doc').text(button.attr('data-ip-name'));
        $('.select-ip-doc').val(button.attr('data-ip-code'));

        //IPモーダル閉じる
        $('#ip-dialog').dialog('close');

        // 関連作品データの検索を行う
        $('#errorMsg').hide();
        self.selectSakuhinByIpCode(button.attr('data-ip-code')).fail(function(){
            $('#errorMsg').show();
        });
    });
};

/**
 * 関連作品データの検索を行う<br>
 * グリッドを使用して表を描画する。
 */
IpBindController.prototype.selectSakuhinByIpCode = function (ip_code) {
    var self = this;
    // 当IPの関連作品データの検索を行う
    
    var param = {
        'select-sakuhin-list' : 'select-sakuhin-list',
        'ip-code' : ip_code
    };
    return AjaxUtil.get('/admin_app/ip_bind/', param).then(function(xhr, status) {
        var promise = $.Deferred();
        if(status == 'success'){
            var result = JSON.parse(xhr.responseText);
            // 関連作品一覧 グリッド生成
            self.createConnectionSakuhinList(result);
            //関連作品管理領域表示
            $('.connection-sakuhin-list').slideDown();

            return promise.resolve();
        }else{
            return promise.reject();
        }
    });
}

/**
 * 関連作品一覧生成<br>
 * グリッドを使用して表を描画する。
 */
IpBindController.prototype.createConnectionSakuhinList = function (result) {
    var self = this;

    // 一覧データが10以下の場合は高さ自動調整
    var height = 'auto';
    if (result.length >= 10) {
        height = 450;
    }

    // グリッドを再描画
    if ($('#gbox_list-grid-connectionsakuhin').is(':visible')) {
        $('#list-grid-connectionsakuhin').jqGrid('clearGridData').trigger('reloadGrid');
        $('#list-grid-connectionsakuhin').jqGrid('setGridHeight', height).trigger('reloadGrid');
        $('#list-grid-connectionsakuhin').jqGrid('setGridParam', {
            data : result,
            rowNum : result.length,
        }).trigger('reloadGrid');
    }else{
        // グリッド生成
        var colModel = self.createConnectionSakuhinColModel('list');
        var option = {
            colNames: colModel.name,
            colModel: colModel.model,
            data: result,
            width: 'auto',
            height : height,
            pager: '#connectionsakuhin-pager',
            loadComplete: function(){self.conSakuhinDelBtn()},
            pgbuttons : false,
            pginput : false,
            viewrecords : true,
            rowList : result.length,
            rowNum : result.length
        };
        // グリッドを初期描画
        GridUtil.renderNormalGrid('#list-grid-connectionsakuhin', option, true);
    }
};

/**
 * グリッド用のカラム定義（関連作品一覧モーダル用）
 */
IpBindController.prototype.createConnectionSakuhinColModel = function (flg) {
    var width = 2200;

    if ("dialog" == flg) {
        width = 1700;
    }

    var modelArray = [];
    modelArray.push(
        GridUtil.createColModel({
            name: 'sakuhin_code',
            width: width * 0.1
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'sakuhin_name',
            width: width * 0.15
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'sakuhin_kana_name',
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
            formatter: function (val, opt, rdt) {
                if ("dialog" == flg) {
                    return (
                        '</button>' + "<button type='button' class='grid-btn-update grid-btn-sakuhin' data-sakuhin-name='"
                        + rdt.sakuhin_name + "' data-ip-map-id='" + rdt.ip_map_id + "' data-sakuhin-code='" 
                        + rdt.sakuhin_code + "'>" + '選択' + '</button>'
                    );
                }else{
                    return (
                        '</button>' + "<button type='button' class='grid-btn-delete connection-sakuhin-del-btn' data-sakuhin-name='"
                        + rdt.sakuhin_name + "' data-ip-map-id='" + rdt.ip_map_id + "' data-sakuhin-code='" 
                        + rdt.sakuhin_code + "'>" + '紐付けを解除' + '</button>'
                    );
                }
            },
            sortable: false
        })
    );
    return {
        model: modelArray,
        name: ['作品コード', '作品名', '作品かな名', '最終更新者', '最終更新日時', 'データ操作']
    };
};

/**
 * 関連作品紐付け解除ボタンイベントを設定する
 */
IpBindController.prototype.conSakuhinDelBtn = function (data) {
    var self = this;
    $('.connection-sakuhin-del-btn').button();

    $('.connection-sakuhin-del-btn').off('click');
    //紐付け解除ボタンをクリックし、紐付け解除処理を行う
    $('.connection-sakuhin-del-btn').on('click', function () {
        var button = $(this);
        // 作品コードと作品名をダイアログに設定
        $('#delete-sakuhin-code').text(button.attr('data-sakuhin-code'));
        $('#delete-sakuhin-name').text(button.attr('data-sakuhin-name'));

        // 作品紐付け解除ダイアログ
        var modal = $('#sakuhin-del-dialog');

        // キャンセル処理
        $('.cancel-botton').on('click', function () {
            modal.dialog('close');
            $('.delete-button').off('click');
        });

        //作品紐付け解除処理
        $('.delete-button').on('click', function () {
            var param = {
                'delete-sakuhin' : 'delete-sakuhin',
                'ip-map-id' : button.attr('data-ip-map-id'),
                'ip-code' : $('.select-ip-doc').val(),
                'ip-name' : $('.select-ip-doc').text(),
                'sakuhin-name' : button.attr('data-sakuhin-name'),
            };
            AjaxUtil.get('/admin_app/ip_bind/', param, function(data) {
                var result = JSON.parse(data.toString());

                // 関連作品管理一覧を再描画
                self.createConnectionSakuhinList(result);
            });

            modal.dialog('close');
            $('.delete-button').off('click');
        });

        modal.dialog({
            modal: true,
            width: 500,
        });
    });
};


/**
 * 関連作品追加モーダル
 */
IpBindController.prototype.selectConnectionSakuhin = function () {
    var self = this;
    // エラーメッセージ削除
    $('.input-err').removeClass('input-err');
    $('.input-err-msg').remove();

    // 入力チェックエラーの場合、検索を行わない
    if (!InputCheckUtil.checkInputValue('#input-con-sakuhin','作品名',100)) {
        return;
    }
    //  関連作品モーダルデータ検索を行う
    self.selectSakuhinBySakuhinName();
};

/**
 * 関連作品モーダルデータ検索を行う
 */
IpBindController.prototype.selectSakuhinBySakuhinName = function () {
    var self = this;
    var param = {
        'sakuhin-modal' : 'sakuhin-modal',
        'sakuhin-name' :  $('#input-con-sakuhin').val()
    };
    AjaxUtil.get('/admin_app/ip_bind/', param, function(data) {

        var result = JSON.parse(data.toString());
        if(result.length > 100){
            InputCheckUtil.showErrMsg('#input-con-sakuhin', '検索結果が100件以上のため、検索条件を絞って、もう一度検索してください。');
            return;
        }

        // 関連作品一覧の表を描画
        self.createConnectionSakuhinModal(result);

        // 関連作品一覧のモーダル定義
        var modal = $('#connection-sakuhin-dialog');
        var title = "関連作品を選択";
        // 関連作品一覧のモーダル作成
        self.createModal(modal, title);

        // モーダル内の「関連作品を選択」ボタンを非活性に設定
        $('.con-sakuhin-add-button').button({disabled: true});
    });
}

/**
 * 関連作品グリッドを作成
 */
IpBindController.prototype.createConnectionSakuhinModal = function (result) {
    var self = this;
    // 関連作品リストの作品コードを取得する
    var conSakuhinCode = $('#list-grid-connectionsakuhin').jqGrid("getCol", "sakuhin_code");
    // 一覧データが10以下の場合は高さ自動調整
    var height = 'auto';
    if (result.length >= 10) {
        height = 450;
    }
    // グリッドを再描画
    $('#list-grid-sakuhin-con').jqGrid('clearGridData');
    $("#list-grid-sakuhin-con").jqGrid("GridUnload");
    // グリッド生成
    var colModel = self.createConnectionSakuhinModalgrid();
    var option = {
        datatype: "local",
        colNames: colModel.name,
        colModel: colModel.model,
        data: result,
        width: 'auto',
        height : height,
        pager: '#modal-sakuhin-pager',
        loadComplete: function(){
            self.addSakuhinBtn();
        },
        pgbuttons : false,
        pginput : false,
        viewrecords : true,
        rowList : result.length,
        rowNum : result.length,
        rowattr: function (rowData, currentObj, rowId) {
            if(conSakuhinCode.indexOf(currentObj.sakuhin_code) > -1){
                  return {"style":"background:silver; height:44px;placeholder: 'placeholderBackground' "};
            }
        }
    };
    // グリッドを初期描画
    GridUtil.renderNormalGrid('#list-grid-sakuhin-con', option, true);
};

/**
 * 関連作品追加モーダル用グリッドのカラム定義
 */
IpBindController.prototype.createConnectionSakuhinModalgrid = function () {
    var width = 1700;

    var modelArray = [];
    var conSakuhinCode = $('#list-grid-connectionsakuhin').jqGrid("getCol", "sakuhin_code");

    modelArray.push(GridUtil.createColModel({
        name: 'checkbox',
        width: width * 0.07,
        align: 'center',
        formatter: function (val, opt, rdt) {
            if(conSakuhinCode.indexOf(rdt.sakuhin_code) > -1){
                return "<label>ー</label>";
            }else{
                return ('<input type="checkbox" class="checkbox sakuhin-checkbox" data-sakuhin-name="'+ rdt.sakuhin_name +'" value="' 
                + rdt.sakuhin_code + '"style="margin: 10px;"' + '">');
            }
        },
        sortable: false
    }));
    modelArray.push(
        GridUtil.createColModel({
            name: 'sakuhin_code',
            width: width * 0.1
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'sakuhin_name',
            width: width * 0.13
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'sakuhin_kana_name',
            width: width * 0.12
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'update_user',
            width: width * 0.08
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
            formatter: function (val, opt, rdt) {
                if(conSakuhinCode.indexOf(rdt.sakuhin_code) > -1){
                    return "<label>" + '登録済み' + '</label>';
                }else{
                    return "<button type='button' class='grid-btn-update select-sakuhin-add-btn' data-sakuhin-name='" 
                    + rdt.sakuhin_name + "'data-sakuhin-code='" + rdt.sakuhin_code+ "'>" + '選択' + '</button>';
                }
            },
            sortable: false
        })
    );
    return {
        model: modelArray,
        name: ['チェックボックス','作品コード', '作品名', '作品かな名', '最終更新者', '最終更新日時', '選択']
    };
};

/**
 * 関連作品追加処理を行う
 */
IpBindController.prototype.addSakuhinBtn = function () {
    var self = this;
    // 選択ボタンの作品追加処理
    self.addSelectSakuhinBtn();

    // チェックボックス選択した場合、「関連作品を選択」ボタン活性に設定
    $('.sakuhin-checkbox').off('click');
    $('.sakuhin-checkbox').on('change', function() {
        var disabled = $('.sakuhin-checkbox:checked').length == 0;
        $('.con-sakuhin-add-button').button({disabled: disabled});
    });

    // 関連作品追加ボタンの追加処理
    self.addConnectionSakuhinBtn();
};

/**
 * 関連作品追加イベントを設定する（選択ボタン）
 */
IpBindController.prototype.addSelectSakuhinBtn = function () {
    var self = this;
    $('.select-sakuhin-add-btn').button();
    $('.select-sakuhin-add-btn').off('click');
    $('.select-sakuhin-add-btn').on('click',function(){
        var button = $(this);
        // 作品モーダルを閉じる
        $('#connection-sakuhin-dialog').dialog('close');

        // 作品コードを取得
        var sakuhin_code = button.attr('data-sakuhin-code');

        $('#errorMsg').hide();
        self.updateConnectionSakuhin([sakuhin_code]).fail(function(){
            $('#errorMsg').show();
        });
    })
}

/**
 * 関連作品追加処理を行う
 */
IpBindController.prototype.updateConnectionSakuhin = function(sakuhinCodeList){
    var self = this;
    // パラメータ設定
     $('#errorMsg').hide();
    var param = {
        'add-sakuhin' : 'add-sakuhin',
        'ip-code' : $('.select-ip-doc').val(),
        'ip-name' : $('.select-ip-doc').text(),
        'sakuhin-code' : JSON.stringify(sakuhinCodeList)
    };
    return AjaxUtil.get('/admin_app/ip_bind/', param).then(function(xhr, status) {
        var promise = $.Deferred();
        // ajax実行成功する場合、関連作品一覧グリッドを描画する
        if(status == 'success'){
            // 最新の関連作品データを取得
            var result = JSON.parse(xhr.responseText);
            // 関連作品一覧 グリッド生成
            self.createConnectionSakuhinList(result);

            return promise.resolve();
        }else{
            return promise.reject();
        }
    });
}

/**
 * 関連作品追加イベントを設定する（関連作品追加ボタン）
 */
IpBindController.prototype.addConnectionSakuhinBtn = function () {
    var self = this;
    $('.con-sakuhin-add-button').button();
    $('.con-sakuhin-add-button').off('click');
    $('.con-sakuhin-add-button').on('click', function () {

        var button = $(this);
        //作品モーダル閉じる
        $('#connection-sakuhin-dialog').dialog('close');

        // sakuhinCode配列を宣言する
        var sakuhinCodeList = [];
        // 関連作品コード取得
        $('.sakuhin-checkbox:checked').each(function() {
            // 作品コードを取得
            var sakuhin_code = $(this).val();
            sakuhinCodeList.push(sakuhin_code);
        });

        if(sakuhinCodeList.length == 0){
            return;
        }
        self.updateConnectionSakuhin(sakuhinCodeList);
    });
};

/**
 * 作品データ検索を行う（タブ２）
 */
IpBindController.prototype.selectSakuhin = function () {
    var self = this;

    // エラーメッセージ削除
    $('.input-err').removeClass('input-err');
    $('.input-err-msg').remove();
    // 入力チェックエラーの場合、検索を行わない
    if (!InputCheckUtil.checkInputValue('#input-sakuhin-name','作品名',100)) {
        return;
    }
    //  関連作品モーダルデータ検索を行う
    self.selectSakuhinModal();
};

/**
 * 作品モーダルデータ検索を行う（タブ２）
 */
IpBindController.prototype.selectSakuhinModal = function () {
    var self = this;
    var param = {
        'sakuhin-modal' : 'sakuhin-modal',
        'sakuhin-name' : $('#input-sakuhin-name').val()
    };
    AjaxUtil.get('/admin_app/ip_bind/', param, function(data) {

        var result = JSON.parse(data.toString());
        if(result.length > 100){
            InputCheckUtil.showErrMsg('#input-sakuhin-name', '検索結果が100件以上のため、検索条件を絞って、もう一度検索してください。');
            return;
        }

        // 作品一覧グリッド作成
        self.createSakuhinGrid(result);

        // 作品一覧のモーダル定義
        var modal = $('#sakuhin-dialog');
        var title = "作品を選択";
        // 関連作品一覧のモーダル作成
        self.createModal(modal, title);
    });
}

/**
 * 作品モーダルデータを作成（タブ２）
 */
IpBindController.prototype.createSakuhinGrid = function (result) {
    var self = this;

    // 一覧データが10以下の場合は高さ自動調整
    var height = 'auto';
    if (result.length >= 10) {
        height = 450;
    }
    // グリッドを再描画
    $('#list-sakuhin-modal').jqGrid('clearGridData');
    $("#list-sakuhin-modal").jqGrid("GridUnload");
    // グリッド生成
    var colModel = self.createConnectionSakuhinColModel('dialog');
    var option = {
        colNames: colModel.name,
        colModel: colModel.model,
        data: result,
        width: $('#sakuhin-list').width(),
        height : height,
        pager: '#sakuhin-pager',
        loadComplete: function(){self.selectSakuhinBtn()},
        pgbuttons : false,
        pginput : false,
        viewrecords : true,
        rowList : result.length,
        rowNum : result.length
    };
    // グリッドを初期描画
    GridUtil.renderNormalGrid('#list-sakuhin-modal', option, true);
};

/**
 * IP選択モーダルイベントを設定する
 */
IpBindController.prototype.selectSakuhinBtn = function () {
    var self = this;
    $('.grid-btn-sakuhin').button();
    $('.grid-btn-sakuhin').off('click')
    $('.grid-btn-sakuhin').on('click', function () {

        var button = $(this);
        //選択作品名を表示
        $('.select-sakuhin-doc').text(button.attr('data-sakuhin-name'));
        $('.select-sakuhin-doc').val(button.attr('data-sakuhin-code'));

        //作品名モーダル閉じる
        $('#sakuhin-dialog').dialog('close');

        // 関連IPデータの検索を行う
        $('#errorMsg').hide();
        self.selectIpBySakuhincode(button.attr('data-sakuhin-code')).fail(function(){
            $('#errorMsg').show();
        });
    });
};

/**
 * 関連IPデータ検索を行う
 */
IpBindController.prototype.selectIpBySakuhincode = function (sakuhin_code) {
    var self = this;
    // データ検索を行う
    var param = {
        'select-ip-list' : 'select-ip-list',
        'sakuhin-code' : sakuhin_code
    };
    return AjaxUtil.get('/admin_app/ip_bind/', param).then(function(xhr, status) {
        var promise = $.Deferred();
        if(status == 'success'){
            var result = JSON.parse(xhr.responseText);
            // 関連IP一覧 グリッド生成
            self.createConnectionIpList(result);
            //関連IP管理領域表示
            $('.connection-ip-list').slideDown();

            return promise.resolve();
        }else{
            return promise.reject();
        }
    });
}

/**
 * 関連IP一覧生成<br>
 * グリッドを使用して表を描画する。
 */
IpBindController.prototype.createConnectionIpList = function (result) {
    var self = this;

    // 一覧データが10以下の場合は高さ自動調整
    var height = 'auto';
    if (result.length >= 10) {
        height = 450;
    }

    // グリッドを再描画
    if ($('#gbox_list-grid-connectionip').is(':visible')) {
        $('#list-grid-connectionip').jqGrid('clearGridData').trigger('reloadGrid');
        $('#list-grid-connectionip').jqGrid('setGridHeight', height).trigger('reloadGrid');
        $('#list-grid-connectionip').jqGrid('setGridParam', {
            data : result,
            rowNum : result.length,
        }).trigger('reloadGrid');
    }else{
        // グリッド生成
        var colModel = self.createIpColModel('list');
        var option = {
            colNames: colModel.name,
            colModel: colModel.model,
            data: result,
            width: 'auto',
            height : height,
            pager: '#connectionip-pager',
            loadComplete: function(){self.connectIpBtn()},
            pgbuttons : false,
            pginput : false,
            viewrecords : true,
            rowList : result.length,
            rowNum : result.length
        };
        // グリッドを初期描画
        GridUtil.renderNormalGrid('#list-grid-connectionip', option, true);
    }
};

/**
 * 関連IP紐付け解除ボタンイベントを設定する
 */
IpBindController.prototype.connectIpBtn = function (data) {
    var self = this;
    $('.connection-ip-del-btn').button();

    //紐付け解除ボタンをクリックし、紐付け解除処理を行う
    $('.connection-ip-del-btn').off('click');
    $('.connection-ip-del-btn').on('click', function () {
        var button = $(this);
        // IPコードとIP名をダイアログに設定
        $('#delete-ip-code').text(button.attr('data-ip-code'));
        $('#delete-ip-name').text(button.attr('data-ip-name'));

        // IP紐付け解除ダイアログ
        var modal = $('#ip-del-dialog');

        // キャンセル処理
        $('.cancel-botton').on('click', function () {
            modal.dialog('close');
            $('.delete-button').off('click');
        });

        //IP紐付け解除処理
        $('.delete-button').on('click', function () {
            var param = {
                'delete-ip' : 'delete-ip',
                'ip-map-id' : button.attr('data-ip-map-id'),
                'sakuhin-code' : $('.select-sakuhin-doc').val(),
                'sakuhin-name' : $('.select-sakuhin-doc').text(),
                'ip-name' : button.attr('data-ip-name'),
            };
            AjaxUtil.get('/admin_app/ip_bind/', param, function(data) {
                var result = JSON.parse(data.toString());
                // IP作品管理一覧を再描画
                self.createConnectionIpList(result);
            });

            modal.dialog('close');
            $('.delete-button').off('click');
        });

        modal.dialog({
            modal: true,
            width: 500,
        });
    });
};

/**
 * 関連IP追加モーダル
 */
IpBindController.prototype.selectConnectionIp = function () {
    var self = this;
    // エラーメッセージ削除
    $('.input-err').removeClass('input-err');
    $('.input-err-msg').remove();

    // 入力チェックエラーの場合、検索を行わない
    if (!InputCheckUtil.checkInputValue('#input-con-ip','IP名',100)) {
        return;
    }
    //  関連IPモーダルデータ検索を行う
    self.selectIpBySakuhinName();
};

/**
 * 関連作品モーダルデータ検索を行う
 */
IpBindController.prototype.selectIpBySakuhinName = function () {
    var self = this;
    var param = {
        'ip-modal' : 'ip-modal',
        'ip-name' : $('#input-con-ip').val()
    };
    AjaxUtil.get('/admin_app/ip_bind/', param, function(data) {

        var result = JSON.parse(data.toString());

        // 関連IP一覧の表を描画
        self.createConnectionIpModal(result);
        if(result.length > 100){
            InputCheckUtil.showErrMsg('#input-con-ip', '検索結果が100件以上のため、検索条件を絞って、もう一度検索してください。');
            return;
        }

        // 関連IP一覧のモーダル定義
        var modal = $('#connection-ip-dialog');
        var title = "関連IPを選択";
        // 関連IP一覧のモーダル作成
        self.createModal(modal, title);
        
        // モーダル内の「関連IPを選択」ボタンを非活性に設定
        $('.con-ip-add-button').button({disabled: true});

    });
}

/**
 * 関連作品グリッドを作成
 */
IpBindController.prototype.createConnectionIpModal = function (result) {
    var self = this;
    // 関連IPリストのIPコードを取得する
    var conIpCode = $('#list-grid-connectionip').jqGrid("getCol", "ip_code");
    // 一覧データが10以下の場合は高さ自動調整
    var height = 'auto';
    if (result.length >= 10) {
        height = 450;
    }
    // グリッドを再描画
    $('#list-grid-ip-con').jqGrid('clearGridData');
    $("#list-grid-ip-con").jqGrid("GridUnload");
    // グリッド生成
    var colModel = self.createConnectionIpModalgrid();
    var option = {
        colNames: colModel.name,
        colModel: colModel.model,
        data: result,
        width: 'auto',
        height : height,
        pager: '#modal-ip-pager',
        loadComplete: function(){self.addIpBtn()},
        pgbuttons : false,
        pginput : false,
        viewrecords : true,
        rowList : result.length,
        rowNum : result.length,
        rowattr: function (rowData, currentObj, rowId) {
            if(conIpCode.indexOf(currentObj.ip_code) > -1){
                  return {"style":"background:silver; height:44px; placeholder: 'placeholderBackground' "};
            }
        }
    };
    // グリッドを初期描画
    GridUtil.renderNormalGrid('#list-grid-ip-con', option, true);
};

/**
 * 関連IP追加モーダル用グリッドのカラム定義
 */
IpBindController.prototype.createConnectionIpModalgrid = function () {
    var width = 1700;

    var modelArray = [];
    // 関連IPリストのIPコードを取得する
    var conIpCode = $('#list-grid-connectionip').jqGrid("getCol", "ip_code");
    modelArray.push(GridUtil.createColModel({
        name: 'checkbox',
        width: width * 0.07,
        align: 'center',
        formatter: function (val, opt, rdt) {
            if(conIpCode.indexOf(rdt.ip_code) > -1){
                return "<label>ー</label>";
            }else{
                return ('<input type="checkbox" class="checkbox ip-checkbox" data-ip-name="'+ rdt.ip_name +'" value="' 
                + rdt.ip_code + '"style="margin: 10px;"' + '">');
            }
        },
        sortable: false
    }));
    modelArray.push(
        GridUtil.createColModel({
            name: 'ip_code',
            width: width * 0.1
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'ip_name',
            width: width * 0.13
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'ip_kana_name',
            width: width * 0.12
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'update_user',
            width: width * 0.08
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
            formatter: function (val, opt, rdt) {
                if(conIpCode.indexOf(rdt.ip_code) > -1){
                    return "<label>" + '登録済み' + '</label>';
                }else{
                    return "<button type='button' class='grid-btn-update select-ip-add-btn' data-ip-name='" 
                    + rdt.ip_name + "'data-ip-code='" + rdt.ip_code + "'>" + '選択' + '</button>';
                }
            },
            sortable: false
        })
    );
    return {
        model: modelArray,
        name: ['チェックボックス','IPコード', 'IP名', 'IPかな名', '最終更新者', '最終更新日時', '選択']
    };
};

/**
 * 関連IP追加処理を行う
 */
IpBindController.prototype.addIpBtn = function () {
    var self = this;
    // 選択ボタンのIP追加処理
    self.addSelectIpBtn();

    // チェックボックス選択した場合、「関連IPを選択」ボタン活性に設定
    $('.ip-checkbox').off('click');
    $('.ip-checkbox').on('change', function() {
        var disabled = $('.ip-checkbox:checked').length == 0;
        $('.con-ip-add-button').button({disabled: disabled});
    });
    
    // 関連IP追加ボタンの追加処理
    self.addConnectionIpBtn();
};

/**
 * 関連IP追加イベントを設定する（選択ボタン）
 */
IpBindController.prototype.addSelectIpBtn = function () {
    var self = this;
    $('.select-ip-add-btn').button();
    $('.select-ip-add-btn').off('click');
    $('.select-ip-add-btn').on('click',function(){
        var button = $(this);
        // IPモーダルを閉じる
        $('#connection-ip-dialog').dialog('close');

        // IPコードを取得
        var ip_code = button.attr('data-ip-code');
        // 関連IP追加処理を行う
        $('#errorMsg').hide();
        self.updateConnectionIp([ip_code]).fail(function(){
            $('#errorMsg').show();
        });
    })
}

/**
 * 関連IP追加処理を行う
 */
IpBindController.prototype.updateConnectionIp = function(ipCodeList){
    var self = this;
    // パラメータ設定
    var param = {
        'add-ip' : 'add-ip',
        'sakuhin-code' : $('.select-sakuhin-doc').val(),
        'sakuhin-name' : $('.select-sakuhin-doc').text(),
        'ip-code' : JSON.stringify(ipCodeList)
    };
    return AjaxUtil.get('/admin_app/ip_bind/', param).then(function(xhr, status) {
        var promise = $.Deferred();
        if(status == 'success'){
            // 最新の関連作品データを取得
            var result = JSON.parse(xhr.responseText);
            // 関連IP一覧 グリッド生成
            self.createConnectionIpList(result);

            return promise.resolve();
        }else{
            return promise.reject();
        }
    });
}

/**
 * 関連IP追加イベントを設定する（関連作品追加ボタン）
 */
IpBindController.prototype.addConnectionIpBtn = function () {
    var self = this;
    $('.con-ip-add-button').button();
    $('.con-ip-add-button').off('click');
    $('.con-ip-add-button').on('click', function () {

        var button = $(this);
        //IPモーダル閉じる
        $('#connection-ip-dialog').dialog('close');

        // ipCode配列を宣言する
        var ipCodeList = [];

        // 関連IPコード取得
        $('.ip-checkbox:checked').each(function() { 
            // IPコードを取得
            var ip_code = $(this).val();
            ipCodeList.push(ip_code);
        });

        if(ipCodeList.length == 0){
            return;
        }
        // 関連IP追加処理を行う
        self.updateConnectionIp(ipCodeList);
    });
};

/**
 * 関連作品モーダル定義
 */
IpBindController.prototype.createModal = function (modal, title) {
    modal.dialog({
        modal: true,
        title: title,
        resizable: false,
        width: 'auto',
        height: 'auto'
    });
    // モーダルを閉じる
    $('.cancel-button').on('click', function() {
        modal.dialog('close');
    });
}

$(function() {
    var controller = new IpBindController();
    controller.init();
});
