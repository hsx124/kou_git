var SearchTitleController = function() {
};
SearchTitleController.prototype = new AbstractController();

/**
 * メニュー選択処理
 */
SearchTitleController.prototype.selectedMenu = function() {
    return '.search,.keyword';
};

/**
 * イベント登録処理
 */
SearchTitleController.prototype.bindEvent = function() {
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
    // タイトル名検索
    $("div.hiragana-map-small>span").on("click", function(e) {
        var target = $(this);
        var temp = target.text();
        var parent = $(target).parent().parent();
        var details = parent.find(".input-panel-child-detail");

        details.each(function(i, v) {
            var str = $(v).find(".input-panel-child-title").text();
            if (str.indexOf(temp) != -1) {
                var elem = $(v).find(".input-panel-child-title").next();
                elem.slideDown(700);
                $(v).find(".input-panel-child-title").find("span").css("transform", "rotate(0deg)");
            } else {
                var elem = $(v).find(".input-panel-child-title").next();
                elem.slideUp(700);
                $(v).find(".input-panel-child-title").find("span").css("transform", "rotate(-90deg)");
            }
        });
    });

    // タイトル名に関する領域表示
    $("div.hiragana-map>span").on("click", function(e) {
        var target = $(this);
        var temp = target.text();
        $(".category-label").each(function(i, elem) {
            var txt = elem.innerText;
            if (txt.indexOf(temp) != -1) {
                var topDistance = elem.offsetTop + 4;
                $("html").animate({
                    "scrollTop" : topDistance
                }, "slow");
                return false;
            }
        });
    });

}

$(function() {
    var controller = new SearchTitleController();
    controller.init();
});