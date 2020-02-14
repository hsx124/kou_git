var DetailController = function() {

};
DetailController.prototype = new AbstractController();

// ----------------------------------------------------------------------------------------------
// 制御処理
// ----------------------------------------------------------------------------------------------

/**
 * 画面の主処理
 */
DetailController.prototype.execute = function() {
    var self = this;

    // 呼び出し元に返却するPromise
    var promise = $.Deferred();

    // 画面描画処理のPromise
    var promises = [];
    // 比較カゴ描画
    promises.push(self.drawHikakuKago());
    // タグ・類似作品描画
    promises.push(self.drawTagAndRuiji());
    // アニメ（放送期間・主要放送局）描画
    promises.push(self.drawAnime());
    // 年代別男女比描画
    promises.push(self.drawGenderRatio());
    // 併売描画
    promises.push(self.drawHeibai());
    // 関連文書描画
    promises.push(self.drawMediaReport());
    // マンガ描画
    promises.push(self.drawManga());
    // twitter描画
    promises.push(self.drawTwitter());
    // ゲーム描画
    promises.push(self.drawGame());
    // アプリ描画
    promises.push(self.drawApp());

    // 画面描画処理を待ち合わせる
    $.when.apply($, promises).then(function() {
        // 各エリア生成が成功した場合の処理
        // グラフの設定
        return self.setPlotOption().then(function() {
            // 呼び出し元に 'resolve' を返却
            promise.resolve();
        });

    }).fail(function() {

        // 各エリア生成が失敗した場合の処理
        // エラー情報を設定
        var errorInfo = new ErrorInfo();
        errorInfo.setMsgDetail(djangoObj.sakuhin_data.sakuhin_name + 'のデータ取得に失敗しました。');

        // 呼び出し元に 'reject' を返却
        promise.reject(errorInfo);
    });

    return promise.promise();
}
/**
 * メニュー選択処理
 */
DetailController.prototype.selectedMenu = function() {

}
/**
 * イベント登録処理
 */
DetailController.prototype.bindEvent = function() {
    var self = this;

    // 比較カゴ追加・削除ボタン
    CompareKago.SetCompareDataAddOrDel();

    // Manga再描画ボタン
    $('#manga-replot-button').on('click', function() {
        self.replotManga();
    });
    // Twitter再描画ボタン
    $('#twitter-replot-button').on('click', function() {
        self.replotTwitter();
    });
    // Game再描画ボタン
    $('#game-replot-button').on('click', function() {
        self.replotGame();
    });
    // App再描画ボタン
    $('#app-replot-button').on('click', function() {
        self.replotApp();
    });
}

// ----------------------------------------------------------------------------------------------
// 内部関数
// ----------------------------------------------------------------------------------------------

/**
 * 比較カゴ描画
 */
DetailController.prototype.drawHikakuKago = function() {

    var promise = $.Deferred();
    CompareKago.getSessionData().then(function(data) {
        // 比較かご作品領域を描画する
        $('.compare-kago-list-contents').empty();
        CompareKago.drawCompareSakuhin(data);
        // [比較カゴに入れる]/[比較カゴから戻す]ボタンを画面に表示する（初期表示時）
        if ($('.compare-kago-add').length == 1) {
            $('.compare-kago-add').css('display', 'block');
        } else {
            $('.compare-kago-del').css('display', 'block');
        }
        promise.resolve();
    }).fail(function() {
        promise.reject();
    });

    return promise
}

/**
 * タグ・類似作品描画
 */
DetailController.prototype.drawTagAndRuiji = function() {
    var self = this;

    // 呼び出し元に返却するPromise
    var promise = $.Deferred();

    // ajaxを5回実行させるPromise
    var promises = [];

    // 分類タグの取得
    promises.push(self.getBunrui());

    // 掲載媒体の取得
    promises.push(self.getMedia());

    // コアの取得
    promises.push(self.getCore());

    // タグ・類似作品の取得
    promises.push(self.getTag());

    $.when.apply($, promises).then(function() {
        promise.resolve();
    });

    return promise.promise();
}

DetailController.prototype.getBunrui = function(){
    // 分類タグの描画
    var param = {
        'sakuhin_code' : djangoObj.sakuhin_data.sakuhin_code,
        'process_code' : '01-01'
    };
    return AjaxUtil.get('/ipdds/detail/', param, function(data) {
        var resultBunrui = JSON.parse(data.toString());
        for(var i = 0;i<resultBunrui.length;i++){
            var bunrui = resultBunrui[i];
            // 取得したデータが'true'のものだけappendする
            if(bunrui[0]){
                var anime = $('<a class="tag anime" href="/ipdds/search_result?name_category=0">アニメ</a>');
                $('#bunrui-area').append(anime);
            }
            if(bunrui[1]){
                var manga = $('<a class="tag manga" href="/ipdds/search_result?name_category=1">マンガ</a>');
                $('#bunrui-area').append(manga);
            }
            if(bunrui[2]){
                var app = $('<a class="tag app" href="/ipdds/search_result?name_category=2">アプリ</a>');
                $('#bunrui-area').append(app);
            }
            if(bunrui[3]){
                var game = $('<a class="tag game" href="/ipdds/search_result?name_category=3">ゲーム</a>');
                $('#bunrui-area').append(game);
            }
        }
    });
}

DetailController.prototype.getMedia = function(){
    // 掲載媒体の描画
    var param = {
        'sakuhin_code' : djangoObj.sakuhin_data.sakuhin_code,
        'process_code' : '01-02'
    };
    return AjaxUtil.get('/ipdds/detail/', param, function(data) {
        var resultMedia = JSON.parse(data.toString());
        if(resultMedia.length != 0){
            for(var i = 0;i<resultMedia.length;i++){
                var media = resultMedia[i];
                var a = $('<a class="tag" href="/ipdds/search_result?name_media='+media[1]+'">'+media[2]+'</a>');
                $('#media-area').append(a);
            }
        }
        else{
            $('#media-area').remove();
        }
    });
}

DetailController.prototype.getCore = function(){
    // コアタグの描画
    param = {
        'sakuhin_code' : djangoObj.sakuhin_data.sakuhin_code,
        'process_code' : '01-03'
    };
    return AjaxUtil.get('/ipdds/detail/', param, function(data) {
        var resultCore = JSON.parse(data.toString());
        if(resultCore.length != 0){
            var core = resultCore[0];
            // 生成するaタグのイメージ：'<a class="tag" href="/ipdds/search_result?name_core=000008">ギャグコメ</a>'
            var a = $('<a class="tag" href="/ipdds/search_result?name_core='+core[1]+'">'+core[2]+'</a>');
            $('#core-area').append(a);
        }
        else{
            $('#core-area').remove();
        }
    });
}

