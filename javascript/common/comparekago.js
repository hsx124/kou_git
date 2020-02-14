/**
 *比較かごの処理
 */
var CompareKago = {
    /**
     * Sessionから比較かご領域のデータを取得
     */
    getSessionData : function(){
        //sessionからデータを取得する
        var param = {
                'kago_get' : 'getdata'
        };
        var result = null;
        var promise = $.Deferred();
        var sessionProimse = AjaxUtil.get('/ipdds/compare_kago/', param);
        sessionProimse.done(function(xhr,status){
            if(status == 'success'){
                result = JSON.parse(xhr.responseText);
            }
            promise.resolve(result);
        });
        return promise.promise();
    },

    /**
     * 比較かご領域の描画
     */
    drawCompareIp : function(data, slideDownFlag){
        var self = this;
        var html = "";

        //データある場合、比較カゴを描画する
        if (data && data.length > 0) {

            //比較カゴを描画する
            data.forEach(function (obj) {
                var keyvisual_file_name = obj.keyvisual;
                var ipname = obj.ip_name;
                var ipcode = obj.ip_code;
                //比較カゴ領域に当IP存在する場合、「比較カゴから戻す」ボタンで表示する
                var checkbox = $("input[value='"+ ipcode +"']");
                if(checkbox.length){
                    //「比較カゴから戻す」ボタンを設定する
                    self.drawCompareButton(checkbox,true);
                }

                //比較カゴ領域を描画する
                html = '<div class="compare-kago-area">'
                    + '<div class="compare-kago-left">'
                    + '<img onclick="window.location.href = \'/ipdds/detail?ip_code=' + ipcode + '\'" oncontextmenu="return false;" onerror="KeyVisualUtil.notFound()"'
                    + 'src="/static/ipdds_app/image/keyvisual/' + ipcode + '/' + keyvisual_file_name + '" class="compare-keyvisual" data-attention="true">'+ '</div>'
                    + '<div class="compare-kago-middle">'
                    + '<a href="/ipdds/detail/?ip_code=' + ipcode + '" class="link">' + ipname + '</a>'+ '</div>'
                    + '<div class="compare-kago-button">'
                    + '<span class="compare-kago-button-text" ip_name="'+ipname+'" ip_code="'+ipcode+'" keyvisual="'+keyvisual_file_name+'" id="compare-' + ipcode + '">かごから戻す</span>' + '</div>'
                    + '</div>';

                if(slideDownFlag){
                    var elem = $(html);
                    $('.compare-kago-list-contents').append(elem);
                    elem.hide();
                    elem.slideDown(700);
                } else {
                    $('.compare-kago-list-contents').append(html);
                }

                //「カゴから外す」ボタン押下時のイベントを追加する
                self.DelCompareKagoData('compare-'+ipcode);
            });

            //比較カゴのボタンを表示する
            $('.not_found_item').css('display','none');
            $('.compare-kago-list-button').css('display','block');
            
        }else{
            //比較かごにデータなしの場合
            $('.not_found_item').css('display','block');
            $('.compare-kago-list-button').css('display','none');
        }
        
    },

    /**
     * 「カゴから外す」ボタンのイベントを設定
     */
    DelCompareKagoData : function(btnId){
        var self = this;
        // 「カゴから外す」ボタン押下時のイベント
        $('#' + btnId).click(function () {
            var btn = this;
            // セッションから最新データを取得して、かご描画処理を行う
            CompareKago.getSessionData().done(function(data){
                self.DelCompareKagoDataClick(btn,  data || []);
            })
        });
    },

    /*
    * 「カゴから外す」ボタンの処理を行う
    */
    DelCompareKagoDataClick : function(btn, sessionData){
        var self = this;

        //session用項目
        var ip_code = $(btn).attr("ip_code");
        var ip_name = $(btn).attr("ip_name");
        var keyvisual_file_name = $(btn).attr("keyvisual");

        // 当IPがセッションに存在するチェック
        var isExists = false;
        for(var i = 0; i < sessionData.length; i++){
            var ipInfo = sessionData[i];
            if(ipInfo.ip_code == ip_code){
                isExists = true;
                break;
            }
        }

        // セッションに存在しないIPのボタンの状態を戻す
        $('.compare-kago-area').each(function(index, elem){
            var tmpIpCode = $(elem).find(".compare-kago-button-text").attr('ip_code');
            var delFlg = true;
            for(var i = 0; i < sessionData.length; i++){
                var ipInfo = sessionData[i];
                if(ipInfo.ip_code == tmpIpCode){
                    delFlg = false;
                    break;
                }
            }
            if(delFlg){
                var checkboxInfo = $('input[value="'+ tmpIpCode +'"]:checkbox');
                if(checkboxInfo.length > 0){
                    //セッションに存在するIPのボタンを「比較カゴから戻す」ボタンに設定する
                    self.drawCompareButton(checkboxInfo,false);
                }
            }
        });

        
        // 最新状態を描画する
        $('.compare-kago-list-contents').empty();
        self.drawCompareIp(sessionData); 

        //当IPがセッションに存在する場合、当IPを削除する
        if(isExists){
            var checkbox = $("input[value=" + ip_code + "]");
            if(checkbox.length > 0){
                //「比較カゴに入れる」ボタンを設定する
                self.drawCompareButton(checkbox,false);
                checkbox.attr('disabled', 'true');
            }

            //sessionから当IPを削除する
            var param = {
                        'kago_delete' : 'delete',
                        'ip_code' : ip_code,
                        'ip_name' : ip_name,
                        'keyvisual' : keyvisual_file_name
            };
            
            AjaxUtil.post('/ipdds/compare_kago/', param);

            //当IPをカゴから削除する
            var html = $('#compare-' + ip_code).parents('.compare-kago-area')
            html.slideUp(700, function () {
                html.remove();
                if ($('.compare-kago-area').length == 0) {
                    //比較かごにデータなしの場合
                    $('.compare-kago-list-button').css('display','none');
                    $('.not_found_item').fadeIn(700);
                }
            });

            setTimeout(function(){
                checkbox.removeAttr('disabled');
            },700);
        }

    },

    /**
     * 「比較カゴに入れる」ボタンのイベントを設定
     */
    SetCompareDataAddOrDel : function(){
        var self = this;
        //比較カゴ追加/削除ボタン
        $('.compare-kago-checkbox').on('click', function () {
            var checkbox = $(this);
            // セッションから最新データを取得して、かご描画処理を行う。
            CompareKago.getSessionData().done(function(data){
                self.CompareKagoCheckboxClick(checkbox, data || []);
            })
        });

    },

    /**
     * 「比較カゴに入れる」ボタンのイベントを設定
     */
    CompareKagoCheckboxClick : function(checkbox, sessionData){
        var self = this;
        // チェックボックスを活性化にする
        checkbox.attr('disabled', 'true');
        //session用項目
        var ip_code = checkbox.attr("value");
        var ip_name = checkbox.attr("ip_name");
        var keyvisual_file_name = checkbox.attr("keyvisual");
        var checked = checkbox.prop('checked');

        //４つある場合エラーメッセージ出す
        var fadeInOut = function ($msg) {
            setTimeout(function () {
                $msg.fadeIn(500);
            }, 10);
            setTimeout(function () {
                $msg.fadeOut(500);
            }, 3000)
        }

        // セッションに存在しないIPのボタンの状態を戻す
        $('.compare-kago-area').each(function(index, elem){
            var ipCode = $(elem).find(".compare-kago-button-text").attr('ip_code');
            var delFlg = true;
            for(var i = 0; i < sessionData.length; i++){
                var ipInfo = sessionData[i];
                if(ipInfo.ip_code == ipCode){
                    delFlg = false;
                    break;
                }
            }
            if(delFlg){
                var checkboxInfo = $('input[value="'+ ipCode +'"]:checkbox');
                if(checkboxInfo.length > 0){
                    //「比較カゴから戻す」ボタンを設定する
                    self.drawCompareButton(checkboxInfo,false);
                }
            }
        });

        
        // 最新状態を描画する
        $('.compare-kago-list-contents').empty();
        self.drawCompareIp(sessionData); 

        // 当IPがセッションに存在するチェック
        var isExists = false;
        for(var i = 0; i < sessionData.length; i++){
            var ipInfo = sessionData[i];
            if(ipInfo.ip_code == checkbox.val()){
                isExists = true;
                break;
            }
        }

        //「比較カゴに入れる」ボタンチェックOFFの場合、当IPが比較カゴ領域から外す
        if (checked) {
            // 再描画時に、チェックボックスのチェック状態をtrueにするので、
            // 当IPがセッションに存在しない場合、チェック状態をfalseにする
            if(!isExists){
                checkbox.prop('checked', false);
            }
            // セッションのデータ数が4件かつ、当IPがセッションに存在しない場合、
            // エラーメッセージを表示する
            if(sessionData.length == 4 && !isExists){
                $msg = $("#id_msg_not_select");
                $msg.text("最大４つまで同時に比較できます。")
                fadeInOut($msg);
                checkbox.removeAttr('disabled');
                if($('.compare-kago-area').length < 4){
                    $('.compare-kago-list-contents').empty();
                    self.drawCompareIp(sessionData); 
                }
                return false;
            } 
            // 当IPがセッションに存在しない場合、かごに追加する
            if(!isExists){
                var param = {
                    'kago_add' : 'add',
                    'ip_code' : ip_code,
                    'ip_name' : ip_name,
                    'keyvisual' : keyvisual_file_name
                };
                AjaxUtil.post('/ipdds/compare_kago/', param).done(function(xhr){
                    var result = JSON.parse(xhr.responseText);
                    if(result){
                        //当IPを描画する
                        self.drawCompareIp([param], true); 
                        //「比較カゴから戻す」ボタンを設定する
                        self.drawCompareButton(checkbox,true);
                    }
                });
            }
        } else {// かごから削除する処理
            // 当IPがセッションに存在する場合、かごとセッションから削除する
            // 逆に何もしない
            if(isExists){
                //sessionに当IPを削除する
                var btnId = "compare-" + checkbox.val();
                $("#" + btnId).click();
                //「比較カゴに入れる」ボタンを設定する
                self.drawCompareButton(checkbox, false);
            }
        }
        // チェックボックスを活性化にする
        setTimeout(function(){
            checkbox.removeAttr('disabled');
        },700);

        return;
    },

    /**
     * 「比較カゴに入れる」ボタンの状態を設定
     */
    drawCompareButton : function(checkbox,flg){
        var parent = checkbox.parent();
        var button = checkbox.next();
        checkbox[0].checked = flg;
        if(flg){
            //「比較カゴから戻す」ボタンを設定する
            parent.removeClass('compare-kago-add');
            parent.addClass('compare-kago-del');
            button.text('かごから戻す');
        }else{
            //「比較カゴに入れる」ボタンを設定する
            parent.removeClass('compare-kago-del');
            parent.addClass('compare-kago-add');
            button.text('かごに入れる');
        }

    }

}