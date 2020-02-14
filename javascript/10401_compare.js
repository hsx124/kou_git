<<<<<<< HEAD:web/web-front/ipdds/ipdds_app/static/ipdds_app/javascript/04_compare.js
var CompareController = function() {

    // 年代別男女比グラフのオプション
    this.genderRatioGraphOption = {
        title : '<div style="float: left; width: 50%; text-align: center;">男性</div><div style="float: right; width: 50%; text-align: center;">女性</div>',
        seriesDefaults : {
            renderer : jQuery.jqplot.PyramidRenderer,
            rendererOptions : {
                barPadding : 15
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
                tickOptions : {
                    formatString : "%'d"
                }
            },
            yaxis : {
                labelRenderer : jQuery.jqplot.CanvasAxisLabelRenderer,
                showMinorTicks : true,
                ticks : [ "51歳以上", "46歳~50歳", "41歳~45歳", "36歳~40歳", "31歳~35歳", "26歳~30歳", "21歳~25歳", "16歳~20歳", "11歳~15歳" ],
                rendererOptions : {
                    category : true,
                    baselineWidth : 2
                }
            },
            y2axis : {
                labelRenderer : jQuery.jqplot.CanvasAxisLabelRenderer,
                showMinorTicks : true,
                ticks : [ "51歳以上", "46歳~50歳", "41歳~45歳", "36歳~40歳", "31歳~35歳", "26歳~30歳", "21歳~25歳", "16歳~20歳", "11歳~15歳" ],
                rendererOptions : {
                    category : true,
                    baselineWidth : 2
                }
            }
        },
        height : 380,
        cursor : {
            zoom : false,
            showTooltip : true
        }
    };

    // Twitterグラフのオプション
    this.commonOptions = {
        colorArray : [ "#cddf54", "#fbd179", "#26B4E3", "#bd70c7" ],
        option : {
            seriesDefaults : {
                pointLabels : {
                    show : true,
                    formatString : "%'d"
                }
            },
            title : "フォロワー数",
            legend : {
                show : true,
                placement : "outsideGrid",
                location : "nw"
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
                    min : (function() {
                        var dt = new Date();
                        dt.setDate(1);
                        dt.setFullYear(dt.getFullYear() - 1);
                        dt.setMonth(dt.getMonth() - 1);
                        return dt.getFullYear() + '-' + StringUtil.lpad(dt.getMonth()+1, 2) + '-' + StringUtil.lpad(dt.getDate(), 2)
                    }()),
                    max : (function() {
                        var dt = new Date();
                        dt.setDate(1);
                        // dt.setMonth(dt.getMonth());
                        return dt.getFullYear() + '-' + StringUtil.lpad(dt.getMonth()+1, 2) + '-' + StringUtil.lpad(dt.getDate(), 2);
                    }()),

                },
                yaxis : {
                    min : 0,
                    tickOptions : {
                        formatString : "%'d"
                    }
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
            }
        }
    };

};
CompareController.prototype = new AbstractController();

/**
 * メニュー選択処理
 */
CompareController.prototype.selectedMenu = function() {
    return '.compare';
};

/**
 * 比較画面の主処理
 */
CompareController.prototype.execute = function() {
    if (djangoObj.ip_not_found) {
        return $.Deferred().resolve().promise();
    }
    if (djangoObj.no_session_data) {
        return $.Deferred().resolve().promise();
    }

    var self = this;

    // 表を描画する
    self.drawGrid();

    // "Nか月目"グラフの最初と最後のtickを削除するhookを登録
    $.jqplot.postDrawHooks.push(function() {
        var graph_id = this.targetId;
        var nthArray = [ '#book-graph1', '#book-graph2', '#game-graph1', '#app-graph-sales1', '#app-graph-download1' ]
        if (self.includes(nthArray, graph_id)) {
            $(graph_id + " .jqplot-xaxis .jqplot-xaxis-tick:first-child").remove();
            $(graph_id + " .jqplot-xaxis .jqplot-xaxis-tick:last-child").remove();
        }
    })

    // 男女比グラフ
    self.plotGenderRatio();

    // Twitterグラフ表示
    self.plotTwitterGraph();

    // マンガグラフ表示
    self.plotBookGraph();

    // ゲームグラフ表示
    self.plotGameGraph();

    // アプリグラフ表示
    self.plotAppGraph();

    $(".link").click(function() {
        window.location.href = "./03_ip_detail.html";
    });

    return $.Deferred().resolve().promise();
};

CompareController.prototype.plotGenderRatio = function() {
    var self = this;
    djangoObj.gender_ratio.forEach(function(obj, index) {
        var param = {
            'gender-ratio' : index,
            'ip-code' : obj.ip_code
        };
        AjaxUtil.get('/ipdds/compare', param, function(data) {
            self.callbackGenderRatio(data, self.genderRatioGraphOption, index, obj.total);
        })
    });
}

CompareController.prototype.callbackGenderRatio = function(data, options, index, total) {
    var self = this;
    var result = JSON.parse(data.toString());
    var male = result[0].slice(0, 9);
    var female = result[0].slice(9);
    var target = "gender-ratio-graph" + (index + 1);

    // データ最大値が3以下の場合目盛りがおかしくなるため
    if (self.isGt3(male) || self.isGt3(female)) {
        options.axes.xaxis.padMin = 2;
        options.axes.xaxis.padMax = 2;
    } else {
        delete options.axes.xaxis.padMin;
        delete options.axes.xaxis.padMax;
    }
    // グラフを描画する
    jQuery.jqplot(target, [ male, female ], options);
    $('#' + target).dblclick(function(e) {
        e.stopPropagation();
    });

    // データが０件の場合、グラフに「データなし」Maskを追加する
    if (total == 0) {
        NoDateUtil.overlay('gender-ratio-graph' + (index + 1));
    }
};

CompareController.prototype.isGt3 = function(data) {
    // データ最大値が3以下の場合目盛りがおかしくなるため
    var is_gt_3 = true;
    data.forEach(function(obj) {
        if (obj > 3) {
            is_gt_3 = false;
        }
    })
    return is_gt_3;
}

CompareController.prototype.twitterGraphInfo = [ {
    options : {
        title : 'フォロワー数'
    }
} ];

CompareController.prototype.plotTwitterGraph = function() {
    var self = this;
    // options定義
    var copiedOptions = jQuery.extend(true, {}, self.commonOptions.option);
    copiedOptions.highlighter = {
        show : true,
        showMarker : true,
        sizeAdjust : 7,
        tooltipLocation : "ne",
        tooltipAxes : "y",
        formatString : "フォロワー数:%s"
    }

    // グラフのラベル定義
    var series = [];
    var series2 = [];
    var data2 = [];
    var promiseArr = [];
    djangoObj.twitter.forEach(function(obj, index) {
        // IpCodeごとにTwitterのデータ取得
        promiseArr.push(self.getTwitterGraphData(obj.twitter_id, obj.ip_name));
    });

    // IpCodeごとのデータを取得後にグラフ１及びグラフ２を描画する
    $.when.apply($, promiseArr).then(function() {
        var values = Array.prototype.slice.call(arguments);
        var graphTwitterData = [];
        var twiter_user;
        var twiter_user_index;
        values.forEach(function(val, i) {
            if (val) {
                series2.push({
                    label : val[1],
                    color : self.commonOptions.colorArray[i]
                });
                data2.push(val[0]);

                var selector1 = '.twitter-graph-checkbox';
                var selector2 = 'input[value="' + val[1] + '"]';

                if ($(selector1).filter(selector2).is(':checked')) {
                    graphTwitterData.push(val[0]);
                    // グラフのラベルを設定
                    series.push({
                        label : val[1],
                        color : self.commonOptions.colorArray[i]
                    });
                }
            }
        });

        // グラフのラベルを設定
        copiedOptions.series = series;
        copiedOptions.series2 = series2;
        copiedOptions.data2 = data2;
        // Twitterのグラフを描画
        self.createGraph("twiter-follower-graph", self.twitterGraphInfo, 0, graphTwitterData, copiedOptions);

        $('#twiter-follower-graph').dblclick(function(e) {
            e.stopPropagation();
        });
    });

    // 再描画のイベントを設定
    self.bindReplot('twitter-replot-button', 'twitter-graph-checkbox', self.twitterGraphInfo);
}

CompareController.prototype.getTwitterGraphData = function(twitter_id, ip_name) {
    var dtd = $.Deferred();
    var param = {
        'twitter' : 'twitter',
        'twitter_id' : twitter_id
    };
    AjaxUtil.get('/ipdds/compare', param, function(data) {
        var result = JSON.parse(data.toString());
        if (result.length != 0) {
            // グラフ１データ
            var graphTwitterData = [];
            result.forEach(function(val) {
                graphTwitterData.push([ val[0], val[1] ]);
            });
            dtd.resolve([ graphTwitterData, ip_name ]);
        } else {
            dtd.resolve(null);
        }
    })
    return dtd;
}

CompareController.prototype.bookGraphInfo = [ {
    options : {
        title : '累計発行部数（発売日からNか月）'
    }
}, {
    options : {
        title : '平均発行部数（単巻あたり）(発売日からNか月）'
    }
}, {
    options : {
        title : '累計発行部数'
    }
}, {
    options : {
        title : '累計発行部数（１巻）'
    }
}, {
    options : {
        title : '累計発行部数（最新巻）'
    }
}, {
    options : {
        title : '平均発行部数（単巻あたり）'
    }
} ];

CompareController.prototype.plotBookGraph = function() {
    var self = this;

    // 累計発行部数(発売日からNか月）
    self.plotBookGraph1();
    // 平均発行部数（単巻あたり）(発売日からNか月）
    self.plotBookGraph2();
    // 累計発行部数
    self.plotBookGraph3();
    // 平均発行部数（単巻あたり）
    self.plotBookGraph6();
    // 累計発行部数（１巻）
    self.plotBookGraph4();
    // 累計発行部数（最新巻）
    self.plotBookGraph5();

    // 再描画のイベントを設定
    self.bindReplot('book-replot-button', 'book-graph-checkbox', self.bookGraphInfo);
}

CompareController.prototype.plotBookGraph1 = function() {
    var self = this;

    // Options定義
    var copiedOptions = jQuery.extend(true, {}, self.commonOptions.option);
    copiedOptions.axes = {
        xaxis : {
            renderer : $.jqplot.DateAxisRenderer,
            tickRenderer : $.jqplot.CanvasAxisTickRenderer,
            tickInterval : "1 months",
            tickOptions : {
                angle : -45,
                formatString : "%#mヵ月目"
            },
            min : '1999-12-01',
            max : '2001-01-01'
        },
        yaxis : {
            min : 0,
            tickOptions : {
                formatString : "%'d"
            }
        }
    };

    // グラフのラベル定義
    var series = [];
    var series2 = [];
    var data2 = [];
    // ajaxから返却したデータ
    var promiseArr = [];
    djangoObj.book.forEach(function(obj, index) {
        // IpCodeごとにデータ取得
        promiseArr.push(self.getGraph1_2Data(obj.ip_code, obj.ip_name));
    });

    // IpCodeごとのデータを取得後にグラフ１及びグラフ２を描画する
    $.when.apply($, promiseArr).then(function() {
        var values = Array.prototype.slice.call(arguments);
        var graph1Data = [];
        values.forEach(function(val, i) {
            if (val) {
                series2.push({
                    label : val[2],
                    color : self.commonOptions.colorArray[i]
                });
                val[0].map(function(e, i) {
                    e[0] = '2000-' + StringUtil.lpad((i + 1), 2) + '-01';
                });
                data2.push(val[0]);
                var selector1 = '.book-graph-checkbox';
                var selector2 = 'input[value="' + val[2] + '"]';

                if ($(selector1).filter(selector2).is(':checked')) {
                    val[0].map(function(e, i) {
                        e[0] = '2000-' + StringUtil.lpad((i + 1), 2) + '-01';
                    });
                    graph1Data.push(val[0]);
                    // グラフのラベルを設定
                    series.push({
                        label : val[2],
                        color : self.commonOptions.colorArray[i]
                    });
                }
            }
        });

        // グラフのラベルを設定
        copiedOptions.series = series;
        copiedOptions.series2 = series2;
        copiedOptions.data2 = data2;
        // グラフ1（累計発行部数(発売日からNか月））を描画
        self.createGraph("book-graph1", self.bookGraphInfo, 0, graph1Data, copiedOptions);
    })
}

CompareController.prototype.plotBookGraph2 = function() {
    var self = this;

    // Options定義
    var copiedOptions = jQuery.extend(true, {}, self.commonOptions.option);
    copiedOptions.axes = {
        xaxis : {
            renderer : $.jqplot.DateAxisRenderer,
            tickRenderer : $.jqplot.CanvasAxisTickRenderer,
            tickInterval : "1 months",
            tickOptions : {
                angle : -45,
                formatString : "%#mヵ月目"
            },
            min : '1999-12-01',
            max : '2001-01-01'
        },
        yaxis : {
            min : 0,
            tickOptions : {
                formatString : "%'d"
            }
        }
    };

    // グラフのラベル定義
    var series = [];
    var series2 = [];
    var data2 = [];
    // ajaxから返却したデータ
    var promiseArr = [];
    djangoObj.book.forEach(function(obj, index) {
        // IpCodeごとにデータ取得
        promiseArr.push(self.getGraph1_2Data(obj.ip_code, obj.ip_name));
    });

    // IpCodeごとのデータを取得後にグラフ１及びグラフ２を描画する
    $.when.apply($, promiseArr).then(function() {
        var values = Array.prototype.slice.call(arguments);
        var graph2Data = [];
        values.forEach(function(val, i) {
            if (val) {
                series2.push({
                    label : val[2],
                    color : self.commonOptions.colorArray[i]
                });
                val[1].map(function(e, i) {
                    e[0] = '2000-' + StringUtil.lpad((i + 1), 2) + '-01';
                });
                data2.push(val[1]);
                var selector1 = '.book-graph-checkbox';
                var selector2 = 'input[value="' + val[2] + '"]';

                if ($(selector1).filter(selector2).is(':checked')) {
                    val[1].map(function(e, i) {
                        e[0] = '2000-' + StringUtil.lpad((i + 1), 2) + '-01';
                    });
                    graph2Data.push(val[1]);
                    // グラフのラベルを設定
                    series.push({
                        label : val[2],
                        color : self.commonOptions.colorArray[i]
                    });
                }
            }
        });

        // グラフのラベルを設定
        copiedOptions.series = series;
        copiedOptions.series2 = series2;
        copiedOptions.data2 = data2;
        // グラフ１（累計発行部数(発売日からNか月））を描画
        self.createGraph("book-graph2", self.bookGraphInfo, 1, graph2Data, copiedOptions);
    });
}

CompareController.prototype.getGraph1_2Data = function(ip_code, ip_name) {
    var dtd = $.Deferred();
    var param = {
        'book1' : 'book1',
        'book_id' : ip_code
    };
    AjaxUtil.get('/ipdds/compare', param, function(data) {
        var result = JSON.parse(data.toString());
        if (result.length != 0) {
            // グラフ１データ
            var graph1Data = [];
            // グラフ２データ
            var graph2Data = [];
            result.forEach(function(val) {
                graph1Data.push([ val[0], val[1] ]);
                graph2Data.push([ val[0], val[2] ]);
            });
            dtd.resolve([ graph1Data, graph2Data, ip_name ]);
        } else {
            dtd.resolve(null);
        }
    })
    return dtd;
}

CompareController.prototype.plotBookGraph3 = function() {
    var self = this;
    // Options定義
    var copiedOptions = jQuery.extend(true, {}, self.commonOptions.option);

    // グラフのラベル定義
    var series = [];
    var series2 = [];
    var data2 = [];
    var promiseArr = [];
    djangoObj.book.forEach(function(obj, index) {
        // IpCodeごとに累計発行部数と平均発行部数（単巻あたり）のデータ取得
        promiseArr.push(self.getGraph3_6Data(obj.ip_code, obj.ip_name));
    });

    // IpCodeごとのデータを取得後にグラフを描画する
    $.when.apply($, promiseArr).then(function() {
        var values = Array.prototype.slice.call(arguments);
        var graph3Data = [];
        values.forEach(function(val, i) {
            if (val) {
                series2.push({
                    label : val[2],
                    color : self.commonOptions.colorArray[i]
                });
                data2.push(val[0]);

                var selector1 = '.book-graph-checkbox';
                var selector2 = 'input[value="' + val[2] + '"]';

                if ($(selector1).filter(selector2).is(':checked')) {
                    graph3Data.push(val[0]);
                    // グラフのラベルを設定
                    series.push({
                        label : val[2],
                        color : self.commonOptions.colorArray[i]
                    });
                }
            }
        });

        // グラフのラベルを設定
        copiedOptions.series = series;
        copiedOptions.series2 = series2;
        copiedOptions.data2 = data2;
        // グラフ（累計発行部数(直近一年））を描画
        self.createGraph("book-graph3", self.bookGraphInfo, 2, graph3Data, copiedOptions);
    })
}

CompareController.prototype.plotBookGraph6 = function() {
    var self = this;
    // Options定義
    var copiedOptions = jQuery.extend(true, {}, self.commonOptions.option);

    // グラフのラベル定義
    var series = [];
    var series2 = [];
    var data2 = [];
    var promiseArr = [];
    djangoObj.book.forEach(function(obj, index) {
        // IpCodeごとに累計発行部数と平均発行部数（単巻あたり）のデータ取得
        promiseArr.push(self.getGraph3_6Data(obj.ip_code, obj.ip_name));
    });

    // IpCodeごとのデータを取得後にグラフを描画する
    $.when.apply($, promiseArr).then(function() {
        var values = Array.prototype.slice.call(arguments);
        var graph6Data = [];
        values.forEach(function(val, i) {
            if (val) {
                series2.push({
                    label : val[2],
                    color : self.commonOptions.colorArray[i]
                });
                data2.push(val[1]);

                var selector1 = '.book-graph-checkbox';
                var selector2 = 'input[value="' + val[2] + '"]';

                if ($(selector1).filter(selector2).is(':checked')) {
                    graph6Data.push(val[1]);
                    // グラフのラベルを設定
                    series.push({
                        label : val[2],
                        color : self.commonOptions.colorArray[i]
                    });
                }
            }
        });

        // グラフのラベルを設定
        copiedOptions.series = series;
        copiedOptions.series2 = series2;
        copiedOptions.data2 = data2;
        // グラフ（平均発行部数（単巻あたり）(直近一年））を描画
        self.createGraph("book-graph6", self.bookGraphInfo, 5, graph6Data, copiedOptions);
    })
}

