var DetailController = function() {
};
DetailController.prototype = new AbstractController();

/**
 * 詳細画面の主処理
 */
DetailController.prototype.execute = function() {

    if (djangoObj.ip_not_found) {
        return $.Deferred().resolve().promise();
    }
    var self = this;

    self.colorArray = [ "#cddf54", "#fbd179", "#26B4E3", "#bd70c7" ];
    self.options = {
        seriesDefaults : {
            pointLabels : {
                show : true,
                formatString : "%'d"
            }
        },
        title : "",
        series : [ {
            label : '',
            color : self.colorArray[0]
        }, {
            label : '',
            color : self.colorArray[1]
        }, {
            label : '',
            color : self.colorArray[2]
        }, {
            label : '',
            color : self.colorArray[3]
        } ],
        legend : {
            show : true,
            placement : "outside",
            location : "s",
        },
        axes : {
            xaxis : {
                renderer : $.jqplot.DateAxisRenderer,
                tickRenderer : $.jqplot.CanvasAxisTickRenderer,
                tickInterval : "1 months",
                tickOptions : {
                    angle : -45,
                    formatString : "%Y/%m"
                },
                min : self.getOneYearAgo(),
                max : self.getNow()
            },
            yaxis : {
                min : 0,
                tickOptions: { formatString: "%'d" }
            }
        },
        cursor : {
            show : true,
            zoom : true,
            constrainZoomTo : "none",
            showTooltip : false
        },
        highlighter : {
            show : true,
            showMarker : true,
            sizeAdjust : 7,
            tooltipLocation : "ne",
            tooltipAxes : "y",
            formatString : "部数:%s"
        },
        height : 400
    };

    // 年代別男女比表
    self.drawGenderRatio();

    // 男女比グラフ
    self.plotGenderRatio();

    // セッションから比較かごデータを取得
    CompareKago.getSessionData().done(function(data){
        // 比較かごIP領域を描画する
        $('.compare-kago-list-contents').empty();
        CompareKago.drawCompareIp(data);
        //[比較カゴに入れる]/[比較カゴから戻す]ボタンを画面に表示する（初期表示時）
        if($('.compare-kago-add').length==1){
            $('.compare-kago-add').css('display','block');
        }else{
            $('.compare-kago-del').css('display','block');
        }
    });

    // 類似IP領域
    self.drawSimilarIp();

    // Twitterグラフ表示
    self.plotTwitterGraph();

    // マンガグラフ表示
    self.plotBookrGraph();

    // ゲームグラフ表示
    self.plotGameGraph();

    // アプリグラフ表示
    self.plotAppGraph();

    // 凡例がoutsideの場合、
    // 凡例の高さがグラフdivに含まれないため、
    // グラフdivの次の要素のdivとして凡例を置く
    var graph_list = [ "twiter-tweet-graph", "twiter-follower-graph", "book-graph", "game-graph", "app-graph-download", "app-graph-sales" ]
    graph_list.forEach(function(obj, idx, array) {
        var chartElement = $("#" + obj);
        var legendTable = chartElement.find("table.jqplot-table-legend");
        legendTable.css("position", "static");
        legendTable.css("margin", "0 auto");
        var legendWrapper = $(document.createElement("div"));
        legendWrapper.attr("id", obj + "-legend")
        legendTable.appendTo(legendWrapper);
        chartElement.after(legendWrapper);
    });
    $.jqplot.postDrawHooks.push(function() {
        var graph_id = this.targetId;
        var chartElement = $(graph_id);
        var legendTable = chartElement.find("table.jqplot-table-legend");
        legendTable.css("position", "static");
        legendTable.css("margin", "0 auto");
        var legendWrapper = $(graph_id + "-legend");
        legendWrapper.empty();
        legendTable.appendTo(legendWrapper);
    })

    return $.Deferred().resolve().promise();
}


/**
 * イベント登録処理
 */
DetailController.prototype.bindEvent = function () {
    //比較カゴ追加/削除ボタン 押下時のイベント
    CompareKago.SetCompareDataAddOrDel();
}

