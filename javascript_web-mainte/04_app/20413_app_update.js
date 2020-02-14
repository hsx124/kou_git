var AppUpdateController = function() {};
AppUpdateController.prototype = new AbstractController();

/**
 * 書籍マスタ新規登録画面の主処理
 */
AppUpdateController.prototype.execute = function() {
    var self = this;

    // DatePicker設定
    InputUtil.setDataPicker();

    return $.Deferred()
        .resolve()
        .promise();
};

/**
 * メニュー選択処理
 */
AppUpdateController.prototype.selectedMenu = function() {
    return '.menu-app-master';
};

/**
 * イベント登録処理
 */
AppUpdateController.prototype.bindEvent = function() {

    // 一覧に戻るボタン
    $('.back-button ').on('click', function() {
        window.location.href = '/admin_app/app_list/';
    });
    return $.Deferred()
        .resolve()
        .promise();
};


$(function() {
    var controller = new AppUpdateController();
    controller.init();
});