CompareController.prototype.getGraph3_6Data = function(ip_code, ip_name) {
    var dtd = $.Deferred();
    var param = {
        'book3' : 'book3',
        'book_id' : ip_code
    };
    AjaxUtil.get('/ipdds/compare', param, function(data) {
        var result = JSON.parse(data.toString());
        if (result.length != 0) {
            // グラフ（累計発行部数）データ
            var graph3Data = [];
            // グラフ（平均発行部数（単巻あたり））データ
            var graph6Data = [];
            result.forEach(function(val) {
                graph3Data.push([ val[0], val[1] ]);
                graph6Data.push([ val[0], val[2] ]);
            });
            dtd.resolve([ graph3Data, graph6Data, ip_name ]);
        } else {
            dtd.resolve(null);
        }
    })
    return dtd;
}

CompareController.prototype.plotBookGraph4 = function() {
    var self = this;
    // Options定義
    var copiedOptions = jQuery.extend(true, {}, self.commonOptions.option);

    // グラフのラベル定義
    var series = [];
    var series2 = [];
    var data2 = [];
    var promiseArr = [];
    djangoObj.book.forEach(function(obj, index) {
        // IpCodeごとに累計発行部数(1巻）のデータ取得
        promiseArr.push(self.getGraph4Data(obj.ip_code, obj.ip_name));
    });

    // IpCodeごとのデータを取得後に累計発行部数(1巻）グラフを描画する
    $.when.apply($, promiseArr).then(function() {
        var values = Array.prototype.slice.call(arguments);
        var graph4Data = [];
        values.forEach(function(val, i) {
            if (val) {
                series2.push({
                    label : val[1],
                    color : self.commonOptions.colorArray[i]
                });
                data2.push(val[0]);

                var selector1 = '.book-graph-checkbox';
                var selector2 = 'input[value="' + val[1] + '"]';

                if ($(selector1).filter(selector2).is(':checked')) {
                    graph4Data.push(val[0]);
                    // グラフのラベルを設定
                    series.push({
                        label : val[1],
                        color : self.commonOptions.colorArray[i]
                    });
                }
            }
        });

        // グラフのラベルを設定
        copiedOptions.series = series;
        copiedOptions.series2 = series2;
        copiedOptions.data2 = data2;
        self.createGraph("book-graph4", self.bookGraphInfo, 3, graph4Data, copiedOptions);
        // グラフ4（累計発行部数(1巻））を描画
    })
}

CompareController.prototype.getGraph4Data = function(ip_code, ip_name) {
    var dtd = $.Deferred();
    var param = {
        'book4' : 'book4',
        'book_id' : ip_code
    };
    AjaxUtil.get('/ipdds/compare', param, function(data) {
        var result = JSON.parse(data.toString());
        if (result.length != 0) {
            // グラフ4（累計発行部数(1巻））データ
            var graph4Data = [];
            result.forEach(function(val) {
                graph4Data.push([ val[0], val[1] ]);
            });
            dtd.resolve([ graph4Data, ip_name ]);
        } else {
            dtd.resolve(null);
        }
    })
    return dtd;
}

CompareController.prototype.plotBookGraph5 = function() {
    var self = this;

    // Options定義
    var copiedOptions = jQuery.extend(true, {}, self.commonOptions.option);

    // グラフのラベル定義
    var series = [];
    var series2 = [];
    var data2 = [];
    var promiseArr = [];
    djangoObj.book.forEach(function(obj, index) {
        // IpCodeごとに累計発行部数(最新巻）のデータ取得
        promiseArr.push(self.getGraph5Data(obj.ip_code, obj.ip_name));
    });

    // IpCodeごとのデータを取得後に累計発行部数(最新巻）グラフを描画する
    $.when.apply($, promiseArr).then(function() {
        var values = Array.prototype.slice.call(arguments);
        var graph5Data = [];
        values.forEach(function(val, i) {
            if (val) {
                series2.push({
                    label : val[1],
                    color : self.commonOptions.colorArray[i]
                });
                data2.push(val[0]);

                var selector1 = '.book-graph-checkbox';
                var selector2 = 'input[value="' + val[1] + '"]';

                if ($(selector1).filter(selector2).is(':checked')) {
                    graph5Data.push(val[0]);
                    // グラフのラベルを設定
                    series.push({
                        label : val[1],
                        color : self.commonOptions.colorArray[i]
                    });
                }
            }
        });

        // グラフのラベルを設定
        copiedOptions.series = series;
        copiedOptions.series2 = series2;
        copiedOptions.data2 = data2;
        // グラフ4（累計発行部数(最新巻））を描画
        self.createGraph("book-graph5", self.bookGraphInfo, 4, graph5Data, copiedOptions);
    })
}

CompareController.prototype.getGraph5Data = function(ip_code, ip_name) {
    var dtd = $.Deferred();
    var param = {
        'book5' : 'book5',
        'book_id' : ip_code
    };
    AjaxUtil.get('/ipdds/compare', param, function(data) {
        var result = JSON.parse(data.toString());
        if (result.length != 0) {
            // グラフ5（累計発行部数(最新巻））データ
            var graph5Data = [];
            result.forEach(function(val) {
                graph5Data.push([ val[0], val[1] ]);
            });
            dtd.resolve([ graph5Data, ip_name ]);
        } else {
            dtd.resolve(null);
        }
    })
    return dtd;
}

CompareController.prototype.gameGraphInfo = [ {
    options : {
        title : '累計売上本数(発売日からNか月)'
    }
}, {
    options : {
        title : '累計売上本数'
    }
} ];

CompareController.prototype.plotGameGraph = function() {
    var self = this;
    // 累計売上本数(発売日からNか月)
    self.plotGameGraph1();
    // 累計売上本数
    self.plotGameGraph2();

    // 再描画のイベントを設定
    self.bindReplot('game-replot-button', 'game-graph-checkbox', self.gameGraphInfo);
}

CompareController.prototype.plotGameGraph1 = function() {
    var self = this;

    // options定義
    var copiedOptions = jQuery.extend(true, {}, self.commonOptions.option);
    copiedOptions.axes = {
        xaxis : {
            renderer : $.jqplot.DateAxisRenderer,
            tickRenderer : $.jqplot.CanvasAxisTickRenderer,
            tickInterval : "1 months",
            tickOptions : {
                angle : -45,
                formatString : "%#mヵ月目"
            },
            min : '1999-12-01',
            max : '2001-01-01'
        },
        yaxis : {
            min : 0,
            tickOptions : {
                formatString : "%'d"
            }
        }
    };
    copiedOptions.highlighter = {
        show : true,
        showMarker : true,
        sizeAdjust : 7,
        tooltipLocation : "ne",
        tooltipAxes : "y",
        formatString : "本数:%s"
    }

    // グラフのラベル定義
    var series = [];
    var series2 = [];
    var data2 = [];
    var promiseArr = [];
    djangoObj.game.forEach(function(obj, index) {
        // IpCodeごとにデータ取得
        promiseArr.push(self.getGameGraph1Data(obj.pkg_soft_code, obj.ip_name + obj.pkg_soft_name + obj.platform_name));
    });

    // IpCodeごとのデータを取得後にゲームグラフ１を描画する
    $.when.apply($, promiseArr).then(function() {
        var values = Array.prototype.slice.call(arguments);
        var gamegraph1Data = [];
        values.forEach(function(val, i) {
            if (val) {
                series2.push({
                    label : val[1],
                    color : self.commonOptions.colorArray[i]
                });
                val[0].map(function(e, i) {
                    e[0] = '2000-' + StringUtil.lpad((i + 1), 2) + '-01';
                });
                data2.push(val[0]);
                var selector1 = '.game-graph-checkbox';
                var selector2 = 'input[value="' + val[1] + '"]';

                if ($(selector1).filter(selector2).is(':checked')) {
                    val[0].map(function(e, i) {
                        e[0] = '2000-' + StringUtil.lpad((i + 1), 2) + '-01';
                    });
                    gamegraph1Data.push(val[0]);
                    // グラフのラベルを設定
                    series.push({
                        label : val[1],
                        color : self.commonOptions.colorArray[i]
                    });
                }
            }
        });

        // グラフのラベルを設定
        copiedOptions.series = series;
        copiedOptions.series2 = series2;
        copiedOptions.data2 = data2;
        // グラフ１（累計発行部数(発売日からNか月））を描画
        self.createGraph("game-graph1", self.gameGraphInfo, 0, gamegraph1Data, copiedOptions);
    });
}

CompareController.prototype.getGameGraph1Data = function(pkg_soft_code, pkg_soft_name) {
    var dtd = $.Deferred();
    var param = {
        'game1' : 'game1',
        'game_soft_code' : pkg_soft_code
    };
    AjaxUtil.get('/ipdds/compare', param, function(data) {
        var result = JSON.parse(data.toString());
        if (result.length != 0) {
            // グラフ１データ
            var gamegraph1Data = [];
            result.forEach(function(val) {
                gamegraph1Data.push([ val[0], val[1] ]);
            });
            dtd.resolve([ gamegraph1Data, pkg_soft_name ]);
        } else {
            dtd.resolve(null);
        }
    })
    return dtd;
}

CompareController.prototype.plotGameGraph2 = function() {
    var self = this;

    // Options定義
    var copiedOptions = jQuery.extend(true, {}, self.commonOptions.option);
    copiedOptions.highlighter = {
        show : true,
        showMarker : true,
        sizeAdjust : 7,
        tooltipLocation : "ne",
        tooltipAxes : "y",
        formatString : "本数:%s"
    }

    // グラフのラベル定義
    var series = [];
    var series2 = [];
    var data2 = [];
    var promiseArr = [];
    djangoObj.game.forEach(function(obj, index) {
        // IpCodeごとにデータ取得
        promiseArr.push(self.getGameGraph2Data(obj.pkg_soft_code, obj.ip_name + obj.pkg_soft_name + obj.platform_name));
    });

    // IpCodeごとのデータを取得後にグラフを描画する
    $.when.apply($, promiseArr).then(function() {
        var values = Array.prototype.slice.call(arguments);
        var gamegraph2Data = [];
        values.forEach(function(val, i) {
            if (val) {
                series2.push({
                    label : val[1],
                    color : self.commonOptions.colorArray[i]
                });
                data2.push(val[0]);

                var selector1 = '.game-graph-checkbox';
                var selector2 = 'input[value="' + val[1] + '"]';

                if ($(selector1).filter(selector2).is(':checked')) {
                    gamegraph2Data.push(val[0]);
                    // グラフのラベルを設定
                    series.push({
                        label : val[1],
                        color : self.commonOptions.colorArray[i]
                    });
                }
            }
        });

        // グラフのラベルを設定
        copiedOptions.series = series;
        copiedOptions.series2 = series2;
        copiedOptions.data2 = data2;
        // グラフ（累計売上本数）を描画
        self.createGraph("game-graph2", self.gameGraphInfo, 1, gamegraph2Data, copiedOptions);
    });
}

CompareController.prototype.getGameGraph2Data = function(pkg_soft_code, pkg_soft_name) {
    var dtd = $.Deferred();
    var param = {
        'game2' : 'game2',
        'game_soft_code' : pkg_soft_code
    };
    AjaxUtil.get('/ipdds/compare', param, function(data) {
        var result = JSON.parse(data.toString());
        if (result.length != 0) {
            // グラフ１データ
            var gamegraph2Data = [];
            result.forEach(function(val) {
                gamegraph2Data.push([ val[0], val[1] ]);
            });
            dtd.resolve([ gamegraph2Data, pkg_soft_name ]);
        } else {
            dtd.resolve(null);
        }
    })
    return dtd;
}

CompareController.prototype.appGraphInfo = [ {
    options : {
        title : '累計売上(発売日からNか月)'
    }
}, {
    options : {
        title : '累計ダウンロード数(発売日からNか月)'
    }
}, {
    options : {
        title : '累計売上'
    }
}, {
    options : {
        title : '累計ダウンロード数'
    }
}, {
    options : {
        title : '平均売上'
    }
}, {
    options : {
        title : '平均ダウンロード数'
    }
} ];

CompareController.prototype.plotAppGraph = function() {
    var self = this;
    // 累計売上(発売日からNか月)
    self.plotAppSalesGraph1();
    // 累計売上
    self.plotAppSalesGraph2();
    // 平均売上
    self.plotAppAvgSalesGraph();
    // 平均ダウンロード数
    self.plotAppAvgDownloadGraph();
    // 累計ダウンロード数(発売日からNか月)
    self.plotAppDownloadGraph1();
    // 累計ダウンロード数
    self.plotAppDownloadGraph2();

    // 再描画のイベントを設定
    self.bindReplot('app-replot-button', 'app-graph-checkbox', self.appGraphInfo);
}

CompareController.prototype.plotAppSalesGraph1 = function() {
    var self = this;

    // Options定義
    var copiedOptions = jQuery.extend(true, {}, self.commonOptions.option);
    copiedOptions.axes = {
        xaxis : {
            renderer : $.jqplot.DateAxisRenderer,
            tickRenderer : $.jqplot.CanvasAxisTickRenderer,
            tickInterval : "1 months",
            tickOptions : {
                angle : -45,
                formatString : "%#mヵ月目"
            },
            min : '1999-12-01',
            max : '2001-01-01'
        },
        yaxis : {
            min : 0,
            tickOptions : {
                formatString : "%'d"
            }
        }
    };
    // アプリグラフ（累計売上（発売日からNか月））を描画
    copiedOptions.highlighter = {
        show : true,
        showMarker : true,
        sizeAdjust : 7,
        tooltipLocation : "ne",
        tooltipAxes : "y",
        formatString : "売上:%s"
    }

    // グラフのラベル定義
    var series = [];
    var series2 = [];
    var data2 = [];
    // ajaxから返却したデータ
    var promiseArr = [];
    djangoObj.app.forEach(function(obj, index) {
        // IpCodeごとにデータ取得
        promiseArr.push(self.getAppSalesGraph1Data(obj.app_name));
    });

    // IpCodeごとのデータを取得後にアプリのグラフ１(累計売上（発売日からNか月）)を描画する
    $.when.apply($, promiseArr).then(function() {
        var values = Array.prototype.slice.call(arguments);
        var appSalesGraph1Data = [];
        values.forEach(function(val, i) {
            if (val) {
                series2.push({
                    label : val[1],
                    color : self.commonOptions.colorArray[i]
                });
                val[0].map(function(e, i) {
                    e[0] = '2000-' + StringUtil.lpad((i + 1), 2) + '-01';
                });
                data2.push(val[0]);
                var selector1 = '.app-graph-checkbox';
                var selector2 = 'input[value="' + val[1] + '"]';

                if ($(selector1).filter(selector2).is(':checked')) {
                    val[0].map(function(e, i) {
                        e[0] = '2000-' + StringUtil.lpad((i + 1), 2) + '-01';
                    });
                    appSalesGraph1Data.push(val[0]);
                    // グラフのラベルを設定
                    series.push({
                        label : val[1],
                        color : self.commonOptions.colorArray[i]
                    });
                }
            }
        });

        // グラフのラベルを設定
        copiedOptions.series = series;
        copiedOptions.series2 = series2;
        copiedOptions.data2 = data2;

        // アプリグラフ１（累計売上(発売日からNか月））を描画
        self.createGraph("app-graph-sales1", self.appGraphInfo, 0, appSalesGraph1Data, copiedOptions);
    });
}

CompareController.prototype.getAppSalesGraph1Data = function(app_name) {
    var dtd = $.Deferred();
    var param = {
        'appSales1' : 'appSales1',
        'app_name' : app_name
    };
    AjaxUtil.get('/ipdds/compare', param, function(data) {
        var result = JSON.parse(data.toString());
        if (result.length != 0) {
            // Appグラフ１データ
            var appSalesGraph1Data = [];
            result.forEach(function(val) {
                appSalesGraph1Data.push([ val[0], val[1] ]);
            });
            dtd.resolve([ appSalesGraph1Data, app_name ]);
        } else {
            dtd.resolve(null);
        }
    })
    return dtd;
}

CompareController.prototype.plotAppSalesGraph2 = function() {
    var self = this;

    // Options定義
    var copiedOptions = jQuery.extend(true, {}, self.commonOptions.option);
    // アプリグラフ（平均売上）を描画
    copiedOptions.highlighter = {
        show : true,
        showMarker : true,
        sizeAdjust : 7,
        tooltipLocation : "ne",
        tooltipAxes : "y",
        formatString : "売上:%s"
    }

    // グラフのラベル定義
    var series = [];
    var series2 = [];
    var data2 = [];
    // ajaxから返却したデータ
    var promiseArr = [];
    djangoObj.app.forEach(function(obj, index) {
        // IpCodeごとにデータ取得
        promiseArr.push(self.getAppSalesGraph2Data(obj.app_name));
    });

    // IpCodeごとのデータを取得後にアプリのグラフ(累計売上)を描画する
    $.when.apply($, promiseArr).then(function() {
        var values = Array.prototype.slice.call(arguments);
        var appSalesGraph2Data = [];
        values.forEach(function(val, i) {
            if (val) {
                series2.push({
                    label : val[1],
                    color : self.commonOptions.colorArray[i]
                });
                data2.push(val[0]);

                var selector1 = '.app-graph-checkbox';
                var selector2 = 'input[value="' + val[1] + '"]';

                if ($(selector1).filter(selector2).is(':checked')) {
                    appSalesGraph2Data.push(val[0]);
                    // グラフのラベルを設定
                    series.push({
                        label : val[1],
                        color : self.commonOptions.colorArray[i]
                    });
                }
            }
        });

        // グラフのラベルを設定
        copiedOptions.series = series;
        copiedOptions.series2 = series2;
        copiedOptions.data2 = data2;
        // アプリグラフ（累計売上）を描画
        self.createGraph("app-graph-sales2", self.appGraphInfo, 2, appSalesGraph2Data, copiedOptions);
    });
}

