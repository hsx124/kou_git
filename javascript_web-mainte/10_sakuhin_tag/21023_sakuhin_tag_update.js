var SakuhinTagUpdateController = function() {
};

SakuhinTagUpdateController.prototype = new AbstractController();

SakuhinTagUpdateController.prototype.selectedMenu = function() {
    return '.tag-list';
}

SakuhinTagUpdateController.prototype.bindEvent = function() {
    // 作品タグ情報一覧画面に戻る
    $('.back-button').on('click', function() {
        window.location.href = '/admin_app/sakuhin_tag_list/';
    });

    return $.Deferred().resolve().promise();
}

$(function() {
    var controller = new SakuhinTagUpdateController();
    controller.init();
});