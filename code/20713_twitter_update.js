var TwitterUpdateController = function() {
};

TwitterUpdateController.prototype = new AbstractController();


TwitterUpdateController.prototype.selectedMenu = function() {
    return '.twitter-list';
}

TwitterUpdateController.prototype.bindEvent = function() {
    var self = this;
    // メインアカウント指定のツールチップを追加
    TextfollowUtil.execute();

    // Twitter基本情報一覧画面に戻る
    $('.back-button').on('click', function() {
        window.location.href = '/admin_app/twitter_list/';
    });
    // Twitterアカウント検索
    $('#user-name-search').on('focusout', function(){
        // 検索欄入力値を取得
        var searchWord = $(this).val();
        // 検索ワードを反映
        $('#twitter-search').attr('href', 'https://twitter.com/search?q='+ searchWord  +'&f=user');
    })
    // Twitter遷移先確認
    $('#twitter-link').on('click', function(){
        // ユーザー名入力値を取得
        var usrName = $('#user-name').val();
        // Twitter遷移先ボタンリンク編集
        $('#twitter-link').attr('href', 'https://twitter.com/'+ usrName);
    })

    $( 'input[name="main_account_flg"]:radio:first' ).on('change',function(){
        self.selectMainFlgData();
    });

    // ajaxで、削除処理を行う
    $('.unlock-button').on('click', function() {
        self.doTwitterCodeUnlock();
    });

    // $('#twitter-form').submit(function(){
    //     self.selectMainFlgData();
    // })

    return $.Deferred().resolve().promise();
}

TwitterUpdateController.prototype.doTwitterCodeUnlock = function() {
    var param = {
        'unlock-twitter-code' : $('#unlock-twitter-code').text(),
        'unlock-account-name' : $('#unlock-account-name').text(),
        'sakuhin_map_id':$('#sakuhin-map-id').val()
    };

    modal.dialog('close');
    return AjaxUtil.post('/admin_app/twitter_update/', param).then(function(xhr, status) {
        var promise = $.Deferred();
        if(status == 'success'){
            var result = JSON.parse(xhr.responseText);
            if(result.is_error){
                // メッセージ表示
                MsgUtil.showStatusMsg('.contents', $('#unlock-account-name').text() , '既に解除');
            }else{
                 // メッセージ表示
                 MsgUtil.showStatusMsg('.contents', $('#unlock-account-name').text() , '解除');
            }
            return promise.resolve();
        }else{
            return promise.reject();
        }
    });
}

TwitterUpdateController.prototype.selectMainFlgData = function() {
    var self = this;
    var param = {
          'change' : $('input[name="twitter_code"]').val()
      };
    return AjaxUtil.get('/admin_app/twitter_update/', param).then(function(xhr, status) {
        var promise = $.Deferred();
        if(status == 'success'){
            var result = JSON.parse(xhr.responseText);
            if(result){
                $('#unlock-twitter-code').text(result.twitter_code);
                $('#unlock-account-name').text(result.account_name);
                $('#sakuhin-map-id').val(result.sakuhin_map_id);
                modal = $('#delete-confirm-dialog');
                modal.dialog({
                    modal: true,
                    width: '500px'
                });
    
                // 削除キャンセル処理
                $('.cancel-botton').on('click', function() {
                    modal.dialog('close');
                    $('input[name="main_account_flg"]:radio:first').prop("checked", false);
                    $('input[name="main_account_flg"]:radio:last').prop("checked", true);
                    $('input[name="main_account_flg"]:radio').button("enable").button('refresh');
                    $('input[name="main_account_flg"]:radio').focus();
                    
                });
            }
            return promise.resolve();
        }else{
            return promise.reject();
        }
    });
}

$(function() {
    var controller = new TwitterUpdateController();
    controller.init();
});