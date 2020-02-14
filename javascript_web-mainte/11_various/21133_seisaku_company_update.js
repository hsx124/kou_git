var SeisakuCompanyUpdateController = function() {
};

SeisakuCompanyUpdateController.prototype = new AbstractController();


SeisakuCompanyUpdateController.prototype.selectedMenu = function() {
    return '.seisaku-company-list';
}

SeisakuCompanyUpdateController.prototype.bindEvent = function() {
    // 制作会社一覧画面に戻る
    $('.back-button').on('click', function() {
        window.location.href = '/admin_app/seisaku_company_list/';
    });

    return $.Deferred().resolve().promise();
}

$(function() {
    var controller = new SeisakuCompanyUpdateController();
    controller.init();
});