var MangaIsbnListController = function() {};
MangaIsbnListController.prototype = new AbstractController();

/**
 * 詳細情報（ISBN）一覧画面の主処理
 */
MangaIsbnListController.prototype.execute = function() {
    var self = this;

    return $.Deferred()
        .resolve()
        .promise();
};

/**
 * メニュー選択処理
 */
MangaIsbnListController.prototype.selectedMenu = function() {
    return '.manga-isbn-list';
};
/**
 * イベント登録処理
 */
MangaIsbnListController.prototype.bindEvent = function() {
    var self = this;
    
    return $.Deferred().resolve().promise();
};


$(function() {
    var controller = new MangaIsbnListController();
    controller.init();
});
