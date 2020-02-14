var HomeController = function() {
};
HomeController.prototype = new AbstractController();

/**
 * HOME画面の主処理
 */
HomeController.prototype.execute = function() {
    var self = this;

    // ピックアップ描画
    self.drawPickup();

    // i-noteからのお知らせ描画
    self.drawInoteNews();

    // NEWSエリア描画
    self.drawNews();

    $('.contents').css('visibility', 'visible');
    return $.Deferred().resolve().promise();
};

/**
 * メニュー選択処理
 */
HomeController.prototype.selectedMenu = function() {
    return '.home';
};

/**
 * イベント登録処理
 */
HomeController.prototype.bindEvent = function() {

    $("#id_button_all").click(function() {
        $(".news-tr").show();
        $(".sakuhin-tr").show();
        $(".update-tr").show();
        $(".news-table").scrollTop(0);
        $("#id_button_all").css("color", "#f39700");
        $("#id_button_news").css("color", "gray");
        $("#id_button_sakuhin").css("color", "gray");
        $("#id_button_update").css("color", "gray");
    });
    $("#id_button_news").click(function() {
        $(".news-tr").show();
        $(".sakuhin-tr").hide();
        $(".update-tr").hide();
        $(".news-table").scrollTop(0);
        $("#id_button_all").css("color", "gray");
        $("#id_button_news").css("color", " #f39700;");
        $("#id_button_sakuhin").css("color", "gray");
        $("#id_button_update").css("color", "gray");
    });
    $("#id_button_sakuhin").click(function() {
        $(".news-tr").hide();
        $(".sakuhin-tr").show();
        $(".update-tr").hide();
        $(".news-table").scrollTop(0);
        $("#id_button_all").css("color", "gray");
        $("#id_button_news").css("color", "gray");
        $("#id_button_sakuhin").css("color", " #f39700;");
        $("#id_button_update").css("color", "gray");
    });
    $("#id_button_update").click(function() {
        $(".news-tr").hide();
        $(".sakuhin-tr").hide();
        $(".update-tr").show();
        $(".news-table").scrollTop(0);
        $("#id_button_all").css("color", "gray");
        $("#id_button_news").css("color", "gray");
        $("#id_button_sakuhin").css("color", "gray");
        $("#id_button_update").css("color", " #f39700;");
    });

    return $.Deferred().resolve().promise();
}

HomeController.prototype.drawPickup = function() {

    var self = this;

    // key-visual-img-area高さ調整
    var deferredArr = [];
    $('.key-visual-list-item').each(function(i, elem) {
        var originSrc = elem.src;
        elem.src = "";
        var dfd = new $.Deferred();
        elem.onload = "";
        elem.onload = function() {
            dfd.resolve();
        };
        deferredArr.push(dfd.promise());
        elem.src = originSrc;
    });

    $.when.apply($, deferredArr).then(function() {
        var maxHeight = 0;
        $(".key-visual-group img").each(function(i, elem) {
            var height = $(elem).height();
            maxHeight = height > maxHeight ? height : maxHeight;
        })
        $(".key-visual-img-area").each(function(i, elem) {
            $(elem).css("height", maxHeight);
        })
        // mask追加
        $(".key-visual-group").each(function(i, elem) {
            var $elem = $(elem);
            var $img = $elem.find("img");
            var width = $img.width();
            var height = $img.height();
            var top = (maxHeight - height) / 2;
            var mask = $('<div class="mask" style="width:' + width + "px;height:" + height + "px;top:" + top + 'px;"oncontextmenu="return false;"></div>');

            var caption = $('<div class="caption" style="width:' + width + "px;height:" + height + 'px;"oncontextmenu="return false;">作品の詳細を見る</div>');
            mask.click(function() {
                window.location.href = "/ipdds/detail?sakuhin_code=" + djangoObj.key_visual[i].sakuhin_code;
            });
            mask.append(caption);
            $elem.find('.key-visual-img-area').append(mask);
        });

        // タグの表示
        self.drawPickupTag();
    });
};