// 年代別男女比グラフ描画処理
DetailController.prototype.plotGenderRatio = function() {
    if (!djangoObj.ip_data.detail_indivisual_item.is_exist_gender_ratio) {
        return;
    }
    var obj = djangoObj.ip_data.detail_indivisual_item;
    var ticks = [ "51歳以上", "46歳~50歳", "41歳~45歳", "36歳~40歳", "31歳~35歳", "26歳~30歳", "21歳~25歳", "16歳~20歳", "11歳~15歳" ];
    var male = [ obj.male_gteq51, obj.male_46to50, obj.male_41to45, obj.male_36to40, obj.male_31to35, obj.male_26to30, obj.male_21to25, obj.male_16to20, obj.male_11to15 ];
    var female = [ obj.female_gteq51, obj.female_46to50, obj.female_41to45, obj.female_36to40, obj.female_31to35, obj.female_26to30, obj.female_21to25, obj.female_16to20, obj.female_11to15 ];
    var gender_options = {
        title : '<div style="float: left; width: 50%; text-align: center;">男性</div><div style="float: right; width: 50%; text-align: center;">女性</div>',
        seriesDefaults : {
            renderer : jQuery.jqplot.PyramidRenderer,
            rendererOptions : {
                barPadding : 10
            },
            shadow : false
        },
        series : [ {
            rendererOptions : {
                side : "left"
            }
        }, {
            yaxis : "y2axis"
        } ],
        grid : {
            drawBorder : true,
            shadow : false
        },
        axes : {
            xaxis : {
                label : "人数",
                rendererOptions : {
                    baselineWidth : 2
                },
                tickOptions: { formatString: "%'d" }
            },
            yaxis : {
                labelRenderer : jQuery.jqplot.CanvasAxisLabelRenderer,
                showMinorTicks : true,
                ticks : ticks,
                rendererOptions : {
                    category : true,
                    baselineWidth : 2
                }
            },
            y2axis : {
                labelRenderer : jQuery.jqplot.CanvasAxisLabelRenderer,
                showMinorTicks : true,
                ticks : ticks,
                rendererOptions : {
                    category : true,
                    baselineWidth : 2
                }
            }
        }
    }

    // データ最大値が3以下の場合目盛りがおかしくなるため
    var is_gt_3 = false;
    male.forEach(function(obj, index, array) {
        if (obj > 3) {
            is_gt_3 = true;
        }
    })
    female.forEach(function(obj, index, array) {
        if (obj > 3) {
            is_gt_3 = true;
        }
    })
    if(!is_gt_3){
        gender_options.axes.xaxis.padMin = 2.4;
        gender_options.axes.xaxis.padMax = 2.4;
    }else{
        delete gender_options.axes.xaxis.padMin;
        delete gender_options.axes.xaxis.padMax;
    }

    jQuery.jqplot("gender-ratio-graph", [ male, female ],gender_options );
    if (obj.total == 0){
        // 総人数が0の場合「データなし」マスク追加
        NoDateUtil.overlay('gender-ratio-graph')
    }
}

/**
 * 類似IP領域の描画
 */
DetailController.prototype.drawSimilarIp = function() {
    var self = this;
    djangoObj.similar_ip.forEach(function(obj, index, array) {
        var html = "";
        var tag = "";
        var code_list = [];
        djangoObj.ip_data.tag.fact_tag.forEach(function(obj, index, array) {
            code_list.push(obj.code)
        });
        if (obj.fact_tag_code1 != '' && obj.fact_tag_name1 != '') {
            tag += '<a class="tag ';
            if (self.includes(code_list, obj.fact_tag_code1)) {
                tag += 'matched';
            }
            tag += '" href="/ipdds/search_result?name_fact_tag=' + obj.fact_tag_code1 + '">' + obj.fact_tag_name1 + '</a>';
        }
        if (obj.fact_tag_code2 != '' && obj.fact_tag_name2 != '') {
            tag += '<a class="tag ';
            if (self.includes(code_list, obj.fact_tag_code2)) {
                tag += 'matched';
            }
            tag += '" href="/ipdds/search_result?name_fact_tag=' + obj.fact_tag_code2 + '">' + obj.fact_tag_name2 + '</a>';
        }
        if (obj.fact_tag_code3 != '' && obj.fact_tag_name3 != '') {
            tag += '<a class="tag ';
            if (self.includes(code_list, obj.fact_tag_code3)) {
                tag += 'matched';
            }
            tag += '" href="/ipdds/search_result?name_fact_tag=' + obj.fact_tag_code3 + '">' + obj.fact_tag_name3 + '</a>';
        }
        if (obj.fact_tag_code4 != '' && obj.fact_tag_name4 != '') {
            tag += '<a class="tag ';
            if (self.includes(code_list, obj.fact_tag_code4)) {
                tag += 'matched';
            }
            tag += '" href="/ipdds/search_result?name_fact_tag=' + obj.fact_tag_code4 + '">' + obj.fact_tag_name4 + '</a>';
        }
        if (obj.fact_tag_code5 != '' && obj.fact_tag_name5 != '') {
            tag += '<a class="tag ';
            if (self.includes(code_list, obj.fact_tag_code5)) {
                tag += 'matched';
            }
            tag += '" href="/ipdds/search_result?name_fact_tag=' + obj.fact_tag_code5 + '">' + obj.fact_tag_name5 + '</a>';
        }
        html = '<div class="similar-ip">' + '<a class="link" href="/ipdds/detail?ip_code=' + obj.ip_code + '">' + obj.ip_name + '</a>' + '<div class="category">' + tag + '</div>' + '</div>'
        $('.similar-ip-list').append(html);
    });
}

