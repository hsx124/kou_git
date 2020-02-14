var MediaUpdateController = function() {
};

MediaUpdateController.prototype = new AbstractController();


MediaUpdateController.prototype.selectedMenu = function() {
    return '.media-list';
}

MediaUpdateController.prototype.bindEvent = function() {
    //優先順位のツールチープを追加
    TextfollowUtil.execute();

    // 掲載媒体一覧画面に戻る
    $('.back-button').on('click', function() {
        window.location.href = '/admin_app/media_list/';
    });

    return $.Deferred().resolve().promise();
}

$(function() {
    var controller = new MediaUpdateController();
    controller.init();
});