CompareController.prototype.getAppSalesGraph2Data = function(app_name) {
    var dtd = $.Deferred();
    var param = {
        'appSales2' : 'appSales2',
        'app_name' : app_name
    };
    AjaxUtil.get('/ipdds/compare', param, function(data) {
        var result = JSON.parse(data.toString());
        if (result.length != 0) {
            // Appグラフ１データ
            var appSalesGraph2Data = [];
            result.forEach(function(val) {
                appSalesGraph2Data.push([ val[0], val[1] ]);
            });
            dtd.resolve([ appSalesGraph2Data, app_name ]);
        } else {
            dtd.resolve(null);
        }
    })
    return dtd;
}

CompareController.prototype.plotAppAvgSalesGraph = function() {
    var self = this;

    // Options定義
    var copiedOptions = jQuery.extend(true, {}, self.commonOptions.option);
    // アプリグラフ（平均売上）を描画
    copiedOptions.highlighter = {
        show : true,
        showMarker : true,
        sizeAdjust : 7,
        tooltipLocation : "ne",
        tooltipAxes : "y",
        formatString : "売上:%s"
    }

    // グラフのラベル定義
    var series = [];
    var series2 = [];
    var data2 = [];
    // ajaxから返却したデータ
    var promiseArr = [];
    djangoObj.app.forEach(function(obj, index) {
        // IpCodeごとにデータ取得
        promiseArr.push(self.getAppGraphAvgData(obj.app_name));
    });

    // IpCodeごとのデータを取得後にアプリのグラフ平均売上を描画する
    $.when.apply($, promiseArr).then(function() {
        var values = Array.prototype.slice.call(arguments);
        var appAvgSalesGraphData = [];
        values.forEach(function(val, i) {
            if (val) {
                series2.push({
                    label : val[2],
                    color : self.commonOptions.colorArray[i]
                });
                data2.push(val[0]);

                var selector1 = '.app-graph-checkbox';
                var selector2 = 'input[value="' + val[2] + '"]';

                if ($(selector1).filter(selector2).is(':checked')) {
                    appAvgSalesGraphData.push(val[0]);
                    // グラフのラベルを設定
                    series.push({
                        label : val[2],
                        color : self.commonOptions.colorArray[i]
                    });
                }
            }
        });

        // グラフのラベルを設定
        copiedOptions.series = series;
        copiedOptions.series2 = series2;
        copiedOptions.data2 = data2;
        // アプリグラフ（平均売上）を描画
        self.createGraph("app-graph-sales3", self.appGraphInfo, 4, appAvgSalesGraphData, copiedOptions);
    });
}

CompareController.prototype.getAppGraphAvgData = function(app_name) {
    var dtd = $.Deferred();
    var param = {
        'appAvg' : 'appAvg',
        'app_name' : app_name
    };
    AjaxUtil.get('/ipdds/compare', param, function(data) {
        var result = JSON.parse(data.toString());
        if (result.length != 0) {
            // Appグラフ(平均売上)データ
            var appAvgSalesGraphData = [];
            // Appグラフ(平均ダウンロード数)データ
            var appAvgDownloadGraphData = [];
            result.forEach(function(val) {
                appAvgSalesGraphData.push([ val[0], val[1] ]);
                appAvgDownloadGraphData.push([ val[0], val[2] ]);
            });
            dtd.resolve([ appAvgSalesGraphData, appAvgDownloadGraphData, app_name ]);
        } else {
            dtd.resolve(null);
        }
    })
    return dtd;
}

CompareController.prototype.plotAppAvgDownloadGraph = function() {
    var self = this;

    // Options定義
    var copiedOptions = jQuery.extend(true, {}, self.commonOptions.option);
    // アプリグラフ（平均ダウンロード数）を描画
    copiedOptions.highlighter = {
        show : true,
        showMarker : true,
        sizeAdjust : 7,
        tooltipLocation : "ne",
        tooltipAxes : "y",
        formatString : "ダウンロード数:%s"
    }

    // グラフのラベル定義
    var series = [];
    var series2 = [];
    var data2 = [];
    // ajaxから返却したデータ
    var promiseArr = [];
    djangoObj.app.forEach(function(obj, index) {
        // IpCodeごとにデータ取得
        promiseArr.push(self.getAppGraphAvgData(obj.app_name));
    });

    // IpCodeごとのデータを取得後にアプリの平均ダウンロード数を描画する
    $.when.apply($, promiseArr).then(function() {
        var values = Array.prototype.slice.call(arguments);
        var appAvgSalesGraphData = [];
        var appAvgDownloadGraphData = [];
        values.forEach(function(val, i) {
            if (val) {
                series2.push({
                    label : val[2],
                    color : self.commonOptions.colorArray[i]
                });
                data2.push(val[1]);

                var selector1 = '.app-graph-checkbox';
                var selector2 = 'input[value="' + val[2] + '"]';

                if ($(selector1).filter(selector2).is(':checked')) {
                    appAvgDownloadGraphData.push(val[1]);
                    // グラフのラベルを設定
                    series.push({
                        label : val[2],
                        color : self.commonOptions.colorArray[i]
                    });
                }
            }
        });

        // グラフのラベルを設定
        copiedOptions.series = series;
        copiedOptions.series2 = series2;
        copiedOptions.data2 = data2;
        // アプリグラフ（平均ダウンロード数）を描画
        self.createGraph("app-graph-download3", self.appGraphInfo, 5, appAvgDownloadGraphData, jQuery.extend(true, {}, copiedOptions));
    });
}

CompareController.prototype.plotAppDownloadGraph1 = function() {
    var self = this;

    // Options定義
    var copiedOptions = jQuery.extend(true, {}, self.commonOptions.option);
    copiedOptions.highlighter = {
        show : true,
        showMarker : true,
        sizeAdjust : 7,
        tooltipLocation : "ne",
        tooltipAxes : "y",
        formatString : "ダウンロード数:%s"
    }
    copiedOptions.axes.xaxis = {
        renderer : $.jqplot.DateAxisRenderer,
        tickRenderer : $.jqplot.CanvasAxisTickRenderer,
        tickInterval : "1 months",
        tickOptions : {
            angle : -45,
            formatString : "%#mヵ月目"
        },
        min : '1999-12-01',
        max : '2001-01-01'
    };

    // グラフのラベル定義
    var series = [];
    var series2 = [];
    var data2 = [];
    // ajaxから返却したデータ
    var promiseArr = [];
    djangoObj.app.forEach(function(obj, index) {
        // IpCodeごとにデータ取得
        promiseArr.push(self.getAppDownloadGraph1Data(obj.app_name));
    });

    // IpCodeごとのデータを取得後にグラフ１及びグラフ２を描画する
    $.when.apply($, promiseArr).then(function() {
        var values = Array.prototype.slice.call(arguments);
        var appDownloadGraph1Data = [];
        values.forEach(function(val, i) {
            if (val) {
                series2.push({
                    label : val[1],
                    color : self.commonOptions.colorArray[i]
                });
                val[0].map(function(e, i) {
                    e[0] = '2000-' + StringUtil.lpad((i + 1), 2) + '-01';
                });
                data2.push(val[0]);
                var selector1 = '.app-graph-checkbox';
                var selector2 = 'input[value="' + val[1] + '"]';

                if ($(selector1).filter(selector2).is(':checked')) {
                    val[0].map(function(e, i) {
                        e[0] = '2000-' + StringUtil.lpad((i + 1), 2) + '-01';
                    });
                    appDownloadGraph1Data.push(val[0]);
                    // グラフのラベルを設定
                    series.push({
                        label : val[1],
                        color : self.commonOptions.colorArray[i]
                    });
                }
            }
        });

        // グラフのラベルを設定
        copiedOptions.series = series;
        copiedOptions.series2 = series2;
        copiedOptions.data2 = data2;
        // アプリグラフ１（累計売上(発売日からNか月））を描画
        self.createGraph("app-graph-download1", self.appGraphInfo, 1, appDownloadGraph1Data, copiedOptions);
    });
}

CompareController.prototype.getAppDownloadGraph1Data = function(app_name) {
    var dtd = $.Deferred();
    var param = {
        'appDownload1' : 'appDownload1',
        'app_name' : app_name
    };
    AjaxUtil.get('/ipdds/compare', param, function(data) {
        var result = JSON.parse(data.toString());
        if (result.length != 0) {
            // Appグラフ１データ
            var appDownloadGraph1Data = [];
            result.forEach(function(val) {
                appDownloadGraph1Data.push([ val[0], val[2] ]);
            });
            dtd.resolve([ appDownloadGraph1Data, app_name ]);
        } else {
            dtd.resolve(null);
        }
    })
    return dtd;
}

CompareController.prototype.plotAppDownloadGraph2 = function() {
    var self = this;

    // Options定義
    var copiedOptions = jQuery.extend(true, {}, self.commonOptions.option);
    copiedOptions.highlighter = {
        show : true,
        showMarker : true,
        sizeAdjust : 7,
        tooltipLocation : "ne",
        tooltipAxes : "y",
        formatString : "ダウンロード数:%s"
    }

    // グラフのラベル定義
    var series = [];
    var series2 = [];
    var data2 = [];
    // ajaxから返却したデータ
    var promiseArr = [];
    djangoObj.app.forEach(function(obj, index) {
        // IpCodeごとにデータ取得
        promiseArr.push(self.getAppDownloadGraph2Data(obj.app_name));
    });

    // IpCodeごとのデータを取得後にグラフ１及びグラフ２を描画する
    $.when.apply($, promiseArr).then(function() {
        var values = Array.prototype.slice.call(arguments);
        var appDownloadGraph2Data = [];
        values.forEach(function(val, i) {
            if (val) {

                series2.push({
                    label : val[1],
                    color : self.commonOptions.colorArray[i]
                });
                data2.push(val[0]);

                var selector1 = '.app-graph-checkbox';
                var selector2 = 'input[value="' + val[1] + '"]';

                if ($(selector1).filter(selector2).is(':checked')) {
                    appDownloadGraph2Data.push(val[0]);
                    // グラフのラベルを設定
                    series.push({
                        label : val[1],
                        color : self.commonOptions.colorArray[i]
                    });
                }
            }
        });

        // グラフのラベルを設定
        copiedOptions.series = series;
        copiedOptions.series2 = series2;
        copiedOptions.data2 = data2;
        // アプリグラフ（累計売上ダウンロード数）を描画
        self.createGraph("app-graph-download2", self.appGraphInfo, 3, appDownloadGraph2Data, copiedOptions);
    })
}

CompareController.prototype.getAppDownloadGraph2Data = function(app_name) {
    var dtd = $.Deferred();
    var param = {
        'appDownload2' : 'appDownload2',
        'app_name' : app_name
    };
    AjaxUtil.get('/ipdds/compare', param, function(data) {
        var result = JSON.parse(data.toString());
        if (result.length != 0) {
            // Appグラフのデータ
            var appDownloadGraph2Data = [];
            result.forEach(function(val) {
                appDownloadGraph2Data.push([ val[0], val[2] ]);
            });
            dtd.resolve([ appDownloadGraph2Data, app_name ]);
        } else {
            dtd.resolve(null);
        }
    })
    return dtd;
}

/**
 * グラフを作成する。
 *
 * @param elemId
 *            要素ID
 * @param graphInfo
 *            グラム情報の配列
 * @param index
 *            インデックス
 * @param data
 *            グラフ表示用データ
 * @param options
 *            グラフ表示用options
 */
CompareController.prototype.createGraph = function(elemId, graphInfo, index, data, options) {
    var self = this;
    var info = graphInfo[index];
    options.title = info.options.title;

    var tmpData = [];
    var tmpSeries = [];
    for (var i = 0; i < data.length; i++) {
        var tmp = 0;
        var subData = data[i];
        for (var j = 0; j < subData.length; j++) {
            tmp += subData[j][1];
        }
        if (tmp > 0) {
            tmpData.push(subData);
            tmpSeries.push(options.series[i]);
        }
    }
    if (tmpData.length == 0) {
        tmpData.push([ [ '9999-01-01', 0 ] ]);
        options.legend = {
            show : false
        };

        NoDateUtil.overlay(elemId)
    }
    options.series = tmpSeries;
    info.data = tmpData
    info.options = options;
    info.elemId = elemId;
    info.graph = $.jqplot(elemId, tmpData, options);
}

/**
 * 指定するボタンに、再描画イベントをセットする。
 *
 * @param btnId
 *            ボタンのID
 * @param checkBoxClassName
 *            チェックボックスのクラス名
 * @param graphInfo
 *            該当するグラム情報の配列
 */
CompareController.prototype.bindReplot = function(btnId, checkBoxClassName, graphInfo) {
    $('#' + btnId).on('click', function(e) {
        var chkBoxs = $('.' + checkBoxClassName + ':checked');
        graphInfo.forEach(function(info, i) {
            var data = [];
            var series = [];
            chkBoxs.each(function(i1, elem) {
                var ipName = $(elem).val();
                info.options.series2.forEach(function(tmp, idx) {
                    if (tmp.label == ipName) {
                        series.push(tmp);
                        if (info.options && info.options.data2) {
                            data.push(info.options.data2[idx]);
                        }
                    }
                });
            });

            var isBlank = false;
            var options = jQuery.extend(true, {}, info.options);
            options.series = series;

            if (!data || data.length == 0) {
                data.push([ [ '9999-01-01', 0 ] ]);
                options.legend = {
                    show : false
                };
                isBlank = true;
            }
            info.graph.destroy();
            // 再描画する
            info.graph = $.jqplot(info.elemId, data, options);
            // データなしの場合、Maskを追加する
            if (isBlank) {
                NoDateUtil.overlay(info.elemId);
            }
        });
    });
}

CompareController.prototype.drawGrid = function() {
    var self = this;
    // ツイッターのグリッドを表示
    self.drawGridForTwitter();
    // マンガのグリッドを表示
    self.drawGridForBook();
    // ゲームのグリッドを表示
    self.drawGridForGame();
    // アプリのグリッドを表示
    self.drawGridForApp();
}

/**
 * ツイッターGridのフォーマットを作成する。
 *
 */
CompareController.prototype.drawGridForTwitter = function() {
    var self = this;

    var medelArray = [];
    var width = $('#grid-twitter').width();
    medelArray.push(GridUtil.createColModel({
        name : 'is_draw',
        align : 'center',
        width : width * 0.09,
        formatter : function(val, opt, rdt) {
            var strVal = JSON.parse(val.toString());
            var dataRow = strVal[0];
            var checkBoxVal = strVal[1];

            if (self.isDrawGridForTwitter) {
                if (self.isTwitterChecked[dataRow]) {
                    return ('<input type="checkbox" class="plot-checkbox twitter-graph-checkbox" value="' + checkBoxVal + '"/ style="margin: 10px;" data-row="' + dataRow + '" checked>');
                } else {
                    return ('<input type="checkbox" class="plot-checkbox twitter-graph-checkbox" value="' + checkBoxVal + '"/ style="margin: 10px;" data-row="' + dataRow + '">');
                }
            } else {
                if (!self.isTwitterChecked) {
                    self.isTwitterChecked = {};
                }
                if (dataRow < 5) {
                    self.isTwitterChecked[dataRow] = true;
                    return ('<input type="checkbox" class="plot-checkbox twitter-graph-checkbox" value="' + checkBoxVal + '"/ style="margin: 10px;" data-row="' + dataRow + '" checked>');
                } else {
                    self.isTwitterChecked[dataRow] = false;
                    return ('<input type="checkbox" class="plot-checkbox twitter-graph-checkbox" value="' + checkBoxVal + '"/ style="margin: 10px;" data-row="' + dataRow + '">');
                }
            }
        },
        sortable : false
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'ip_name',
        width : width * 0.20,
        formatter : function(val, opt, rdt) {
            return '<a href="/ipdds/detail/?ip_code=' + val[0] + '" class="link">' + val[1] + '</a>'
        },
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'followers_latest',
        align : 'right',
        width : width * 0.15,
        sorttype : 'number',
        formatter : function(val, opt, rdt) {
            return val ? StringUtil.comma_separated(val) : 'ー';
        }
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'followers_3months_ago',
        align : 'right',
        width : width * 0.15,
        sorttype : 'number',
        formatter : function(val, opt, rdt) {
            return val ? StringUtil.comma_separated(val) : 'ー';
        }
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'followers_1year_ago',
        align : 'right',
        width : width * 0.15,
        sorttype : 'number',
        formatter : function(val, opt, rdt) {
            return val ? StringUtil.comma_separated(val) : 'ー';
        }
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'user_name',
        width : width * 0.07,
        align : 'center',
        formatter : function(val, opt, rdt) {
            if ((rdt.followers_latest || rdt.followers_3months_ago || rdt.followers_1year_ago) && rdt.user_name) {
                return '<a  class="twitter-link" onclick="window.open(\'https://twitter.com/' + val + '\')"><i class="fab fa-twitter-square" style="font-size: 30px"></i></a></a>'
            } else {
                return '';
            }
        },
    }));

    var data = self.createTwitterData();
    var pager = '';
    var search = false;
    if (data.length > 10) {
        var pager = '#pager-twitter';
        var search = true;
    }
    console.log(data.length);

    var option = {
        colNames : [ 'グラフ描画', 'IP名', '最新の<br>フォロワー数', '三か月前の<br>フォロワー数', '一年前の<br>フォロワー数', 'Twitter' ],
        colModel : medelArray,
        data : data,
        width : width,
        pager : pager,
        loadComplete : function() {
            if ($('.twitter-graph-checkbox:checked').length == 5) {
                $('.twitter-graph-checkbox:not(:checked)').prop('disabled', true);
            }
            self.isDrawGridForTwitter = true;
            $('.twitter-graph-checkbox').on('click', function() {
                var elem = $(this);
                var val = elem.attr('data-row');
                self.isTwitterChecked[val] = elem.is(':checked');
                if ($('.twitter-graph-checkbox:checked').length == 5) {
                    $('.twitter-graph-checkbox:not(:checked)').prop('disabled', true);
                } else {
                    console.log($('.twitter-graph-checkbox:checked').length)
                    $('.twitter-graph-checkbox:not(:checked)').prop('disabled', false);
                }

            });
        }
    };
    GridUtil.renderNormalGrid('#grid-twitter', option, search);

}
/**
 * ツイッターGridのデータを作成する。
 *
 */
