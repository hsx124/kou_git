var IpUpdateController = function() {
};

IpUpdateController.prototype = new AbstractController();

IpUpdateController.prototype.selectedMenu = function() {
    return '.ip-list';
}

IpUpdateController.prototype.bindEvent = function() {
    // Ip情報一覧画面に戻る
    $('.back-button').on('click', function() {
        window.location.href = '/admin_app/ip_list/';
    });

    return $.Deferred().resolve().promise();
}

$(function() {
    var controller = new IpUpdateController();
    controller.init();
});