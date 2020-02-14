var SakuhinTagCategoryCreateController = function() {
};

SakuhinTagCategoryCreateController.prototype = new AbstractController();

SakuhinTagCategoryCreateController.prototype.selectedMenu = function() {
    return '.sakuhin_tag_category-list';
}

SakuhinTagCategoryCreateController.prototype.bindEvent = function() {
    // タグカテゴリー情報一覧画面に戻る
    $('.back-button').on('click', function() {
        window.location.href = '/admin_app/sakuhin_tag_category_list/';
    });

    return $.Deferred().resolve().promise();
}

$(function() {
    var controller = new SakuhinTagCategoryCreateController();
    controller.init();
});