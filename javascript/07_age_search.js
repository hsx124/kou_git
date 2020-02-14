var AgeSearchController = function() {
};
AgeSearchController.prototype = new AbstractController();

/**
 * メニュー選択処理
 */
AgeSearchController.prototype.selectedMenu = function() {
    return ".search, .age";
};

$(function() {
    var controller = new AgeSearchController();
    controller.init();
});