/**
 * メニュー選択処理
 */
DetailController.prototype.selectedMenu = function() {
    return '.link-tab > .ip';
};

// Twitterグラフ描画処理
DetailController.prototype.plotTwitterGraph = function() {
    var self = this;
    var copiedOptions = jQuery.extend(true, {}, self.options);
    copiedOptions.title = "フォロワー数";
    copiedOptions.highlighter = {
        show : true,
        showMarker : true,
        sizeAdjust : 7,
        tooltipLocation : "ne",
        tooltipAxes : "y",
        formatString : "フォロワー数:%s"
    };
    if (!djangoObj.twitter_graph_data.length) {
        return;
    }
    var data1 = self.convertGraphData(djangoObj.twitter_graph_data);
    copiedOptions.series = [];
    copiedOptions.series.push({
        label : djangoObj.ip_data.detail_indivisual_item.twitter_account_name,
        color : self.colorArray[0]
    });
    $.jqplot("twiter-follower-graph", [ data1 ], copiedOptions);
}

// マンガグラフ描画処理
DetailController.prototype.plotBookrGraph = function() {
    var self = this;
    var copiedOptions = jQuery.extend(true, {}, self.options);
    copiedOptions.title = "累計発行部数";
    var data = [];
    var label = [];
    // 初刊
    if (djangoObj.manga_first_graph_data.length) {
        var convertedData = self.convertGraphData(djangoObj.manga_first_graph_data);
        if (convertedData.length > 0) {
            data.push(convertedData);
            label.push(djangoObj.ip_data.book_volume[0].book_name);
        }
    }
    // 最新巻
    if (djangoObj.manga_latest_graph_data.length) {
        var convertedData = self.convertGraphData(djangoObj.manga_latest_graph_data);
        if (convertedData.length > 0) {
            data.push(convertedData);
            label.push(djangoObj.ip_data.book_volume[1].book_name);
        }
    }
    if (!data.length) {
        return;
    }
    copiedOptions.series = [];
    for (var i = 0; i < label.length; i++) {
        copiedOptions.series.push({
            label : label[i],
            color : self.colorArray[i]
        });
    }
    $.jqplot("book-graph", data, copiedOptions);
}

