var SakuhinTagBindController = function() {};
SakuhinTagBindController.prototype = new AbstractController();

/**
 * タグ情報一覧画面の主処理
 */
SakuhinTagBindController.prototype.execute = function() {
    var self = this;

    return $.Deferred().resolve().promise();
};

/**
 * メニュー選択処理
 */
SakuhinTagBindController.prototype.selectedMenu = function() {
    return '.tag-bind';
};
/**
 * イベント登録処理
 */
SakuhinTagBindController.prototype.bindEvent = function() {
    var self = this;
    

    // 更新履歴DLエリアのイベント設定
    NoticeTableUtil.setDLArea();

    // 更新履歴CSVダウンロード
    NoticeTableUtil.downloadTableCsv('m_sakuhin_tag_map', 'タグ紐付け情報');

    // タイトル検索モーダルイベント
    $('.title-search-button').on('click', function() {
        self.searchTitle();
    });
    // TODO:タグソート、ドラッグイベント
    // self.setTagEvent();

    // タグ削除イベント
    // self.clickTagDeleteButton();



    // タグをクリアボタンイベント
    // $('.clear-button').on('click', function() {
    //     $('.jquery-ui-sortable').empty();
    // });

    // タグ候補表示
    $('.tag-select-button').on('click', function() {
        self.selectTagArea();
    });

    return $.Deferred().resolve().promise();
};

/**
 * タイトル検索
 */
SakuhinTagBindController.prototype.searchTitle = function() {
    var self = this;

    // 入力チェックエラーの場合、検索を行わない
    if (!InputCheckUtil.checkInputValue('#input-title-name','タイトル名',100)) {
        return;
    }

    // タイトル選択モーダル
    self.openTitleModal();

};

/**
 * タイトル選択モーダル
 */
SakuhinTagBindController.prototype.openTitleModal = function() {
    var self = this;
    modal = $('#title-search-dialog');

    // タイトルカテゴリを取得
    var categoryList = [];
    $('input[name=checkbox]:checked').each(function(){
        categoryList.push($(this).val());
    });  

    // パラメータを設定する
    var param = {
        'title-modal' : 'title-modal',
        'title-name' : $('#input-title-name').val(),
        'category' : JSON.stringify(categoryList)
    };
    // 検索処理（非同期）
    AjaxUtil.get('/admin_app/sakuhin_tag_bind/', param).then(function(xhr, status){
        // ajax実行成功する場合、作品モーダルグリッドを描画する
        if(status == 'success'){
            // データを取得
            var result = JSON.parse(xhr.responseText);
            if(result.length > 100){
                InputCheckUtil.showErrMsg('#input-title-name', '検索結果が100件以上のため、検索条件を絞って、もう一度検索してください。');
                return;
            }

            // データを取得後、グリッド設定処理
            self.setTitleSeatchModelGrid(result);
        }else{
            // ajax実行失敗する場合、エラーメッセージを表示する
            $('#errorMsg').show();
        }
        
    });

};

SakuhinTagBindController.prototype.setTitleSeatchModelGrid = function(searchResult) {

        // グリッド生成
        var colModel = self.createColModel();
        var option = {
            colNames: colModel.name,
            colModel: colModel.model,
            data: searchResult,
            pager: '#pager',
            loadComplete: self.gridBtnEvent,
        };
        GridUtil.renderNormalGrid('#list-grid', option, true);
    
        // モーダル生成
        modal.dialog({
            title: 'タイトルを選択',
            resizable: false,
            modal: true,
            width: 'auto',
            height: 'auto',
        });
};
/**
 * タグ候補表示エリア
 */
SakuhinTagBindController.prototype.selectTagArea = function() {
    var self = this;


    // TODO:コアコード取得


    // タグリスト
    var tagList = [
        'LGBT',
        'アイドル',
        '相棒・バディ',
        '赤ちゃん',
        '医師',
        '異星人',
        'ヴァンパイア・吸血鬼',
        '宇宙飛行士',
        '幼馴染',
        '親子',
        '外国人・ハーフ主人公',
        '海賊',
        '学生',
        '家庭教師',
        '神・仏',
        '監督',
        '兄弟・姉妹',
    ];
    // タグ選択要素生成
    $('.tag-list-area')
        .children()
        .remove();
    var tagSelectList = $('<ul class="tag-select-list"></ul>');
    if (tagList) {
        for (i = 0; i < tagList.length; i++) {
            var val = tagList[i];
            var tagElem = $('<li class="jquery-ui-draggable">' + val + '<span class="tag-delete-button display-none">×</span></li>');
            tagSelectList.append(tagElem);
        }
    }
    // タグリスト
    $('.tag-list-area').append(tagSelectList);

    // タグ削除イベント
    self.clickTagDeleteButton();

    // ドラッグ付与
    self.setDragEvent('.jquery-ui-draggable');
};

/**
 * jQGrid用のカラム定義
 */
SakuhinTagBindController.prototype.createColModel = function() {
    var width = $('#list').width();

    var modelArray = [];
    modelArray.push(
        GridUtil.createColModel({
            name: 'titleName',
            width: width * 0.15,
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'category',
            width: width * 0.06,
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'platform_name',
            width: width * 0.06,
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'release_yyyymmdd',
            width: width * 0.06,
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'updateUser',
            width: width * 0.08,
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'updateDate',
            width: width * 0.08,
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
                    '</button>' +
                    "<button type='button' class='grid-btn-update grid-btn-connectionIpDel' data-ipName='" +
                    rdt.titleName +
                    "'data-ipCode='" +
                    rdt.category +
                    "'data-row-id='" +
                    opt.rowId +
                    "'>" +
                    '編集' +
                    '</button>'
                );
            },
            sortable: false,
        })
    );
    return {
        model: modelArray,
        name: ['タイトル名', '種別', 'プラットフォーム名','発売日','更新者', '更新日時', '編集'],
    };
};

/**
 * jQGrid用のボタンイベント定義
 */
SakuhinTagBindController.prototype.gridBtnEvent = function(data) {
    var local = data;
    $('.grid-btn-update').button();
    $('.grid-btn-update').on('click', function() {
        // タイトル
        $('.select-title').text('ドラゴンボール ファイターズデラックスエディション');
        $('.tag-select-area').slideDown('slow');
        var modal = $('#title-search-dialog');
        modal.dialog('close');
    });
    $('.title-select-cancel-button').on('click', function() {
        modal.dialog('close');
    });
};

/**
 * タグ要素削除イベント
 */
SakuhinTagBindController.prototype.clickTagDeleteButton = function() {
    //
    $('.tag-delete-button').on('click', function() {
        // 親要素のliを削除
        $(this)
            .parent()
            .remove();
    });
};

SakuhinTagBindController.prototype.setDragEvent = function(elem) {
    var self = this;
    $(elem).draggable({
        connectToSortable: '.jquery-ui-sortable',
        revert: 'invalid',
        zIndex: '100',
    });
};
/**
 * ソート機能、ドラッグ付与
 */
SakuhinTagBindController.prototype.setTagEvent = function() {
    var self = this;
    $('.jquery-ui-sortable').sortable({
        revert: 'invalid',
        // ドラッグ要素が上に乗った時のイベント
        receive: function(event, ui) {
            $(ui.item)
                .children('span')
                .removeClass('display-none');
        },
    });

    self.setDragEvent('.jquery-ui-draggable');
};

$(function() {
    var controller = new SakuhinTagBindController();
    controller.init();
});
