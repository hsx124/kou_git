var StaffUpdateController = function() {
};

StaffUpdateController.prototype = new AbstractController();

StaffUpdateController.prototype.selectedMenu = function() {
    return '.staff-list';
}

StaffUpdateController.prototype.bindEvent = function() {
    // スタッフ情報一覧画面に戻る
    $('.back-button').on('click', function() {
        window.location.href = '/admin_app/staff_list/';
    });

    return $.Deferred().resolve().promise();
}

$(function() {
    var controller = new StaffUpdateController();
    controller.init();
});