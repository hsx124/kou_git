var IpCreateController = function() {
};

IpCreateController.prototype = new AbstractController();

IpCreateController.prototype.selectedMenu = function() {
    return '.ip-list';
}

IpCreateController.prototype.bindEvent = function() {
    // Ip情報一覧画面に戻る
    $('.back-button').on('click', function() {
        window.location.href = '/admin_app/ip_list/';
    });

    return $.Deferred().resolve().promise();
}

$(function() {
    var controller = new IpCreateController();
    controller.init();
});