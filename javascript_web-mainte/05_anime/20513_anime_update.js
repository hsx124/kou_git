var AnimeUpdateController = function() {
};

AnimeUpdateController.prototype = new AbstractController();

AnimeUpdateController.prototype.selectedMenu = function() {
    return '.menu-anime-master';
}

AnimeUpdateController.prototype.bindEvent = function() {

    $('.back-button ').on('click', function() {
        window.location.href = '/admin_app/anime_list/';
    });

    return $.Deferred().resolve().promise();
}

$(function() {
    var controller = new AnimeUpdateController();
    controller.init();
});