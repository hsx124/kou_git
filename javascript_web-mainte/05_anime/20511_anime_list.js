var AnimeListController = function() {};
AnimeListController.prototype = new AbstractController();

/**
 * アニメマスタ一覧画面の主処理
 */
AnimeListController.prototype.execute = function() {
    var self = this;


    // アニメグリッド表示
    // self.createAnimeGrid()

    return $.Deferred()
        .resolve()
        .promise();
};

/**
 * メニュー選択処理
 */
AnimeListController.prototype.selectedMenu = function() {
    return '.anime-list';
};

/**
 * イベント登録処理
 */
AnimeListController.prototype.bindEvent = function() {
    var self = this;

    // 更新履歴DLエリアのイベント設定
    NoticeTableUtil.setDLArea();

    // 更新履歴CSVダウンロード
    NoticeTableUtil.downloadTableCsv('m_anime_title', 'アニメタイトル基本マスタ');

    // // 作品コード検索
    // self.searchSakuhinBySakuhinCode();

    // // 作品名検索
    // self.searchSakuhinBySakuhinName();

    // CSVダウンロード
    self.downloadCsv();

    return $.Deferred()
        .resolve()
        .promise();
};


/**
 * アニメマスタ情報一覧生成<br>
 * jQGridを使用して表を描画する。
 */
AnimeListController.prototype.createAnimeGrid = function(djangoObj) {
    var self = this;

    // 新規登録ボタン無効化判定
    self.checkCreateBtnDisabled(djangoObj);

    if ($('#gbox_list-grid').is(':visible')) {
        $('#list-grid').jqGrid('clearGridData').trigger('reloadGrid');
        $('#list-grid').jqGrid('setGridParam', {
            data : djangoObj,
        }).trigger('reloadGrid');
    } else {

    // グリッド生成
    var colModel = self.createColModel();
    var option = {
        colNames: colModel.name,
        colModel: colModel.model,
        data: djangoObj,
        width: $('#list').width(),
        pager: '#pager',
        loadComplete: self.gridBtnEvent
    };
        GridUtil.renderNormalGrid('#list-grid', option, true);
    }
};

/**
 * アニメ一覧生成<br>
 * jQGridを使用して表を描画する。
 */
AnimeListController.prototype.createAnimeList = function(djangoObj) {
    var self = this;

    // 新規登録ボタン無効化判定
    self.checkCreateBtnDisabled(djangoObj);

    if ($('#gbox_list-grid').is(':visible')) {
        $('#list-grid').jqGrid('clearGridData').trigger('reloadGrid');
        $('#list-grid').jqGrid('setGridParam', {
            data : djangoObj,
        }).trigger('reloadGrid');
    } else {

    // グリッド生成
    var colModel = self.createColModel();
    var option = {
        colNames: colModel.name,
        colModel: colModel.model,
        data: djangoObj,
        width: $('#list').width(),
        pager: '#pager',
        loadComplete: self.gridBtnEvent
    };
        GridUtil.renderNormalGrid('#list-grid', option, true);
    }
};

/**
 * jQGrid用のカラム定義
 */
AnimeListController.prototype.createColModel = function() {
    var width = $('#list').width();

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
            name: 'tv_program_name',
            width: width * 0.2
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'period',
            width: width * 0.1,
            align: 'center',
            formatter: GridUtil.formatMaruBatsu,
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'broadcaster',
            width: width * 0.1,
            align: 'center',
            formatter: GridUtil.formatMaruBatsu,
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
            name: 'update_date',
            formatter : 'date',
            width: width * 0.08,
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
            width: width * 0.1,
            align: 'center',
            formatter: function(val, opt, rdt) {
                return (
                    '<button type="button" class="grid-btn-update" data-sakuhin-code="' + rdt.sakuhin_code +
                    '" data-anime-name="' + rdt.tv_program_name +'">編集</button>' +
                    '<button type="button" class="grid-btn-delete" data-sakuhin-name="' + rdt.sakuhin_name +
                    '" data-anime-name="' + rdt.tv_program_name +
                    '" data-sakuhin-code="' + rdt.sakuhin_code +
                    '"data-row-id="' + opt.rowId + '">' +'削除' +'</button>'
                );
            },
            sortable: false
        })
    );
    return {
        model: modelArray,
        name: ['作品コード', '作品名', 'Wikipedia - アニメタイトル', '放送期間', '放送局', '最終更新者', '最終更新日時', 'データ操作']
    };
};

