var GameListController = function() {};
GameListController.prototype = new AbstractController();

/**
 * ゲーム一覧画面の主処理
 */
GameListController.prototype.execute = function() {
    var self = this;

    return $.Deferred()
        .resolve()
        .promise();
};

/**
 * メニュー選択処理
 */
GameListController.prototype.selectedMenu = function() {
    return '.game-list';
};
/**
 * イベント登録処理
 */
GameListController.prototype.bindEvent = function() {
    var self = this;
    
    return $.Deferred().resolve().promise();
};


$(function() {
    var controller = new GameListController();
    controller.init();
});
