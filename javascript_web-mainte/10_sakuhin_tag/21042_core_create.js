var CoreCreateController = function() {
};

CoreCreateController.prototype = new AbstractController();

CoreCreateController.prototype.selectedMenu = function() {
    return '.core-list';
}

CoreCreateController.prototype.bindEvent = function() {
    // コア情報一覧画面に戻る
    $('.back-button').on('click', function() {
        window.location.href = '/admin_app/core_list/';
    });

    return $.Deferred().resolve().promise();
}

$(function() {
    var controller = new CoreCreateController();
    controller.init();
});