/**
 * jQGrid用のボタンイベント定義
 */
AnimeListController.prototype.gridBtnEvent = function(data) {
    var local = data;

    // 編集ボタン
    $('.grid-btn-update').button();
    $('.grid-btn-update').on('click', function() {
        var button = $(this);
        var sakuhinCode = button.attr('data-sakuhin-code');
        var animeName = button.attr('data-anime-name');

        window.location.href = '/admin_app/anime_update?sakuhinc='+sakuhinCode + '&anime_name=' + animeName;
    });

    // 削除ボタン
    $('.grid-btn-delete').button();

    $('.grid-btn-delete').off('click');
    $('.grid-btn-delete').on('click', function() {
        var button = $(this);
        var rowId = button.attr('data-row-id');
        $('#delete-sakuhin-name').text(button.attr('data-sakuhin-name'));
        $('#delete-anime-name').text(button.attr('data-anime-name'));

        var modal = $('#delete-confirm-dialog');
        $('.cancel-botton').on('click', function() {
            modal.dialog('close');
            $('.delete-button').off('click');
        });
        $('.delete-button').on('click', function() {
            var param = {
                'reload-sakuhin-code' : $('.grid-btn-delete').attr('data-sakuhin-code'),
                'delete-anime-name' : $('#delete-anime-name').text(),
            };
            AjaxUtil.post('/admin_app/anime_list/', param, function(data) {
                var result = JSON.parse(data.toString());

                // グリッド描画
                AnimeListController.prototype.createAnimeList(result);

                // 削除メッセージ表示
                MsgUtil.showStatusMsg('#grid-area', $('#delete-anime-name').text() , '削除');
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
 * 作品検索時のコールバック処理
 *
 * @param data
 *            非同期通信結果
 */
AnimeListController.prototype.searchResultCallback = function(data) {
    var self = this;
    var result = JSON.parse(data.toString());

    // 作品選択ボタン生成
    self.createSakuhinSelect(result)

    // 作品選択時にグリッド生成イベント付与
    self.createGrid()

    $('.sakuhin-name-result').slideDown('slow');

    // 検索結果表示位置までスクロール
    var position = $('.sakuhin-name-result').offset().top -300;
    $('html,body').animate({
        scrollTop : position}
        ,1000
    );
};

/**
 * 作品コード検索<br>
 * ajaxで作品コード検索結果を取得
 */
AnimeListController.prototype.searchSakuhinBySakuhinCode = function() {
    var self = this;

    // 作品コード検索ボタン
    $('#search-sakuhin-code-button').click(function(event) {

        // グリッド非表示
        $('.search-list').slideUp('slow');
        setTimeout(function() {
            $('#list-grid').GridUnload();
        }, 500);

        // エラーメッセージ削除
        $('.input-err').removeClass('input-err');
        $('.input-err-msg').remove();

        // 入力チェックエラーの場合、検索を行わない
        // if (!InputCheckUtil.checkSakuhinCode()) {
        //     return;
        // }

        // 作品コードの場合、コード決めうちなので10桁半角英数以外は拒否する。
        var param = {
            'input-sakuhin-code' : $('#input-sakuhin-code').val()
        };
        AjaxUtil.get('/admin_app/anime_list/', param, function(data) {
            self.searchResultCallback(data);
        });
    });
}
/**
 * 作品名検索<br>
 * ajaxで作品名検索結果を取得
 */
AnimeListController.prototype.searchSakuhinBySakuhinName = function() {
    var self = this;
    // 作品コード検索ボタン
    $('#search-sakuhin-name-button').click(function(event) {

        // グリッド非表示
        $('.search-list').slideUp('slow');
        setTimeout(function() {
            $('#list-grid').GridUnload();
        }, 500);

        // エラーメッセージ削除
        $('.input-err').removeClass('input-err');
        $('.input-err-msg').remove();
        
        // 入力チェックエラーの場合、検索を行わない
        // if (!InputCheckUtil.checkSakuhinName()) {
        //     return;
        // }

        // 作品コードの場合、コード決めうちなので10桁半角英数以外は拒否する。
        var param = {
            'input-sakuhin-name' : $('#input-sakuhin-name').val()
        };
        
        AjaxUtil.get('/admin_app/anime_list/', param, function(data) {
            self.searchResultCallback(data);
        });
    })
}

/**
 * 作品名選択（ラジオボタン）生成<br>
 */
AnimeListController.prototype.createSakuhinSelect = function(data) {
    var self = this;

    // 作品選択ボタン削除
    $('#sakuhin-search-result').children().remove();

    // 検索件数が0件の場合、ラジオ生成しない
    if (data.length) {
        // ラジオボタン生成
        for (var i = 0; i < data.length; i++) {
            var $radio = $('<label for="radio' + i + '"></label>');
            $radio.text(data[i].sakuhin_code + ':' + data[i].sakuhin_name);
            $radio.append('<input type="radio" name="sakuhin-list" id="radio' + i + '" value="' + data[i].sakuhin_code + '">');
            $radio.append('<input type="hidden" id="' + data[i].sakuhin_code + '" value="' + data[i].sakuhin_name + '">');
            $('#sakuhin-search-result').append($radio);
        }
        // ラジオボタンにjQueryUIのスタイルを適応
        self.setJqueryUI();

        // ラジオボタンを縦に配置
        $(".controlgroup-vertical").controlgroup({
            "direction" : "vertical"
        });
    } else {
        $('#sakuhin-search-result').append('<div>検索条件に該当する作品が見つかりませんでした。</div>');
    }

}

/**
 * グリッド生成<br>
 */
AnimeListController.prototype.createGrid = function() {

    var self = this;
    // グリッド生成
    $('input[name="sakuhin-list"]').on('change', function() {
        var param = {
            'sakuhin-list' : $(this).val()
        };
        setTimeout(function() {
            AjaxUtil.get('/admin_app/anime_list/', param, function(data) {
                var result = JSON.parse(data.toString());

                self.createAnimeList(result);

                $('.search-list').slideDown('slow');

                // グリッド表示位置までスクロール
                var position = $('.search-list').offset().top -300;
                $('html,body').animate({
                    scrollTop : position}
                    ,1000
                );
            });
        }, 1000);

    });
}

/**
 * CSVダウンロードイベント追加
 */
AnimeListController.prototype.downloadCsv = function() {

    var self = this;

    // CSVダウンロード全件
    $('#csv-all').click(function() {
        AjaxUtil.get('/admin_app/anime_list/csv_download/', {}, function(data) {
            var fileName = 'アニメマスタ_全件.csv';
            FileUtil.outputCsv(data, fileName);
        });
    });

}

/**
 * 新規登録ボタン無効化判定
 */
AnimeListController.prototype.checkCreateBtnDisabled = function(gridData) {

    $('.disable-msg').remove();

    if(0 < gridData.length){
        // 新規登録ボタン無効化
        // 1作品に紐づけられるアニメは1作品のみとする。
        $('.create-button').off()

        $('.create-button').parent().prepend('<div class="disable-msg input-err-msg">既にアニメ情報が登録されているため、アニメ情報の編集と削除のみ行うことができます。</div>');
        $('.create-button').addClass('disable-button');
    } else {
        // 新規登録ボタン有効化

        // 削除で既存アニメがなくなった場合、新規登録可能とする
        $('.create-button').on('click', function() {
            var sakuhincode = $('input[name="sakuhin-list"]:checked').val()
            window.location.href = '/admin_app/anime_create?sakuhinc=' + sakuhincode;
        });
        $('.create-button').removeClass('disable-button');
    }
}

$(function() {
    var controller = new AnimeListController();
    controller.init();
});