CompareController.prototype.createTwitterData = function() {
    var self = this;

    var data = [];
    for (var i = 0; i <= djangoObj.twitter.length; i++) {
        if (djangoObj.twitter[i]) {
            var row = [];
            var jsonStr = JSON.stringify([ i, djangoObj.twitter[i].ip_name ]);
            row.push(jsonStr);
            row.push([ djangoObj.twitter[i].ip_code, djangoObj.twitter[i].ip_name ]);
            row.push(djangoObj.twitter[i].followers_latest);
            row.push(djangoObj.twitter[i].followers_3months_ago);
            row.push(djangoObj.twitter[i].followers_1year_ago);
            row.push(djangoObj.twitter[i].user_name);
            data.push(row);
        }
    }
    var colNames = [ 'is_draw', 'ip_name', 'followers_latest', 'followers_3months_ago', 'followers_1year_ago', 'user_name' ];
    return GridUtil.createGridData(colNames, data);
}

/**
 * マンガGridのフォーマットを作成する。
 *
 */
CompareController.prototype.drawGridForBook = function() {
    var self = this;

    var medelArray = [];
    var width = $('#grid-book').width();
    medelArray.push(GridUtil.createColModel({
        name : 'is_draw',
        align : 'center',
        width : width * 0.06,
        formatter : function(val, opt, rdt) {
            var strVal = JSON.parse(val.toString());
            var dataRow = strVal[0];
            var checkBoxVal = strVal[1];

            if (self.isDrawGridForBook) {
                if (self.isBookChecked[dataRow]) {
                    return ('<input type="checkbox" class="plot-checkbox book-graph-checkbox" value="' + checkBoxVal + '"/ style="margin: 10px;" data-row="' + dataRow + '" checked>');
                } else {
                    return ('<input type="checkbox" class="plot-checkbox book-graph-checkbox" value="' + checkBoxVal + '"/ style="margin: 10px;" data-row="' + dataRow + '">');
                }
            } else {
                if (!self.isBookChecked) {
                    self.isBookChecked = {};
                }
                if (dataRow < 5) {
                    self.isBookChecked[dataRow] = true;
                    return ('<input type="checkbox" class="plot-checkbox book-graph-checkbox" value="' + checkBoxVal + '"/ style="margin: 10px;" data-row="' + dataRow + '" checked>');
                } else {
                    self.isBookChecked[dataRow] = false;
                    return ('<input type="checkbox" class="plot-checkbox book-graph-checkbox" value="' + checkBoxVal + '"/ style="margin: 10px;" data-row="' + dataRow + '">');
                }
            }
        },
        sortable : false
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'ip_name',
        width : width * 0.20,
        formatter : function(val, opt, rdt) {
            return '<a href="/ipdds/detail/?ip_code=' + val[0] + '" class="link">' + val[1] + '</a>'
        },
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'cumulative',
        align : 'right',
        width : width * 0.19,
        sorttype : 'number',
        formatter : function(val, opt, rdt) {
            return val ? StringUtil.comma_separated(val) + '部' : 'ー';
        }
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'cumulative_first',
        align : 'right',
        width : width * 0.19,
        sorttype : 'number',
        formatter : function(val, opt, rdt) {
            return val ? StringUtil.comma_separated(val) + '部' : 'ー';
        }
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'cumulative_latest',
        align : 'right',
        width : width * 0.19,
        sorttype : 'number',
        formatter : function(val, opt, rdt) {
            return val ? StringUtil.comma_separated(val) + '部' : 'ー';
        }
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'average_1book',
        align : 'right',
        width : width * 0.19,
        sorttype : 'number',
        formatter : function(val, opt, rdt) {
            return val ? StringUtil.comma_separated(val) + '部' : 'ー';
        }
    }));

    var data = self.createBookData();
    var pager = '';
    var search = false;
    if (data.length > 10) {
        var pager = '#pager-book';
        var search = true;
    }

    var option = {
        colNames : [ 'グラフ描画', 'IP名', '累計発行部数', '累計発行部数（１巻）', '累計発行部数（最新刊）', '平均発行部数（単巻あたり）' ],
        colModel : medelArray,
        data : data,
        width : width,
        pager : pager,
        loadComplete : function() {
            if ($('.book-graph-checkbox:checked').length == 5) {
                $('.book-graph-checkbox:not(:checked)').prop('disabled', true);
            }
            self.isDrawGridForBook = true;
            $('.book-graph-checkbox').on('click', function() {
                var elem = $(this);
                var val = elem.attr('data-row');
                self.isBookChecked[val] = elem.is(':checked');
                if ($('.book-graph-checkbox:checked').length == 5) {
                    $('.book-graph-checkbox:not(:checked)').prop('disabled', true);
                } else {
                    console.log($('.book-graph-checkbox:checked').length)
                    $('.book-graph-checkbox:not(:checked)').prop('disabled', false);
                }

            });
        }
    };
    GridUtil.renderNormalGrid('#grid-book', option, search);

}
/**
 * マンガGridのデータを作成する。
 *
 */
CompareController.prototype.createBookData = function() {
    var self = this;

    var data = [];
    for (var i = 0; i <= djangoObj.book.length; i++) {
        if (djangoObj.book[i]) {
            var row = [];
            var jsonStr = JSON.stringify([ i, djangoObj.book[i].ip_name ]);
            row.push(jsonStr);
            row.push([ djangoObj.book[i].ip_code, djangoObj.book[i].ip_name ]);
            row.push(djangoObj.book[i].cumulative);
            row.push(djangoObj.book[i].cumulative_first);
            row.push(djangoObj.book[i].cumulative_latest);
            row.push(djangoObj.book[i].average_1book);
            data.push(row);
        }
    }
    var colNames = [ 'is_draw', 'ip_name', 'cumulative', 'cumulative_first', 'cumulative_latest', 'average_1book' ];
    return GridUtil.createGridData(colNames, data);
}

/**
 * ゲームGridのフォーマットを作成する。
 *
 */
CompareController.prototype.drawGridForGame = function() {
    var self = this;

    var medelArray = [];
    var width = $('#grid-game').width();
    medelArray.push(GridUtil.createColModel({
        name : 'is_draw',
        align : 'center',
        width : width * 0.06,
        formatter : function(val, opt, rdt) {
            var strVal = JSON.parse(val.toString());
            var dataRow = strVal[0];
            var checkBoxVal = strVal[1] + strVal[2] + strVal[3];

            if (self.isDrawGridForGame) {
                if (self.isGameChecked[dataRow]) {
                    return ('<input type="checkbox" class="plot-checkbox game-graph-checkbox" value="' + checkBoxVal + '"/ style="margin: 10px;" data-row="' + dataRow + '" checked>');
                } else {
                    return ('<input type="checkbox" class="plot-checkbox game-graph-checkbox" value="' + checkBoxVal + '"/ style="margin: 10px;" data-row="' + dataRow + '">');
                }
            } else {
                if (!self.isGameChecked) {
                    self.isGameChecked = {};
                }
                if (dataRow < 5) {
                    self.isGameChecked[dataRow] = true;
                    return ('<input type="checkbox" class="plot-checkbox game-graph-checkbox" value="' + checkBoxVal + '"/ style="margin: 10px;" data-row="' + dataRow + '" checked>');
                } else {
                    self.isGameChecked[dataRow] = false;
                    return ('<input type="checkbox" class="plot-checkbox game-graph-checkbox" value="' + checkBoxVal + '"/ style="margin: 10px;" data-row="' + dataRow + '">');
                }
            }
        },
        sortable : false
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'ip_name',
        width : width * 0.10,
        formatter : function(val, opt, rdt) {
            return '<a href="/ipdds/detail/?ip_code=' + val[0] + '" class="link">' + val[1] + '</a>'
        },
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'pkg_soft_name',
        width : width * 0.40,
        formatter : function(val, opt, rdt) {
            return val || 'ー';
        }
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'platform_name',
        width : width * 0.10,
        formatter : function(val, opt, rdt) {
            return val || 'ー';
        }
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'distributor_name',
        width : width * 0.18,
        formatter : function(val, opt, rdt) {
            return val || 'ー';
        }
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'release_date',
        width : width * 0.07,
        formatter : function(val, opt, rdt) {
            return val || 'ー';
        }
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'qty_total_sales',
        align : 'right',
        width : width * 0.09,
        sorttype : 'number',
        formatter : function(val, opt, rdt) {
            return val ? StringUtil.comma_separated(val) + '本' : 'ー';
        }
    }));

    var data = self.createGameData();
    var pager = '';
    var search = false;
    if (data.length > 10) {
        var pager = '#pager-game';
        var search = true;
    }

    var rowList = [ 10, 20, 50 ];
    if (data.length > 50) {
        rowList.push(data.length);
    }
    var option = {
        colNames : [ 'グラフ描画', 'IP名', 'ゲーム名', '対応機種', '発売元', '発売日', '累計売上本数' ],
        colModel : medelArray,
        data : data,
        width : width,
        pager : pager,
        pgbuttons : false,
        pginput : false,
        rowList : rowList,
        loadComplete : function() {
            if ($('.game-graph-checkbox:checked').length == 5) {
                $('.game-graph-checkbox:not(:checked)').prop('disabled', true);
            }
            self.isDrawGridForGame = true;
            $('.game-graph-checkbox').on('click', function() {
                var elem = $(this);
                var val = elem.attr('data-row');
                self.isGameChecked[val] = elem.is(':checked');
                if ($('.game-graph-checkbox:checked').length == 5) {
                    $('.game-graph-checkbox:not(:checked)').prop('disabled', true);
                } else {
                    console.log($('.game-graph-checkbox:checked').length)
                    $('.game-graph-checkbox:not(:checked)').prop('disabled', false);
                }

            });
        }
    };
    GridUtil.renderNormalGrid('#grid-game', option, search);

}
/**
 * ゲームGridのデータを作成する。
 *
 */
CompareController.prototype.createGameData = function() {
    var self = this;

    var data = [];
    for (var i = 0; i <= djangoObj.game.length; i++) {
        if (djangoObj.game[i]) {
            var row = [];
            var jsonStr = JSON.stringify([ i, djangoObj.game[i].ip_name, djangoObj.game[i].pkg_soft_name, djangoObj.game[i].platform_name ]);
            row.push(jsonStr);
            row.push([ djangoObj.game[i].ip_code, djangoObj.game[i].ip_name ]);
            row.push(djangoObj.game[i].pkg_soft_name);
            row.push(djangoObj.game[i].platform_name);
            row.push(djangoObj.game[i].distributor_name);
            row.push(djangoObj.game[i].release_date);
            row.push(djangoObj.game[i].qty_total_sales);
            data.push(row);
        }
    }
    var colNames = [ 'is_draw', 'ip_name', 'pkg_soft_name', 'platform_name', 'distributor_name', 'release_date', 'qty_total_sales' ];
    return GridUtil.createGridData(colNames, data);
}

/**
 * アプリGridのフォーマットを作成する。
 *
 */
CompareController.prototype.drawGridForApp = function() {
    var self = this;

    var medelArray = [];
    var width = $('#grid-app').width();
    medelArray.push(GridUtil.createColModel({
        name : 'is_draw',
        align : 'center',
        width : width * 0.06,
        formatter : function(val, opt, rdt) {
            var dataRow = val[0];
            var checkBoxVal = val[1];
            if (self.isDrawGridForApp) {
                if (self.isAppChecked[dataRow]) {
                    return ('<input type="checkbox" class="plot-checkbox app-graph-checkbox" value="' + checkBoxVal + '"/ style="margin: 10px;" data-row="' + dataRow + '" checked>');
                } else {
                    return ('<input type="checkbox" class="plot-checkbox app-graph-checkbox" value="' + checkBoxVal + '"/ style="margin: 10px;" data-row="' + dataRow + '">');
                }
            } else {
                if (!self.isAppChecked) {
                    self.isAppChecked = {};
                }
                if (dataRow < 5) {
                    self.isAppChecked[dataRow] = true;
                    return ('<input type="checkbox" class="plot-checkbox app-graph-checkbox" value="' + checkBoxVal + '"/ style="margin: 10px;" data-row="' + dataRow + '" checked>');
                } else {
                    self.isAppChecked[dataRow] = false;
                    return ('<input type="checkbox" class="plot-checkbox app-graph-checkbox" value="' + checkBoxVal + '"/ style="margin: 10px;" data-row="' + dataRow + '">');
                }
            }
        },
        sortable : false
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'ip_name',
        width : width * 0.14,
        formatter : function(val, opt, rdt) {
            return '<a href="/ipdds/detail/?ip_code=' + val[0] + '" class="link">' + val[1] + '</a>'
        },
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'app_name',
        width : width * 0.14,
        formatter : function(val, opt, rdt) {
            return val || 'ー';
        }
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'platform',
        width : width * 0.08,
        formatter : function(val, opt, rdt) {
            return val || 'ー';
        }
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'distributor_name',
        width : width * 0.14,
        formatter : function(val, opt, rdt) {
            return val || 'ー';
        }
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'release_date',
        width : width * 0.07,
        formatter : function(val, opt, rdt) {
            return val || 'ー';
        }
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'total_sales',
        align : 'right',
        width : width * 0.09,
        sorttype : 'number',
        formatter : function(val, opt, rdt) {
            return val ? '$' + StringUtil.comma_separated(val) : 'ー';
        }
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'total_download_count',
        align : 'right',
        width : width * 0.1,
        sorttype : 'number',
        formatter : function(val, opt, rdt) {
            return val ? StringUtil.comma_separated(val) : 'ー';
        }
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'avg_sales',
        align : 'right',
        width : width * 0.08,
        sorttype : 'number',
        formatter : function(val, opt, rdt) {
            return val ? '$' + StringUtil.comma_separated(val) : 'ー';
        }
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'avg_download_count',
        align : 'right',
        width : width * 0.1,
        sorttype : 'number',
        formatter : function(val, opt, rdt) {
            return val ? StringUtil.comma_separated(val) : 'ー';
        }
    }));

    var data = self.createAppData();
    var pager = '';
    var search = false;
    if (data.length > 10) {
        var pager = '#pager-app';
        var search = true;
    }

    var rowList = [ 10, 20, 50 ];
    if (data.length > 50) {
        rowList.push(data.length);
    }

    var option = {
        colNames : [ 'グラフ描画', 'IP名', 'アプリ名', 'プラットフォーム', '発売元', '発売日', '累計売上', '累計ダウンロード数', '平均売上', '平均ダウンロード数' ],
        colModel : medelArray,
        data : data,
        width : width,
        pager : pager,
        pgbuttons : false,
        pginput : false,
        rowList : rowList,
        loadComplete : function() {
            if ($('.app-graph-checkbox:checked').length == 5) {
                $('.app-graph-checkbox:not(:checked)').prop('disabled', true);
            }
            self.isDrawGridForApp = true;
            $('.app-graph-checkbox').on('click', function() {
                var elem = $(this);
                var val = elem.attr('data-row');
                self.isAppChecked[val] = elem.is(':checked');
                if ($('.app-graph-checkbox:checked').length == 5) {
                    $('.app-graph-checkbox:not(:checked)').prop('disabled', true);
                } else {
                    console.log($('.app-graph-checkbox:checked').length)
                    $('.app-graph-checkbox:not(:checked)').prop('disabled', false);
                }

            });
        }
    };
    GridUtil.renderNormalGrid('#grid-app', option, search);

}
/**
 * アプリGridのデータを作成する。
 *
 */
CompareController.prototype.createAppData = function() {
    var self = this;

    var data = [];
    for (var i = 0; i <= djangoObj.app.length; i++) {
        if (djangoObj.app[i]) {
            var row = [];
            row.push([ i, djangoObj.app[i].app_name ]);
            row.push([ djangoObj.app[i].ip_code, djangoObj.app[i].ip_name ]);
            row.push(djangoObj.app[i].app_name);
            row.push(djangoObj.app[i].platform);
            row.push(djangoObj.app[i].distributor_name);
            row.push(djangoObj.app[i].release_date);
            row.push(djangoObj.app[i].total_sales);
            row.push(djangoObj.app[i].total_download_count);
            row.push(djangoObj.app[i].avg_sales);
            row.push(djangoObj.app[i].avg_download_count);
            data.push(row);
        }
    }
    var colNames = [ 'is_draw', 'ip_name', 'app_name', 'platform', 'distributor_name', 'release_date', 'total_sales', 'total_download_count', 'avg_sales', 'avg_download_count' ];
    return GridUtil.createGridData(colNames, data);
}

// リストに対象の要素が含まれているか判定
CompareController.prototype.includes = function(array, target) {
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
    var controller = new CompareController();
    controller.init();
});
=======
var CompareController = function() {

    // 年代別男女比グラフのオプション
    this.genderRatioGraphOption = {
        title : '<div style="float: left; width: 50%; text-align: center;">男性</div><div style="float: right; width: 50%; text-align: center;">女性</div>',
        seriesDefaults : {
            renderer : jQuery.jqplot.PyramidRenderer,
            rendererOptions : {
                barPadding : 15
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
                tickOptions : {
                    formatString : "%'d"
                },
            },
            yaxis : {
                labelRenderer : jQuery.jqplot.CanvasAxisLabelRenderer,
                showMinorTicks : true,
                ticks : [ "51歳以上", "46歳~50歳", "41歳~45歳", "36歳~40歳", "31歳~35歳", "26歳~30歳", "21歳~25歳", "16歳~20歳", "11歳~15歳" ],
                rendererOptions : {
                    category : true,
                    baselineWidth : 2
                }
            },
            y2axis : {
                labelRenderer : jQuery.jqplot.CanvasAxisLabelRenderer,
                showMinorTicks : true,
                ticks : [ "51歳以上", "46歳~50歳", "41歳~45歳", "36歳~40歳", "31歳~35歳", "26歳~30歳", "21歳~25歳", "16歳~20歳", "11歳~15歳" ],
                rendererOptions : {
                    category : true,
                    baselineWidth : 2
                }
            }
        },
        height : 380,
        cursor : {
            zoom : false,
            showTooltip : true
        }
    };

    // グラフのオプション
    this.commonOptions = {
        colorArray : [ "#cddf54", "#fbd179", "#26B4E3", "#bd70c7" ],
        option : {
            seriesDefaults : {
                pointLabels : {
                    show : true,
                    formatString : "%'d"
                }
            },
            title : "フォロワー数",
            legend : {
                show : true,
                placement : "outsideGrid",
                location : "s"
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
                    min : (function() {
                        var dt = new Date();
                        dt.setDate(1);
                        dt.setFullYear(dt.getFullYear() - 1);
                        dt.setMonth(dt.getMonth() - 1);
                        return dt.getFullYear() + '-' + StringUtil.lpad(dt.getMonth()+1, 2) + '-' + StringUtil.lpad(dt.getDate(), 2)
                    }()),
                    max : (function() {
                        var dt = new Date();
                        dt.setDate(1);
                        return dt.getFullYear() + '-' + StringUtil.lpad(dt.getMonth()+1, 2) + '-' + StringUtil.lpad(dt.getDate(), 2);
                    }()),

                },
                yaxis : {
                    min : 0,
                    tickOptions : {
                        formatString : "%'d"
                    }
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
            }
        }
    };

};
CompareController.prototype = new AbstractController();

