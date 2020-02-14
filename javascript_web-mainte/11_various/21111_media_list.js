var MediaListController = function() {};
MediaListController.prototype = new AbstractController();

/**
 * メニュー選択処理
 */
MediaListController.prototype.selectedMenu = function() {
    return '.media-list';
};

/**
 * イベント登録処理
 */
MediaListController.prototype.bindEvent = function() {
    var self = this;

    // 新規登録ボタン
    $('.create-button').on('click', function() {
        window.location.href = '/admin_app/media_create/';
    });

    // 更新履歴DLエリアのイベント設定
    NoticeTableUtil.setDLArea();

    // 更新履歴CSVダウンロード
    NoticeTableUtil.downloadTableCsv('m_media', '掲載媒体情報');

    // 掲載媒体マスタCSVダウンロード
    self.downloadCsv();

    // 掲載媒体マスタ一覧生成
    self.selectMediaList();

    return $.Deferred().resolve().promise();
};

/**
 * 掲載媒体マスタ検索 (ajaxで掲載媒体一覧検索結果を取得)
 */
MediaListController.prototype.selectMediaList = function() {
    var self = this;
    var param = {
          'media' : 'meida-list'
      };
      
    AjaxUtil.get('/admin_app/media_list/', param, function(data) {
        self.searchResultCallback(data);
    });
}

/**
 * ajaxで掲載媒体一覧検索結果を処理
 */
MediaListController.prototype.searchResultCallback = function(data) {
    var self = this;
    var result = JSON.parse(data.toString());

    // データエスケープ処理
    Escape.escapeHtml(result);

    // 掲載媒体マスタ一覧の表を描画
    self.createMediaList(result);
}

/**
 * 掲載媒体マスタ一覧の表を描画する
 */
MediaListController.prototype.createMediaList = function(result) {
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
MediaListController.prototype.createColModel = function() {
    var width = $('#list').width();

    var modelArray = [];
    modelArray.push(
        GridUtil.createColModel({
            name: 'media_code',
            width: width * 0.1
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'media_name',
            width: width * 0.2,
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'show_flg',
            width: width * 0.07,
            align: 'center',
            formatter : function(val, opt, rdt) {
                return GridUtil.formatTrueFalse(val,'表示','非表示')
            },
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'priority',
            width: width * 0.07,
            align: 'center',
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
                    '<button type="button" class="grid-btn-update" data-media-code="' + rdt.media_code + '">' + '編集' +'</button>'
                    + '<button type="button" class="grid-btn-delete" data-media-name="' + rdt.media_name 
                    + '" data-media-code="' + rdt.media_code + '" data-row-id="' + opt.rowId + '">' + '削除' + '</button>'
                );
            },
            sortable: false
        })
    );
    return {
        model: modelArray,
        name: ['掲載媒体コード', '掲載媒体名','表示/非表示','優先順位','最終更新者', '最終更新日時', 'データ操作']
    };
};

/**
 * jQGrid用のボタンイベント定義
 */
MediaListController.prototype.gridBtnEvent = function(data) {
    var self = this;
    $('.grid-btn-delete, .grid-btn-update').button();

    // 編集ボタンをクリックし、編集画面へ遷移する
    $('.grid-btn-update').on('click', function() {
        var button = $(this);
        // 掲載媒体コードを取得
        var mediacode = button.attr('data-media-code');
        // 掲載媒体編集画面へ遷移
        window.location.href = '/admin_app/media_update?mediac=' + mediacode;
    });

    $('.grid-btn-delete').off('click');
    // 削除ボタンをクリックし、削除処理を行う
    $('.grid-btn-delete').on('click', function() {
        var button = $(this);
        $('#delete-media-code').text(button.attr('data-media-code'));
        $('#delete-media-name').text(button.attr('data-media-name'));
        var modal = $('#delete-confirm-dialog');

        // 削除キャンセル処理
        $('.cancel-botton').on('click', function() {
            modal.dialog('close');
            $('.delete-button').off('click');
        });

        // ajaxで、削除処理を行う
        $('.delete-button').on('click', function() {
            var param = {
                'delete-media-code' : $('#delete-media-code').text(),
                'delete-media-name' : $('#delete-media-name').text(),
            };
            AjaxUtil.post('/admin_app/media_list/', param, function(data) {

                var result = JSON.parse(data.toString());
                
                if(result.is_error){
                    // 削除メッセージ表示
                    MsgUtil.showStatusMsg('#list', $('#delete-media-name').text() , '既に削除');
                }else{
                     // 削除メッセージ表示
                     MsgUtil.showStatusMsg('#list', $('#delete-media-name').text() , '削除');
                }

                // データエスケープ処理
                Escape.escapeHtml(result.mediaList);

                // 掲載媒体マスタ一覧の表を再描画
                MediaListController.prototype.createMediaList(result.mediaList);

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
MediaListController.prototype.downloadCsv = function() {
    var self = this;

    // CSVダウンロード全件
    $('#csv-all').click(function() {
        AjaxUtil.get('/admin_app/media_list/csv_download/', {}, function(data) {
            var fileName = '掲載媒体情報_全件.csv';
            FileUtil.outputCsv(data, fileName);
        });
    });
}

$(function() {
    var controller = new MediaListController();
    controller.init();
});
