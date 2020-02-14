var MediaReportListController = function() {};
MediaReportListController.prototype = new AbstractController();

/**
 * 白書管理一覧画面の主処理
 */
MediaReportListController.prototype.execute = function() {
    var self = this;

    return $.Deferred()
        .resolve()
        .promise();
};

/**
 * メニュー選択処理
 */
MediaReportListController.prototype.selectedMenu = function() {
    return '.media-report-list';
};
/**
 * イベント登録処理
 */
MediaReportListController.prototype.bindEvent = function() {
    var self = this;
    
    return $.Deferred().resolve().promise();
};


$(function() {
    var controller = new MediaReportListController();
    controller.init();
});