HomeController.prototype.drawPickupTag = function() {
    var self = this;
    $('.key-visual-img-area').each(function() {
        var elem = $(this);
        var sakuhinCode = elem.find('img').attr('data-sakuhin-code');

        var param = {
            'sakuhin_code' : sakuhinCode
        };
        AjaxUtil.get('/ipdds/home/', param, function(data) {
            var tagInfo = JSON.parse(data.toString());
            var sakuhinCode = tagInfo['sakuhin_code'];
            var aTag1 = $('<a class="tag" href="' + self.getTagUrl(tagInfo['tag_code1']) + '">' + tagInfo['tag_name1'] + '</a>');
            var aTag2 = $('<a class="tag" href="' + self.getTagUrl(tagInfo['tag_code2']) + '">' + tagInfo['tag_name2'] + '</a>');
            var aTag3 = $('<a class="tag" href="' + self.getTagUrl(tagInfo['tag_code3']) + '">' + tagInfo['tag_name3'] + '</a>');
            var aTag4 = $('<a class="tag" href="' + self.getTagUrl(tagInfo['tag_code4']) + '">' + tagInfo['tag_name4'] + '</a>');
            var aTag5 = $('<a class="tag" href="' + self.getTagUrl(tagInfo['tag_code5']) + '">' + tagInfo['tag_name5'] + '</a>');

            $('#tag-' + sakuhinCode).append(aTag1, aTag2, aTag3, aTag4, aTag5);
        });
    });
};

HomeController.prototype.getTagUrl = function(tagCode) {
    var url = '/ipdds/search_result/?name_fact_tag=';
    return url + tagCode;
};

HomeController.prototype.drawInoteNews = function() {
    $('.js-text-overflow').each(function() {

        var $target = $(this);
        var html = $target.html();
        var $clone = $target.clone();
        $clone.width($target.width() + 56).height('auto');
        $target.after($clone);
        for (var i = 3; i >= 0; i--) {
            var beforeHtml = html;
            $clone.html(beforeHtml)
            while ($clone.height() > $target.height() + 30) {
                beforeHtml = html;
                html = html.substr(0, html.length - Math.pow(10, i));
                $clone.html(html + '...');
            }
            html = beforeHtml;
        }
        $target.html($clone.html());
        $clone.remove();
    });
};
HomeController.prototype.drawNews = function() {
    djangoObj.news.forEach(function(obj, index, array) {
        var tr = $("<tr>");
        var td_date = $("<td>");
        var td_category = $("<td>");
        var td_headline = $("<td>");
        if (obj.category == "お知らせ") {
            tr.addClass("news-tr");
            td_category.addClass("blue");
            var a = $("<a class='link detail-link' onclick=\"TransitionUtil.transition('" + obj.link_url + "')\">");
            a.append(obj.headline)
            td_headline.append(a);
        } else if (obj.category == "新着作品") {
            tr.addClass("sakuhin-tr");
            td_category.addClass("orange");
            var a = $("<a class='link detail-link' href='/ipdds/detail?sakuhin_code=" + obj.link_url + "'>");
            a.append(obj.headline);
            td_headline.append(a);
            td_headline.append("を追加しました。")
        } else {
            tr.addClass("update-tr");
            td_category.addClass("green");
            var a = $("<a class='link detail-link' href='/ipdds/detail?sakuhin_code=" + obj.link_url + "'>");
            a.append(obj.headline);
            td_headline.append(a);
            td_headline.append("を更新しました。")
        }

        td_date.addClass("date");
        td_date.append(obj.datetime);
        tr.append(td_date);
        td_category.append(obj.category);
        tr.append(td_category);
        tr.append(td_headline);

        $('.news-table').append(tr);
    });
};

$(function() {
    var controller = new HomeController();
    controller.init();
});