/**
 * メニュー選択処理
 */
CompareController.prototype.selectedMenu = function() {
    return '.compare';
};

/**
 * 比較画面の主処理
 */
CompareController.prototype.execute = function() {
    if (djangoObj.sakuhin_not_found) {
        return $.Deferred().resolve().promise();
    }
    if (djangoObj.no_session_data) {
        return $.Deferred().resolve().promise();
    }

    var self = this;

    // 表を描画する
    self.drawGrid();

    // "Nか月目"グラフの最初と最後のtickを削除するhookを登録
    $.jqplot.postDrawHooks.push(function() {
        var graph_id = this.targetId;
        var nthArray = [ '#manga-graph1', '#manga-graph2', '#game-graph1', '#app-graph-sales1', '#app-graph-download1' ]
        if (self.includes(nthArray, graph_id)) {
            $(graph_id + " .jqplot-xaxis .jqplot-xaxis-tick:first-child").remove();
            $(graph_id + " .jqplot-xaxis .jqplot-xaxis-tick:last-child").remove();
        }
    })

    // 男女比グラフ
    self.plotGenderRatio();

    // Twitterグラフ表示
    self.plotTwitterGraph();

    // マンガグラフ表示
    self.plotMangaGraph();

    // ゲームグラフ表示
    self.plotGameGraph();

    // アプリグラフ表示
    self.plotAppGraph();

    $(".link").click(function() {
        window.location.href = "./03_ip_detail.html";
    });

    return $.Deferred().resolve().promise();
};

CompareController.prototype.plotGenderRatio = function() {
    var self = this;
    djangoObj.gender_ratio.forEach(function(obj, index) {
        var param = {
            'gender-ratio' : index,
            'sakuhin_code' : obj.sakuhin_code
        };
        AjaxUtil.get('/ipdds/compare/', param, function(data) {
            self.callbackGenderRatio(data, self.genderRatioGraphOption, index, obj.total);
        })
    });
}

CompareController.prototype.callbackGenderRatio = function(data, options, index, total) {
    var self = this;
    var result = JSON.parse(data.toString());
    if(result.length == 0){
        result.push([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]);
    }
    var male = result[0].slice(0, 9);
    var female = result[0].slice(9);
    var target = "gender-ratio-graph" + (index + 1);

    // データ最大値が3以下の場合目盛りがおかしくなるため
    if (self.isGt3(male) || self.isGt3(female)) {
        options.axes.xaxis.padMin = 2;
        options.axes.xaxis.padMax = 2;
    } else {
        delete options.axes.xaxis.padMin;
        delete options.axes.xaxis.padMax;
    }
    // グラフを描画する
    jQuery.jqplot(target, [ male, female ], options);
    $('#' + target).dblclick(function(e) {
        e.stopPropagation();
    });

    // データが０件の場合、グラフに「データなし」Maskを追加する
    if (total == 0) {
        NoDateUtil.overlay('gender-ratio-graph' + (index + 1));
    }
};

CompareController.prototype.isGt3 = function(data) {
    // データ最大値が3以下の場合目盛りがおかしくなるため
    var is_gt_3 = true;
    data.forEach(function(obj) {
        if (obj > 3) {
            is_gt_3 = false;
        }
    })
    return is_gt_3;
}

CompareController.prototype.twitterGraphInfo = [ {
    options : {
        title : 'フォロワー数'
    }
} ];

CompareController.prototype.plotTwitterGraph = function() {
    var self = this;
    // options定義
    var copiedOptions = jQuery.extend(true, {}, self.commonOptions.option);
    copiedOptions.highlighter = {
        show : true,
        showMarker : true,
        sizeAdjust : 7,
        tooltipLocation : "ne",
        tooltipAxes : "y",
        formatString : "フォロワー数:%s"
    }

    // グラフのラベル定義
    var series = [];
    var series2 = [];
    var data2 = [];
    var promiseArr = [];
    djangoObj.twitter.forEach(function(obj, index) {
        // 作品ごとにTwitterのデータ取得
        promiseArr.push(self.getTwitterGraphData(obj.twitter_id, obj.sakuhin_name));
    });

    // 作品ごとのデータを取得後にグラフ１及びグラフ２を描画する
    $.when.apply($, promiseArr).then(function() {
        var values = Array.prototype.slice.call(arguments);
        var graphTwitterData = [];
        var twiter_user;
        var twiter_user_index;
        values.forEach(function(val, i) {
            if (val) {
                series2.push({
                    name : val[1],
                    label : val[1],
                    color : self.commonOptions.colorArray[i]
                });
                data2.push(val[0]);

                var selector1 = '.twitter-graph-checkbox';
                var selector2 = 'input[value="' + val[1] + '"]';

                if ($(selector1).filter(selector2).is(':checked')) {
                    graphTwitterData.push(val[0]);
                    // グラフのラベルを設定
                    series.push({
                        label : val[1],
                        color : self.commonOptions.colorArray[i]
                    });
                }
            }
        });

        // グラフのラベルを設定
        copiedOptions.series = series;
        copiedOptions.series2 = series2;
        copiedOptions.data2 = data2;
        // Twitterのグラフを描画
        self.createGraph("twiter-follower-graph", self.twitterGraphInfo, 0, graphTwitterData, copiedOptions);

        $('#twiter-follower-graph').dblclick(function(e) {
            e.stopPropagation();
        });
    });

    // 再描画のイベントを設定
    GridUtil.bindReplot('twitter-replot-button', 'twitter-graph-checkbox', self.twitterGraphInfo);
}

CompareController.prototype.getTwitterGraphData = function(twitter_id, sakuhin_name) {
    var dtd = $.Deferred();
    var param = {
        'twitter' : 'twitter',
        'twitter_id' : twitter_id
    };
    AjaxUtil.get('/ipdds/compare', param, function(data) {
        var result = JSON.parse(data.toString());
        if (result.length != 0) {
            // グラフ１データ
            var graphTwitterData = [];
            result.forEach(function(val) {
                graphTwitterData.push([ val[0], val[1] ]);
            });
            dtd.resolve([ graphTwitterData, sakuhin_name ]);
        } else {
            dtd.resolve(null);
        }
    })
    return dtd;
}

CompareController.prototype.mangaGraphInfo = [ {
    options : {
        title : '累計発行部数（発売日からNか月）'
    }
}, {
    options : {
        title : '平均発行部数（単巻あたり）(発売日からNか月）'
    }
}, {
    options : {
        title : '累計発行部数'
    }
}, {
    options : {
        title : '累計発行部数（１巻）'
    }
}, {
    options : {
        title : '累計発行部数（最新巻）'
    }
}, {
    options : {
        title : '平均発行部数（単巻あたり）'
    }
} ];

CompareController.prototype.plotMangaGraph = function() {
    var self = this;

    // 累計発行部数(発売日からNか月）
    self.plotMangaGraph1();
    // 平均発行部数（単巻あたり）(発売日からNか月）
    self.plotMangaGraph2();
    // // 累計発行部数
    self.plotMangaGraph3();
    // // 平均発行部数（単巻あたり）
    self.plotMangaGraph6();
    // // 累計発行部数（１巻）
    self.plotMangaGraph4();
    // // 累計発行部数（最新巻）
    self.plotMangaGraph5();

    // 再描画のイベントを設定
    GridUtil.bindReplot('manga-replot-button', 'manga-graph-checkbox', self.mangaGraphInfo);
}

CompareController.prototype.plotMangaGraph1 = function() {
    var self = this;

    // Options定義
    var copiedOptions = jQuery.extend(true, {}, self.commonOptions.option);
    copiedOptions.axes = {
        xaxis : {
            renderer : $.jqplot.DateAxisRenderer,
            tickRenderer : $.jqplot.CanvasAxisTickRenderer,
            tickInterval : "1 months",
            tickOptions : {
                angle : -45,
                formatString : "%#mヵ月目"
            },
            min : '1999-12-01',
            max : '2001-01-01'
        },
        yaxis : {
            min : 0,
            tickOptions : {
                formatString : "%'d"
            }
        }
    };

    // グラフのラベル定義
    var series = [];
    var series2 = [];
    var data2 = [];
    // ajaxから返却したデータ
    var promiseArr = [];
    djangoObj.manga.forEach(function(obj, index) {
        // mangaCodeごとにデータ取得
        promiseArr.push(self.getGraph1_2Data(obj.manga_code, obj.manga_name));
    });

    // mangaCodeごとのデータを取得後にグラフ１及びグラフ２を描画する
    $.when.apply($, promiseArr).then(function() {
        var values = Array.prototype.slice.call(arguments);
        var graph1Data = [];
        values.forEach(function(val, i) {
            if (val) {
                series2.push({
                    name : val[2] + val[3],
                    label : "<span>"+ val[2] +"</span><span style='display:none'>"+ val[3] +"</span>",
                    color : self.commonOptions.colorArray[i]
                });
                val[0].map(function(e, i) {
                    e[0] = '2000-' + StringUtil.lpad((i + 1), 2) + '-01';
                });
                data2.push(val[0]);
                var selector1 = '.manga-graph-checkbox';
                var selector2 = 'input[value="' + val[2] + val[3] + '"]';

                if ($(selector1).filter(selector2).is(':checked')) {
                    val[0].map(function(e, i) {
                        e[0] = '2000-' + StringUtil.lpad((i + 1), 2) + '-01';
                    });
                    graph1Data.push(val[0]);
                    // グラフのラベルを設定
                    series.push({
                        // label : val[2],
                        label : "<span>"+ val[2] +"</span><span style='display:none'>"+ val[3] +"</span>",
                        color : self.commonOptions.colorArray[i]
                    });
                }
            }
        });

        // グラフのラベルを設定
        copiedOptions.series = series;
        copiedOptions.series2 = series2;
        copiedOptions.data2 = data2;
        // グラフ1（累計発行部数(発売日からNか月））を描画
        self.createGraph("manga-graph1", self.mangaGraphInfo, 0, graph1Data, copiedOptions);
    })
}

CompareController.prototype.plotMangaGraph2 = function() {
    var self = this;

    // Options定義
    var copiedOptions = jQuery.extend(true, {}, self.commonOptions.option);
    copiedOptions.axes = {
        xaxis : {
            renderer : $.jqplot.DateAxisRenderer,
            tickRenderer : $.jqplot.CanvasAxisTickRenderer,
            tickInterval : "1 months",
            tickOptions : {
                angle : -45,
                formatString : "%#mヵ月目"
            },
            min : '1999-12-01',
            max : '2001-01-01'
        },
        yaxis : {
            min : 0,
            tickOptions : {
                formatString : "%'d"
            }
        }
    };

    // グラフのラベル定義
    var series = [];
    var series2 = [];
    var data2 = [];
    // ajaxから返却したデータ
    var promiseArr = [];
    djangoObj.manga.forEach(function(obj, index) {
        // マンガコードごとにデータ取得
        promiseArr.push(self.getGraph1_2Data(obj.manga_code, obj.manga_name));
    });

    // マンガコードごとのデータを取得後にグラフ１及びグラフ２を描画する
    $.when.apply($, promiseArr).then(function() {
        var values = Array.prototype.slice.call(arguments);
        var graph2Data = [];
        values.forEach(function(val, i) {
            if (val) {
                series2.push({
                    name : val[2] + val[3],
                    label : "<span>"+ val[2] +"</span><span style='display:none'>"+ val[3] +"</span>",
                    color : self.commonOptions.colorArray[i]
                });
                val[1].map(function(e, i) {
                    e[0] = '2000-' + StringUtil.lpad((i + 1), 2) + '-01';
                });
                data2.push(val[1]);
                var selector1 = '.manga-graph-checkbox';
                var selector2 = 'input[value="' + val[2] + val[3] + '"]';

                if ($(selector1).filter(selector2).is(':checked')) {
                    val[1].map(function(e, i) {
                        e[0] = '2000-' + StringUtil.lpad((i + 1), 2) + '-01';
                    });
                    graph2Data.push(val[1]);
                    // グラフのラベルを設定
                    series.push({
                        label : "<span>"+ val[2] +"</span><span style='display:none'>"+ val[3] +"</span>",
                        color : self.commonOptions.colorArray[i]
                    });
                }
            }
        });

        // グラフのラベルを設定
        copiedOptions.series = series;
        copiedOptions.series2 = series2;
        copiedOptions.data2 = data2;
        // グラフ１（累計発行部数(発売日からNか月））を描画
        self.createGraph("manga-graph2", self.mangaGraphInfo, 1, graph2Data, copiedOptions);
    });
}

CompareController.prototype.getGraph1_2Data = function(manga_code, manga_name) {
    var dtd = $.Deferred();
    var param = {
        'manga1' : 'manga1',
        'manga_code' : manga_code
    };
    AjaxUtil.get('/ipdds/compare', param, function(data) {
        var result = JSON.parse(data.toString());
        if (result.length != 0) {
            // グラフ１データ
            var graph1Data = [];
            // グラフ２データ
            var graph2Data = [];
            result.forEach(function(val) {
                graph1Data.push([ val[0], val[1] ]);
                graph2Data.push([ val[0], val[2] ]);
            });
            dtd.resolve([ graph1Data, graph2Data, manga_name, manga_code ]);
        } else {
            dtd.resolve(null);
        }
    })
    return dtd;
}

CompareController.prototype.plotMangaGraph3 = function() {
    var self = this;
    // Options定義
    var copiedOptions = jQuery.extend(true, {}, self.commonOptions.option);

    // グラフのラベル定義
    var series = [];
    var series2 = [];
    var data2 = [];
    var promiseArr = [];
    djangoObj.manga.forEach(function(obj, index) {
        // マンガコードごとに累計発行部数と平均発行部数（単巻あたり）のデータ取得
        promiseArr.push(self.getGraph3_6Data(obj.manga_code, obj.manga_name));
    });

    // マンガコードごとのデータを取得後にグラフを描画する
    $.when.apply($, promiseArr).then(function() {
        var values = Array.prototype.slice.call(arguments);
        var graph3Data = [];
        values.forEach(function(val, i) {
            if (val) {
                series2.push({
                    name : val[2] + val[3],
                    label : "<span>"+ val[2] +"</span><span style='display:none'>"+ val[3] +"</span>",
                    color : self.commonOptions.colorArray[i]
                });
                data2.push(val[0]);

                var selector1 = '.manga-graph-checkbox';
                var selector2 = 'input[value="' + val[2] + val[3] + '"]';

                if ($(selector1).filter(selector2).is(':checked')) {
                    graph3Data.push(val[0]);
                    // グラフのラベルを設定
                    series.push({
                        label : "<span>"+ val[2] +"</span><span style='display:none'>"+ val[3] +"</span>",
                        color : self.commonOptions.colorArray[i]
                    });
                }
            }
        });

        // グラフのラベルを設定
        copiedOptions.series = series;
        copiedOptions.series2 = series2;
        copiedOptions.data2 = data2;
        // グラフ（累計発行部数(直近一年））を描画
        self.createGraph("manga-graph3", self.mangaGraphInfo, 2, graph3Data, copiedOptions);
    })
}

CompareController.prototype.plotMangaGraph6 = function() {
    var self = this;
    // Options定義
    var copiedOptions = jQuery.extend(true, {}, self.commonOptions.option);

    // グラフのラベル定義
    var series = [];
    var series2 = [];
    var data2 = [];
    var promiseArr = [];
    djangoObj.manga.forEach(function(obj, index) {
        // マンガコードごとに累計発行部数と平均発行部数（単巻あたり）のデータ取得
        promiseArr.push(self.getGraph3_6Data(obj.manga_code, obj.manga_name));
    });

    // マンガコードごとのデータを取得後にグラフを描画する
    $.when.apply($, promiseArr).then(function() {
        var values = Array.prototype.slice.call(arguments);
        var graph6Data = [];
        values.forEach(function(val, i) {
            if (val) {
                series2.push({
                    name : val[2] + val[3],
                    label : "<span>"+ val[2] +"</span><span style='display:none'>"+ val[3] +"</span>",
                    color : self.commonOptions.colorArray[i]
                });
                data2.push(val[1]);

                var selector1 = '.manga-graph-checkbox';
                var selector2 = 'input[value="' + val[2] + val[3] + '"]';

                if ($(selector1).filter(selector2).is(':checked')) {
                    graph6Data.push(val[1]);
                    // グラフのラベルを設定
                    series.push({
                        label : "<span>"+ val[2] +"</span><span style='display:none'>"+ val[3] +"</span>",
                        color : self.commonOptions.colorArray[i]
                    });
                }
            }
        });

        // グラフのラベルを設定
        copiedOptions.series = series;
        copiedOptions.series2 = series2;
        copiedOptions.data2 = data2;
        // グラフ（平均発行部数（単巻あたり）(直近一年））を描画
        self.createGraph("manga-graph6", self.mangaGraphInfo, 5, graph6Data, copiedOptions);
    })
}

CompareController.prototype.getGraph3_6Data = function(manga_code, manga_name) {
    var dtd = $.Deferred();
    var param = {
        'manga3' : 'manga3',
        'manga_code' : manga_code
    };
    AjaxUtil.get('/ipdds/compare', param, function(data) {
        var result = JSON.parse(data.toString());
        if (result.length != 0) {
            // グラフ（累計発行部数）データ
            var graph3Data = [];
            // グラフ（平均発行部数（単巻あたり））データ
            var graph6Data = [];
            result.forEach(function(val) {
                graph3Data.push([ val[0], val[1] ]);
                graph6Data.push([ val[0], val[2] ]);
            });
            dtd.resolve([ graph3Data, graph6Data, manga_name, manga_code ]);
        } else {
            dtd.resolve(null);
        }
    })
    return dtd;
}

