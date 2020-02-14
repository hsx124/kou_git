var NovelIsbnListController = function() {};
NovelIsbnListController.prototype = new AbstractController();

/**
 * 小説一覧画面の主処理
 */
NovelIsbnListController.prototype.execute = function() {
    var self = this;

    return $.Deferred()
        .resolve()
        .promise();
};

/**
 * メニュー選択処理
 */
NovelIsbnListController.prototype.selectedMenu = function() {
    return '.novel-isbn-list';
};
/**
 * イベント登録処理
 */
NovelIsbnListController.prototype.bindEvent = function() {
    var self = this;
    
    return $.Deferred().resolve().promise();
};


$(function() {
    var controller = new NovelIsbnListController();
    controller.init();
});
