var CoreUpdateController = function() {
};

CoreUpdateController.prototype = new AbstractController();

CoreUpdateController.prototype.selectedMenu = function() {
    return '.core-list';
}

CoreUpdateController.prototype.bindEvent = function() {
    // コア情報一覧画面に戻る
    $('.back-button').on('click', function() {
        window.location.href = '/admin_app/core_list/';
    });

    return $.Deferred().resolve().promise();
}

$(function() {
    var controller = new CoreUpdateController();
    controller.init();
});