// ゲームグラフ描画処理
DetailController.prototype.plotGameGraph = function() {
    var self = this;
    var copiedOptions = jQuery.extend(true, {}, self.options);
    if (!djangoObj.game_area.length) {
        return;
    }
    var data = [];
    var label = [];
    copiedOptions.title = "累計売上本数";
    copiedOptions.highlighter = {
        show : true,
        showMarker : true,
        sizeAdjust : 7,
        tooltipLocation : "ne",
        tooltipAxes : "y",
        formatString : "本数:%s"
    };
    copiedOptions.series = [];
    djangoObj.game_area.forEach(function(obj, index, array) {
        var convertedData = self.convertGraphData(obj.game_graph_data);
        if (convertedData == 0) {
            return;
        }
        label.push(obj.game_data.pkg_soft_name);
        data.push(convertedData);
    });
    copiedOptions.series = [];
    for (var i = 0; i < label.length; i++) {
        copiedOptions.series.push({
            label : label[i],
            color : self.colorArray[i]
        });
    }
    if (data.length) {
        $.jqplot("game-graph", data, copiedOptions);
    }

}
// アプリグラフ描画処理
DetailController.prototype.plotAppGraph = function() {
    var self = this;
    var copiedOptions = jQuery.extend(true, {}, self.options);
    if (!djangoObj.app_area.length) {
        return;
    }
    copiedOptions.title = "ダウンロード数";
    copiedOptions.highlighter = {
        show : true,
        showMarker : true,
        sizeAdjust : 7,
        tooltipLocation : "ne",
        tooltipAxes : "y",
        formatString : "ダウンロード数:%s"
    };
    var data1 = [];
    var label1 = [];
    djangoObj.app_area.forEach(function(obj, index, array) {
        var convertedData = self.convertGraphData(obj.app_download_count_graph_data)
        if (convertedData == 0) {
            return;
        }
        label1.push(obj.app_data.app_name);
        data1.push(convertedData);
    });
    copiedOptions.series = [];
    for (var i = 0; i < label1.length; i++) {
        copiedOptions.series.push({
            label : label1[i],
            color : self.colorArray[i]
        });
    }
    if (data1.length) {
        $.jqplot("app-graph-download", data1, copiedOptions);
    }

    copiedOptions = jQuery.extend(true, {}, self.options);
    copiedOptions.title = "収益";
    copiedOptions.highlighter = {
        show : true,
        showMarker : true,
        sizeAdjust : 7,
        tooltipLocation : "ne",
        tooltipAxes : "y",
        formatString : "月商:%s"
    };
    var data2 = [];
    var label2 = [];
    djangoObj.app_area.forEach(function(obj, index, array) {
        var convertedData = self.convertGraphData(obj.app_monthly_sales_graph_data);
        if (convertedData == 0) {
            return;
        }
        label2.push(obj.app_data.app_name);
        data2.push(convertedData);
    });
    copiedOptions.series = [];
    for (var i = 0; i < label2.length; i++) {
        copiedOptions.series.push({
            label : label2[i],
            color : self.colorArray[i]
        });
    }
    if (data2.length) {
        $.jqplot("app-graph-sales", data2, copiedOptions);
    }

}
// 年代別男女比の表を表示する
DetailController.prototype.drawGenderRatio = function(checkedVal) {

    var self = this;
    var obj = djangoObj.ip_data.detail_indivisual_item;
    var total = obj.total
    if (total == null) {
        var total = '-'
    } else {
        var total = total.toString().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,");
    }

    var gender_ratio_table = '        <table class="ipdds-table gender">' + '        <tr>' + '            <td>年代</td>' + '            <td>男性(%)</td>' + '            <td>女性(%)</td>' + '        </tr>'
            + '        <tr>'
            + '            <td>11歳～15歳</td>'
            + '            <td>'
            + self.calcGenderPercentage(obj.male_11to15, obj.female_11to15)
            + '</td>'
            + '            <td>'
            + self.calcGenderPercentage(obj.female_11to15, obj.male_11to15)
            + '</td>'
            + '        </tr>'
            + '        <tr>'
            + '            <td>16歳～20歳</td>'
            + '            <td>'
            + self.calcGenderPercentage(obj.male_16to20, obj.female_16to20)
            + '</td>'
            + '            <td>'
            + self.calcGenderPercentage(obj.female_16to20, obj.male_16to20)
            + '</td>'
            + '        </tr>'
            + '        <tr>'
            + '            <td>21歳～25歳</td>'
            + '            <td>'
            + self.calcGenderPercentage(obj.male_21to25, obj.female_21to25)
            + '</td>'
            + '            <td>'
            + self.calcGenderPercentage(obj.female_21to25, obj.male_21to25)
            + '</td>'
            + '        </tr>'
            + '        <tr>'
            + '            <td>26歳～30歳</td>'
            + '            <td>'
            + self.calcGenderPercentage(obj.male_26to30, obj.female_26to30)
            + '</td>'
            + '            <td>'
            + self.calcGenderPercentage(obj.female_26to30, obj.male_26to30)
            + '</td>'
            + '        </tr>'
            + '        <tr>'
            + '            <td>31歳～35歳</td>'
            + '            <td>'
            + self.calcGenderPercentage(obj.male_31to35, obj.female_31to35)
            + '</td>'
            + '            <td>'
            + self.calcGenderPercentage(obj.female_31to35, obj.male_31to35)
            + '</td>'
            + '        </tr>'
            + '        <tr>'
            + '            <td>36歳～40歳</td>'
            + '            <td>'
            + self.calcGenderPercentage(obj.male_36to40, obj.female_36to40)
            + '</td>'
            + '            <td>'
            + self.calcGenderPercentage(obj.female_36to40, obj.male_36to40)
            + '</td>'
            + '        </tr>'
            + '        <tr>'
            + '            <td>41歳～45歳</td>'
            + '            <td>'
            + self.calcGenderPercentage(obj.male_41to45, obj.female_41to45)
            + '</td>'
            + '            <td>'
            + self.calcGenderPercentage(obj.female_41to45, obj.male_41to45)
            + '</td>'
            + '        </tr>'
            + '        <tr>'
            + '            <td>46歳～50歳</td>'
            + '            <td>'
            + self.calcGenderPercentage(obj.male_46to50, obj.female_46to50)
            + '</td>'
            + '            <td>'
            + self.calcGenderPercentage(obj.female_46to50, obj.male_46to50)
            + '</td>'
            + '        </tr>'
            + '        <tr>'
            + '            <td>51歳以上</td>'
            + '            <td>'
            + self.calcGenderPercentage(obj.male_gteq51, obj.female_gteq51)
            + '</td>'
            + '            <td>'
            + self.calcGenderPercentage(obj.female_gteq51, obj.male_gteq51)
            + '</td>'
            + '        </tr>'
            + '    </table>'
            + '    <p class="total">'
            + '        【総人数:<span class="total-data">'
            + total
            + '</span>】' + '    </p>'
    $('.gender-ratio-table').append(gender_ratio_table);
}
// 年代別男女比のパーセンテージを計算する
DetailController.prototype.calcGenderPercentage = function(val1, val2) {
    if (val1 == null || val2 == null || val1 + val2 == 0 ) {
        return "-";
    }
    return Math.round((val1 / (val1 + val2) * 100)) + "%";
}
// 現在から１年前を取得（例：現在＝2019/08/27 ⇒ 戻り値＝ "2018-08-01"）
DetailController.prototype.getOneYearAgo = function() {
    var dt = new Date();
    dt.setDate(1);
    dt.setFullYear(dt.getFullYear() - 1);
    dt.setMonth(dt.getMonth() - 1);
    return dt.getFullYear() + '-' + StringUtil.lpad(dt.getMonth()+1, 2) + '-' + StringUtil.lpad(dt.getDate(), 2)
}
// 現在を取得（例：現在＝2019/08/27 ⇒ 戻り値＝ "2019-08-01"）
DetailController.prototype.getNow = function() {
    var dt = new Date();
    dt.setDate(1);
    // dt.setMonth(dt.getMonth() + 1);
    return dt.getFullYear() + '-' + StringUtil.lpad(dt.getMonth()+1, 2) + '-' + StringUtil.lpad(dt.getDate(), 2);
}
// jqplotグラフ用データに変換(連想配列⇒リスト)
DetailController.prototype.convertGraphData = function(dataFromDjngo) {
    var data = [];
    dataFromDjngo.forEach(function(obj, index, array) {
        if (obj.num) {
            data.push([ obj.yyyymm, obj.num ]);
        }
    });
    return data;
}
// リストに対象の要素が含まれているか判定
DetailController.prototype.includes = function(array, target) {
    var is_contains = false;
    array.forEach(function(obj, index, array) {
        if (obj == target) {
            is_contains = true;
        }
    })
    return is_contains;
}

var NoDateUtil = {
    overlay : function(id) {
        var $elem = $('#' + id);
        var width = $elem.width();
        var height = $elem.height();
        var top = 0;
        var mask = $('<div class="mask" style="width:' + width + "px;height:" + height + "px;top:" + top + 'px;"oncontextmenu="return false;"></div>');
        var caption = $('<div class="caption" style="width:' + width + "px;height:" + height + 'px;"oncontextmenu="return false;">データなし</div>');
        mask.append(caption);
        $elem.append(mask);
    }
}

$(function() {
    var controller = new DetailController();
    controller.init();
});