var SeisakuCompanyCreateController = function() {
};

SeisakuCompanyCreateController.prototype = new AbstractController();

SeisakuCompanyCreateController.prototype.selectedMenu = function() {
    return '.seisaku-company-list';
}

SeisakuCompanyCreateController.prototype.bindEvent = function() {
    // 制作会社一覧画面に戻る
    $('.back-button').on('click', function() {
        window.location.href = '/admin_app/seisaku_company_list/';
    });

    return $.Deferred().resolve().promise();
}

$(function() {
    var controller = new SeisakuCompanyCreateController();
    controller.init();
});