CompareController.prototype.plotMangaGraph4 = function() {
    var self = this;
    // Options定義
    var copiedOptions = jQuery.extend(true, {}, self.commonOptions.option);

    // グラフのラベル定義
    var series = [];
    var series2 = [];
    var data2 = [];
    var promiseArr = [];
    djangoObj.manga.forEach(function(obj, index) {
        // マンガコードごとに累計発行部数(1巻）のデータ取得
        promiseArr.push(self.getGraph4Data(obj.manga_code, obj.manga_name));
    });

    // マンガコードごとのデータを取得後に累計発行部数(1巻）グラフを描画する
    $.when.apply($, promiseArr).then(function() {
        var values = Array.prototype.slice.call(arguments);
        var graph4Data = [];
        values.forEach(function(val, i) {
            if (val) {
                series2.push({
                    name : val[1] + val[2],
                    label : "<span>"+ val[1] +"</span><span style='display:none'>"+ val[2] +"</span>",
                    color : self.commonOptions.colorArray[i]
                });
                data2.push(val[0]);

                var selector1 = '.manga-graph-checkbox';
                var selector2 = 'input[value="' + val[1] + val[2] + '"]';

                if ($(selector1).filter(selector2).is(':checked')) {
                    graph4Data.push(val[0]);
                    // グラフのラベルを設定
                    series.push({
                        label : "<span>"+ val[1] +"</span><span style='display:none'>"+ val[2] +"</span>",
                        color : self.commonOptions.colorArray[i]
                    });
                }
            }
        });

        // グラフのラベルを設定
        copiedOptions.series = series;
        copiedOptions.series2 = series2;
        copiedOptions.data2 = data2;
        self.createGraph("manga-graph4", self.mangaGraphInfo, 3, graph4Data, copiedOptions);
        // グラフ4（累計発行部数(1巻））を描画
    })
}

CompareController.prototype.getGraph4Data = function(manga_code, manga_name) {
    var dtd = $.Deferred();
    var param = {
        'manga4' : 'manga4',
        'manga_code' : manga_code
    };
    AjaxUtil.get('/ipdds/compare', param, function(data) {
        var result = JSON.parse(data.toString());
        if (result.length != 0) {
            // グラフ4（累計発行部数(1巻））データ
            var graph4Data = [];
            result.forEach(function(val) {
                graph4Data.push([ val[0], val[1] ]);
            });
            dtd.resolve([ graph4Data, manga_name, manga_code ]);
        } else {
            dtd.resolve(null);
        }
    })
    return dtd;
}

CompareController.prototype.plotMangaGraph5 = function() {
    var self = this;

    // Options定義
    var copiedOptions = jQuery.extend(true, {}, self.commonOptions.option);

    // グラフのラベル定義
    var series = [];
    var series2 = [];
    var data2 = [];
    var promiseArr = [];
    djangoObj.manga.forEach(function(obj, index) {
        // マンガコードごとに累計発行部数(最新巻）のデータ取得
        promiseArr.push(self.getGraph5Data(obj.manga_code, obj.manga_name));
    });

    // マンガコードごとのデータを取得後に累計発行部数(最新巻）グラフを描画する
    $.when.apply($, promiseArr).then(function() {
        var values = Array.prototype.slice.call(arguments);
        var graph5Data = [];
        values.forEach(function(val, i) {
            if (val) {
                series2.push({
                    name : val[1] + val[2],
                    label : "<span>"+ val[1] +"</span><span style='display:none'>"+ val[2] +"</span>",
                    color : self.commonOptions.colorArray[i]
                });
                data2.push(val[0]);

                var selector1 = '.manga-graph-checkbox';
                var selector2 = 'input[value="' + val[1] + val[2]+ '"]';

                if ($(selector1).filter(selector2).is(':checked')) {
                    graph5Data.push(val[0]);
                    // グラフのラベルを設定
                    series.push({
                        label : "<span>"+ val[1] +"</span><span style='display:none'>"+ val[2] +"</span>",
                        color : self.commonOptions.colorArray[i]
                    });
                }
            }
        });

        // グラフのラベルを設定
        copiedOptions.series = series;
        copiedOptions.series2 = series2;
        copiedOptions.data2 = data2;
        // グラフ4（累計発行部数(最新巻））を描画
        self.createGraph("manga-graph5", self.mangaGraphInfo, 4, graph5Data, copiedOptions);
    })
}

CompareController.prototype.getGraph5Data = function(manga_code, manga_name) {
    var dtd = $.Deferred();
    var param = {
        'manga5' : 'manga5',
        'manga_code' : manga_code
    };
    AjaxUtil.get('/ipdds/compare', param, function(data) {
        var result = JSON.parse(data.toString());
        if (result.length != 0) {
            // グラフ5（累計発行部数(最新巻））データ
            var graph5Data = [];
            result.forEach(function(val) {
                graph5Data.push([ val[0], val[1] ]);
            });
            dtd.resolve([ graph5Data, manga_name, manga_code ]);
        } else {
            dtd.resolve(null);
        }
    })
    return dtd;
}

CompareController.prototype.gameGraphInfo = [ {
    options : {
        title : '累計売上本数(発売日からNか月)'
    }
}, {
    options : {
        title : '累計売上本数'
    }
} ];

CompareController.prototype.plotGameGraph = function() {
    var self = this;
    // 累計売上本数(発売日からNか月)
    self.plotGameGraph1();
    // 累計売上本数
    self.plotGameGraph2();

    // 再描画のイベントを設定
    GridUtil.bindReplot('game-replot-button', 'game-graph-checkbox', self.gameGraphInfo);
}

CompareController.prototype.plotGameGraph1 = function() {
    var self = this;

    // options定義
    var copiedOptions = jQuery.extend(true, {}, self.commonOptions.option);
    copiedOptions.axes = {
        xaxis : {
            renderer : $.jqplot.DateAxisRenderer,
            tickRenderer : $.jqplot.CanvasAxisTickRenderer,
            tickInterval : "1 months",
            tickOptions : {
                angle : -45,
                formatString : "%#mヵ月目"
            },
            min : '1999-12-01',
            max : '2001-01-01'
        },
        yaxis : {
            min : 0,
            tickOptions : {
                formatString : "%'d"
            }
        }
    };
    copiedOptions.highlighter = {
        show : true,
        showMarker : true,
        sizeAdjust : 7,
        tooltipLocation : "ne",
        tooltipAxes : "y",
        formatString : "本数:%s"
    }

    // グラフのラベル定義
    var series = [];
    var series2 = [];
    var data2 = [];
    var promiseArr = [];
    djangoObj.game.forEach(function(obj, index) {
        // ゲームタイトルコードごとにデータ取得
        promiseArr.push(self.getGameGraph1Data(obj.game_title_code, obj.game_title_name +'/ '+ obj.platform_name +'/ '+ obj.release_yyyymmdd));
    });

    // ゲームタイトルコードごとのデータを取得後にゲームグラフ１を描画する
    $.when.apply($, promiseArr).then(function() {
        var values = Array.prototype.slice.call(arguments);
        var gamegraph1Data = [];
        values.forEach(function(val, i) {
            if (val) {
                series2.push({
                    name : val[1],
                    label : val[1],
                    color : self.commonOptions.colorArray[i]
                });
                val[0].map(function(e, i) {
                    e[0] = '2000-' + StringUtil.lpad((i + 1), 2) + '-01';
                });
                data2.push(val[0]);
                var selector1 = '.game-graph-checkbox';
                var selector2 = 'input[value="' + val[1] + '"]';

                if ($(selector1).filter(selector2).is(':checked')) {
                    val[0].map(function(e, i) {
                        e[0] = '2000-' + StringUtil.lpad((i + 1), 2) + '-01';
                    });
                    gamegraph1Data.push(val[0]);
                    // グラフのラベルを設定
                    series.push({
                        label : val[1],
                        color : self.commonOptions.colorArray[i]
                    });
                }
            }
        });

        // グラフのラベルを設定
        copiedOptions.series = series;
        copiedOptions.series2 = series2;
        copiedOptions.data2 = data2;
        // グラフ１（累計発行部数(発売日からNか月））を描画
        self.createGraph("game-graph1", self.gameGraphInfo, 0, gamegraph1Data, copiedOptions);
    });
}

CompareController.prototype.getGameGraph1Data = function(game_title_code, game_title_name) {
    var dtd = $.Deferred();
    var param = {
        'game1' : 'game1',
        'game_title_code' : game_title_code
    };
    AjaxUtil.get('/ipdds/compare', param, function(data) {
        var result = JSON.parse(data.toString());
        if (result.length != 0) {
            // グラフ１データ
            var gamegraph1Data = [];
            result.forEach(function(val) {
                gamegraph1Data.push([ val[0], val[1] ]);
            });
            dtd.resolve([ gamegraph1Data, game_title_name ]);
        } else {
            dtd.resolve(null);
        }
    })
    return dtd;
}

CompareController.prototype.plotGameGraph2 = function() {
    var self = this;

    // Options定義
    var copiedOptions = jQuery.extend(true, {}, self.commonOptions.option);
    copiedOptions.highlighter = {
        show : true,
        showMarker : true,
        sizeAdjust : 7,
        tooltipLocation : "ne",
        tooltipAxes : "y",
        formatString : "本数:%s"
    }

    // グラフのラベル定義
    var series = [];
    var series2 = [];
    var data2 = [];
    var promiseArr = [];
    djangoObj.game.forEach(function(obj, index) {
        // ゲームタイトルコードごとにデータ取得
        promiseArr.push(self.getGameGraph2Data(obj.game_title_code, obj.game_title_name +'/ '+ obj.platform_name +'/ '+ obj.release_yyyymmdd));
    });

    // ゲームタイトルコードごとのデータを取得後にグラフを描画する
    $.when.apply($, promiseArr).then(function() {
        var values = Array.prototype.slice.call(arguments);
        var gamegraph2Data = [];
        values.forEach(function(val, i) {
            if (val) {
                series2.push({
                    name : val[1],
                    label : val[1],
                    color : self.commonOptions.colorArray[i]
                });
                data2.push(val[0]);

                var selector1 = '.game-graph-checkbox';
                var selector2 = 'input[value="' + val[1] + '"]';

                if ($(selector1).filter(selector2).is(':checked')) {
                    gamegraph2Data.push(val[0]);
                    // グラフのラベルを設定
                    series.push({
                        label : val[1],
                        color : self.commonOptions.colorArray[i]
                    });
                }
            }
        });

        // グラフのラベルを設定
        copiedOptions.series = series;
        copiedOptions.series2 = series2;
        copiedOptions.data2 = data2;
        // グラフ（累計売上本数）を描画
        self.createGraph("game-graph2", self.gameGraphInfo, 1, gamegraph2Data, copiedOptions);
    });
}

CompareController.prototype.getGameGraph2Data = function(game_title_code, game_title_name) {
    var dtd = $.Deferred();
    var param = {
        'game2' : 'game2',
        'game_title_code' : game_title_code
    };
    AjaxUtil.get('/ipdds/compare', param, function(data) {
        var result = JSON.parse(data.toString());
        if (result.length != 0) {
            // グラフ１データ
            var gamegraph2Data = [];
            result.forEach(function(val) {
                gamegraph2Data.push([ val[0], val[1] ]);
            });
            dtd.resolve([ gamegraph2Data, game_title_name ]);
        } else {
            dtd.resolve(null);
        }
    })
    return dtd;
}

CompareController.prototype.appGraphInfo = [ {
    options : {
        title : '累計売上(発売日からNか月)'
    }
}, {
    options : {
        title : '累計ダウンロード数(発売日からNか月)'
    }
}, {
    options : {
        title : '累計売上'
    }
}, {
    options : {
        title : '累計ダウンロード数'
    }
}, {
    options : {
        title : '平均売上'
    }
}, {
    options : {
        title : '平均ダウンロード数'
    }
} ];

CompareController.prototype.plotAppGraph = function() {
    var self = this;
    // 累計売上(発売日からNか月)
    self.plotAppSalesGraph1();
    // // 累計売上
    self.plotAppSalesGraph2();
    // 平均売上
    self.plotAppAvgSalesGraph();
    // 平均ダウンロード数
    self.plotAppAvgDownloadGraph();
    // 累計ダウンロード数(発売日からNか月)
    self.plotAppDownloadGraph1();
    // 累計ダウンロード数
    self.plotAppDownloadGraph2();

    // 再描画のイベントを設定
    GridUtil.bindReplot('app-replot-button', 'app-graph-checkbox', self.appGraphInfo);
}

CompareController.prototype.plotAppSalesGraph1 = function() {
    var self = this;

    // Options定義
    var copiedOptions = jQuery.extend(true, {}, self.commonOptions.option);
    copiedOptions.axes = {
        xaxis : {
            renderer : $.jqplot.DateAxisRenderer,
            tickRenderer : $.jqplot.CanvasAxisTickRenderer,
            tickInterval : "1 months",
            tickOptions : {
                angle : -45,
                formatString : "%#mヵ月目"
            },
            min : '1999-12-01',
            max : '2001-01-01'
        },
        yaxis : {
            min : 0,
            tickOptions : {
                formatString : "%'d"
            }
        }
    };
    // アプリグラフ（累計売上（発売日からNか月））を描画
    copiedOptions.highlighter = {
        show : true,
        showMarker : true,
        sizeAdjust : 7,
        tooltipLocation : "ne",
        tooltipAxes : "y",
        formatString : "売上:%s"
    }

    // グラフのラベル定義
    var series = [];
    var series2 = [];
    var data2 = [];
    // ajaxから返却したデータ
    var promiseArr = [];
    djangoObj.app.forEach(function(obj, index) {
        // アプリタイトルコードごとにデータ取得
        promiseArr.push(self.getAppSalesGraph1Data(obj.app_title_code, obj.app_title_name,obj.app_id_ios,obj.app_id_android));
    });

    // アプリタイトルコードごとのデータを取得後にアプリのグラフ１(累計売上（発売日からNか月）)を描画する
    $.when.apply($, promiseArr).then(function() {
        var values = Array.prototype.slice.call(arguments);
        var appSalesGraph1Data = [];
        values.forEach(function(val, i) {
            if (val) {
                series2.push({
                    name : val[1] + val[2],
                    label : "<span>"+ val[1] +"</span><span style='display:none'>"+ val[2] +"</span>",
                    color : self.commonOptions.colorArray[i]
                });
                val[0].map(function(e, i) {
                    e[0] = '2000-' + StringUtil.lpad((i + 1), 2) + '-01';
                });
                data2.push(val[0]);
                var selector1 = '.app-graph-checkbox';
                var selector2 = 'input[value="' + val[1] + val[2] + '"]';

                if ($(selector1).filter(selector2).is(':checked')) {
                    val[0].map(function(e, i) {
                        e[0] = '2000-' + StringUtil.lpad((i + 1), 2) + '-01';
                    });
                    appSalesGraph1Data.push(val[0]);
                    // グラフのラベルを設定
                    series.push({
                        label : "<span>"+ val[1] +"</span><span style='display:none'>"+ val[2] +"</span>",
                        color : self.commonOptions.colorArray[i]
                    });
                }
            }
        });

        // グラフのラベルを設定
        copiedOptions.series = series;
        copiedOptions.series2 = series2;
        copiedOptions.data2 = data2;

        // アプリグラフ１（累計売上(発売日からNか月））を描画
        self.createGraph("app-graph-sales1", self.appGraphInfo, 0, appSalesGraph1Data, copiedOptions);
    });
}

CompareController.prototype.getAppSalesGraph1Data = function(app_title_code, app_title_name,app_id_ios,app_id_android) {
    var dtd = $.Deferred();
    var param = {
        'appSales1' : 'appSales1',
        'app_title_code' : app_title_code,
        'app_title_name' : app_title_name,
        'app_id_ios' : app_id_ios,
        'app_id_android' : app_id_android
    };
    AjaxUtil.get('/ipdds/compare', param, function(data) {
        var result = JSON.parse(data.toString());
        if (result.length != 0) {
            // Appグラフ１データ
            var appSalesGraph1Data = [];
            result.forEach(function(val) {
                appSalesGraph1Data.push([ val[0], val[1] ]);
            });
            dtd.resolve([ appSalesGraph1Data, app_title_name, app_title_code ]);
        } else {
            dtd.resolve(null);
        }
    })
    return dtd;
}

CompareController.prototype.plotAppSalesGraph2 = function() {
    var self = this;

    // Options定義
    var copiedOptions = jQuery.extend(true, {}, self.commonOptions.option);
    // アプリグラフ（平均売上）を描画
    copiedOptions.highlighter = {
        show : true,
        showMarker : true,
        sizeAdjust : 7,
        tooltipLocation : "ne",
        tooltipAxes : "y",
        formatString : "売上:%s"
    }

    // グラフのラベル定義
    var series = [];
    var series2 = [];
    var data2 = [];
    // ajaxから返却したデータ
    var promiseArr = [];
    djangoObj.app.forEach(function(obj, index) {
        // アプリタイトルコードごとにデータ取得
        promiseArr.push(self.getAppSalesGraph2Data(obj.app_title_code, obj.app_title_name,obj.app_id_ios,obj.app_id_android));
    });

    // アプリタイトルコードごとのデータを取得後にアプリのグラフ(累計売上)を描画する
    $.when.apply($, promiseArr).then(function() {
        var values = Array.prototype.slice.call(arguments);
        var appSalesGraph2Data = [];
        values.forEach(function(val, i) {
            if (val) {
                series2.push({
                    name : val[1] + val[2],
                    label : "<span>"+ val[1] +"</span><span style='display:none'>"+ val[2] +"</span>",
                    color : self.commonOptions.colorArray[i]
                });
                data2.push(val[0]);

                var selector1 = '.app-graph-checkbox';
                var selector2 = 'input[value="' + val[1] + val[2] + '"]';

                if ($(selector1).filter(selector2).is(':checked')) {
                    appSalesGraph2Data.push(val[0]);
                    // グラフのラベルを設定
                    series.push({
                        label : "<span>"+ val[1] +"</span><span style='display:none'>"+ val[2] +"</span>",
                        color : self.commonOptions.colorArray[i]
                    });
                }
            }
        });

        // グラフのラベルを設定
        copiedOptions.series = series;
        copiedOptions.series2 = series2;
        copiedOptions.data2 = data2;
        // アプリグラフ（累計売上）を描画
        self.createGraph("app-graph-sales2", self.appGraphInfo, 2, appSalesGraph2Data, copiedOptions);
    });
}

