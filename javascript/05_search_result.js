var SearchResultController = function() {
};
SearchResultController.prototype = new AbstractController();

/**
 * 検索結果一覧画面の主処理
 */
SearchResultController.prototype.execute = function() {

    var self = this;

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

    self.loadPromise = $.Deferred();
    // 検索結果(キーワード検索)
    self.search_result_keyword = djangoObj.search_result_keyword;
    // 検索結果(類似検索)
    self.search_result_similar = djangoObj.search_result_similar;
    // 平均発行部数が多い順のソート結果保持用
    self.search_result_sorted_by_book_avg = [];
    // 累計発行部数が多い順のソート結果保持用
    self.search_result_sorted_by_book_sum = [];
    // 更新日付が新しい順のソート結果保持用
    self.search_result_sorted_by_update_newer = [];
    // 連載開始が新しい順のソート結果保持用
    self.search_result_sorted_by_release_newer = [];
    // 連載開始が古い順のソート結果保持用
    self.search_result_sorted_by_release_older = [];
    // タグ一致率順のソート結果保持用
    self.search_result_sorted_by_similar_rate = [];
    /*
     * 0:平均発行部数が多い順 1:累計発行部数が多い順 2:更新日付が新しい順 3:連載開始が新しい順 4:連載開始が古い順 5:タグ一致率順
     */
    self.sort_pattern = '5'

    // 各ソート処理を実行しておく
    self.sortAll();

    // チェックボックスフォントサイズ調整
    $(".label").each(function(e){
        var target = $(this);
        var textLength = target.text().length;
        if(textLength >= 12) {
            target.css("fontSize", "12px"); 
        }
    });

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

    // 類似検索領域にユーザ入力内容を反映
    self.applyInput();

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
SearchResultController.prototype.selectedMenu = function() {
    return '.similar';
};

/**
 * イベント登録処理
 */
SearchResultController.prototype.bindEvent = function() {
    var self = this;

    // 再検索時のajax処理
    $("#id_search_form").submit(function(event) {
        $(".search-button button").prop("disabled", true);
        $('#id_redraw_area').children().remove()
        LoadingUtil.stop();
        LoadingUtil.start('再検索中...', $('.ratio-4'));
        event.preventDefault();

        var param = $('#id_search_form').serializeArray();
        AjaxUtil.post('/ipdds/search_result/', param, function(data) {
            LoadingUtil.stop();
            var tmpDjangoObj = data.toString();
            djangoObj = JSON.parse(tmpDjangoObj);
            // 検索結果(キーワード検索)
            self.search_result_keyword = djangoObj.search_result_keyword;
            // 検索結果(類似検索)
            self.search_result_similar = djangoObj.search_result_similar;
            self.sortAll();
            self.draw(self.sort_pattern).then(function(){ 
                $(".search-button button").prop("disabled", false); 
            });
        })

    });

    // ソートモーダル
    var modal = $("#id_sort_type_select_dialog");
    $(".sort-button").click(function() {
        modal.dialog({
            title : "ソート順",
            resizable : false,
            modal : true,
            width : "380px"
        });
        $(".dialog-select-area input[type=radio]").checkboxradio();
    });
    $(".enter").on("click", function() {
        $('#id_redraw_area').children().remove()
        var checked = $('input[name=name_radio]:checked');
        self.draw(checked.val());
        self.sort_pattern = checked.val();
        $(".sort-pattern").text(checked.parent().text())
        modal.dialog("close");
    });
    $(".cancel").on("click", function() {
        modal.dialog("close");
    });

    // 類似検索
    // キーワード検索の領域の開閉
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

    // 類似検索の「すべてのチェックを外す」ボタン押下時
    $(".all-uncheck").on("click", function() {
        $(".select-item").find("input").prop("checked", false);
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

    // 描画処理の登録
    self.draw('5');

    return $.Deferred().resolve().promise();
};

// ユーザ入力情報をフォームに反映する
SearchResultController.prototype.applyInput = function() {
    var self = this;
    // キーワード
    keyword = djangoObj.input_contents.keyword;
    $(".search-keyword-text").children("input").prop("value", keyword[0]);
    if (keyword.length > 1) {
        for (var i = 1; i < keyword.length; i++) {
            self.appendHtml().show().find("input").prop("value", keyword[i]);
        }
        ;
    }
    // 分類
    self.applyCheck(djangoObj.input_contents.category, "name_category");
    // ジャンル
    self.applyCheck(djangoObj.input_contents.core, "name_core");
    // 掲載媒体
    self.applyCheck(djangoObj.input_contents.media, "name_media");
    // 印象
    self.applyCheck(djangoObj.input_contents.imp, "name_imp");
    // 現実フラグ
    self.applyCheck(djangoObj.input_contents.fiction, "name_fiction_flag");
    // 事実メタ
    self.applyCheck(djangoObj.input_contents.fact_tag, "name_fact_tag");
    // 展開期間(開始)
    $('select[name="name_start_date"].date-year').val(djangoObj.input_contents.start_date[0] || '----')
    $('select[name="name_start_date"].date-month').val(djangoObj.input_contents.start_date[1] || '--')
    $('select[name="name_start_date"].date-day').val(djangoObj.input_contents.start_date[2] || '--')
    // 展開期間(終了)
    $('select[name="name_end_date"].date-year').val(djangoObj.input_contents.end_date[0] || '----')
    $('select[name="name_end_date"].date-month').val(djangoObj.input_contents.end_date[1] || '--')
    $('select[name="name_end_date"].date-day').val(djangoObj.input_contents.end_date[2] || '--')

}


// ユーザ入力情報をフォーム（チェックボックス/ラジオボタン）に反映する
SearchResultController.prototype.applyCheck = function(list, name) {
    $("input[name=" + name + "]").each(function(idx, val) {
        if (list.some(function(o) {
            return o == $(val).val()
        })) {
            $(val).prop('checked', true);
        }
    });
}

// キーワード検索の入力を追加する
SearchResultController.prototype.appendHtml = function() {
    var self = this;
    var html = self.createHtml();
    html.hide();
    $(".search-keyword-area .input-panel-body").append(html);
    return html;
}
SearchResultController.prototype.createHtml = function() {
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

// 検索結果エリアの描画を行う
SearchResultController.prototype.drawResult = function(search_result) {
    var self = this;

    $('#id_search_result_cnt').text("(" + djangoObj.search_result_cnt + "件)")

    search_result.forEach(function(obj, index, array) {
        // 分類
        var tag_category = ""
        if (obj.tag.category[0] == 'True') {
            tag_category += "<a class=\"tag anime\" href=\"/ipdds/search_result?name_category=0\" >アニメ</a>"
        }
        if (obj.tag.category[1] == 'True') {
            tag_category += "<a class=\"tag manga\" href=\"/ipdds/search_result?name_category=1\" >マンガ</a>"
        }
        if (obj.tag.category[2] == 'True') {
            tag_category += "<a class=\"tag app\" href=\"/ipdds/search_result?name_category=2\">アプリ</a>"
        }
        if (obj.tag.category[3] == 'True') {
            tag_category += "<a class=\"tag game\" href=\"/ipdds/search_result?name_category=3\">ゲーム</a>"
        }
        if (obj.tag.category[4] == 'True') {
            tag_category += "<a class=\"tag theater\" href=\"/ipdds/search_result?name_category=4\">劇場</a>"
        }
        // ジャンル
        var tag = ""
        obj.tag.core.forEach(function(obj, index, array) {
            tag += "<a class=\"tag "
            if (self.includes(djangoObj.input_contents.core, obj.code)) {
                tag += "matched"
            }
            tag += "\" href=\"/ipdds/search_result?name_core=" + obj.code + "\">" + obj.name + "</a>"
        })
        // 掲載媒体
        if (obj.tag.media.code != "" && obj.tag.media.name != "") {
            tag += "<a class=\"tag "
            if (self.includes(djangoObj.input_contents.media, obj.tag.media.code)) {
                tag += "matched"
            }
            tag += "\" href=\"/ipdds/search_result?name_media=" + obj.tag.media.code + "\">" + obj.tag.media.name + "</a>"
        }
        // 印象
        obj.tag.imp.forEach(function(obj, index, array) {
            tag += "<a class=\"tag "
            if (self.includes(djangoObj.input_contents.imp, obj.code)) {
                tag += "matched"
            }
            tag += "\" href=\"/ipdds/search_result?name_imp=" + obj.code + "\">" + obj.name + "</a>"
        });
        // 現実フラグ
        if (obj.tag.fiction_flag == "0") {
            tag += "<a class=\"tag "
            if (self.includes(djangoObj.input_contents.fiction, "0")) {
                tag += "matched"
            }
            tag += "\" href=\"/ipdds/search_result?name_fiction_flag=0\">現実的</a>"
        } else if (obj.tag.fiction_flag == "1") {
            tag += "<a class=\"tag "
            if (self.includes(djangoObj.input_contents.fiction, "1")) {
                tag += "matched"
            }
            tag += "\" href=\"/ipdds/search_result?name_fiction_flag=1\">非現実的</a>"
        }
        // 事実メタ
        var fact_tag = ""
        obj.tag.fact_tag.forEach(function(obj, index, array) {
            fact_tag += "<a class=\"tag "
            if (self.includes(djangoObj.input_contents.fact_tag, obj.code)) {
                fact_tag += "matched"
            }
            fact_tag += "\" href=\"/ipdds/search_result?name_fact_tag=" + obj.code + "\">" + obj.name + "</a>"
        });

        html = '<div class="description-area">' 
                + '<h5>' + obj.ip_name + '</h5>'
                + '<div class="description-area-left">'
                +   '<img onclick="window.location.href = \'/ipdds/detail?ip_code=' + obj.ip_code + '\'" onload="KeyVisualUtil.execute()" onerror="KeyVisualUtil.notFound()"'
                +   'src="/static/ipdds_app/image/keyvisual/' + obj.ip_code + '/' + obj.keyvisual_file_name + '" class="keyvisual" data-attention="true">'+ '</div>' 
                + '<div class="description-area-right">'
                + '    <div class="description-detail-category">'
                + '      <div class="category">' + tag_category + '</div>'+ '<div class="category">' + tag + '</div>'+ '<div class="category">' + fact_tag + '</div>'
                + '    </div>'
                + '    <div class="description-detail-button">'
                + '      <label class="compare-kago-add">'
                + '        <input type="checkbox" ip_name="'+obj.ip_name+'" keyvisual="'+obj.keyvisual_file_name+'" value="'+ obj.ip_code +'" class="compare-kago-checkbox">'
                + '        <span class="compare-kago-button-add">かごに入れる</span>'
                + '      </label>'
                + '      <a class="detail-button" href="/ipdds/detail?ip_code=' + obj.ip_code + '">詳細を見る</a >'
                + '    </div>'
                + '    <div style="width:100%;float:left">'
                + '      <div class="multiline-text">'+ StringUtil.coalesce(obj.overview, "not found OverView") + '</div>'
                + '    </div>'
                + '</div>'
                + '</div>'

        $('#id_redraw_area').append(html);

        
        //比較カゴに当IPが存在する場合、「比較カゴから戻す」ボタンを設定する
        if($("span#compare-" + obj.ip_code).length > 0 ){
            var checkbox = $("input[value=" + obj.ip_code + "]");
            if(checkbox.length>0){
                //「比較カゴから戻す」ボタンを設定する
                CompareKago.drawCompareButton(checkbox,true);
            }
        }
        
    });

    // セッションから比較かごデータを取得する
    CompareKago.getSessionData().done(function(data){
        // 比較かごIP領域を描画する
        $('.compare-kago-list-contents').empty();
        CompareKago.drawCompareIp(data);
    });
    //「比較カゴに入れる」ボタンのイベントを設定
    CompareKago.SetCompareDataAddOrDel();

    if (search_result.length == 0) {
        html = '<div style="width:400px;font-size:20px;margin:auto;margin-bottom:200px;">条件に該当するIPが存在しません</div>'
        $('#id_redraw_area').append(html);
    }
}

// ソートパターンを引数をもとにソート完了時に実行する描画処理の登録を行う
SearchResultController.prototype.draw = function(checkedVal) {
    var self = this;
    var dfd = $.Deferred();

    var targetResult = [];
    LoadingUtil.start('ソート中...', $('.ratio-4'));

    var exec = function(data) {
        LoadingUtil.stop(self.search_result);
        LoadingUtil.start('描画中...', $('.ratio-4'));
        setTimeout(function() {
            self.drawResult(data)
            LoadingUtil.stop(self.search_result);
            dfd.resolve();
        }, 500)
    }

    switch (checkedVal) {
    case '0':
        self.promiseSortByBookAvg.then(function() {
            exec(self.search_result_sorted_by_book_avg);
        })
        break;
    case '1':
        self.promiseSortByBookSum.then(function() {
            exec(self.search_result_sorted_by_book_sum);
        })
        break;
    case '2':
        self.promiseSortByUpdateNewer.then(function() {
            exec(self.search_result_sorted_by_update_newer);
        })
        break;
    case '3':
        self.promiseSortByReleaseNewer.then(function() {
            exec(self.search_result_sorted_by_release_newer);
        })
        break;
    case '4':
        self.promiseSortByReleaseOlder.then(function() {
            exec(self.search_result_sorted_by_release_older);
        })
        break;
    case '5':
        self.promiseSortBySimilarRate.then(function() {
            exec(self.search_result_sorted_by_similar_rate);
        })
        break;
    }

    return dfd;
}
// 各ソート処理を実行する
SearchResultController.prototype.sortAll = function() {
    var self = this;

    self.promiseSortByBookAvg = $.Deferred();
    self.promiseSortByBookSum = $.Deferred();
    self.promiseSortByUpdateNewer = $.Deferred();
    self.promiseSortByReleaseNewer = $.Deferred();
    self.promiseSortByReleaseOlder = $.Deferred();
    self.promiseSortBySimilarRate = $.Deferred();

    self.sortByBookAvg();
    self.sortByBookSum();
    self.sortByUpdateNewer();
    self.sortByReleaseNewer();
    self.sortByReleaseOlder();
    self.sortBySimilarRate();

}

// ソート処理：平均発行部数が多い順
SearchResultController.prototype.sortByBookAvg = function() {
    var self = this;
    self.search_result_sorted_by_book_avg = jQuery.extend(true, [], self.search_result_similar).sort(function(a, b) {
        if (!a.book_series[0].avg_per_volume && b.book_series[0].avg_per_volume)
            return 1;
        if (a.book_series[0].avg_per_volume && !b.book_series[0].avg_per_volume)
            return -1;
        if (a.book_series[0].avg_per_volume < b.book_series[0].avg_per_volume)
            return 1;
        if (a.book_series[0].avg_per_volume > b.book_series[0].avg_per_volume)
            return -1;
        if (a.ip_kana_name > b.ip_kana_name)
            return 1;
        if (a.ip_kana_name < b.ip_kana_name)
            return -1;
        return 0
    })
    self.search_result_sorted_by_book_avg = self.search_result_keyword.concat(self.search_result_sorted_by_book_avg)

    self.promiseSortByBookAvg.resolve();
}

// ソート処理：累計発行部数が多い順
SearchResultController.prototype.sortByBookSum = function() {
    var self = this;
    self.search_result_sorted_by_book_sum = jQuery.extend(true, [], self.search_result_similar).sort(function(a, b) {
        if (!a.book_series[0].qty_total_sales_2 && b.book_series[0].qty_total_sales_2)
            return 1;
        if (a.book_series[0].qty_total_sales_2 && !b.book_series[0].qty_total_sales_2)
            return -1;
        if (a.book_series[0].qty_total_sales_2 < b.book_series[0].qty_total_sales_2)
            return 1;
        if (a.book_series[0].qty_total_sales_2 > b.book_series[0].qty_total_sales_2)
            return -1;
        if (a.ip_kana_name > b.ip_kana_name)
            return 1;
        if (a.ip_kana_name < b.ip_kana_name)
            return -1;
        return 0
    })
    self.search_result_sorted_by_book_sum = self.search_result_keyword.concat(self.search_result_sorted_by_book_sum)

    self.promiseSortByBookSum.resolve();
}

// ソート処理：更新日付順
SearchResultController.prototype.sortByUpdateNewer = function() {
    var self = this;
    self.search_result_sorted_by_update_newer = jQuery.extend(true, [], self.search_result_similar).sort(function(a, b) {
        if (a.update_date < b.update_date)
            return 1;
        if (a.update_date > b.update_date)
            return -1;
        if (a.ip_kana_name > b.ip_kana_name)
            return 1;
        if (a.ip_kana_name < b.ip_kana_name)
            return -1;
        return 0
    })
    self.search_result_sorted_by_update_newer = self.search_result_keyword.concat(self.search_result_sorted_by_update_newer)

    self.promiseSortByUpdateNewer.resolve();
}

// ソート処理：連載開始が新しい順
SearchResultController.prototype.sortByReleaseNewer = function() {
    var self = this;
    self.search_result_sorted_by_release_newer = jQuery.extend(true, [], self.search_result_similar).sort(function(a, b) {
        if (a.release_date < b.release_date)
            return 1;
        if (a.release_date > b.release_date)
            return -1;
        if (a.ip_kana_name > b.ip_kana_name)
            return 1;
        if (a.ip_kana_name < b.ip_kana_name)
            return -1;
        return 0
    })
    self.search_result_sorted_by_release_newer = self.search_result_keyword.concat(self.search_result_sorted_by_release_newer)

    self.promiseSortByReleaseNewer.resolve();
}

// ソート処理：連載開始が古い順
SearchResultController.prototype.sortByReleaseOlder = function() {
    var self = this;

    self.search_result_sorted_by_release_older = jQuery.extend(true, [], self.search_result_similar).sort(function(a, b) {
        if (a.release_date > b.release_date)
            return 1;
        if (a.release_date < b.release_date)
            return -1;
        if (a.ip_kana_name > b.ip_kana_name)
            return 1;
        if (a.ip_kana_name < b.ip_kana_name)
            return -1;
        return 0
    })
    self.search_result_sorted_by_release_older = self.search_result_keyword.concat(self.search_result_sorted_by_release_older)

    self.promiseSortByReleaseOlder.resolve();
}

// ソート処理：タグ一致率順
SearchResultController.prototype.sortBySimilarRate = function() {
    var self = this;

    self.search_result_sorted_by_similar_rate = jQuery.extend(true, [], self.search_result_similar).sort(function(a, b) {
        if (a.similar_rate < b.similar_rate)
            return 1;
        if (a.similar_rate > b.similar_rate)
            return -1;
        if (a.ip_kana_name > b.ip_kana_name)
            return 1;
        if (a.ip_kana_name < b.ip_kana_name)
            return -1;
        return 0
    })
    self.search_result_sorted_by_similar_rate = self.search_result_keyword.concat(self.search_result_sorted_by_similar_rate)

    self.promiseSortBySimilarRate.resolve();
}

// リストに対象の要素が含まれているか判定
SearchResultController.prototype.includes = function(array, target) {
    var is_contains = false;
    array.forEach(function(obj, index, array) {
        if (obj == target) {
            is_contains = true;
        }
    })
    return is_contains;
}

$(function() {
    var controller = new SearchResultController();
    controller.init();
});
