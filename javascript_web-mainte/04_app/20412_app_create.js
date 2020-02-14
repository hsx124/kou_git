var AppCreateController = function() {};
AppCreateController.prototype = new AbstractController();

/**
 * アプリマスタ新規登録画面の主処理
 */
AppCreateController.prototype.execute = function() {
    // DatePicker設定
    InputUtil.setDataPicker();

    return $.Deferred()
        .resolve()
        .promise();
};

/**
 * メニュー選択処理
 */
AppCreateController.prototype.selectedMenu = function() {
    return '.menu-app-master';
};

/**
 * イベント登録処理
 */
AppCreateController.prototype.bindEvent = function() {

    // 一覧に戻るボタン
    $('.back-button ').on('click', function() {
        window.location.href = '/admin_app/app_list/';
    });

    return $.Deferred()
        .resolve()
        .promise();
};

$(function() {
    var controller = new AppCreateController();
    controller.init();
});