CompareController.prototype.getAppSalesGraph2Data = function(app_title_code,app_title_name,app_id_ios,app_id_android) {
    var dtd = $.Deferred();
    var param = {
        'appSales2' : 'appSales2',
        'app_title_code' : app_title_code,
        'app_title_name' : app_title_name,
        'app_id_ios' : app_id_ios,
        'app_id_android' : app_id_android
    };
    AjaxUtil.get('/ipdds/compare', param, function(data) {
        var result = JSON.parse(data.toString());
        if (result.length != 0) {
            // Appグラフ１データ
            var appSalesGraph2Data = [];
            result.forEach(function(val) {
                appSalesGraph2Data.push([ val[0], val[1] ]);
            });
            dtd.resolve([ appSalesGraph2Data, app_title_name, app_title_code ]);
        } else {
            dtd.resolve(null);
        }
    })
    return dtd;
}

CompareController.prototype.plotAppAvgSalesGraph = function() {
    var self = this;

    // Options定義
    var copiedOptions = jQuery.extend(true, {}, self.commonOptions.option);
    // アプリグラフ（平均売上）を描画
    copiedOptions.highlighter = {
        show : true,
        showMarker : true,
        sizeAdjust : 7,
        tooltipLocation : "ne",
        tooltipAxes : "y",
        formatString : "売上:%s"
    }

    // グラフのラベル定義
    var series = [];
    var series2 = [];
    var data2 = [];
    // ajaxから返却したデータ
    var promiseArr = [];
    djangoObj.app.forEach(function(obj, index) {
        // アプリタイトルコードごとにデータ取得
        promiseArr.push(self.getAppGraphAvgData(obj.app_title_code, obj.app_title_name,obj.app_id_ios,obj.app_id_android));
    });

    // アプリタイトルコードごとのデータを取得後にアプリのグラフ平均売上を描画する
    $.when.apply($, promiseArr).then(function() {
        var values = Array.prototype.slice.call(arguments);
        var appAvgSalesGraphData = [];
        values.forEach(function(val, i) {
            if (val) {
                series2.push({
                    name : val[2] + val[3],
                    label : "<span>"+ val[2] +"</span><span style='display:none'>"+ val[3] +"</span>",
                    color : self.commonOptions.colorArray[i]
                });
                data2.push(val[0]);

                var selector1 = '.app-graph-checkbox';
                var selector2 = 'input[value="' + val[2] + val[3] + '"]';

                if ($(selector1).filter(selector2).is(':checked')) {
                    appAvgSalesGraphData.push(val[0]);
                    // グラフのラベルを設定
                    series.push({
                        label : "<span>"+ val[2] +"</span><span style='display:none'>"+ val[3] +"</span>",
                        color : self.commonOptions.colorArray[i]
                    });
                }
            }
        });

        // グラフのラベルを設定
        copiedOptions.series = series;
        copiedOptions.series2 = series2;
        copiedOptions.data2 = data2;
        // アプリグラフ（平均売上）を描画
        self.createGraph("app-graph-sales3", self.appGraphInfo, 4, appAvgSalesGraphData, copiedOptions);
    });
}

CompareController.prototype.getAppGraphAvgData = function(app_title_code,app_title_name,app_id_ios,app_id_android) {
    var dtd = $.Deferred();
    var param = {
        'appAvg' : 'appAvg',
        'app_title_code' : app_title_code,
        'app_title_name' : app_title_name,
        'app_id_ios' : app_id_ios,
        'app_id_android' : app_id_android
    };
    AjaxUtil.get('/ipdds/compare', param, function(data) {
        var result = JSON.parse(data.toString());
        if (result.length != 0) {
            // Appグラフ(平均売上)データ
            var appAvgSalesGraphData = [];
            // Appグラフ(平均ダウンロード数)データ
            var appAvgDownloadGraphData = [];
            result.forEach(function(val) {
                appAvgSalesGraphData.push([ val[0], val[1] ]);
                appAvgDownloadGraphData.push([ val[0], val[2] ]);
            });
            dtd.resolve([ appAvgSalesGraphData, appAvgDownloadGraphData, app_title_name, app_title_code ]);
        } else {
            dtd.resolve(null);
        }
    })
    return dtd;
}

CompareController.prototype.plotAppAvgDownloadGraph = function() {
    var self = this;

    // Options定義
    var copiedOptions = jQuery.extend(true, {}, self.commonOptions.option);
    // アプリグラフ（平均ダウンロード数）を描画
    copiedOptions.highlighter = {
        show : true,
        showMarker : true,
        sizeAdjust : 7,
        tooltipLocation : "ne",
        tooltipAxes : "y",
        formatString : "ダウンロード数:%s"
    }

    // グラフのラベル定義
    var series = [];
    var series2 = [];
    var data2 = [];
    // ajaxから返却したデータ
    var promiseArr = [];
    djangoObj.app.forEach(function(obj, index) {
        // アプリタイトルコードごとにデータ取得
        promiseArr.push(self.getAppGraphAvgData(obj.app_title_code, obj.app_title_name,obj.app_id_ios,obj.app_id_android));
    });

    // アプリタイトルコードごとのデータを取得後にアプリの平均ダウンロード数を描画する
    $.when.apply($, promiseArr).then(function() {
        var values = Array.prototype.slice.call(arguments);
        var appAvgSalesGraphData = [];
        var appAvgDownloadGraphData = [];
        values.forEach(function(val, i) {
            if (val) {
                series2.push({
                    name : val[2] + val[3],
                    label : "<span>"+ val[2] +"</span><span style='display:none'>"+ val[3] +"</span>",
                    color : self.commonOptions.colorArray[i]
                });
                data2.push(val[1]);

                var selector1 = '.app-graph-checkbox';
                var selector2 = 'input[value="' + val[2] + val[3] + '"]';

                if ($(selector1).filter(selector2).is(':checked')) {
                    appAvgDownloadGraphData.push(val[1]);
                    // グラフのラベルを設定
                    series.push({
                        label : "<span>"+ val[2] +"</span><span style='display:none'>"+ val[3] +"</span>",
                        color : self.commonOptions.colorArray[i]
                    });
                }
            }
        });

        // グラフのラベルを設定
        copiedOptions.series = series;
        copiedOptions.series2 = series2;
        copiedOptions.data2 = data2;
        // アプリグラフ（平均ダウンロード数）を描画
        self.createGraph("app-graph-download3", self.appGraphInfo, 5, appAvgDownloadGraphData, jQuery.extend(true, {}, copiedOptions));
    });
}

CompareController.prototype.plotAppDownloadGraph1 = function() {
    var self = this;

    // Options定義
    var copiedOptions = jQuery.extend(true, {}, self.commonOptions.option);
    copiedOptions.highlighter = {
        show : true,
        showMarker : true,
        sizeAdjust : 7,
        tooltipLocation : "ne",
        tooltipAxes : "y",
        formatString : "ダウンロード数:%s"
    }
    copiedOptions.axes.xaxis = {
        renderer : $.jqplot.DateAxisRenderer,
        tickRenderer : $.jqplot.CanvasAxisTickRenderer,
        tickInterval : "1 months",
        tickOptions : {
            angle : -45,
            formatString : "%#mヵ月目"
        },
        min : '1999-12-01',
        max : '2001-01-01'
    };

    // グラフのラベル定義
    var series = [];
    var series2 = [];
    var data2 = [];
    // ajaxから返却したデータ
    var promiseArr = [];
    djangoObj.app.forEach(function(obj, index) {
        // アプリタイトルコードごとにデータ取得
        promiseArr.push(self.getAppDownloadGraph1Data(obj.app_title_code, obj.app_title_name,obj.app_id_ios,obj.app_id_android));
    });

    // アプリタイトルコードごとのデータを取得後にグラフ１及びグラフ２を描画する
    $.when.apply($, promiseArr).then(function() {
        var values = Array.prototype.slice.call(arguments);
        var appDownloadGraph1Data = [];
        values.forEach(function(val, i) {
            if (val) {
                series2.push({
                    name : val[1] + val[2],
                    label : "<span>"+ val[1] +"</span><span style='display:none'>"+ val[2] +"</span>",
                    color : self.commonOptions.colorArray[i]
                });
                val[0].map(function(e, i) {
                    e[0] = '2000-' + StringUtil.lpad((i + 1), 2) + '-01';
                });
                data2.push(val[0]);
                var selector1 = '.app-graph-checkbox';
                var selector2 = 'input[value="' + val[1] + val[2] + '"]';

                if ($(selector1).filter(selector2).is(':checked')) {
                    val[0].map(function(e, i) {
                        e[0] = '2000-' + StringUtil.lpad((i + 1), 2) + '-01';
                    });
                    appDownloadGraph1Data.push(val[0]);
                    // グラフのラベルを設定
                    series.push({
                        label : "<span>"+ val[1] +"</span><span style='display:none'>"+ val[2] +"</span>",
                        color : self.commonOptions.colorArray[i]
                    });
                }
            }
        });

        // グラフのラベルを設定
        copiedOptions.series = series;
        copiedOptions.series2 = series2;
        copiedOptions.data2 = data2;
        // アプリグラフ１（累計売上(発売日からNか月））を描画
        self.createGraph("app-graph-download1", self.appGraphInfo, 1, appDownloadGraph1Data, copiedOptions);
    });
}

CompareController.prototype.getAppDownloadGraph1Data = function(app_title_code, app_title_name,app_id_ios,app_id_android) {
    var dtd = $.Deferred();
    var param = {
        'appDownload1' : 'appDownload1',
        'app_title_code' : app_title_code,
        'app_title_name' : app_title_name,
        'app_id_ios' : app_id_ios,
        'app_id_android' : app_id_android
    };
    AjaxUtil.get('/ipdds/compare', param, function(data) {
        var result = JSON.parse(data.toString());
        if (result.length != 0) {
            // Appグラフ１データ
            var appDownloadGraph1Data = [];
            result.forEach(function(val) {
                appDownloadGraph1Data.push([ val[0], val[1] ]);
            });
            dtd.resolve([ appDownloadGraph1Data, app_title_name,app_title_code ]);
        } else {
            dtd.resolve(null);
        }
    })
    return dtd;
}

CompareController.prototype.plotAppDownloadGraph2 = function() {
    var self = this;

    // Options定義
    var copiedOptions = jQuery.extend(true, {}, self.commonOptions.option);
    copiedOptions.highlighter = {
        show : true,
        showMarker : true,
        sizeAdjust : 7,
        tooltipLocation : "ne",
        tooltipAxes : "y",
        formatString : "ダウンロード数:%s"
    }

    // グラフのラベル定義
    var series = [];
    var series2 = [];
    var data2 = [];
    // ajaxから返却したデータ
    var promiseArr = [];
    djangoObj.app.forEach(function(obj, index) {
        // アプリタイトルコードごとにデータ取得
        promiseArr.push(self.getAppDownloadGraph2Data(obj.app_title_code, obj.app_title_name,obj.app_id_ios,obj.app_id_android));
    });

    // アプリタイトルコードごとのデータを取得後にグラフ１及びグラフ２を描画する
    $.when.apply($, promiseArr).then(function() {
        var values = Array.prototype.slice.call(arguments);
        var appDownloadGraph2Data = [];
        values.forEach(function(val, i) {
            if (val) {
                series2.push({
                    name : val[1] + val[2],
                    label : "<span>"+ val[1] +"</span><span style='display:none'>"+ val[2] +"</span>",
                    color : self.commonOptions.colorArray[i]
                });
                data2.push(val[0]);

                var selector1 = '.app-graph-checkbox';
                var selector2 = 'input[value="' + val[1] + val[2] + '"]';

                if ($(selector1).filter(selector2).is(':checked')) {
                    appDownloadGraph2Data.push(val[0]);
                    // グラフのラベルを設定
                    series.push({
                        label : "<span>"+ val[1] +"</span><span style='display:none'>"+ val[2] +"</span>",
                        color : self.commonOptions.colorArray[i]
                    });
                }
            }
        });

        // グラフのラベルを設定
        copiedOptions.series = series;
        copiedOptions.series2 = series2;
        copiedOptions.data2 = data2;
        // アプリグラフ（累計売上ダウンロード数）を描画
        self.createGraph("app-graph-download2", self.appGraphInfo, 3, appDownloadGraph2Data, copiedOptions);
    })
}

CompareController.prototype.getAppDownloadGraph2Data = function(app_title_code, app_title_name,app_id_ios,app_id_android) {
    var dtd = $.Deferred();
    var param = {
        'appDownload2' : 'appDownload2',
        'app_title_code' : app_title_code,
        'app_title_name' : app_title_name,
        'app_id_ios' : app_id_ios,
        'app_id_android' : app_id_android
    };
    AjaxUtil.get('/ipdds/compare', param, function(data) {
        var result = JSON.parse(data.toString());
        if (result.length != 0) {
            // Appグラフのデータ
            var appDownloadGraph2Data = [];
            result.forEach(function(val) {
                appDownloadGraph2Data.push([ val[0], val[1] ]);
            });
            dtd.resolve([ appDownloadGraph2Data, app_title_name, app_title_code ]);
        } else {
            dtd.resolve(null);
        }
    })
    return dtd;
}

/**
 * グラフを作成する。
 *
 * @param elemId
 *            要素ID
 * @param graphInfo
 *            グラム情報の配列
 * @param index
 *            インデックス
 * @param data
 *            グラフ表示用データ
 * @param options
 *            グラフ表示用options
 */
CompareController.prototype.createGraph = function(elemId, graphInfo, index, data, options) {
    var self = this;
    var info = graphInfo[index];
    options.title = info.options.title;

    var tmpData = [];
    var tmpSeries = [];
    for (var i = 0; i < data.length; i++) {
        var tmp = 0;
        var subData = data[i];
        for (var j = 0; j < subData.length; j++) {
            tmp += subData[j][1];
        }
        if (tmp > 0) {
            tmpData.push(subData);
            tmpSeries.push(options.series[i]);
        }
    }
    if (tmpData.length == 0) {
        tmpData.push([ [ '9999-01-01', 0 ] ]);
        options.legend = {
            show : false
        };

        NoDateUtil.overlay(elemId)
    }
    options.series = tmpSeries;
    info.data = tmpData
    info.options = options;
    info.elemId = elemId;
    info.graph = $.jqplot(elemId, tmpData, options);
}

CompareController.prototype.drawGrid = function() {
    var self = this;
    // ツイッターのグリッドを表示
    self.drawGridForTwitter();
    // マンガのグリッドを表示
    self.drawGridForManga();
    // ゲームのグリッドを表示
    self.drawGridForGame();
    // アプリのグリッドを表示
    self.drawGridForApp();
}

/**
 * ツイッターGridのフォーマットを作成する。
 *
 */
CompareController.prototype.drawGridForTwitter = function() {
    var self = this;

    var medelArray = [];
    var width = $('#grid-twitter').width();
    medelArray.push(GridUtil.createColModel({
        name : 'is_draw',
        align : 'center',
        width : width * 0.09,
        formatter : function(val, opt, rdt) {
            var strVal = JSON.parse(val.toString());
            var dataRow = strVal[0];
            var checkBoxVal = strVal[1];

            if (self.isDrawGridForTwitter) {
                if (self.isTwitterChecked[dataRow]) {
                    return ('<input type="checkbox" class="plot-checkbox twitter-graph-checkbox" value="' + checkBoxVal + '"/ style="margin: 10px;" data-row="' + dataRow + '" checked>');
                } else {
                    return ('<input type="checkbox" class="plot-checkbox twitter-graph-checkbox" value="' + checkBoxVal + '"/ style="margin: 10px;" data-row="' + dataRow + '">');
                }
            } else {
                if (!self.isTwitterChecked) {
                    self.isTwitterChecked = {};
                }
                if (dataRow < 5) {
                    self.isTwitterChecked[dataRow] = true;
                    return ('<input type="checkbox" class="plot-checkbox twitter-graph-checkbox" value="' + checkBoxVal + '"/ style="margin: 10px;" data-row="' + dataRow + '" checked>');
                } else {
                    self.isTwitterChecked[dataRow] = false;
                    return ('<input type="checkbox" class="plot-checkbox twitter-graph-checkbox" value="' + checkBoxVal + '"/ style="margin: 10px;" data-row="' + dataRow + '">');
                }
            }
        },
        sortable : false
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'sakuhin_name',
        width : width * 0.20,
        formatter : function(val, opt, rdt) {
            return '<a href="/ipdds/detail/?sakuhin_code=' + val[0] + '" class="link">' + val[1] + '</a>'
        },
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'followers_latest',
        align : 'right',
        width : width * 0.15,
        sorttype : 'number',
        formatter : function(val, opt, rdt) {
            return val ? StringUtil.comma_separated(val) : 'ー';
        }
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'followers_3months_ago',
        align : 'right',
        width : width * 0.15,
        sorttype : 'number',
        formatter : function(val, opt, rdt) {
            return val ? StringUtil.comma_separated(val) : 'ー';
        }
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'followers_1year_ago',
        align : 'right',
        width : width * 0.15,
        sorttype : 'number',
        formatter : function(val, opt, rdt) {
            return val ? StringUtil.comma_separated(val) : 'ー';
        }
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'user_name',
        width : width * 0.07,
        align : 'center',
        formatter : function(val, opt, rdt) {
            if ((rdt.followers_latest || rdt.followers_3months_ago || rdt.followers_1year_ago) && rdt.user_name) {
                return '<a  class="twitter-link" onclick="window.open(\'https://twitter.com/' + val + '\')"><i class="fab fa-twitter-square" style="font-size: 30px"></i></a></a>'
            } else {
                return '';
            }
        },
    }));

    var data = self.createTwitterData();
    var pager = '';
    var search = false;
    if (data.length > 10) {
        var pager = '#pager-twitter';
        var search = true;
    }
    console.log(data.length);

    var option = {
        colNames : [ 'グラフ描画', '作品名', '最新の<br>フォロワー数', '三か月前の<br>フォロワー数', '一年前の<br>フォロワー数', 'Twitter' ],
        colModel : medelArray,
        data : data,
        width : width,
        pager : pager,
        loadComplete : function() {
            if ($('.twitter-graph-checkbox:checked').length == 5) {
                $('.twitter-graph-checkbox:not(:checked)').prop('disabled', true);
            }
            self.isDrawGridForTwitter = true;
            $('.twitter-graph-checkbox').on('click', function() {
                var elem = $(this);
                var val = elem.attr('data-row');
                self.isTwitterChecked[val] = elem.is(':checked');
                if ($('.twitter-graph-checkbox:checked').length == 5) {
                    $('.twitter-graph-checkbox:not(:checked)').prop('disabled', true);
                } else {
                    console.log($('.twitter-graph-checkbox:checked').length)
                    $('.twitter-graph-checkbox:not(:checked)').prop('disabled', false);
                }

            });
        }
    };
    GridUtil.renderNormalGrid('#grid-twitter', option, search);

}
/**
 * ツイッターGridのデータを作成する。
 *
 */
