var SimilarSearchController = function() {
};
SimilarSearchController.prototype = new AbstractController();

/**
 * 類似検索画面の主処理
 */
SimilarSearchController.prototype.execute = function() {
    var self = this;

    // チェックボックスフォントサイズ調整
    $(".label").each(function(e){
        var target = $(this);
        var textLength = target.text().length;
        if(textLength >= 12) {
            target.css("fontSize", "12px"); 
        }
    });
    
    // +-ボタン制御用
    self.divKeywordText = $('<div class="search-keyword-text"></div>');
    self.inputText = $('<input type="text" name="name_keyword" placeholder="「タイトル」または「キーワード」を検索してください" />');
    self.buttonArea = $('<div class="keyword-button-area"></div>');
    self.addButton = $('<div class="keyword-add-button">＋</div>');
    self.delButton = $('<div class="keyword-del-button">ー</div>');
    // キーワード＋－ボタン制御
    var buttonAreaClone = self.buttonArea.clone();
    var addButtonClone = self.addButton.clone().on("click", function() {
        self.appendHtml().slideDown();
    });
    buttonAreaClone.append(addButtonClone);
    var divKeywordTextClone = self.divKeywordText.clone();
    divKeywordTextClone.append(self.inputText.clone());
    divKeywordTextClone.append(buttonAreaClone);

    $(".search-keyword-area .input-panel-body").append(divKeywordTextClone);

    // 展開時期年月日生成
    var now = new Date();
    var yearOptions = '<option value="----" > ---- </option>';
    var monthOptions = '<option value="--" > -- </option>';
    var dayOptions = '<option value="--" > -- </option>';
    for (var year = now.getFullYear(); year >= 1950; year--) {
        yearOptions += '<option value="' + StringUtil.lpad(year, 4) + '" >' + year + '</option>';
    }
    for (var month = 1; month <= 12; month++) {
        monthOptions += '<option value="' + StringUtil.lpad(month, 2) + '" >' + month + '</option>';
    }
    for (var day = 1; day <= 31; day++) {
        dayOptions += '<option value="' + StringUtil.lpad(day, 2) + '" >' + day + '</option>';
    }
    $(".date-year").each(function(i, val) {
        $(val).append(yearOptions);
    })
    $(".date-month").each(function(i, val) {
        $(val).append(monthOptions);
    })
    $(".date-day").each(function(i, val) {
        $(val).append(dayOptions);
    })

    // セッションから比較かごデータを取得する。
    CompareKago.getSessionData().done(function(data){
        // 比較かごIP領域を描画する
        $('.compare-kago-list-contents').empty();
        CompareKago.drawCompareIp(data);
    });

    return $.Deferred().resolve().promise();
};

/**
 * メニュー選択処理
 */
SimilarSearchController.prototype.selectedMenu = function() {
    return '.search, .similar';
};

/**
 * イベント登録処理
 */
SimilarSearchController.prototype.bindEvent = function() {
    var self = this;

    // 類似検索の領域の開閉
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

    // 事実メタ_全表示/非表示ボタン
    $(".all-open-close").on("click", function() {
        var all_close = true;
        $(".input-panel-child-title").each(function(i, val) {
            var elem = $(val).next();
            if (elem.is(":hidden") == false) {
                all_close = false;
                return false;
            }
        });
        $(".input-panel-child-title").each(function(i, val) {
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

    // 事実メタの開閉
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

    // 類似検索の「すべてのチェックを外す」ボタン押下時
    $(".all-uncheck").on("click", function() {
        $(".select-item").find("input").prop("checked", false);
    });

    // ラジオボタン風チェックボックスの制御
    $(".checkbox-radio").click(function() {
        $(this).closest('.checkbox-radio-group').find('input:checkbox').not(this).prop('checked', false);
    });

    // ラジオボタン2度押しで解除
    var checkedArray = {};
    $('input[type="radio"].can-release').click(function() {
        if (checkedArray[$(this).attr('name')] == $(this).attr('value')) {
            $(this).prop('checked', false);
            delete checkedArray[$(this).attr('name')];
        } else {
            checkedArray[$(this).attr('name')] = $(this).attr('value');
        }
    });

    return $.Deferred().resolve().promise();
}

// キーワード検索の入力を追加する
SimilarSearchController.prototype.appendHtml = function() {
    var self = this;
    var html = self.createHtml();
    html.hide();
    $(".search-keyword-area .input-panel-body").append(html);
    return html;
}
SimilarSearchController.prototype.createHtml = function() {
    var self = this;
    var buttonAreaClone = self.buttonArea.clone();
    var addButtonClone = self.addButton.clone().on("click", function() {
        self.appendHtml().slideDown();
    });
    var delButtonClone = self.delButton.clone().on("click", function() {
        var html = $(this).parent().parent();
        html.slideUp('normal', function() {
            html.remove();
        });
    });
    buttonAreaClone.append(addButtonClone);
    buttonAreaClone.append(delButtonClone);

    var divKeywordTextClone = self.divKeywordText.clone();
    divKeywordTextClone.append(self.inputText.clone());
    divKeywordTextClone.append(buttonAreaClone);
    return divKeywordTextClone;
}

$(function() {
    var controller = new SimilarSearchController();
    controller.init();
});
