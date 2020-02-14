var LinkCollectionController = function() {
};
LinkCollectionController.prototype = new AbstractController();

/**
 * メニュー選択処理
 */
LinkCollectionController.prototype.selectedMenu = function() {
    return '.linkCollection';
};

/**
 * イベント登録処理
 */
LinkCollectionController.prototype.bindEvent = function() {

    // アコーディオンの領域の開閉
    $(".input-panel-body").hide();
    $(".input-panel-label").on("click", function() {
        var elem = $(this).next();
        if (elem.is(":hidden")) {
            elem.slideDown(700);
            $(this).find("span").css("transform", "rotate(0deg)");
        } else {
            elem.slideUp(700);
            $(this).find("span").css("transform", "rotate(-90deg)");
        }
    });

    // アコーディオン（子）の開閉
    $(".input-panel-child-title").on("click", function() {
        var elem = $(this).next();
        if (elem.is(":hidden")) {
            elem.slideDown(700);
            $(this).find("span").css("transform", "rotate(0deg)");
        } else {
            elem.slideUp(700);
            $(this).find("span").css("transform", "rotate(-90deg)");
        }
    });
    // カテゴリ_全表示/非表示ボタン
    $(".all-open-close").on("click", function() {
        var all_close = true;
        $(this).parent().find(".input-panel-child-title").each(function(i, val) {
            var elem = $(val).next();
            if (elem.is(":hidden") == false) {
                all_close = false;
                return false;
            }
        });
        $(this).parent().find(".input-panel-child-title").each(function(i, val) {
            var elem = $(val).next();
            if (all_close) {
                elem.stop().slideDown(700);
                $(this).find("span").css("transform", "rotate(0deg)");
            } else {
                elem.stop().slideUp(700);
                $(this).find("span").css("transform", "rotate(-90deg)");
            }
        });
    });

    return $.Deferred().resolve().promise();
};

$(function() {
    var controller = new LinkCollectionController();
    controller.init();
});
