var LoginController = function() {};
LoginController.prototype = new AbstractController();

/**
 * IPマスタ一覧画面の主処理
 */
LoginController.prototype.execute = function() {
    return $.Deferred()
        .resolve()
        .promise();
};

/**
 * 継承元クラスのメニュー描画処理を無効化
 */
LoginController.prototype.createMenu = function() {
    // ログイン画面はメニュー不要のため空で上書き
    return $.Deferred()
    .resolve()
    .promise();
};

/**
 * イベント登録処理
 */
LoginController.prototype.bindEvent = function() {
    return $.Deferred()
        .resolve()
        .promise();
};

$(function() {
    var controller = new LoginController();
    controller.init();
});
