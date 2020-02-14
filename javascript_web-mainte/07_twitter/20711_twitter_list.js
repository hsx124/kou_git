var TwitterListController = function() {};
TwitterListController.prototype = new AbstractController();

/**
 * Twitter一覧画面の主処理
 */
TwitterListController.prototype.execute = function() {
    var self = this;

    return $.Deferred()
        .resolve()
        .promise();
};

/**
 * メニュー選択処理
 */
TwitterListController.prototype.selectedMenu = function() {
    return '.twitter-list';
};
/**
 * イベント登録処理
 */
TwitterListController.prototype.bindEvent = function() {
    var self = this;
    
    return $.Deferred().resolve().promise();
};


$(function() {
    var controller = new TwitterListController();
    controller.init();
});
