var HomeListController = function() {};
HomeListController.prototype = new AbstractController();

/**
 * HOME管理画面の主処理
 */
HomeListController.prototype.execute = function() {
    var self = this;

    // メッセージ欄表示
    // MockMsgUtil.showStatusMsg('#target-ipname');

    // バナープレビュー表示
    self.bannerPreview();

    return $.Deferred()
        .resolve()
        .promise();
};
HomeListController.prototype.bannerPreview = function() {

    // オーバーレイ表示切替
    var hideOverlayFlg = false;
    for(var obj in djangoObj.banner){
        if(false===djangoObj.banner[obj].is_invalid){
            hideOverlayFlg = true;
        }
    };

    if(hideOverlayFlg){
        $('.preview-overlay').hide();
    }else{
        $('.preview-overlay').show();
    }
};

/**
 * メニュー選択処理
 */
HomeListController.prototype.selectedMenu = function() {
    return '.menu-home-master';
};

/**
 * イベント登録処理
 */
HomeListController.prototype.bindEvent = function() {
    var self = this;

    // 新規登録ボタン
    self.newsCreateButton();
    // 更新ボタン
    self.newsUpdateButton();

    // プレビューエリアクリック
    $('#preview-1').on('click', function() {
        window.location.href = '../home_update?preview=1';
    });

    $('#preview-2').on('click', function() {
        window.location.href = '../home_update?preview=2';
    });

    $('#preview-3').on('click', function() {
        window.location.href = '../home_update?preview=3';
    });

    self.homeBannerDispButton();

    // 入力値をクリアボタン
    $('.back-button').on('click', function() {
        $('input').each(function(index, element) {
            if(!($(element).attr('name') == 'csrfmiddlewaretoken' || $(element).attr('name') == 'news-id')){
                $(element).val('');
            }
        });
        $('textarea').val('');
    });

    // 更新履歴DLエリアのイベント設定
    NoticeTableUtil.setDLArea();

    // 更新履歴CSVダウンロード
    self.downloadTableCsv('t_top_news','m_banner', 'HOME画面');

    return $.Deferred()
        .resolve()
        .promise();
};
HomeListController.prototype.homeBannerDispButton = function() {
    // 表示/非表示ボタン
    $('.display-button').on('click', function() {
        var dispButton = $(this);

        if (dispButton.hasClass('disable-button')) {
            var param = {
                'banner-disable' : false,
            };
            AjaxUtil.post('/admin_app/home_list/', param, function(){
                dispButton.removeClass('disable-button');
                $('.preview-overlay').hide();
                dispButton.text('表示');   
            });
        } else {
            var param = {
                'banner-disable' : true,
            };

            AjaxUtil.post('/admin_app/home_list/', param, function(){
               dispButton.addClass('disable-button');
                $('.preview-overlay').show();
                dispButton.text('非表示');
            });
        }
    });
}
// 新規登録ボタン
HomeListController.prototype.newsCreateButton = function() {
    var self = this;
    $('.create').on('click', function() {
        var param = {
            'news_create': true,
            'news_id' : $('#news-id').val(),
            'news_subject' : $('#news-subject').val(),
            'news_headline' : $('#news-headline').val(),
            'news_info_detail' : $('#info-detail').val(),
            'news_link_url' : $('#news-link-url').val()
        };
        AjaxUtil.post('/admin_app/home_list/', param, function(data){
            self.drawResult(data,function(){
                $('.messege').text('お知らせを新規登録しました。');
                $('.status-msg').slideDown();
                setTimeout(function(){$('.status-msg').slideUp('slow')},5000);
            });
        });
    });
};

// 更新ボタン
HomeListController.prototype.newsUpdateButton = function() {
    var self = this;
    $('.update').on('click', function() {
        var param = {
            'news_update': true,
            'news_id' : $('#news-id').val(),
            'news_subject' : $('#news-subject').val(),
            'news_headline' : $('#news-headline').val(),
            'news_info_detail' : $('#info-detail').val(),
            'news_link_url' : $('#news-link-url').val()
        };
        AjaxUtil.post('/admin_app/home_list/', param, function(data){
            self.drawResult(data,function(){
                $('.messege').text('お知らせを更新しました。');
                $('.status-msg').stop().slideDown();
                setTimeout(function(){$('.status-msg').stop().slideUp('slow')},5000);
            });
        });
    });
}
HomeListController.prototype.drawResult = function(data,callback){
    var result = JSON.parse(data.toString());
    $('#news-subject-err').text('');
    $('#news-headline-err').text('');
    $('#news-info-detail-err').text('');
    $('#news-link-url-err').text('');
    if(result.is_error){
        if(!(typeof result.errors.news_subject === 'undefined')){
            result.errors.news_subject.forEach(function(obj,idx,array){
                $('#news-subject-err').text(obj.message)
            });
        }
        if(!(typeof result.errors.news_headline === 'undefined')){
            result.errors.news_headline.forEach(function(obj,idx,array){
                $('#news-headline-err').text(obj.message)
            });
        }
        if(!(typeof result.errors.news_info_detail === 'undefined')){
            result.errors.news_info_detail.forEach(function(obj,idx,array){
                $('#news-info-detail-err').text(obj.message)
            });
        }
        if(!(typeof result.errors.news_link_url === 'undefined')){
            result.errors.news_link_url.forEach(function(obj,idx,array){
                $('#news-link-url-err').text(obj.message)
            });
        }
    }else{
        callback();
    }
} 
/**
 * 更新履歴CSVダウンロード
 * 
 */
HomeListController.prototype.downloadTableCsv= function(tableName, tableName2,csvUpdateName) {
    // ダウンロードボタン押下
    $('#csv-change-table').on('click', function(){
        
        var selectVal = $('select[name=filter]').val()
        // 更新履歴CSV（全件）
        if ('all' === selectVal){
            var param = {
                'table-name':tableName
                ,'table-name2':tableName2
            }
            // GET通信でテーブル名渡す
            AjaxUtil.get('/admin_app/home_list/change_csv_download/', param, function(data) {
                var fileName = '更新履歴_' + csvUpdateName + '.csv';
                FileUtil.outputCsv(data, fileName);
            });
        // 更新履歴CSV（全件期間指定）
        } else if ('date'=== selectVal){
            var start = $('#date-start').val();
            var end = $('#date-end').val();
            // エラーメッセージ削除
            $('.input-err').removeClass('input-err');
            $('.input-err-msg').remove();
            // 入力チェックエラーの場合、CSV出力を行わない
            if(!NoticeTableUtil.checkDateStart()){
                return
            }
            if(!NoticeTableUtil.checkDateEnd()){
                return
            }
            var param = {
                'table-name':tableName,
                'table-name2':tableName2,
                'date-start':start,
                'date-end':end
            }
            // GET通信でテーブル名渡す
            AjaxUtil.get('/admin_app/home_list/change_csv_download/', param, function(data) {
                var fileName = '更新履歴_' + csvUpdateName + '_' + start + '_' + end + '.csv';
                FileUtil.outputCsv(data, fileName);
            });
        }
    })
}

$(function() {
    var controller = new HomeListController();
    controller.init();
});