DetailController.prototype.getTag = function(){
    var self = this;
    // 呼び出し元に返すプロミス
    var promise = $.Deferred();
    // 事実タグの描画
    param = {
        'sakuhin_code' : djangoObj.sakuhin_data.sakuhin_code,
        'process_code' : '01-04'
    };
    var tagPromise = $.Deferred();
    AjaxUtil.get('/ipdds/detail/', param, function(data) {
        var resultTag = JSON.parse(data.toString());
        if(resultTag.length != 0){
            var tag = resultTag[0];
            var array = '';
            var tagList = [];
            for(var j = 1;j<=5;j++){
                var nameIndex = j*2;
                var codeIndex = nameIndex -1;
                if(tag[codeIndex]){
                    tagList.push(tag[codeIndex]);
                    array += '<a class="tag" href="/ipdds/search_result?name_fact_tag='+tag[codeIndex]+'">'+tag[nameIndex]+'</a>';
                }
            }
            $('#tag-area').append(array);
            tagPromise.resolve(tagList);
        }
        else{
            $('#tag-area').remove();
            tagPromise.resolve();
        }
    });

    tagPromise.then(function(tagList){
        // 類似作品の描画
        if(tagList && tagList.length){
            param = {
                'sakuhin_code' : djangoObj.sakuhin_data.sakuhin_code,
                'tag_code_list' : JSON.stringify(tagList),
                'process_code' : '01-05'
            };
            AjaxUtil.get('/ipdds/detail/', param, function(data) {
                var resultRuiji = JSON.parse(data.toString());
                if(resultRuiji.length){
                    for(var i = 0;i<resultRuiji.length;i++){
                        var ruiji = resultRuiji[i];
                        var ruijiSakuhin = $('<div class="similar-sakuhin"></div>');
                        var sakuhinName = $('<a class="link" href="/ipdds/detail?sakuhin_code='+ruiji[0]+'">'+ruiji[1]+'</a>');
                        var category = $('<div class="category"><div>');
                        var tag = '';
                        for(var j = 1;j<=5;j++){
                            var codeIndex = j*2;
                            var nameIndex = codeIndex+1;
                            if(ruiji[codeIndex]){
                                if(self.isSimilar(ruiji[codeIndex],tagList)){
                                    tag += '<a class="tag matched" href="/ipdds/search_result?name_fact_tag='+ruiji[codeIndex]+'">'+ruiji[nameIndex]+'</a>';
                                }
                                else{
                                    tag += '<a class="tag" href="/ipdds/search_result?name_fact_tag='+ruiji[codeIndex]+'">'+ruiji[nameIndex]+'</a>';
                                }
                            }
                        }
                        category.append(tag);
                        ruijiSakuhin.append(sakuhinName,category);
                        $('.similar-sakuhin-list').append(ruijiSakuhin);
                    }
                }
            }).then(function(){
                promise.resolve();
            });
        }
    })
    return promise.promise();
}

DetailController.prototype.isSimilar = function(code,list){
    for(var i = 0;i<list.length;i++){
        if(list[i] == code){
            return true;
        }
    }
    return false;
}

/**
 * アニメ（放送期間・主要放送局）描画
 */
DetailController.prototype.drawAnime = function() {
    var param = {
        'sakuhin_code' : djangoObj.sakuhin_data.sakuhin_code,
        'process_code' : '02'
    };
    return AjaxUtil.get('/ipdds/detail/', param, function(data) {
        var resultAnime = JSON.parse(data.toString());
        if(resultAnime[0][1] != '' || resultAnime[0][2] != ''){
            for (var i = 0; i < resultAnime.length; i++) {
                var anime = resultAnime[i];
                var strong = $('<strong>' + anime[0] + '</strong>');
                var div1 = $('<div class="broadcast">' + anime[1] + '<br>' + anime[2] + '</div>');
                var div2 = $('<div class="spacer_8"></div>');
                $('.description-area-left-detail').append(strong, div1, div2);
            }
        }
        else{
        $('.description-area-left-detail').remove();
        }
    });
}

/**
 * 年代別男女比描画
 */
DetailController.prototype.drawGenderRatio = function() {
    var self = this;
    var param = {
        'sakuhin_code' : djangoObj.sakuhin_data.sakuhin_code,
        'process_code' : '03'
    };
    return AjaxUtil.get('/ipdds/detail/', param, function(data) {
        var resultGenderRatio = JSON.parse(data.toString());
        // データを比率でテーブルで表示
        self.drawGenderRatioGrid(resultGenderRatio[0]);
        // plot用にデータを取得する
        self.drawGenderRatioPlot(resultGenderRatio[0]);
    });
}

// 年代別男女比の表を表示する
DetailController.prototype.drawGenderRatioGrid = function(genderRatioData) {
    var self = this;
    var total = genderRatioData[0];
    if (total == null) {
        var total = '-'
    } else {
        var total = total.toString().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, '$1,');
    }
    var tableHead = '<table class="ipdds-table gender"><tr><td>年代</td><td>男性(%)</td><td>女性(%)</td></tr>'
    var tr11to15 = '<tr><td>11歳～15歳</td><td>' + self.calcGenderPercentage(genderRatioData[3], genderRatioData[12]) + '</td><td>' + self.calcGenderPercentage(genderRatioData[12], genderRatioData[3]) + '</td></tr>'
    var tr16to20 = '<tr><td>16歳～20歳</td><td>' + self.calcGenderPercentage(genderRatioData[4], genderRatioData[13]) + '</td><td>' + self.calcGenderPercentage(genderRatioData[13], genderRatioData[4]) + '</td></tr>'
    var tr21to25 = '<tr><td>21歳～25歳</td><td>' + self.calcGenderPercentage(genderRatioData[5], genderRatioData[14]) + '</td><td>' + self.calcGenderPercentage(genderRatioData[14], genderRatioData[5]) + '</td></tr>'
    var tr26to30 = '<tr><td>26歳～30歳</td><td>' + self.calcGenderPercentage(genderRatioData[6], genderRatioData[15]) + '</td><td>' + self.calcGenderPercentage(genderRatioData[15], genderRatioData[6]) + '</td></tr>'
    var tr31to35 = '<tr><td>31歳～35歳</td><td>' + self.calcGenderPercentage(genderRatioData[7], genderRatioData[16]) + '</td><td>' + self.calcGenderPercentage(genderRatioData[16], genderRatioData[7]) + '</td></tr>'
    var tr36to40 = '<tr><td>36歳～40歳</td><td>' + self.calcGenderPercentage(genderRatioData[8], genderRatioData[17]) + '</td><td>' + self.calcGenderPercentage(genderRatioData[17], genderRatioData[8]) + '</td></tr>'
    var tr41to45 = '<tr><td>41歳～45歳</td><td>' + self.calcGenderPercentage(genderRatioData[9], genderRatioData[18]) + '</td><td>' + self.calcGenderPercentage(genderRatioData[18], genderRatioData[9]) + '</td></tr>'
    var tr46to50 = '<tr><td>46歳～50歳</td><td>' + self.calcGenderPercentage(genderRatioData[10], genderRatioData[19]) + '</td><td>' + self.calcGenderPercentage(genderRatioData[19], genderRatioData[10]) + '</td></tr>'
    var tr51 = '<tr><td>51歳以上</td><td>' + self.calcGenderPercentage(genderRatioData[11], genderRatioData[20]) + '</td><td>' + self.calcGenderPercentage(genderRatioData[20], genderRatioData[11]) + '</td></tr>'
    var tableFoot = '</table><p class="total">【総人数:<span class="total-data">' + total + '人</span>】</p>'
    var gender_ratio_table = tableHead + tr11to15 + tr16to20 + tr21to25 + tr26to30 + tr31to35 + tr36to40 + tr41to45 + tr46to50 + tr51 + tableFoot
    $('.gender-ratio-table').append(gender_ratio_table);
}

