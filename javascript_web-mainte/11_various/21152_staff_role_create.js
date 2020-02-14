var StaffRoleCreateController = function() {
};

StaffRoleCreateController.prototype = new AbstractController();

StaffRoleCreateController.prototype.selectedMenu = function() {
    return '.staff-role-list';
}

StaffRoleCreateController.prototype.bindEvent = function() {
    // スタッフ役割情報一覧画面に戻る
    $('.back-button').on('click', function() {
        window.location.href = '/admin_app/staff_role_list/';
    });

    return $.Deferred().resolve().promise();
}

$(function() {
    var controller = new StaffRoleCreateController();
    controller.init();
});