var SakuhinBindController = function() {};
SakuhinBindController.prototype = new AbstractController();

/**
 * メニュー選択処理
 */
SakuhinBindController.prototype.selectedMenu = function() {
    return '.sakuhin-bind';
};
/**
 * イベント登録処理
 */
SakuhinBindController.prototype.bindEvent = function() {
    var self = this;

    //ツールチープを追加
    TextfollowUtil.execute();

    // 更新履歴DLエリアのイベント設定
    NoticeTableUtil.setDLArea();

    // 更新履歴CSVダウンロード
    NoticeTableUtil.downloadTableCsv('m_sakuhin_map', '作品紐付け情報');

    // 作品検索モーダル
    $('.search-sakuhin').click(function () {
        self.selectSakuhin();
    });

    // 関連タイトル検索モーダル
    $('.search-title').click(function () {
        self.selectTitle();
    });

    // 関連作品名検索モーダル（Twitter）
    $('.search-twitter-sakuhin').click(function () {
        $('#status-msg').remove();
        self.selectTwitterSakuhin();
    });
    
    // Twitterアカウント名検索モーダル
    $('.search-twitter').click(function () {
        $('#status-msg').remove();
        self.selectTwitter();
    });

    // game名検索モーダル
    $('.search-game').click(function () {
        self.selectGame();
    });

    // 関連作品名検索モーダル（Game）
    $('.search-game-sakuhin').click(function () {
        self.selectGameConSakuhin();
    });
    
    return $.Deferred().resolve().promise();
};

/**
 * 作品データ検索を行う
 */
SakuhinBindController.prototype.selectSakuhin = function () {
    var self = this;
    // エラーメッセージ削除
    $('.input-err').removeClass('input-err');
    $('.input-err-msg').remove();
    // 入力チェックエラーの場合、検索を行わない
    if (!InputCheckUtil.checkInputValue('#input-sakuhin-name','作品名',100)) {
        return;
    }
    //  作品モーダルデータ検索を行う
    self.selectSakuhinModal();
};

/**
 * 作品モーダルデータ検索を行う
 */
SakuhinBindController.prototype.selectSakuhinModal = function () {
    var self = this;
    $('#errorMsg').hide();

    // パラメータ設定
    var param = {
        'sakuhin-modal' : 'sakuhin-modal',
        'sakuhin-name' : $('#input-sakuhin-name').val()
    };
    AjaxUtil.get('/admin_app/sakuhin_bind/', param).then(function(xhr, status){
        // ajax実行成功する場合、作品モーダルグリッドを描画する
        if(status == 'success'){
            // データを取得
            var result = JSON.parse(xhr.responseText);
            if(result.length > 100){
                InputCheckUtil.showErrMsg('#input-sakuhin-name', '検索結果が100件以上のため、検索条件を絞って、もう一度検索してください。');
                return;
            }
            // データを取得後、グリッド設定処理
            self.setSakuhinModelGrid(result);
        }else{
            // ajax実行失敗する場合、エラーメッセージを表示する
            $('#errorMsg').show();
        }
    });
};

/**
 * 作品モーダルグリッド設定
 */
SakuhinBindController.prototype.setSakuhinModelGrid = function (result) {
    var self = this;

    // グリッド生成
    var colModel = self.createSakuhinColModel('dialog');
    // グリッドイベント設定
    var event = self.selectSakuhinBtn;
    // グリッドoption設定
    self.createModelOption(result,'#list-sakuhin-modal','#sakuhin-pager',colModel,event);

    // 作品を選択モーダル定義
    var modal = $('#sakuhin-dialog');
    var title = "作品を選択";
    //作品を選択モーダル作成
    self.createModal(modal, title);
}

/**
 * 作品一覧モーダルグリッド用のカラム定義
 */