// 年代別男女比のパーセンテージを計算する
DetailController.prototype.calcGenderPercentage = function(val1, val2) {
    if (val1 == null || val2 == null || val1 + val2 == 0) {
        return '-';
    }
    return Math.round((val1 / (val1 + val2) * 100)) + '%';
}

// 年代別男女比グラフ描画処理
DetailController.prototype.drawGenderRatioPlot = function(genderRatioData) {
    if (genderRatioData == null) {
        return;
    }
    var total = genderRatioData[0];
    var ticks = [ '51歳以上', '46歳~50歳', '41歳~45歳', '36歳~40歳', '31歳~35歳', '26歳~30歳', '21歳~25歳', '16歳~20歳', '11歳~15歳' ];
    var male = [ genderRatioData[11], genderRatioData[10], genderRatioData[9], genderRatioData[8], genderRatioData[7], genderRatioData[6], genderRatioData[5], genderRatioData[4], genderRatioData[3] ];
    var female = [ genderRatioData[20], genderRatioData[19], genderRatioData[18], genderRatioData[17], genderRatioData[16], genderRatioData[15], genderRatioData[14], genderRatioData[13], genderRatioData[12] ];
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
                side : 'left'
            }
        }, {
            yaxis : 'y2axis'
        } ],
        grid : {
            drawBorder : true,
            shadow : false
        },
        axes : {
            xaxis : {
                label : '人数',
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
    $.jqplot('gender-ratio-graph', [ male, female ],gender_options );
    if (total == 0){
        // 総人数が0の場合「データなし」マスク追加
        NoDateUtil.overlay('gender-ratio-graph');
    }
}

/**
 * 併売描画
 */
DetailController.prototype.drawHeibai = function() {
    var self = this;
    var param = {
        'sakuhin_code' : djangoObj.sakuhin_data.sakuhin_code,
        'process_code' : '04-01'
    };
    var promise = $.Deferred();
    var promiseAjax = $.Deferred();
    AjaxUtil.get('/ipdds/detail/', param, function(data) {
        var resultHeibai = JSON.parse(data.toString());
        promiseAjax.resolve(resultHeibai);
    }).then(function() {
        promiseAjax.then(function(resultHeibai) {
            var promisesGrid = [];
            var promises = [];
            for (var i = 0; i < resultHeibai.length; i++) {
                var titleCode = resultHeibai[i][0];
                promisesGrid.push(self.getHeibaiGridData(titleCode));
            }
            var grid = $.Deferred();
            promises.push(grid);

            $.when.apply($, promisesGrid).then(function() {
                var emptyCnt = 0;
                for (var i = 0; i < arguments.length; i++) {
                    var invalid = arguments[i];
                    if (invalid.length != 0) {
                        self.drawHeibaiGrid(arguments);
                    } else {
                        emptyCnt++;
                    }
                }
                if (emptyCnt == arguments.length) {
                    // 空の配列がlengthと同じ値だった場合
                    // Heibai領域を削除する
                    $('.heibai-area').remove();
                }
                grid.resolve();
            });
            $.when.apply($, promises).then(function() {
                promise.resolve();
            });
        });
    });
    return promise.promise();
}

DetailController.prototype.getHeibaiGridData = function(titleCode) {
    // グリッド表示用データの取得
    var promise = $.Deferred();
    var param = {
        'title_code' : titleCode,
        'process_code' : '04-02'
    };
    AjaxUtil.get('/ipdds/detail/', param, function(data) {
        var resultHeibaiData = JSON.parse(data.toString());
        promise.resolve(resultHeibaiData);
    });
    return promise.promise();
}

DetailController.prototype.drawHeibaiGrid = function(heibaiData) {
    var self = this;
    var resultData = [];
    var dataList;
    for (var i = 0; i < heibaiData.length; i++) {
        dataList = heibaiData[i];
        for (var j = 0; j < dataList.length; j++) {
            resultData.push(dataList[j]);
        }
    }
    var colNames = [ 'sakuhinName', 'mangaName', 'staff1', 'staff2', 'staff3', 'publisher' ];
    var modelArray = [];
    var data = GridUtil.createGridData(colNames, resultData);
    var width = $('#grid-heibai').width();
    var height = 'auto';
    if (data.length >= 16) {
        height = 345;
    }

    modelArray.push(GridUtil.createColModel({
        name : 'sakuhinName',
        align : 'left',
        width : width * 0.20,
        formatter : function(val, opt, rdt) {
            var sakuhinCode = val.substring(0, 10);
            var sakuhinName = val.substring(11);
            return '<a class="link" style="margin : 0px;" href="/ipdds/detail/?sakuhin_code=' + sakuhinCode + '">' + sakuhinName + '</a>'
        }
    }));
    modelArray.push(GridUtil.createColModel({
        name : 'mangaName',
        align : 'left',
        width : width * 0.30
    }));
    modelArray.push(GridUtil.createColModel({
        name : 'staff1',
        align : 'left',
        width : width * 0.15,
    }));
    modelArray.push(GridUtil.createColModel({
        name : 'staff2',
        align : 'left',
        width : width * 0.15,
    }));
    modelArray.push(GridUtil.createColModel({
        name : 'staff3',
        align : 'left',
        width : width * 0.15,
    }));
    modelArray.push(GridUtil.createColModel({
        name : 'publisher',
        align : 'left',
        width : width * 0.10,
    }));
    var option = {
        colNames : [ '作品名', 'マンガ名', 'スタッフ1', 'スタッフ2', 'スタッフ3', '出版社' ],
        colModel : modelArray,
        data : data,
        width : width,
        height : height,
        rowNum : data.length
    };

    GridUtil.renderNormalGrid('#grid-heibai', option, false);
}

/**
 * 関連文書描画
 */
DetailController.prototype.drawMediaReport = function() {
    var self = this;
    var param = {
        'sakuhin_code' : djangoObj.sakuhin_data.sakuhin_code,
        'process_code' : '05'
    };
    return AjaxUtil.get('/ipdds/detail/', param, function(data) {
        var resultMediaReport = JSON.parse(data.toString());
        if (resultMediaReport.length) {
            self.drawMediaReportGrid(resultMediaReport);
        } else {
            // 作品に紐づく関連文書が存在しない場合
            // MediaReport領域を削除
            $('.media-report-area').remove();
        }
    });
}

DetailController.prototype.drawMediaReportGrid = function(mediaReportData) {
    var colNames = [ 'year', 'category', 'mediaReportName' ];
    var modelArray = [];
    var data = GridUtil.createGridData(colNames, mediaReportData);
    var width = $('#grid-media-report').width();

    modelArray.push(GridUtil.createColModel({
        name : 'year',
        align : 'center',
        width : width * 0.15,
        formatter : function(val, opt, rdt) {
            return val + '年度'
        }
    }));
    modelArray.push(GridUtil.createColModel({
        name : 'category',
        align : 'center',
        width : width * 0.20
    }));
    modelArray.push(GridUtil.createColModel({
        name : 'mediaReportName',
        align : 'left',
        width : width * 0.65,
        formatter : function(val, opt, rdt) {
            var mediaReportCode = val.substring(0, 10);
            var mediaReportName = val.substring(11);
            return '<a class="link" onclick="window.open(\'/static/ipdds_app/file/media_report/' + mediaReportCode + '/' + mediaReportName + '\')">' + mediaReportName + '</a>'
        }
    }));

    var option = {
        colNames : [ '年度', 'カテゴリ', 'ファイル' ],
        colModel : modelArray,
        data : data,
        width : width,
    };

    GridUtil.renderNormalGrid('#grid-media-report', option, false);
}

/**
 * マンガ描画
 */
DetailController.prototype.drawManga = function() {
    var self = this;
    var param = {
        'sakuhin_code' : djangoObj.sakuhin_data.sakuhin_code,
        'process_code' : '06-01'
    };

    var promise = $.Deferred();
    var promiseAjax = $.Deferred();
    AjaxUtil.get('/ipdds/detail/', param, function(data) {
        var resultManga = JSON.parse(data.toString());
        promiseAjax.resolve(resultManga);
    }).then(function() {
        promiseAjax.then(function(resultManga) {
            var promisesGrid = [];
            var promisesGrid2 = [];
            var promisesPlot = [];
            var promises = [];
            for (var i = 0; i < resultManga.length; i++) {
                var titleCode = resultManga[i][0];
                promisesGrid.push(self.getMangaGridData(titleCode));
                promisesGrid2.push(self.getMangaGridData2(titleCode));
                promisesPlot.push(self.getMangaPlotData(titleCode));
            }

            var grid = $.Deferred();
            promises.push(grid);
            var grid2 = $.Deferred();
            promises.push(grid2);
            var plot = $.Deferred();
            promises.push(plot)

            $.when.apply($, promisesGrid).then(function() {
                // gridの処理をする。
                self.drawMangaGrid(arguments);
                grid.resolve();
            });

            $.when.apply($, promisesGrid2).then(function() {
                // grid2の処理をする。
                self.drawMangaIsbnGrid(arguments);
                grid2.resolve();
            });

            $.when.apply($, promisesPlot).then(function() {
                // plotの処理をする。
                self.drawMangaPlot(arguments);
                plot.resolve();
            });

            $.when.apply($, promises).then(function() {
                promise.resolve();
            });
        });
    });
    return promise.promise();
}

DetailController.prototype.getMangaGridData = function(titleCode) {
    // グリッド表示用データの取得(基本データ)
    var promise = $.Deferred();
    var param = {
        'title_code' : titleCode,
        'process_code' : '06-02'
    };
    AjaxUtil.get('/ipdds/detail/', param, function(data) {
        var resultMangaData = JSON.parse(data.toString());
        promise.resolve(resultMangaData);
    });
    return promise.promise();
}

DetailController.prototype.getMangaGridData2 = function(titleCode) {
    // グリッド表示用データの取得(実績データ)
    var promise = $.Deferred();
    var param = {
        'title_code' : titleCode,
        'process_code' : '06-03'
    };
    AjaxUtil.get('/ipdds/detail/', param, function(data) {
        var resultMangaData = JSON.parse(data.toString());
        promise.resolve(resultMangaData);
    });
    return promise.promise();
}

DetailController.prototype.getMangaPlotData = function(titleCode) {
    // グラフ表示用データの取得
    var promise = $.Deferred();
    var param = {
        'title_code' : titleCode,
        'process_code' : '06-04'
    };
    AjaxUtil.get('/ipdds/detail/', param, function(data) {
        var resultMangaData = JSON.parse(data.toString());
        promise.resolve(resultMangaData);
    });
    return promise.promise();
}

DetailController.prototype.drawMangaGrid = function(mangaData) {
    var self = this;
    var resultData = self.drawResultGridData(mangaData);
    var colNames = [ 'mangaName', 'staff1', 'staff2', 'staff3', 'publisher', 'rensai', 'published', 'endFlg', 'award' ];
    var modelArray = [];
    var data = GridUtil.createGridData(colNames, resultData);
    var width = $('#grid-manga').width();
    var height = 'auto';
    if (data.length >= 16) {
        height = 345;
    }

    modelArray.push(GridUtil.createColModel({
        name : 'mangaName',
        width : width * 0.28
    }));
    modelArray.push(GridUtil.createColModel({
        name : 'staff1',
        align : 'left',
        width : width * 0.07,
    }));
    modelArray.push(GridUtil.createColModel({
        name : 'staff2',
        align : 'left',
        width : width * 0.07,
    }));
    modelArray.push(GridUtil.createColModel({
        name : 'staff3',
        align : 'left',
        width : width * 0.07,
    }));
    modelArray.push(GridUtil.createColModel({
        name : 'publisher',
        align : 'left',
        width : width * 0.05,
    }));
    modelArray.push(GridUtil.createColModel({
        name : 'rensai',
        align : 'left',
        width : width * 0.05,
        formatter : function(val, opt, rdt) {
            if(val && val != '0001年01月'){
                return val;
            } else {
                return ' ';
            }
        }
    }));
    modelArray.push(GridUtil.createColModel({
        name : 'published',
        align : 'right',
        width : width * 0.02,
        sorttype : 'number'
    }));
    modelArray.push(GridUtil.createColModel({
        name : 'endFlg',
        align : 'center',
        width : width * 0.04,
    }));
    modelArray.push(GridUtil.createColModel({
        name : 'award',
        align : 'left',
        width : width * 0.35,
    }));

    var option = {
        colNames : [ 'マンガ名', 'スタッフ1', 'スタッフ2', 'スタッフ3', '出版社', '連載開始年月', '既刊', '連載終了<br>フラグ', '作品受賞歴' ],
        colModel : modelArray,
        data : data,
        width : width,
        height : height,
        rowNum : data.length
    };

    GridUtil.renderNormalGrid('#grid-manga', option, false);
}

DetailController.prototype.drawMangaIsbnGrid = function(mangaData) {
    var self = this;
    var resultData = self.drawResultGridData(mangaData);
    var colNames = [ 'is_draw', 'mangaName', 'firstTotalSales', 'lastestTotalSales', 'avgSales', 'sumSales' ];
    var modelArray = [];
    var data = GridUtil.createGridData(colNames, resultData);
    var width = $('#grid-manga-isbn').width();
    var height = 'auto';
    if (data.length >= 16) {
        height = 345;
    }
    modelArray.push(GridUtil.createColModel({
        name : 'is_draw',
        align : 'center',
        width : width * 0.05,
        formatter : function(val, opt, rdt) {
            if(opt.rowId < 5){
                return '<input type="checkbox" class="grid-checkbox manga" value="' + val + '"/ style="margin: 10px;" checked>';
            }
            else{
                return '<input type="checkbox" class="grid-checkbox manga" value="' + val + '"/ style="margin: 10px;" >';
            }
        }
    }));
    modelArray.push(GridUtil.createColModel({
        name : 'mangaName',
        width : width * 0.50
    }));
    modelArray.push(GridUtil.createColModel({
        name : 'firstTotalSales',
        align : 'right',
        width : width * 0.10,
        sorttype : 'number',
        formatter : function(val, opt, rdt) {
            return val ? StringUtil.comma_separated(val+'部') : 'ー';
        },
    }));
    modelArray.push(GridUtil.createColModel({
        name : 'lastestTotalSales',
        align : 'right',
        width : width * 0.10,
        sorttype : 'number',
        formatter : function(val, opt, rdt) {
            return val ? StringUtil.comma_separated(val+'部') : 'ー';
        },
    }));
    modelArray.push(GridUtil.createColModel({
        name : 'avgSales',
        align : 'right',
        width : width * 0.10,
        sorttype : 'number',
        formatter : function(val, opt, rdt) {
            return val ? StringUtil.comma_separated(val+'部') : 'ー';
        },
    }));
    modelArray.push(GridUtil.createColModel({
        name : 'sumSales',
        align : 'right',
        width : width * 0.10,
        sorttype : 'number',
        formatter : function(val, opt, rdt) {
            return val ? StringUtil.comma_separated(val+'部') : 'ー';
        },
    }));

    var option = {
        colNames : [ '描画', 'マンガ名', '1巻の<br>累計発行部数', '最新刊の<br>累計発行部数', '単巻あたりの<br>平均発行部数', '累計発行部数' ],
        colModel : modelArray,
        data : data,
        width : width,
        height : height,
        rowNum : data.length
    };

    GridUtil.renderNormalGrid('#grid-manga-isbn', option, false);
}

DetailController.prototype.drawMangaPlot = function(mangaData) {
    var self = this;

    var copiedOptions = jQuery.extend(true, {}, self.defaultPlotOption.options);
    copiedOptions.title = '累計発行部数';
    copiedOptions.highlighter = {
        show : true,
        showMarker : true,
        sizeAdjust : 7,
        tooltipLocation : 'ne',
        tooltipAxes : 'y',
        formatString : "部数:%s"
    };
    copiedOptions.legend.location = 's'

    var data = self.convertPlotData(arguments);
    var array = []
    var length = 4;
    if(data.length<length){
        length = data.length;
    }
    copiedOptions.series = [];
    for(var i = 0;i<length;i++){
        copiedOptions.series.push({
            label : data[i].name,
            color : self.defaultPlotOption.colorArray[i]
        });
        array.push(data[i].data);
    }
    $.jqplot('plot-manga', array, copiedOptions);
    self.jqPlot.manga = $.jqplot("plot-manga", array, copiedOptions);
}

DetailController.prototype.replotManga = function() {
    var self = this;

    // Mangaグラフ削除
    self.jqPlot.manga.destroy();

    // グラフ表示用のデータ取得
    var promisesPlot = [];
    $('.grid-checkbox.manga').each(function(i, elem) {
        var checkbox = $(elem);
        if (checkbox.is(':checked')) {
            promisesPlot.push(self.getMangaPlotData(checkbox.val()));
        }
    });

    $.when.apply($, promisesPlot).then(function() {
        self.drawMangaPlot(arguments);
    });
}

/**
 * Twitter描画
 */
DetailController.prototype.drawTwitter = function() {
    var self = this;
    var param = {
        'sakuhin_code' : djangoObj.sakuhin_data.sakuhin_code,
        'process_code' : '07-01'
    };

    var promise = $.Deferred();
    var promiseAjax = $.Deferred();
    AjaxUtil.get('/ipdds/detail/', param, function(data) {
        var resultTwitter = JSON.parse(data.toString());
        promiseAjax.resolve(resultTwitter);
    }).then(function() {
        promiseAjax.then(function(resultTwitter) {

            if (resultTwitter.length) {
                // 作品に紐づくTwitterデータが存在する場合
                // Grid・Plotの表示を行う
                var promisesGrid = [];
                var promisesPlot = [];
                var promises = [];
                for (var i = 0; i < resultTwitter.length; i++) {
                    var twitterId = resultTwitter[i][0];
                    promisesGrid.push(self.getTwitterGridData(twitterId));
                    promisesPlot.push(self.getTwitterPlotData(twitterId));
                }

                var grid = $.Deferred();
                promises.push(grid);
                var plot = $.Deferred();
                promises.push(plot);

                $.when.apply($, promisesGrid).then(function() {
                    self.drawTwitterGrid(arguments);
                    grid.resolve();
                });

                $.when.apply($, promisesPlot).then(function() {
                    self.drawTwitterPlot(arguments);
                    plot.resolve();
                });

                $.when.apply($, promises).then(function() {
                    promise.resolve();
                });
            } else {
                // 作品に紐づくTwitterデータが存在しない場合
                // Twitter領域を削除
                $('.twitter-area').remove();
                promise.resolve();
            }
        });
    });
    return promise.promise();
}

DetailController.prototype.getTwitterGridData = function(twitterId) {
    // グリッド表示用データの取得
    var promise = $.Deferred();
    var param = {
        'twitter_id' : twitterId,
        'process_code' : '07-02'
    };
    AjaxUtil.get('/ipdds/detail/', param, function(data) {
        var resultTwitterData = JSON.parse(data.toString());
        promise.resolve(resultTwitterData);
    });
    return promise.promise();
}

DetailController.prototype.getTwitterPlotData = function(twitterId) {
    // グラフ表示用データの取得
    var promise = $.Deferred();
    var param = {
        'twitter_id' : twitterId,
        'process_code' : '07-03'
    };
    AjaxUtil.get('/ipdds/detail/', param, function(data) {
        var resultTwitterData = JSON.parse(data.toString());
        promise.resolve(resultTwitterData);
    });
    return promise.promise();
}

DetailController.prototype.drawTwitterGrid = function(twitterData) {
    var self = this;
    var resultData = self.drawResultGridData(twitterData);
    var colNames = [ 'is_draw', 'accountName', 'latest', '3monthsAgo', '1yearAgo', 'link' ];
    var modelArray = [];
    var data = GridUtil.createGridData(colNames, resultData);
    var width = $('#grid-twitter').width();
    var height = 'auto';
    if (data.length >= 16) {
        height = 345;
    }

    modelArray.push(GridUtil.createColModel({
        name : 'is_draw',
        width : width * 0.05,
        align : 'center',
        formatter : function(val, opt, rdt) {
            if (opt.rowId < 5) {
                return '<input type="checkbox" class="grid-checkbox twitter" value="' + val + '"/ style="margin: 10px;" checked>';
            } else {
                return '<input type="checkbox" class="grid-checkbox twitter" value="' + val + '"/ style="margin: 10px;" >';
            }
        },
    }));
    modelArray.push(GridUtil.createColModel({
        name : 'accountName',
        width : width * 0.40
    }));
    modelArray.push(GridUtil.createColModel({
        name : 'latest',
        align : 'right',
        width : width * 0.13,
        sorttype : 'number',
        formatter : function(val, opt, rdt) {
            return val ? StringUtil.comma_separated(val) : 'ー';
        }
    }));
    modelArray.push(GridUtil.createColModel({
        name : '3monthsAgo',
        align : 'right',
        width : width * 0.13,
        sorttype : 'number',
        formatter : function(val, opt, rdt) {
            return val ? StringUtil.comma_separated(val) : 'ー';
        }
    }));
    modelArray.push(GridUtil.createColModel({
        name : '1yearAgo',
        align : 'right',
        width : width * 0.13,
        sorttype : 'number',
        formatter : function(val, opt, rdt) {
            return val ? StringUtil.comma_separated(val) : 'ー';
        }
    }));
    modelArray.push(GridUtil.createColModel({
        name : 'link',
        width : width * 0.10,
        align : 'center',
        formatter : function(val, opt, rdt) {
            return '<a  class="twitter-link" onclick="window.open(\'https://twitter.com/' + val + '\')"><i class="fab fa-twitter-square" style="font-size: 30px"></i></a></a>'
        },
    }));

    var option = {
        colNames : [ '描画', 'アカウント名', '最新<br>フォロワー', '三か月前<br>フォロワー', '一年前<br>フォロワー', 'Twitter' ],
        colModel : modelArray,
        data : data,
        width : width,
        height : height,
        rowNum : data.length
    };

    GridUtil.renderNormalGrid('#grid-twitter', option, false);
}

DetailController.prototype.drawTwitterPlot = function(twitterData) {
    var self = this;

    var copiedOptions = jQuery.extend(true, {}, self.defaultPlotOption.options);
    copiedOptions.title = 'フォロワー数';
    copiedOptions.highlighter = {
        show : true,
        showMarker : true,
        sizeAdjust : 7,
        tooltipLocation : 'ne',
        tooltipAxes : 'y',
        formatString : "フォロワー数:%s"
    };
    copiedOptions.legend.location = 's'

    var data = self.convertPlotData(arguments);
    var array = []
    var length = 4;
    if(data.length<length){
        length = data.length;
    }
    copiedOptions.series = [];
    for(var i = 0;i<length;i++){
        copiedOptions.series.push({
            label : data[i].name,
            color : self.defaultPlotOption.colorArray[i]
        });
        array.push(data[i].data);
    }
    $.jqplot('plot-twitter', array, copiedOptions);
    self.jqPlot.twitter = $.jqplot("plot-twitter", array, copiedOptions);
}

DetailController.prototype.replotTwitter = function() {
    var self = this;

    // Twitterグラフ削除
    self.jqPlot.twitter.destroy();

    // グラフ表示用のデータ取得
    var promisesPlot = [];
    $('.grid-checkbox.twitter').each(function(i, elem) {
        var checkbox = $(elem);
        if (checkbox.is(':checked')) {
            promisesPlot.push(self.getTwitterPlotData(checkbox.val()));
        }
    });

    $.when.apply($, promisesPlot).then(function() {
        self.drawTwitterPlot(arguments);
    });
}

/**
 * ゲーム描画
 */
DetailController.prototype.drawGame = function() {
    var self = this;
    var param = {
        'sakuhin_code' : djangoObj.sakuhin_data.sakuhin_code,
        'process_code' : '08-01'
    };

    var promise = $.Deferred();
    var promiseAjax = $.Deferred();
    AjaxUtil.get('/ipdds/detail/', param, function(data) {
        var resultGame = JSON.parse(data.toString());
        promiseAjax.resolve(resultGame);
    }).then(function() {
        promiseAjax.then(function(resultGame) {
            if (resultGame.length) {
                // 作品に紐づくゲームデータが存在する場合
                // Grid・Plotの表示を行う
                var promisesGrid = [];
                var promisesPlot = [];
                var promises = [];
                for (var i = 0; i < resultGame.length; i++) {
                    var titleCode = resultGame[i][0];
                    promisesGrid.push(self.getGameGridData(titleCode));
                    promisesPlot.push(self.getGamePlotData(titleCode));
                }

                var grid = $.Deferred();
                promises.push(grid);
                var plot = $.Deferred();
                promises.push(plot);

                $.when.apply($, promisesGrid).then(function() {
                    // gridの処理をする。
                    self.drawGameGrid(arguments);
                    grid.resolve();
                });

                $.when.apply($, promisesPlot).then(function() {
                    // plotの処理をする。
                    self.drawGamePlot(arguments);
                    plot.resolve();
                });

                $.when.apply($, promises).then(function() {
                    promise.resolve();
                });
            } else {
                // 作品に紐づくゲームデータが存在しない場合
                // Game領域を削除
                $('.game-area').remove();
                promise.resolve();
            }
        });
    });
    return promise.promise();
}

DetailController.prototype.getGameGridData = function(titleCode) {
    // グリッド表示用データの取得
    var promise = $.Deferred();
    var param = {
        'title_code' : titleCode,
        'process_code' : '08-02'
    };
    AjaxUtil.get('/ipdds/detail/', param, function(data) {
        var resultGameData = JSON.parse(data.toString());
        promise.resolve(resultGameData);
    });
    return promise.promise();
}

DetailController.prototype.getGamePlotData = function(titleCode) {
    // グラフ表示用データの取得
    var promise = $.Deferred();
    var param = {
        'title_code' : titleCode,
        'process_code' : '08-03'
    };
    AjaxUtil.get('/ipdds/detail/', param, function(data) {
        var resultGameData = JSON.parse(data.toString());
        promise.resolve(resultGameData);
    });
    return promise.promise();
}

DetailController.prototype.drawGameGrid = function(gameData) {
    var self = this;
    var resultData = self.drawResultGridData(gameData);
    var colNames = [ 'is_draw', 'gameName', 'platform', 'haibaiCompany', 'release', 'totalSales' ];
    var modelArray = [];
    var data = GridUtil.createGridData(colNames, resultData);
    var width = $('#grid-game').width();
    var height = 'auto';
    if (data.length >= 16) {
        height = 345;
    }

    modelArray.push(GridUtil.createColModel({
        name : 'is_draw',
        width : width * 0.05,
        align : 'center',
        formatter : function(val, opt, rdt) {
            if (opt.rowId < 5) {
                return '<input type="checkbox" class="grid-checkbox game" value="' + val + '"/ style="margin: 10px;" checked>';
            } else {
                return '<input type="checkbox" class="grid-checkbox game" value="' + val + '"/ style="margin: 10px;" >';
            }
        },
    }));
    modelArray.push(GridUtil.createColModel({
        name : 'gameName',
        align : 'left',
        width : width * 0.50
    }));
    modelArray.push(GridUtil.createColModel({
        name : 'platform',
        align : 'left',
        width : width * 0.06,
    }));
    modelArray.push(GridUtil.createColModel({
        name : 'haibaiCompany',
        align : 'left',
        width : width * 0.25,
        formatter : function(val, opt, rdt) {
            return val ? val : 'ー';
        }
    }));
    modelArray.push(GridUtil.createColModel({
        name : 'release',
        align : 'left',
        width : width * 0.09,
        formatter : function(val, opt, rdt) {
            return val ? val : 'ー';
        }
    }));
    modelArray.push(GridUtil.createColModel({
        name : 'totalSales',
        align : 'right',
        width : width * 0.10,
        sorttype : 'number',
        formatter : function(val, opt, rdt) {
            return val ? StringUtil.comma_separated(val+'本') : 'ー';
        },
    }));

    var option = {
        colNames : [ '描画' ,'ゲーム名', '対応機種', '発売元', '発売日', '売上<br>累計本数' ],
        colModel : modelArray,
        data : data,
        width : width,
        height : height,
        rowNum : data.length
    };

    GridUtil.renderNormalGrid('#grid-game', option, false);
}

DetailController.prototype.drawGamePlot = function(appData) {
    var self = this;

    var copiedOptions = jQuery.extend(true, {}, self.defaultPlotOption.options);
    copiedOptions.title = '累計売上本数';
    copiedOptions.highlighter = {
        show : true,
        showMarker : true,
        sizeAdjust : 7,
        tooltipLocation : 'ne',
        tooltipAxes : 'y',
        formatString : "本数:%s"
    };
    copiedOptions.legend.location = 's'

    var data = self.convertPlotData(arguments);
    var array = []
    var length = 4;
    if(data.length<length){
        length = data.length;
    }
    copiedOptions.series = [];
    for(var i = 0;i<length;i++){
        copiedOptions.series.push({
            label : data[i].name,
            color : self.defaultPlotOption.colorArray[i]
        });
        array.push(data[i].data);
    }
    $.jqplot('plot-game', array, copiedOptions);
    self.jqPlot.game = $.jqplot("plot-game", array, copiedOptions);
}

DetailController.prototype.replotGame = function() {
    var self = this;

    // Gameグラフ削除
    self.jqPlot.game.destroy();

     // グラフ表示用のデータ取得
    var promisesPlot = [];
    $('.grid-checkbox.game').each(function(i, elem) {
        var checkbox = $(elem);
        if (checkbox.is(':checked')) {
            promisesPlot.push(self.getGamePlotData(checkbox.val()));
        }
    });

    $.when.apply($, promisesPlot).then(function() {
        self.drawGamePlot(arguments);
    });
}

/**
 * アプリ描画
 */
DetailController.prototype.drawApp = function() {
    var self = this;
    var param = {
        'sakuhin_code' : djangoObj.sakuhin_data.sakuhin_code,
        'process_code' : '09-01'
    };

    var promise = $.Deferred();
    var promiseAjax = $.Deferred();
    AjaxUtil.get('/ipdds/detail/', param, function(data) {
        // アプリタイトルコード,ios,android取得
        var resultApp = JSON.parse(data.toString());
        promiseAjax.resolve(resultApp);
    }).then(function() {
        promiseAjax.then(function(resultApp) {
            if (resultApp.length) {
                // 作品に紐づくアプリデータが存在する場合
                // Grid・Plotの表示を行う
                var promisesGrid = [];
                var promisesPlot = [];
                var promisesPlot2 = [];
                var promises = [];
                for (var i = 0; i < resultApp.length; i++) {
                    // app_id_ios,app_id_androidを渡す
                    var titleCode = resultApp[i][0];
                    var appIdIos = resultApp[i][1];
                    var appIdAndroid = resultApp[i][2];
                    promisesGrid.push(self.getAppGridData(titleCode, appIdIos, appIdAndroid));
                    promisesPlot.push(self.getAppPlotData(appIdIos, appIdAndroid));
                    promisesPlot2.push(self.getAppPlotData2(appIdIos, appIdAndroid));
                }

                var grid = $.Deferred();
                promises.push(grid);
                var plot = $.Deferred();
                promises.push(plot);
                var plot2 = $.Deferred();
                promises.push(plot2);

                $.when.apply($, promisesGrid).then(function() {
                    // gridの処理をする。
                    self.drawAppGrid(arguments);
                    grid.resolve();
                });

                $.when.apply($, promisesPlot).then(function() {
                    // plotの処理をする。
                    self.drawAppPlot(arguments);
                    plot.resolve();
                });

                $.when.apply($, promisesPlot2).then(function() {
                    // plot2の処理をする。
                    self.drawAppPlot2(arguments);
                    plot2.resolve();
                });

                $.when.apply($, promises).then(function() {
                    promise.resolve();
                });
            } else {
                // 作品に紐づくアプリデータが存在しない場合
                // App領域を削除
                $('.app-area').remove();
                promise.resolve();
            }
        });
    });
    return promise.promise();
}

DetailController.prototype.getAppGridData = function(titleCode, appIdIos, appIdAndroid) {
    // グリッド表示用データの取得(基本データ)
    var promise = $.Deferred();
    var param = {
        'title_code' : titleCode,
        'app_id_ios' : appIdIos,
        'app_id_android' : appIdAndroid,
        'process_code' : '09-02'
    };
    AjaxUtil.get('/ipdds/detail/', param, function(data) {
        var resultAppData = JSON.parse(data.toString());
        promise.resolve(resultAppData);
    });
    return promise.promise();
}

DetailController.prototype.getAppPlotData = function(appIdIos, appIdAndroid) {
    // グラフ表示用データの取得(ダウンロード数情報)
    var promise = $.Deferred();
    var param = {
        'app_id_ios' : appIdIos,
        'app_id_android' : appIdAndroid,
        'process_code' : '09-03'
    };
    AjaxUtil.get('/ipdds/detail/', param, function(data) {
        var resultAppData = JSON.parse(data.toString());
        promise.resolve(resultAppData);
    });
    return promise.promise();
}

DetailController.prototype.getAppPlotData2 = function(appIdIos, appIdAndroid) {
    // グラフ表示用データの取得(収益情報)
    var promise = $.Deferred();
    var param = {
        'app_id_ios' : appIdIos,
        'app_id_android' : appIdAndroid,
        'process_code' : '09-04'
    };
    AjaxUtil.get('/ipdds/detail/', param, function(data) {
        var resultAppData = JSON.parse(data.toString());
        promise.resolve(resultAppData);
    });
    return promise.promise();
}

DetailController.prototype.drawAppGrid = function(appData) {
    var self = this;
    var resultData = self.drawResultGridData(appData);
    var colNames = [ 'is_draw' ,'appName', 'platform', 'haibaiCompany', 'release', 'lastThreeMonthsSales' ];
    var modelArray = [];
    var data = GridUtil.createGridData(colNames, resultData);
    var width = $('#grid-app').width();
    var height = 'auto';
    if (data.length >= 16) {
        height = 345;
    }

    modelArray.push(GridUtil.createColModel({
        name : 'is_draw',
        width : width * 0.05,
        align : 'center',
        formatter : function(val, opt, rdt) {
            if (opt.rowId < 5) {
                var array = val.split('/');
                return '<input type="checkbox" class="grid-checkbox app" data-app-id-ios="'+array[0]+'" data-app-id-android="'+array[1]+'"/ style="margin: 10px;" checked>';
            } else {
                return '<input type="checkbox" class="grid-checkbox app" data-app-id-ios="'+array[0]+'" data-app-id-android="'+array[1]+'"/ style="margin: 10px;" >';
            }
        },
    }));
    modelArray.push(GridUtil.createColModel({
        name : 'appName',
        width : width * 0.50
    }));
    modelArray.push(GridUtil.createColModel({
        name : 'platform',
        align : 'left',
        width : width * 0.10,
        sorttype : 'number'
    }));
    modelArray.push(GridUtil.createColModel({
        name : 'haibaiCompany',
        align : 'left',
        width : width * 0.20,
        sorttype : 'number',
        formatter : function(val, opt, rdt) {
            return val ? val : 'ー';
        }
    }));
    modelArray.push(GridUtil.createColModel({
        name : 'release',
        align : 'left',
        width : width * 0.10,
        sorttype : 'number',
        formatter : function(val, opt, rdt) {
            return val ? val : 'ー';
        }
    }));
    modelArray.push(GridUtil.createColModel({
        name : 'lastThreeMonthsSales',
        width : width * 0.10,
        align : 'right',
        sorttype : 'number',
        formatter : function(val, opt, rdt) {
            return val ? StringUtil.comma_separated('$'+val) : 'ー';
        },
    }));

    var option = {
        colNames : [ '描画' ,'アプリ名', 'プラットフォーム', '発売元', '発売日', '直近3か月の<br>月商平均' ],
        colModel : modelArray,
        data : data,
        width : width,
        height : height,
        rowNum : data.length
    };

    GridUtil.renderNormalGrid('#grid-app', option, false);
}

DetailController.prototype.drawAppPlot = function(appData) {
    var self = this;

    var copiedOptions = jQuery.extend(true, {}, self.defaultPlotOption.options);
    copiedOptions.title = 'ダウンロード数';
    copiedOptions.highlighter = {
        show : true,
        showMarker : true,
        sizeAdjust : 7,
        tooltipLocation : 'ne',
        tooltipAxes : 'y',
        formatString : "ダウンロード数:%s"
    };
    copiedOptions.legend.location = 's'

    var data = self.convertPlotData(arguments);
    var array = []
    var length = 4;
    if(data.length<length){
        length = data.length;
    }
    copiedOptions.series = [];
    for(var i = 0;i<length;i++){
        copiedOptions.series.push({
            label : data[i].name,
            color : self.defaultPlotOption.colorArray[i]
        });
        array.push(data[i].data);
    }
    $.jqplot('plot-app-download', array, copiedOptions);
    self.jqPlot.appDownload = $.jqplot("plot-app-download", array, copiedOptions);
}

DetailController.prototype.drawAppPlot2 = function(appData) {
    var self = this;

    var copiedOptions = jQuery.extend(true, {}, self.defaultPlotOption.options);
    copiedOptions.title = '収益';
    copiedOptions.highlighter = {
        show : true,
        showMarker : true,
        sizeAdjust : 7,
        tooltipLocation : 'ne',
        tooltipAxes : 'y',
        formatString : "月商:%s"
    };
    copiedOptions.legend.location = 's'

    var data = self.convertPlotData(arguments);
    var array = []
    var length = 4;
    if(data.length<length){
        length = data.length;
    }
    copiedOptions.series = [];
    for(var i = 0;i<length;i++){
        copiedOptions.series.push({
            label : data[i].name,
            color : self.defaultPlotOption.colorArray[i]
        });
        array.push(data[i].data);
    }
    $.jqplot('plot-app-sales', array, copiedOptions);
    self.jqPlot.appSales = $.jqplot("plot-app-sales", array, copiedOptions);
}

DetailController.prototype.replotApp = function() {
    var self = this;

    // Appダウンロードグラフ削除
    self.jqPlot.appDownload.destroy();
    // App収益グラフ削除
    self.jqPlot.appSales.destroy();

    // グラフ表示用のデータ取得
    var promisesPlot = [];
    var promisesPlot2 = [];
    $('.grid-checkbox.app').each(function(i, elem) {
        var checkbox = $(elem);
        console.log(checkbox);
        if (checkbox.is(':checked')) {
            var appIdIos = checkbox.attr('data-app-id-ios');
            var appIdAndroid = checkbox.attr('data-app-id-android');

            promisesPlot.push(self.getAppPlotData(appIdIos, appIdAndroid));
            promisesPlot2.push(self.getAppPlotData2(appIdIos, appIdAndroid));
        }
    });
    $.when.apply($, promisesPlot).then(function() {
        self.drawAppPlot(arguments);
    });
    $.when.apply($, promisesPlot2).then(function() {
        self.drawAppPlot2(arguments);
    });
}

/**
 * グラフの設定
 */
DetailController.prototype.defaultPlotOption = {
    colorArray : [ '#cddf54', '#fbd179', '#26B4E3', '#bd70c7' ],
    options : {
        seriesDefaults : {
            pointLabels : {
                show : true,
                formatString : "%'d"
            }
        },
        title : '実績グラフ',
        legend : {
            show : true,
            placement : 'outsideGrid',
            location : 's'
        },
        axes : {
            xaxis : {
                renderer : $.jqplot.DateAxisRenderer,
                tickRenderer : $.jqplot.CanvasAxisTickRenderer,
                tickInterval : '1 months',
                tickOptions : {
                    angle : -45,
                    formatString : "%Y/%m"
                },
                min : (function() {
                    var dt = new Date();
                    dt.setDate(1);
                    dt.setFullYear(dt.getFullYear() - 1);
                    dt.setMonth(dt.getMonth() - 1);
                    return dt.getFullYear() + '-' + StringUtil.lpad(dt.getMonth() + 1, 2) + '-' + StringUtil.lpad(dt.getDate(), 2)
                }()),
                max : (function() {
                    var dt = new Date();
                    dt.setDate(1);
                    // dt.setMonth(dt.getMonth() + 1);
                    return dt.getFullYear() + '-' + StringUtil.lpad(dt.getMonth() + 1, 2) + '-' + StringUtil.lpad(dt.getDate(), 2);
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
            constrainZoomTo : 'none',
            showTooltip : false
        },
        highlighter : {
            show : true,
            showMarker : true,
            sizeAdjust : 7,
            tooltipLocation : 'ne',
            tooltipAxes : 'y',
            formatString : ":%s"
        }
    }
}
DetailController.prototype.setPlotOption = function() {
    return $.Deferred().resolve().promise();
}

DetailController.prototype.convertPlotData = function(data) {
    var self = this;
    var ret = [];
    data = data[0];
    for (var i = 0; i < data.length; i++) {
        for (var j = 0; j < data[i].length; j++) {
            ret.push(data[i][j]);
        }
    }
    var arrayList = []
    for (var i = 0; i < ret.length; i++) {
        var temp = self.findPlotData(arrayList,ret[i][0],ret[i][1]);
        if(temp){
            temp['data'].push( [ret[i][2],ret[i][3]]);
        }
        else{
            var array = {
                'key' : ret[i][0],
                'name' : ret[i][1],
                'data' : [[ret[i][2],ret[i][3]]]
            };
            arrayList.push(array);
        }
    }
    return arrayList;
}

DetailController.prototype.findPlotData = function(array,key,name){
    for(var i = 0;i<array.length;i++){
        if(array[i]['key']==key){
            if(array[i]['name']==name){
                return array[i];
            }
        }
    }
    return null;
}

/**
 * plotデータの一時格納
 */
DetailController.prototype.jqPlot = {
    manga : {},
    twitter : {},
    game : {},
    appDownload : {},
    appSales : {}
}

/**
 * 取得したデータをgridで表示可能な形に変換する
 */
DetailController.prototype.drawResultGridData = function(data){
    var resultData = [];
    var dataList;
    for (var i = 0; i < data.length; i++) {
        dataList = data[i];
        for (var j = 0; j < dataList.length; j++) {
            resultData.push(dataList[j]);
        }
    }
    return resultData;
}

// ----------------------------------------------------------------------------------------------
// 初期化処理
// ----------------------------------------------------------------------------------------------
$(function() {
    var controller = new DetailController();
    controller.init();
});
