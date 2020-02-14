var AnimeCreateController = function() {};
AnimeCreateController.prototype = new AbstractController();

/**
 * アニメマスタ新規登録画面の主処理
 */
AnimeCreateController.prototype.execute = function() {
    // DatePicker設定
    InputUtil.setDataPicker();

    return $.Deferred()
        .resolve()
        .promise();
};

/**
 * メニュー選択処理
 */
AnimeCreateController.prototype.selectedMenu = function() {
    return '.menu-anime-master';
};

/**
 * イベント登録処理
 */
AnimeCreateController.prototype.bindEvent = function() {

    // 一覧に戻るボタン
    $('.back-button ').on('click', function() {
        window.location.href = '/admin_app/anime_list/';
    });

    return $.Deferred()
        .resolve()
        .promise();
};

$(function() {
    var controller = new AnimeCreateController();
    controller.init();
});
