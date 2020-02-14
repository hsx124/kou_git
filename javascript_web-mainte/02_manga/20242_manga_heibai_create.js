var MangaHeibaiCreateController = function() {
};

MangaHeibaiCreateController.prototype = new AbstractController();

MangaHeibaiCreateController.prototype.selectedMenu = function() {
    return '.manga-heibai-list';
}

MangaHeibaiCreateController.prototype.bindEvent = function() {
    var self = this;
    // 併売情報一覧画面に戻る
    $('.back-button').on('click', function() {
        window.location.href = '/admin_app/manga_heibai_list/';
    });

    // マンガタイトル基本マスタ一覧生成
    $('.search-button').on('click',function(){
        // 選択した検索ボタンを判別する
        var select = $(this).attr('data-heibai');
        self.selectMangaList(select);
    })

    return $.Deferred().resolve().promise();
}

/**
 * マンガタイトル基本マスタ検索 (ajaxでマンガ一覧検索結果を取得)
 */
MangaHeibaiCreateController.prototype.selectMangaList = function(select) {
    var self = this;
    var param = {
        'manga' : 'manga-heibai-create',
        'keyword' : document.getElementById(select).value
    };

    AjaxUtil.get('/admin_app/manga_heibai_create/', param, function(data) {
        self.searchResultCallback(data);
    });
}

/**
 * ajaxでマンガ一覧検索結果を処理
 */
MangaHeibaiCreateController.prototype.searchResultCallback = function(data) {
    var self = this;
    var result = JSON.parse(data.toString());
    console.log(result)

    // データエスケープ処理
    Escape.escapeHtml(result);

    // マンガタイトル基本マスタ一覧の表を描画
    self.createMangaList(result);
}

/**
 * マンガタイトル基本マスタ一覧の表を描画する
 */
MangaHeibaiCreateController.prototype.createMangaList = function(result) {
    var self = this;

    var modal = $('#manga-confirm-dialog');

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
        GridUtil.renderNormalGrid('#grid-list', option, true);
    }
};

/**
 * jQGrid用のカラム定義
 */
MangaHeibaiCreateController.prototype.createColModel = function() {
    var width = $('#list').width();

    var modelArray = [];
    modelArray.push(
        GridUtil.createColModel({
            name: 'manga_title_code',
            width: width * 0.1
        })
    );

    var modelArray = [];
    modelArray.push(
        GridUtil.createColModel({
            name: 'manga_title_name',
            width: width * 0.2
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'rensai_start_yyyymm',
            width: width * 0.1,
            formatter : function(val) {
                if(val && val.length == 6){
                    return val.substring(0,4) + '/' + val.substring(4);
                } else if (val && val.length == 4) {
                    return val;
                } else {
                    return ' ';
                }
            }
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'media_name',
            width: width * 0.1,
            align: 'left',
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'publisher_name',
            width: width * 0.1,
            align: 'left',
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
                    '<button type="button" class="grid-btn-select" data-manga-code="' + rdt.manga_title_code + '" data-manga-name="' + rdt.manga_title_name + '">' + '編集' +'</button>'
                    );
                },
            sortable: false
        })
    );
    return {
        model: modelArray,
        name: ['マンガタイトルコード','マンガタイトル名', '連載開始年月','掲載媒体','出版社','最終更新者', '最終更新日時', '操作']
    };
};


$(function() {
    var controller = new MangaHeibaiCreateController();
    controller.init();
});