SakuhinBindController.prototype.createSakuhinColModel = function (flg) {
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
                    return ('</button>' + "<button type='button' class='grid-btn-update select-sakuhin-btn' data-sakuhin-name='"
                        + Escape.escapeString(rdt.sakuhin_name) + "' data-sakuhin-code='" + rdt.sakuhin_code + "'>" + '選択' + '</button>');
                }else{
                    return (
                        '</button>' + "<button type='button' class='grid-btn-delete del-sakuhin-btn' data-sakuhin-name='"
                        + Escape.escapeString(rdt.sakuhin_name) + "' data-sakuhin-map-id='" + rdt.sakuhin_map_id + "' data-sakuhin-code='" 
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
 * 作品を選択モーダルイベントを設定する
 */
SakuhinBindController.prototype.selectSakuhinBtn = function (self) {
    var self = self;
    $('.select-sakuhin-btn').button();
    $('.select-sakuhin-btn').off('click')
    $('.select-sakuhin-btn').on('click', function () {

        var button = $(this);
        //選択作品名を表示
        $('.select-sakuhin-doc').text(button.attr('data-sakuhin-name'));
        $('.select-sakuhin-doc').val(button.attr('data-sakuhin-code'));

        //作品名モーダル閉じる
        $('#sakuhin-dialog').dialog('close');

        // 関連タイトルの検索を行う
        var sakuhin_code = button.attr('data-sakuhin-code');
        self.selectTitleList(sakuhin_code);
    });
};

/**
 * 関連タイトル検索を行う
 */
SakuhinBindController.prototype.selectTitleList = function (sakuhin_code) {
    var self = this;
    // データ検索を行う
    $('#errorMsg').hide();
    var param = {
        'title-list' : 'title-list',
        'sakuhin-code' : sakuhin_code
    };
    AjaxUtil.get('/admin_app/sakuhin_bind/', param).then(function(xhr, status) {
        if(status == 'success'){
            // データを取得
            var result = JSON.parse(xhr.responseText);

            // データを取得後、関連タイトル管理一覧グリッドを描画
            self.setTtileListGrid(result);
        }else{
            $('#errorMsg').show();
        }
    });
};

/**
 * 関連タイトルグリッド設定
 */
SakuhinBindController.prototype.setTtileListGrid = function (result) {
    var self = this;
    // 関連タイトルグリッドOption設定
    var colModel = self.createTitleColModel();
    var event = self.titleDelBut;
    self.createListOption(result,'#list-grid-title','#title-pager',colModel,event,'#gbox_list-grid-title');
    
    //関連タイトル管理領域表示
    $('.title-list').slideDown();
}

/**
 * 関連タイトルグリッド用のカラム定義
 */
SakuhinBindController.prototype.createTitleColModel = function () {
    var width = 2200;

    var modelArray = [];
    modelArray.push(
        GridUtil.createColModel({
            name: 'title_code',
            width: width * 0.27,
            hidden: true
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'title_name',
            width: width * 0.27
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'title_category_name',
            width: width * 0.1
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
                return (
                    '</button>' + "<button type='button' class='grid-btn-delete del-title-btn' data-title-name='" 
                    + Escape.escapeString(rdt.title_name) + "'data-title-code='" + rdt.title_code + "'data-sakuhin-map-id='" 
                    + rdt.sakuhin_map_id + "'data-category-name='" + rdt.title_category_name +"'>" + '紐付けを解除' + '</button>'
                );
            },
            sortable: false
        })
    );
    return {
        model: modelArray,
        name: ['タイトルコード','タイトル名', '種別', '最終更新者', '最終更新日時', 'データ操作']
    };
};

/**
 * 関連タイトル紐付け解除処理を行う
 */
SakuhinBindController.prototype.titleDelBut = function (self) {
    var self = self;
    $('.del-title-btn').button();
    $('.del-title-btn').off('click');
    //紐付け解除ボタンをクリックし、紐付け解除処理を行う
    $('.del-title-btn').on('click', function () {
        var button = $(this);
        // タイトルコードとタイトル名をダイアログに設定
        $('#delete-title-code').text(button.attr('data-title-code'));
        $('#delete-title-name').text(button.attr('data-title-name'));

        // タイトル紐付け解除ダイアログ
        var modal = $('#del-title-dialog');

        // キャンセル処理
        $('.cancel-botton').on('click', function () {
            modal.dialog('close');
            $('.delete-button').off('click');
        });

        //タイトル紐付け解除処理
        $('.delete-button').on('click', function () {
            var param = {
                'delete-title' : 'delete-title',
                'sakuhin-map-id' : button.attr('data-sakuhin-map-id'),
                'sakuhin-code' : $('.select-sakuhin-doc').val(),
                'sakuhin-name' : $('.select-sakuhin-doc').text(),
                'title-name' : button.attr('data-title-name'),
                'category-name': button.attr('data-category-name'),
            };
            AjaxUtil.get('/admin_app/sakuhin_bind/', param).then(function(xhr,status) {
                // ajax実行成功する場合、関連タイトル管理一覧を再描画
                if(status == 'success'){
                    var result = JSON.parse(xhr.responseText);
                    // 関連タイトル管理一覧を再描画
                    self.setTtileListGrid(result);
                }
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
 * タイトルモーダルデータ検索を行う
 */
SakuhinBindController.prototype.selectTitle = function () {
    var self = this;
    // エラーメッセージ削除
    $('.input-err').removeClass('input-err');
    $('.input-err-msg').remove();
    // 入力チェックエラーの場合、検索を行わない
    if (!InputCheckUtil.checkInputValue('#input-title-name','タイトル名',100)) {
        return;
    }
    //  タイトルモーダルデータ検索を行う
    self.selectTitleModal();
};

/**
 * タイトルモーダルデータ検索を行う
 */
SakuhinBindController.prototype.selectTitleModal = function () {
    var self = this;
    $('#errorMsg').hide();

    // タイトルカテゴリを取得
    var categoryList = [];
    $('input[name=checkbox]:checked').each(function(){
        categoryList.push($(this).val());
    });  

    if(categoryList.length == 0){
        InputCheckUtil.showErrMsg('#input-title-name', '検索カテゴリを選択してください。');
        return;
    }

    // パラメータを設定する
    var param = {
        'title-modal' : 'title-modal',
        'title-name' : $('#input-title-name').val(),
        'category' : JSON.stringify(categoryList)
    };
    AjaxUtil.get('/admin_app/sakuhin_bind/', param).then(function(xhr, status){
        // ajax実行成功する場合、作品モーダルグリッドを描画する
        if(status == 'success'){
            // データを取得
            var result = JSON.parse(xhr.responseText);
            if(result.length > 100){
                InputCheckUtil.showErrMsg('#input-title-name', '検索結果が100件以上のため、検索条件を絞って、もう一度検索してください。');
                return;
            }

            // データを取得後、グリッド設定処理
            self.setTitleModelGrid(result);
        }else{
            // ajax実行失敗する場合、エラーメッセージを表示する
            $('#errorMsg').show();
        }
    });
};

/**
 * タイトルモーダルグリッド設定
 */
SakuhinBindController.prototype.setTitleModelGrid = function (result) {
    var self = this;

    // グリッドOption設定
    self.createListModelOption(result);

    // タイトルを選択モーダル定義
    var modal = $('#title-dialog');
    var title = "関連タイトルを選択";
    //タイトルを選択モーダル作成
    self.createModal(modal, title);

    // 関連タイトルを追加ボタンを非活性に設定
    $('.add-title-button').button({disabled: true});
}

/**
 * モーダルのグリッドoption設定する
 */
SakuhinBindController.prototype.createListModelOption = function (result) {
    var self = this;

    // 関連タイトルリストのタイトルコードを取得する
    var titleCode = $('#list-grid-title').jqGrid("getCol", "title_code");

    // 一覧データが10以下の場合は高さ自動調整
    var height = 'auto';
    if (result.length >= 10) {
        height = 450;
    }
    // グリッドを再描画
    $('#list-title-modal').jqGrid('clearGridData');
    $('#list-title-modal').jqGrid("GridUnload");

    // グリッド項目定義
    var colModel = self.createTitleModalColModel(titleCode);
    var option = {
        colNames: colModel.name,
        colModel: colModel.model,
        data: result,
        width: 'auto',
        height : height,
        pager: '#title-modal-pager',
        loadComplete: function(){self.addTitleBtn()},
        pgbuttons : false,
        pginput : false,
        viewrecords : true,
        rowList : result.length,
        rowNum : result.length,
        rowattr: function (rowData, currentObj, rowId) {
            if(titleCode.indexOf(currentObj.title_code) > -1){
                  return {"style":"background:silver; height:44px;placeholder: 'placeholderBackground' "};
            }
        }
    };
    // グリッドを初期描画
    GridUtil.renderNormalGrid('#list-title-modal', option, true);
};

/**
 * 関連タイトルモーダル用グリッドのカラム定義
 */
SakuhinBindController.prototype.createTitleModalColModel = function (titleCode) {
    var width = 1700;
    var modelArray = [];

    modelArray.push(GridUtil.createColModel({
        name: 'checkbox',
        width: width * 0.07,
        align: 'center',
        formatter: function (val, opt, rdt) {
            if(titleCode.indexOf(rdt.title_code) > -1){
                return "<label>ー</label>";
            }else{
                return ('<input type="checkbox" class="checkbox title-checkbox" data-title-name="'
                + Escape.escapeString(rdt.title_name) +'" data-title-code="' + rdt.title_code +'" data-category-code="' 
                + rdt.title_category_code + '" data-category-name="' + rdt.title_category_name + '">');
            }
        },
        sortable: false
    }));
    modelArray.push(
        GridUtil.createColModel({
            name: 'title_name',
            width: width * 0.19
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'title_category_name',
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
            width: width * 0.09,
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
                if(titleCode.indexOf(rdt.title_code) > -1){
                    return "<label>" + '登録済み' + '</label>';
                }else{
                    return "<button type='button' class='grid-btn-update select-title-btn' data-title-name='" 
                    + Escape.escapeString(rdt.title_name) + "'data-title-code='" + rdt.title_code + "'data-category-code='" 
                    + rdt.title_category_code + "'data-category-name='" + rdt.title_category_name +"'>" + '選択' + '</button>';
                }
            },
            sortable: false
        })
    );
    return {
        model: modelArray,
        name: ['チェックボックス', 'タイトル名', '種別', '最終更新者', '最終更新日時', '選択']
    };
};

/**
 * 関連タイトル追加処理を行う
 */
SakuhinBindController.prototype.addTitleBtn = function () {
    var self = this;
    // 選択ボタンの追加処理
    self.addSelectTtileBtn();

    $('.title-checkbox').off('click');
    $('.title-checkbox').on('change', function() {
        var disabled = $('.title-checkbox:checked').length == 0;
        $('.add-title-button').button({disabled: disabled});
    });

    // 関連タイトルを紐付けボタンの追加処理
    self.addConnectionTitleBtn();
}

/**
 * 関連タイトル追加イベントを設定する（選択ボタン）
 */
SakuhinBindController.prototype.addSelectTtileBtn = function () {
    var self = this;
    $('.select-title-btn').button();
    $('.select-title-btn').off('click');
    $('.select-title-btn').on('click',function(){
        var button = $(this);
        // タイトルモーダルを閉じる
        $('#title-dialog').dialog('close');

        // タイトルコードを取得
        var title_code = button.attr('data-title-code');
        // タイトル名を取得
        var title_name = button.attr('data-title-name');
        // カテゴリコードを取得
        var category_code = button.attr('data-category-code');
        // カテゴリ名を取得
        var category_name = button.attr('data-category-name');

        // 関連タイトル追加処理を行う
        self.updateConnectionTitle([title_code],[category_code],[title_name],[category_name]);
    })
}

/**
 * 関連タイトル追加処理を行う
 */
SakuhinBindController.prototype.updateConnectionTitle = function(titleCodeList,categoryList,titleNameList,categoryNameList){
    var self = this;
    // パラメータ設定
     $('#errorMsg').hide();
    var param = {
        'add-title' : 'add-title',
        'sakuhin-code' : $('.select-sakuhin-doc').val(),
        'sakuhin-name' : $('.select-sakuhin-doc').text(),
        'title-code' : JSON.stringify(titleCodeList),
        'category-code': JSON.stringify(categoryList),
        'title-name' : JSON.stringify(titleNameList),
        'category-name' : JSON.stringify(categoryNameList),
    };
    AjaxUtil.get('/admin_app/sakuhin_bind/', param).then(function(xhr, status) {
        // ajax実行成功する場合、関連タイトル一覧グリッドを描画する
        if(status == 'success'){
            // 最新の関連タイトルデータを取得
            var result = JSON.parse(xhr.responseText);

            // 関連タイトル一覧グリッド生成
            self.setTtileListGrid(result);
        }else{
            // ajax実行成功する場合、エラーメッセージを表示する
            $('#errorMsg').show();
        }
    });
}

/**
 * 関連タイトルを紐付けイベントを設定する（関連タイトルを追加ボタン）
 */
SakuhinBindController.prototype.addConnectionTitleBtn = function () {
    var self = this;
    $('.add-title-button').button();
    $('.add-title-button').off('click');
    $('.add-title-button').on('click', function () {
        var button = $(this);
        //関連タイトルモーダル閉じる
        $('#title-dialog').dialog('close');

        // titleCode配列を宣言する
        var titleCodeList = [];
        var titleNameList = [];
        var categoryCodeList = [];
        var categoryNameList = [];
        // 関連タイトルデータ取得
        $('.title-checkbox:checked').each(function() {
            // タイトルコードを取得
            titleCodeList.push($(this).data()['titleCode']);
            // タイトル名を取得
            titleNameList.push($(this).data()['titleName']);
            // カテゴリコードを取得
            categoryCodeList.push($(this).data()['categoryCode']);
            // カテゴリ名を取得
            categoryNameList.push($(this).data()['categoryName']);
        });

        if(titleCodeList.length == 0||titleNameList.length == 0||categoryCodeList.length == 0||categoryNameList.length == 0){
            return;
        }
        self.updateConnectionTitle(titleCodeList,categoryCodeList,titleNameList,categoryNameList);
    });
};

//////////////////////////// Twitter /////////////////////////
/**
 * 作品データ検索を行う
 */
SakuhinBindController.prototype.selectTwitterSakuhin = function () {
    var self = this;
    // エラーメッセージ削除
    $('.input-err').removeClass('input-err');
    $('.input-err-msg').remove();
    // 入力チェックエラーの場合、検索を行わない
    if (!InputCheckUtil.checkInputValue('#twitter-sakuhin-name','作品名',100)) {
        return;
    }
    //  作品モーダルデータ検索を行う
    self.selectTwitterSakuhinModal();
};

/**
 * 作品モーダルデータ検索を行う
 */
SakuhinBindController.prototype.selectTwitterSakuhinModal = function () {
    var self = this;
    $('#errorMsg').hide();

    // パラメータ設定
    var param = {
        'sakuhin-modal' : 'sakuhin-modal',
        'sakuhin-name' : $('#twitter-sakuhin-name').val()
    };
    AjaxUtil.get('/admin_app/sakuhin_bind/', param).then(function(xhr, status){
        // ajax実行成功する場合、作品モーダルグリッドを描画する
        if(status == 'success'){
            // データを取得
            var result = JSON.parse(xhr.responseText);
            if(result.length > 100){
                InputCheckUtil.showErrMsg('#twitter-sakuhin-name', '検索結果が100件以上のため、検索条件を絞って、もう一度検索してください。');
                return;
            }
            // データを取得後、グリッド設定処理
            self.setTwitterSakuhinModelGrid(result);
        }else{
            // ajax実行失敗する場合、エラーメッセージを表示する
            $('#errorMsg').show();
        }
    });
};

/**
 * 作品モーダルグリッド設定
 */
SakuhinBindController.prototype.setTwitterSakuhinModelGrid = function (result) {
    var self = this;

    // グリッド生成
    var colModel = self.createSakuhinColModel('dialog');
    // グリッドイベント設定
    var event = self.selectTwitterSakuhinBtn;
    // グリッドoption設定
    self.createModelOption(result,'#twitter-sakuhin-modal','#twitter-sakuhin-pager',colModel,event);

    // 作品を選択モーダル定義
    var modal = $('#twitter-sakuhin-dialog');
    var title = "作品を選択";
    //作品を選択モーダル作成
    self.createModal(modal, title);
}

/**
 * 作品を選択モーダルイベントを設定する
 */
SakuhinBindController.prototype.selectTwitterSakuhinBtn = function (self) {
    var self = self;
    $('.select-sakuhin-btn').button();
    $('.select-sakuhin-btn').off('click')
    $('.select-sakuhin-btn').on('click', function () {

        var button = $(this);
        //選択作品名を表示
        $('.select-twitter-doc').text(button.attr('data-sakuhin-name'));
        $('.select-twitter-doc').val(button.attr('data-sakuhin-code'));

        //作品名モーダル閉じる
        $('#twitter-sakuhin-dialog').dialog('close');

        // 関連タイトルの検索を行う
        var sakuhin_code = button.attr('data-sakuhin-code');
        self.selectTwitterList(sakuhin_code);
    });
};

/**
 * Twitterに関連作品検索を行う
 */
SakuhinBindController.prototype.selectTwitterList = function (sakuhin_code) {
    var self = this;
    // データ検索を行う
    $('#errorMsg').hide();
    var param = {
        'twitter-list' : 'twitter-list',
        'sakuhin-code' : sakuhin_code
    };
    AjaxUtil.get('/admin_app/sakuhin_bind/', param).then(function(xhr, status) {
        if(status == 'success'){
            // データを取得
            var result = JSON.parse(xhr.responseText);

            // データを取得後、一覧グリッドを描画
            self.setTwitterSakuhinListGrid(result);
        }else{
            $('#errorMsg').show();
        }
    });
};

/**
 * Twitter一覧グリッド設定
 */
SakuhinBindController.prototype.setTwitterSakuhinListGrid = function (result) {
    var self = this;

    // グリッド生成
    var colModel = self.createTwitterListColModel();
    // グリッドイベント設定
    var event = self.delTwitterBtn;
    // Twitter一覧グリッドOption設定
    self.createListOption(result,'#grid-twitter-sakuhin','#list-twitter-sakuhin-pager',colModel,event,'#gbox_grid-twitter-sakuhin');
    
    //Twitter一覧管理領域表示
    $('.twitter-sakuhin-list').slideDown();
}

/**
 * Twitter一覧モーダルグリッド用のカラム定義
 */
SakuhinBindController.prototype.createTwitterListColModel = function () {
    var width = 2200;
    var modelArray = [];

    modelArray.push(
        GridUtil.createColModel({
            name: 'twitter_code',
            width: width * 0.12
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'account_name',
            width: width * 0.15
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'main_account_flg',
            width: width * 0.1,
            align: 'center',
            formatter : function(val, opt, rdt) {
                return GridUtil.formatMaruBatsu(val)
            },
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'update_user',
            width: width * 0.1,
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
                return ('</button>' + "<button type='button' class='grid-btn-delete del-twitter-btn' data-account-name='"
                + Escape.escapeString(rdt.account_name) + "' data-twitter-code='" + rdt.twitter_code + "' data-main-flg='" 
                + rdt.main_account_flg +"'data-sakuhin-map-id='" + rdt.sakuhin_map_id +"'>" + '紐付けを解除' + '</button>');
            },
            sortable: false
        })
    );
    return {
        model: modelArray,
        name: ['Twitterコード','アカウント名', 'メインフラグ', '最終更新者', '最終更新日時', 'データ操作']
    };
};

/**
 * Twitter紐付け解除処理を行う
 */
SakuhinBindController.prototype.delTwitterBtn = function (self) {
    var self = self;
    $('.del-twitter-btn').button();
    $('.del-twitter-btn').off('click');
    //紐付け解除ボタンをクリックし、紐付け解除処理を行う
    $('.del-twitter-btn').on('click', function () {
        $('#status-msg').remove();
        var button = $(this);
        // 作品コードとタイトル名をダイアログに設定
        $('#delete-twitter-code').text(button.attr('data-twitter-code'));
        $('#delete-twitter-name').text(button.attr('data-account-name'));

        // 作品紐付け解除ダイアログ
        var modal = $('#del-twitter-dialog');

        // キャンセル処理
        $('.cancel-botton').on('click', function () {
            modal.dialog('close');
            $('.delete-button').off('click');
        });

        //作品紐付け解除処理
        $('.delete-button').on('click', function () {
            var param = {
                'del-twitter-sakuhin' : 'del-twitter-sakuhin',
                'sakuhin-map-id' : button.attr('data-sakuhin-map-id'),
                'sakuhin-name' :　$('.select-twitter-doc').text(),
                'sakuhin-code' : $('.select-twitter-doc').val(),
                'account-name' : button.attr('data-account-name'),
            };
            AjaxUtil.get('/admin_app/sakuhin_bind/', param).then(function(xhr,status) {
                // ajax実行成功する場合、作品管理一覧を再描画
                if(status == 'success'){
                    var result = JSON.parse(xhr.responseText);

                    // 作品管理一覧を再描画
                    self.setTwitterSakuhinListGrid(result);
                }
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
 * Twitterデータ検索を行う
 */
SakuhinBindController.prototype.selectTwitter = function () {
    var self = this;
    // エラーメッセージ削除
    $('.input-err').removeClass('input-err');
    $('.input-err-msg').remove();
    // 入力チェックエラーの場合、検索を行わない
    if (!InputCheckUtil.checkInputValue('#input-twitter-name','アカウント名',50)) {
        return;
    }
    //  Twitterモーダルデータ検索を行う
    self.selectTwitterModal();
};

/**
 * Twitterモーダルデータ検索を行う
 */
SakuhinBindController.prototype.selectTwitterModal = function () {
    var self = this;
    $('#errorMsg').hide();

    // パラメータ設定
    var param = {
        'twitter-modal' : 'twitter-modal',
        'twitter-name' : $('#input-twitter-name').val()
    };
    AjaxUtil.get('/admin_app/sakuhin_bind/', param).then(function(xhr, status){
        // ajax実行成功する場合、グリッドを描画する
        if(status == 'success'){
            // データを取得
            var result = JSON.parse(xhr.responseText);
            if(result.length > 100){
                InputCheckUtil.showErrMsg('#input-twitter-name', '検索結果が100件以上のため、検索条件を絞って、もう一度検索してください。');
                return;
            }
            // 関連作品の表を描画
            self.createTwitterSakuhinModal(result);

            // 関連作品のモーダル定義
            var modal = $('#add-twitter-dialog');
            var title = "関連Twitterを選択";
            // 関連作品のモーダル作成
            self.createModal(modal, title);
        }else{
            // ajax実行失敗する場合、エラーメッセージを表示する
            $('#errorMsg').show();
        }
    });
};

/**
 * 関連作品グリッドを作成(Twitter)
 */
SakuhinBindController.prototype.createTwitterSakuhinModal = function (result) {
    var self = this;
    // 関連作品リストの作品コードを取得する
    var twitterCode = $('#grid-twitter-sakuhin').jqGrid("getCol", "twitter_code");
    // 一覧データが10以下の場合は高さ自動調整
    var height = 'auto';
    if (result.length >= 10) {
        height = 450;
    }
    // グリッドを再描画
    $('#twitter-list').jqGrid('clearGridData');
    $('#twitter-list').jqGrid("GridUnload");
    // グリッド生成
    var colModel = self.createTwitterSakuhinModalgrid(twitterCode);
    var option = {
        datatype: "local",
        colNames: colModel.name,
        colModel: colModel.model,
        data: result,
        width: 'auto',
        height : height,
        pager: '#twitter-sakuhin-pager',
        loadComplete: function(){self.addTwitterSakuhinBtn()},
        pgbuttons : false,
        pginput : false,
        viewrecords : true,
        rowList : result.length,
        rowNum : result.length,
        rowattr: function (rowData, currentObj, rowId) {
            if(twitterCode.indexOf(currentObj.twitter_code) > -1){
                    return {"style":"background:silver; height:44px;placeholder: 'placeholderBackground' "};
            }
            if(currentObj.main_account_flg){
                return {"style":"background:#fac93d; height:44px;placeholder: 'placeholderBackground' "};
            }
        }
    };
    // グリッドを初期描画
    GridUtil.renderNormalGrid('#twitter-list', option, true);
};

/**
 * 関連作品追加モーダル用グリッドのカラム定義
 */
SakuhinBindController.prototype.createTwitterSakuhinModalgrid = function (twitterCode) {
    var width = 1700;
    var modelArray = [];

    modelArray.push(
        GridUtil.createColModel({
            name: 'twitter_code',
            width: width * 0.12
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'account_name',
            width: width * 0.15
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'main_account_flg',
            width: width * 0.1,
            align: 'center',
            formatter : function(val, opt, rdt) {
                return GridUtil.formatMaruBatsu(val)
            },
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
                if(twitterCode.indexOf(rdt.twitter_code) > -1){
                    return "<label>" + '登録済み' + '</label>';
                }else{
                    return "<button type='button' class='grid-btn-update select-twitter-button' data-account-name='" 
                    + Escape.escapeString(rdt.account_name) + "'data-twitter-code='" + rdt.twitter_code 
                    + "'data-main-flg='" + rdt.main_account_flg +"'>" + '選択' + '</button>';
                }
            },
            sortable: false
        })
    );
    return {
        model: modelArray,
        name: ['Twitterコード','アカウント名', 'メインフラグ', '最終更新者', '最終更新日時', 'データ操作']
    };
};

/**
 * 関連作品追加イベントを設定する（選択ボタン）(Twitter)
 */
SakuhinBindController.prototype.addTwitterSakuhinBtn = function () {
    var self = this;
    $('.select-twitter-button').button();
    $('.select-twitter-button').off('click');
    $('.select-twitter-button').on('click',function(){
        var button = $(this);
        // 作品モーダルを閉じる
        $('#add-twitter-dialog').dialog('close');

        // 作品コードを取得
        var twitter_code = button.attr('data-twitter-code');
        var account_name = button.attr('data-account-name');
        var main_flg =  button.attr('data-main-flg');

        self.updateTwitterSakuhin(twitter_code, account_name,main_flg);
    })
}

/**
 * 関連作品追加処理を行う(Twitter)
 */
SakuhinBindController.prototype.updateTwitterSakuhin = function(twitter_code, account_name,main_flg){
    var self = this;
    // パラメータ設定
     $('#errorMsg').hide();
    var param = {
        'add-twitter-sakuhin' : 'add-twitter-sakuhin',
        'sakuhin-code' : $('.select-twitter-doc').val(),
        'sakuhin-name' : $('.select-twitter-doc').text(),
        'twitter-code' : twitter_code,
        'account-name' : account_name,
        'main-flg' : main_flg,

    };
    AjaxUtil.get('/admin_app/sakuhin_bind/', param).then(function(xhr, status) {
        // ajax実行成功する場合、関連作品一覧グリッドを描画する
        if(status == 'success'){
            // 最新の関連作品データを取得
            var result = JSON.parse(xhr.responseText);

            // 強制解除行った場合、画面に提示メッセージを表示
            if(result.delflg){
                // 削除メッセージ表示
                MsgUtil.showStatusMsg('#con-sakuhin-list', result.del_user,'強制解除');
            }

            // 関連作品一覧グリッド生成
            self.setTwitterSakuhinListGrid(result.twitter_list);
        }else{
            // ajax実行成功する場合、エラーメッセージを表示する
            $('#errorMsg').show();
        }
    });
}

/////////////////////////// Game /////////////////////////////////////////
/**
 * Gameデータ検索を行う
 */
SakuhinBindController.prototype.selectGame = function () {
    var self = this;
    // エラーメッセージ削除
    $('.input-err').removeClass('input-err');
    $('.input-err-msg').remove();
    // 入力チェックエラーの場合、検索を行わない
    if (!InputCheckUtil.checkInputValue('#input-game-name','ゲーム名',255)) {
        return;
    }
    //  ゲームモーダルデータ検索を行う
    self.selectGameModal();
};

/**
 * Gameモーダルデータ検索を行う
 */
SakuhinBindController.prototype.selectGameModal = function () {
    var self = this;
    $('#errorMsg').hide();

    // パラメータ設定
    var param = {
        'game-modal' : 'game-modal',
        'game-name' : $('#input-game-name').val()
    };
    AjaxUtil.get('/admin_app/sakuhin_bind/', param).then(function(xhr, status){
        // ajax実行成功する場合、グリッドを描画する
        if(status == 'success'){
            // データを取得
            var result = JSON.parse(xhr.responseText);
            if(result.length > 100){
                InputCheckUtil.showErrMsg('#input-game-name', '検索結果が100件以上のため、検索条件を絞って、もう一度検索してください。');
                return;
            }
            // データを取得後、グリッド設定処理
            self.setGameModalGrid(result);
        }else{
            // ajax実行失敗する場合、エラーメッセージを表示する
            $('#errorMsg').show();
        }
    });
};

/**
 * Gameモーダルグリッド設定
 */
SakuhinBindController.prototype.setGameModalGrid = function (result) {
    var self = this;

    // グリッド生成
    var colModel = self.createGameModalColModel();
    // グリッドイベント設定
    var event = self.selectGameBtn;
    // モーダルOption設定
    self.createModelOption(result,'#list-game-modal','#game-pager',colModel,event);

    // 作品を選択モーダル定義
    var modal = $('#select-game-dialog');
    var title = "ゲームを選択";
    //作品を選択モーダル作成
    self.createModal(modal, title);
}

/**
 * Game一覧モーダルグリッド用のカラム定義
 */
SakuhinBindController.prototype.createGameModalColModel = function () {
    var width = 1700;

    var modelArray = [];
    modelArray.push(
        GridUtil.createColModel({
            name: 'game_title_code',
            width: width * 0.1,
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'game_title_name',
            width: width * 0.2
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'platform_name',
            width: width * 0.09
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'update_user',
            width: width * 0.09,
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'update_time',
            width: width * 0.09,
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
                return ('</button>' + "<button type='button' class='grid-btn-update select-game-btn' data-game-name='"
                + Escape.escapeString(rdt.game_title_name) + "' data-game-code='" + rdt.game_title_code 
                + "' data-platform-name='" + rdt.platform_name +"'>" + '選択' + '</button>');
            },
            sortable: false
        })
    );
    return {
        model: modelArray,
        name: ['ゲームタイトルコード','ゲームタイトル名','プラットフォーム名','最終更新者', '最終更新日時', 'データ操作']
    };
};

/**
 * Gameを選択モーダルイベントを設定する
 */
SakuhinBindController.prototype.selectGameBtn = function (self) {
    var self = self;
    $('.select-game-btn').button();
    $('.select-game-btn').off('click')
    $('.select-game-btn').on('click', function () {

        var button = $(this);
        //選択Game名を表示
        $('.select-game-doc').text(button.attr('data-game-name'));
        $('.select-game-doc').val(button.attr('data-game-code'));

        //作品名モーダル閉じる
        $('#select-game-dialog').dialog('close');

        // Gameに関連作品の検索を行う
        var game_code = button.attr('data-game-code');
        self.selectGameSakuhinList(game_code);
    });
};

/**
 * Gameに関連作品検索を行う
 */
SakuhinBindController.prototype.selectGameSakuhinList = function (game_code) {
    var self = this;
    // データ検索を行う
    $('#errorMsg').hide();
    var param = {
        'game-list' : 'game-list',
        'game-code' : game_code
    };
    AjaxUtil.get('/admin_app/sakuhin_bind/', param).then(function(xhr, status) {
        if(status == 'success'){
            // データを取得
            var result = JSON.parse(xhr.responseText);

            // データを取得後、一覧グリッドを描画
            self.setGameSakuhinListGrid(result);
        }else{
            $('#errorMsg').show();
        }
    });
};

/**
 * Game一覧グリッド設定
 */
SakuhinBindController.prototype.setGameSakuhinListGrid = function (result) {
    var self = this;

    // グリッド生成
    var colModel = self.createSakuhinColModel('list');
    // グリッドイベント設定
    var event = self.delGameBtn;
    // Game一覧グリッドOption設定
    self.createListOption(result,'#grid-game-sakuhin','#list-game-pager',colModel,event,'#gbox_grid-game-sakuhin');
    
    //Game一覧管理領域表示
    $('.game-sakuhin-list').slideDown();
}

/**
 * Game紐付け解除処理を行う
 */
SakuhinBindController.prototype.delGameBtn = function (self) {
    var self = self;
    $('.del-sakuhin-btn').button();
    $('.del-sakuhin-btn').off('click');
    //紐付け解除ボタンをクリックし、紐付け解除処理を行う
    $('.del-sakuhin-btn').on('click', function () {
        var button = $(this);
        // 作品コードと作品名をダイアログに設定
        $('#delete-game-code').text(button.attr('data-sakuhin-code'));
        $('#delete-game-name').text(button.attr('data-sakuhin-name'));

        // 作品紐付け解除ダイアログ
        var modal = $('#del-game-dialog');

        // キャンセル処理
        $('.cancel-botton').on('click', function () {
            modal.dialog('close');
            $('.delete-button').off('click');
        });

        //作品紐付け解除処理
        $('.delete-button').on('click', function () {
            var param = {
                'del-game-sakuhin' : 'del-game-sakuhin',
                'sakuhin-map-id' : button.attr('data-sakuhin-map-id'),
                'game-code' : $('.select-game-doc').val(),
                'game-name' : $('.select-game-doc').text(),
                'sakuhin-name' : button.attr('data-sakuhin-name'),
            };
            AjaxUtil.get('/admin_app/sakuhin_bind/', param).then(function(xhr,status) {
                // ajax実行成功する場合、作品管理一覧を再描画
                if(status == 'success'){
                    var result = JSON.parse(xhr.responseText);

                    // 作品管理一覧を再描画
                    self.setGameSakuhinListGrid(result);
                }
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
 * 関連作品追加モーダル(Game)
 */
SakuhinBindController.prototype.selectGameConSakuhin = function () {
    var self = this;
    // エラーメッセージ削除
    $('.input-err').removeClass('input-err');
    $('.input-err-msg').remove();

    // 入力チェックエラーの場合、検索を行わない
    if (!InputCheckUtil.checkInputValue('#game-sakuhin-name','作品名',100)) {
        return;
    }
    //  関連作品モーダルデータ検索を行う
    self.selecSakuhinForGame();
};

/**
 * 関連作品モーダルデータ検索を行う(Twitter)
 */
SakuhinBindController.prototype.selecSakuhinForGame = function () {
    var self = this;
    var param = {
        'sakuhin-modal' : 'sakuhin-modal',
        'sakuhin-name' :  $('#game-sakuhin-name').val()
    };
    AjaxUtil.get('/admin_app/sakuhin_bind/', param, function(data) {

        var result = JSON.parse(data.toString());

        // 関連作品モーダルの表を描画
        self.createGameSakuhinModal(result);

        // 関連作品のモーダル定義
        var modal = $('#add-game-dialog');
        var title = "関連作品を選択";
        // 関連作品のモーダル作成
        self.createModal(modal, title);

        // 関連作品を追加ボタンを非活性に設定
        $('.add-game-button').button({disabled: true});
    });
}

/**
 * 関連作品グリッドを作成(Game)
 */
SakuhinBindController.prototype.createGameSakuhinModal = function (result) {
    var self = this;
    // 関連作品リストの作品コードを取得する
    var sakuhinCode = $('#grid-game-sakuhin').jqGrid("getCol", "sakuhin_code");
    // 一覧データが10以下の場合は高さ自動調整
    var height = 'auto';
    if (result.length >= 10) {
        height = 450;
    }
    // グリッドを再描画
    $('#game-sakuhin-modal').jqGrid('clearGridData');
    $('#game-sakuhin-modal').jqGrid("GridUnload");
    // グリッド生成
    var colModel = self.createGameSakuhinModalgrid(sakuhinCode);
    var option = {
        datatype: "local",
        colNames: colModel.name,
        colModel: colModel.model,
        data: result,
        width: 'auto',
        height : height,
        pager: '#game-sakuhin-pager',
        loadComplete: function(){self.addGameSakuhinBtn()},
        pgbuttons : false,
        pginput : false,
        viewrecords : true,
        rowList : result.length,
        rowNum : result.length,
        rowattr: function (rowData, currentObj, rowId) {
            if(sakuhinCode.indexOf(currentObj.sakuhin_code) > -1){
                  return {"style":"background:silver; height:44px;placeholder: 'placeholderBackground' "};
            }
        }
    };
    // グリッドを初期描画
    GridUtil.renderNormalGrid('#game-sakuhin-modal', option, true);
};

/**
 * 関連作品追加モーダル用グリッドのカラム定義
 */
SakuhinBindController.prototype.createGameSakuhinModalgrid = function (sakuhinCode) {
    var width = 1700;
    var modelArray = [];

    modelArray.push(GridUtil.createColModel({
        name: 'checkbox',
        width: width * 0.07,
        align: 'center',
        formatter: function (val, opt, rdt) {
            if(sakuhinCode.indexOf(rdt.sakuhin_code) > -1){
                return "<label>ー</label>";
            }else{
                return ('<input type="checkbox" class="checkbox game-checkbox" data-sakuhin-name="'
                + Escape.escapeString(rdt.sakuhin_name) +'" data-sakuhin-code="' + rdt.sakuhin_code +'">');
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
                if(sakuhinCode.indexOf(rdt.sakuhin_code) > -1){
                    return "<label>" + '登録済み' + '</label>';
                }else{
                    return "<button type='button' class='grid-btn-update select-game-button' data-sakuhin-name='" 
                    + Escape.escapeString(rdt.sakuhin_name) + "'data-sakuhin-code='" + rdt.sakuhin_code+ "'>" + '選択' + '</button>';
                }
            },
            sortable: false
        })
    );
    return {
        model: modelArray,
        name: ['チェックボックス','作品コード', '作品名', '作品かな名', '最終更新者', '最終更新日時', 'データ操作']
    };
};

/**
 * 関連作品追加イベントを設定する(Game)
 */
SakuhinBindController.prototype.addGameSakuhinBtn = function () {
    var self = this;
    // 選択ボタンの追加処理
    self.addSelectSakuhinBtn();

    // チェックボックス選択した場合、「関連作品を選択」ボタン活性に設定
    $('.game-checkbox').off('click');
    $('.game-checkbox').on('change', function() {
        var disabled = $('.game-checkbox:checked').length == 0;
        $('.add-game-button').button({disabled: disabled});
    });

    // 関連ゲームを紐付けボタンの追加処理
    self.addConnectionSakuhinBtn();
}

/**
 * 関連作品追加イベントを設定する（選択ボタン）(Game)
 */
SakuhinBindController.prototype.addSelectSakuhinBtn = function () {
    var self = this;
    $('.select-game-button').button();
    $('.select-game-button').off('click');
    $('.select-game-button').on('click',function(){
        var button = $(this);
        // 作品モーダルを閉じる
        $('#add-game-dialog').dialog('close');

        // 作品コードを取得
        var sakuhin_code = button.attr('data-sakuhin-code');
        var sakuhin_name = button.attr('data-sakuhin-name');

        self.updateGameSakuhin([sakuhin_code]);
    })
}

/**
 * 関連作品追加処理を行う(Game)
 */
SakuhinBindController.prototype.updateGameSakuhin = function(sakuhinCodeList){
    var self = this;
    // パラメータ設定
     $('#errorMsg').hide();
    var param = {
        'add-game-sakuhin' : 'add-game-sakuhin',
        'game-code' : $('.select-game-doc').val(),
        'game-name' : $('.select-game-doc').text(),
        'sakuhin-code' : JSON.stringify(sakuhinCodeList)
    };
    AjaxUtil.get('/admin_app/sakuhin_bind/', param).then(function(xhr, status) {
        // ajax実行成功する場合、関連作品一覧グリッドを描画する
        if(status == 'success'){
            // 最新の関連作品データを取得
            var result = JSON.parse(xhr.responseText);

            // 関連作品一覧グリッド生成
            self.setGameSakuhinListGrid(result);
        }else{
            // ajax実行成功する場合、エラーメッセージを表示する
            $('#errorMsg').show();
        }
    });
}

/**
 * 関連ゲームを紐付けイベントを設定する（関連ゲームを追加ボタン）
 */
SakuhinBindController.prototype.addConnectionSakuhinBtn = function () {
    var self = this;
    $('.add-game-button').button();
    $('.add-game-button').off('click');
    $('.add-game-button').on('click', function () {
        var button = $(this);
        //関連タイトルモーダル閉じる
        $('#add-game-dialog').dialog('close');

        // sakuhinCode配列を宣言する
        var sakuhinCodeList = [];

        // 関連作品コード取得
        $('.game-checkbox:checked').each(function(){
            // 作品コードを取得
            var sakuhin_code = $(this).data()['sakuhinCode'];
            sakuhinCodeList.push(sakuhin_code);
        });

        if(sakuhinCodeList.length == 0){
            return;
        }
        self.updateGameSakuhin(sakuhinCodeList);
    });
};

/**
 * モーダルのグリッドoption設定する
 * 
 * @param  result 
 *              グリッド用データ
 * @param  tableId 
 *              グリッド描画用ID
 * @param  pager 
 *              グリッド用ページ
 * @param  colModel 
 *              グリッドcolModel
 * @param  event 
 *              グリッドのイベント
 */
SakuhinBindController.prototype.createModelOption = function (result,tableId,pager,colModel,event) {
    var self = this;
    // 一覧データが10以下の場合は高さ自動調整
    var height = 'auto';
    if (result.length >= 10) {
        height = 450;
    }
    // グリッドを再描画
    $(tableId).jqGrid('clearGridData');
    $(tableId).jqGrid("GridUnload");
    var option = {
        colNames: colModel.name,
        colModel: colModel.model,
        data: result,
        width: 'auto',
        height : height,
        pager: pager,
        loadComplete: function(){event(self)},
        pgbuttons : false,
        pginput : false,
        viewrecords : true,
        rowList : result.length,
        rowNum : result.length
    };
    // グリッドを初期描画
    GridUtil.renderNormalGrid(tableId, option, true);
};

/**
 * 一覧のグリッドoption設定する
 * 
 * @param  result 
 *              グリッド用データ
 * @param  tableId 
 *              グリッド描画用ID
 * @param  pager 
 *              グリッド用ページ
 * @param  colModel 
 *              グリッドcolModel
 * @param  event 
 *              グリッドのイベント
 * @param  reloadId 
 *              グリッド再描画用ID
 */
SakuhinBindController.prototype.createListOption = function (result,tableId,pager,colModel,event,reloadId) {
    var self = this;
    // 一覧データが10以下の場合は高さ自動調整
    var height = 'auto';
    if (result.length >= 10) {
        height = 450;
    }
    // グリッドを再描画
    if ($(reloadId).is(':visible')) {
        $(tableId).jqGrid('clearGridData').trigger('reloadGrid');
        $(tableId).jqGrid('setGridHeight', height).trigger('reloadGrid');
        $(tableId).jqGrid('setGridParam', {
            data : result,
            rowNum : result.length,
        }).trigger('reloadGrid');
    }else{
        var option = {
            colNames: colModel.name,
            colModel: colModel.model,
            data: result,
            width: 'auto',
            height : height,
            pager: pager,
            loadComplete: function(){event(self)},
            pgbuttons : false,
            pginput : false,
            viewrecords : true,
            rowList : result.length,
            rowNum : result.length
        };
        // グリッドを初期描画
        GridUtil.renderNormalGrid(tableId, option, true);
    }
}

/**
 * モーダル定義
 */
SakuhinBindController.prototype.createModal = function (modal, title) {
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
    var controller = new SakuhinBindController();
    controller.init();
});
