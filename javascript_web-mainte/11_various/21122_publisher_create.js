var PublisherCreateController = function() {
};

PublisherCreateController.prototype = new AbstractController();

PublisherCreateController.prototype.selectedMenu = function() {
    return '.publisher-list';
}

PublisherCreateController.prototype.bindEvent = function() {
    // 出版社一覧画面に戻る
    $('.back-button').on('click', function() {
        window.location.href = '/admin_app/publisher_list/';
    });

    return $.Deferred().resolve().promise();
}

$(function() {
    var controller = new PublisherCreateController();
    controller.init();
});