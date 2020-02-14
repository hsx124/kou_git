var PublisherUpdateController = function() {
};

PublisherUpdateController.prototype = new AbstractController();


PublisherUpdateController.prototype.selectedMenu = function() {
    return '.publisher-list';
}

PublisherUpdateController.prototype.bindEvent = function() {
    // 出版社一覧画面に戻る
    $('.back-button').on('click', function() {
        window.location.href = '/admin_app/publisher_list/';
    });

    return $.Deferred().resolve().promise();
}

$(function() {
    var controller = new PublisherUpdateController();
    controller.init();
});