CompareController.prototype.createTwitterData = function() {
    var self = this;

    var data = [];
    for (var i = 0; i <= djangoObj.twitter.length; i++) {
        if (djangoObj.twitter[i]) {
            var row = [];
            var jsonStr = JSON.stringify([ i, djangoObj.twitter[i].sakuhin_name ]);
            row.push(jsonStr);
            row.push([ djangoObj.twitter[i].sakuhin_code, djangoObj.twitter[i].sakuhin_name ]);
            row.push(djangoObj.twitter[i].followers_latest);
            row.push(djangoObj.twitter[i].followers_3months_ago);
            row.push(djangoObj.twitter[i].followers_1year_ago);
            row.push(djangoObj.twitter[i].user_name);
            data.push(row);
        }
    }
    var colNames = [ 'is_draw', 'sakuhin_name', 'followers_latest', 'followers_3months_ago', 'followers_1year_ago', 'user_name' ];
    return GridUtil.createGridData(colNames, data);
}

/**
 * マンガGridのフォーマットを作成する。
 *
 */
CompareController.prototype.drawGridForManga = function() {
    var self = this;

    var medelArray = [];
    var width = $('#grid-manga').width();
    medelArray.push(GridUtil.createColModel({
        name : 'is_draw',
        align : 'center',
        width : width * 0.06,
        formatter : function(val, opt, rdt) {
            var strVal = JSON.parse(val.toString());
            var dataRow = strVal[0];
            var checkBoxVal = strVal[1] + strVal[2];

            if (self.isDrawGridForManga) {
                if (self.isMangaChecked[dataRow]) {
                    return ('<input type="checkbox" class="plot-checkbox manga-graph-checkbox" value="' + checkBoxVal + '"/ style="margin: 10px;" data-row="' + dataRow + '" checked>');
                } else {
                    return ('<input type="checkbox" class="plot-checkbox manga-graph-checkbox" value="' + checkBoxVal + '"/ style="margin: 10px;" data-row="' + dataRow + '">');
                }
            } else {
                if (!self.isMangaChecked) {
                    self.isMangaChecked = {};
                }
                if (dataRow < 5) {
                    self.isMangaChecked[dataRow] = true;
                    return ('<input type="checkbox" class="plot-checkbox manga-graph-checkbox" value="' + checkBoxVal + '"/ style="margin: 10px;" data-row="' + dataRow + '" checked>');
                } else {
                    self.isMangaChecked[dataRow] = false;
                    return ('<input type="checkbox" class="plot-checkbox manga-graph-checkbox" value="' + checkBoxVal + '"/ style="margin: 10px;" data-row="' + dataRow + '">');
                }
            }
        },
        sortable : false
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'sakuhin_name',
        width : width * 0.2,
        formatter : function(val, opt, rdt) {
            return '<a href="/ipdds/detail/?sakuhin_code=' + val[0] + '" class="link">' + val[1] + '</a>'
        },
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'manga_name',
        width : width * 0.2,
        formatter : function(val, opt, rdt) {
            return val || 'ー';
        }
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'cumulative',
        align : 'right',
        width : width * 0.15,
        sorttype : 'number',
        formatter : function(val, opt, rdt) {
            return val ? StringUtil.comma_separated(val) + '部' : 'ー';
        }
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'cumulative_first',
        align : 'right',
        width : width * 0.15,
        sorttype : 'number',
        formatter : function(val, opt, rdt) {
            return val ? StringUtil.comma_separated(val) + '部' : 'ー';
        }
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'cumulative_latest',
        align : 'right',
        width : width * 0.15,
        sorttype : 'number',
        formatter : function(val, opt, rdt) {
            return val ? StringUtil.comma_separated(val) + '部' : 'ー';
        }
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'average_1manga',
        align : 'right',
        width : width * 0.15,
        sorttype : 'number',
        formatter : function(val, opt, rdt) {
            return val ? StringUtil.comma_separated(val) + '部' : 'ー';
        }
    }));

    var data = self.createMangaData();
    var pager = '';
    var search = false;
    if (data.length > 10) {
        var pager = '#pager-manga';
        var search = true;
    }

    var height = 'auto';
    if (data.length >= 10) {
        height = 345;
    }
    var option = {
        colNames : [ 'グラフ描画', '作品名','マンガ名', '累計発行部数', '累計発行部数（１巻）', '累計発行部数（最新刊）', '平均発行部数（単巻あたり）' ],
        colModel : medelArray,
        data : data,
        width : width,
        height : height,
        pager : pager,
        pgbuttons : false,
        pginput : false,
        rowNum : data.length,
        rowList : data.length,
        loadComplete : function() {
            if ($('.manga-graph-checkbox:checked').length == 5) {
                $('.manga-graph-checkbox:not(:checked)').prop('disabled', true);
            }
            self.isDrawGridForManga = true;
            $('.manga-graph-checkbox').on('click', function() {
                var elem = $(this);
                var val = elem.attr('data-row');
                self.isMangaChecked[val] = elem.is(':checked');
                if ($('.manga-graph-checkbox:checked').length == 5) {
                    $('.manga-graph-checkbox:not(:checked)').prop('disabled', true);
                } else {
                    console.log($('.manga-graph-checkbox:checked').length)
                    $('.manga-graph-checkbox:not(:checked)').prop('disabled', false);
                }

            });
        }
    };
    GridUtil.renderNormalGrid('#grid-manga', option, search);

}
/**
 * マンガGridのデータを作成する。
 *
 */
CompareController.prototype.createMangaData = function() {
    var self = this;

    var data = [];
    for (var i = 0; i <= djangoObj.manga.length; i++) {
        if (djangoObj.manga[i]) {
            var row = [];
            var jsonStr = JSON.stringify([ i, djangoObj.manga[i].manga_name,djangoObj.manga[i].manga_code ]);
            row.push(jsonStr);
            row.push([ djangoObj.manga[i].sakuhin_code, djangoObj.manga[i].sakuhin_name ]);
            row.push(djangoObj.manga[i].manga_name);
            row.push(djangoObj.manga[i].cumulative);
            row.push(djangoObj.manga[i].cumulative_first);
            row.push(djangoObj.manga[i].cumulative_latest);
            row.push(djangoObj.manga[i].average_1manga);
            data.push(row);
        }
    }
    var colNames = [ 'is_draw', 'sakuhin_name', 'manga_name','cumulative', 'cumulative_first', 'cumulative_latest', 'average_1manga' ];
    return GridUtil.createGridData(colNames, data);
}

/**
 * ゲームGridのフォーマットを作成する。
 *
 */
CompareController.prototype.drawGridForGame = function() {
    var self = this;

    var medelArray = [];
    var width = $('#grid-game').width();

    medelArray.push(GridUtil.createColModel({
        name : 'is_draw',
        align : 'center',
        width : width * 0.06,
        formatter : function(val, opt, rdt) {
            var strVal = JSON.parse(val.toString());
            var dataRow = strVal[0];
            var checkBoxVal = strVal[1] +'/ '+ strVal[2] +'/ '+ strVal[3];

            if (self.isDrawGridForGame) {
                if (self.isGameChecked[dataRow]) {
                    return ('<input type="checkbox" class="plot-checkbox game-graph-checkbox" value="' + checkBoxVal + '"/ style="margin: 10px;" data-row="' + dataRow + '" checked>');
                } else {
                    return ('<input type="checkbox" class="plot-checkbox game-graph-checkbox" value="' + checkBoxVal + '"/ style="margin: 10px;" data-row="' + dataRow + '">');
                }
            } else {
                if (!self.isGameChecked) {
                    self.isGameChecked = {};
                }
                if (dataRow < 5) {
                    self.isGameChecked[dataRow] = true;
                    return ('<input type="checkbox" class="plot-checkbox game-graph-checkbox" value="' + checkBoxVal + '"/ style="margin: 10px;" data-row="' + dataRow + '" checked>');
                } else {
                    self.isGameChecked[dataRow] = false;
                    return ('<input type="checkbox" class="plot-checkbox game-graph-checkbox" value="' + checkBoxVal + '"/ style="margin: 10px;" data-row="' + dataRow + '">');
                }
            }
        },
        sortable : false
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'sakuhin_name',
        width : width * 0.10,
        formatter : function(val, opt, rdt) {
            return '<a href="/ipdds/detail/?sakuhin_code=' + val[0] + '" class="link">' + val[1] + '</a>'
        },
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'game_title_name',
        width : width * 0.40,
        formatter : function(val, opt, rdt) {
            return val || 'ー';
        }
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'platform_name',
        width : width * 0.10,
        formatter : function(val, opt, rdt) {
            return val || 'ー';
        }
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'hanbai_company_name',
        width : width * 0.18,
        formatter : function(val, opt, rdt) {
            return val || 'ー';
        }
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'release_yyyymmdd',
        width : width * 0.07,
        formatter : function(val, opt, rdt) {
            return val || 'ー';
        }
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'total_sales_cnt',
        align : 'right',
        width : width * 0.09,
        sorttype : 'number',
        formatter : function(val, opt, rdt) {
            return val ? StringUtil.comma_separated(val) + '本' : 'ー';
        }
    }));

    var data = self.createGameData();
    var pager = '';
    var search = false;
    if (data.length > 10) {
        var pager = '#pager-game';
        var search = true;
    }

    var height = 'auto';
    if (data.length >= 10) {
        height = 345;
    }
    var option = {
        colNames : [ 'グラフ描画', '作品名', 'ゲーム名', '対応機種', '発売元', '発売日', '累計売上本数' ],
        colModel : medelArray,
        data : data,
        width : width,
        height : height,
        pager : pager,
        pgbuttons : false,
        pginput : false,
        rowNum : data.length,
        rowList : data.length,
        loadComplete : function() {
            if ($('.game-graph-checkbox:checked').length == 5) {
                $('.game-graph-checkbox:not(:checked)').prop('disabled', true);
            }
            self.isDrawGridForGame = true;
            $('.game-graph-checkbox').on('click', function() {
                var elem = $(this);
                var val = elem.attr('data-row');
                self.isGameChecked[val] = elem.is(':checked');
                if ($('.game-graph-checkbox:checked').length == 5) {
                    $('.game-graph-checkbox:not(:checked)').prop('disabled', true);
                } else {
                    console.log($('.game-graph-checkbox:checked').length)
                    $('.game-graph-checkbox:not(:checked)').prop('disabled', false);
                }

            });
        }
    };
    GridUtil.renderNormalGrid('#grid-game', option, search);

}
/**
 * ゲームGridのデータを作成する。
 *
 */
CompareController.prototype.createGameData = function() {
    var self = this;

    var data = [];
    for (var i = 0; i <= djangoObj.game.length; i++) {
        if (djangoObj.game[i]) {
            var row = [];
            var jsonStr = JSON.stringify([ i, djangoObj.game[i].game_title_name, djangoObj.game[i].platform_name, djangoObj.game[i].release_yyyymmdd ]);
            row.push(jsonStr);
            row.push([ djangoObj.game[i].sakuhin_code, djangoObj.game[i].sakuhin_name ]);
            row.push(djangoObj.game[i].game_title_name);
            row.push(djangoObj.game[i].platform_name);
            row.push(djangoObj.game[i].hanbai_company_name);
            row.push(djangoObj.game[i].release_yyyymmdd);
            row.push(djangoObj.game[i].total_sales_cnt);
            data.push(row);
        }
    }
    var colNames = [ 'is_draw', 'sakuhin_name', 'game_title_name', 'platform_name', 'hanbai_company_name', 'release_yyyymmdd', 'total_sales_cnt' ];
    return GridUtil.createGridData(colNames, data);
}

/**
 * アプリGridのフォーマットを作成する。
 *
 */
CompareController.prototype.drawGridForApp = function() {
    var self = this;

    var medelArray = [];
    var width = $('#grid-app').width();
    medelArray.push(GridUtil.createColModel({
        name : 'is_draw',
        align : 'center',
        width : width * 0.06,
        formatter : function(val, opt, rdt) {
            var dataRow = val[0];
            var checkBoxVal = val[1] + val[2];
            if (self.isDrawGridForApp) {
                if (self.isAppChecked[dataRow]) {
                    return ('<input type="checkbox" class="plot-checkbox app-graph-checkbox" value="' + checkBoxVal + '"/ style="margin: 10px;" data-row="' + dataRow + '" checked>');
                } else {
                    return ('<input type="checkbox" class="plot-checkbox app-graph-checkbox" value="' + checkBoxVal + '"/ style="margin: 10px;" data-row="' + dataRow + '">');
                }
            } else {
                if (!self.isAppChecked) {
                    self.isAppChecked = {};
                }
                if (dataRow < 5) {
                    self.isAppChecked[dataRow] = true;
                    return ('<input type="checkbox" class="plot-checkbox app-graph-checkbox" value="' + checkBoxVal + '"/ style="margin: 10px;" data-row="' + dataRow + '" checked>');
                } else {
                    self.isAppChecked[dataRow] = false;
                    return ('<input type="checkbox" class="plot-checkbox app-graph-checkbox" value="' + checkBoxVal + '"/ style="margin: 10px;" data-row="' + dataRow + '">');
                }
            }
        },
        sortable : false
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'sakuhin_name',
        width : width * 0.14,
        formatter : function(val, opt, rdt) {
            return '<a href="/ipdds/detail/?sakuhin_code=' + val[0] + '" class="link">' + val[1] + '</a>'
        },
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'app_title_name',
        width : width * 0.14,
        formatter : function(val, opt, rdt) {
            return val || 'ー';
        }
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'platform',
        width : width * 0.08,
        formatter : function(val, opt, rdt) {
            return val || 'ー';
        }
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'hanbai_company_name',
        width : width * 0.14,
        formatter : function(val, opt, rdt) {
            return val || 'ー';
        }
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'service_start_yyyymmdd',
        width : width * 0.07,
        formatter : function(val, opt, rdt) {
            return val || 'ー';
        }
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'total_sales',
        align : 'right',
        width : width * 0.09,
        sorttype : 'number',
        formatter : function(val, opt, rdt) {
            return val ? '$' + StringUtil.comma_separated(val) : 'ー';
        }
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'total_download_cnt',
        align : 'right',
        width : width * 0.1,
        sorttype : 'number',
        formatter : function(val, opt, rdt) {
            return val ? StringUtil.comma_separated(val) : 'ー';
        }
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'avg_sales',
        align : 'right',
        width : width * 0.08,
        sorttype : 'number',
        formatter : function(val, opt, rdt) {
            return val ? '$' + StringUtil.comma_separated(val) : 'ー';
        }
    }));
    medelArray.push(GridUtil.createColModel({
        name : 'avg_download_cnt',
        align : 'right',
        width : width * 0.1,
        sorttype : 'number',
        formatter : function(val, opt, rdt) {
            return val ? StringUtil.comma_separated(val) : 'ー';
        }
    }));

    var data = self.createAppData();
    var pager = '';
    var search = false;
    if (data.length > 10) {
        var pager = '#pager-app';
        var search = true;
    }

    var height = 'auto';
    if (data.length >= 10) {
        height = 345;
    }
    var option = {
        colNames : [ 'グラフ描画', '作品名', 'アプリ名', 'プラットフォーム', '発売元', '発売日', '累計売上', '累計ダウンロード数', '平均売上', '平均ダウンロード数' ],
        colModel : medelArray,
        data : data,
        width : width,
        height : height,
        pager : pager,
        pgbuttons : false,
        pginput : false,
        rowNum : data.length,
        rowList : data.length,
        loadComplete : function() {
            if ($('.app-graph-checkbox:checked').length == 5) {
                $('.app-graph-checkbox:not(:checked)').prop('disabled', true);
            }
            self.isDrawGridForApp = true;
            $('.app-graph-checkbox').on('click', function() {
                var elem = $(this);
                var val = elem.attr('data-row');
                self.isAppChecked[val] = elem.is(':checked');
                if ($('.app-graph-checkbox:checked').length == 5) {
                    $('.app-graph-checkbox:not(:checked)').prop('disabled', true);
                } else {
                    console.log($('.app-graph-checkbox:checked').length)
                    $('.app-graph-checkbox:not(:checked)').prop('disabled', false);
                }

            });
        }
    };
    GridUtil.renderNormalGrid('#grid-app', option, search);

}
/**
 * アプリGridのデータを作成する。
 *
 */
CompareController.prototype.createAppData = function() {
    var self = this;

    var data = [];
    for (var i = 0; i <= djangoObj.app.length; i++) {
        if (djangoObj.app[i]) {
            var row = [];
            row.push([ i, djangoObj.app[i].app_title_name, djangoObj.app[i].app_title_code ]);
            row.push([ djangoObj.app[i].sakuhin_code, djangoObj.app[i].sakuhin_name ]);
            row.push(djangoObj.app[i].app_title_name);
            row.push(djangoObj.app[i].platform);
            row.push(djangoObj.app[i].hanbai_company_name);
            row.push(djangoObj.app[i].service_start_yyyymmdd);
            row.push(djangoObj.app[i].total_sales);
            row.push(djangoObj.app[i].total_download_cnt);
            row.push(djangoObj.app[i].avg_sales);
            row.push(djangoObj.app[i].avg_download_cnt);
            data.push(row);
        }
    }
    var colNames = [ 'is_draw', 'sakuhin_name', 'app_title_name', 'platform', 'hanbai_company_name', 'service_start_yyyymmdd', 'total_sales', 'total_download_cnt', 'avg_sales', 'avg_download_cnt' ];
    return GridUtil.createGridData(colNames, data);
}

// リストに対象の要素が含まれているか判定
CompareController.prototype.includes = function(array, target) {
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
    var controller = new CompareController();
    controller.init();
});
>>>>>>> remotes/origin/feature/ph1.3:web/web-front/ipdds/ipdds_app/static/ipdds_app/javascript/10401_compare.js
