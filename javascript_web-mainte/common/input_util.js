/**
 * 入力パーツの共通ユーティリティ
 */
var InputUtil = {
    // datepickerデフォルトオプション
    defaultOption: {
        // 年プルダウン選択
        changeYear: true,

        // 月プルダウン選択
        changeMonth: true,

        // 年月日フォーマット ex) 2019/02/18
        dateFormat: 'yy/mm/dd'
    },
    // datepicker設定
    setDataPicker: function(paramOption) {
        var option = {};
        $.extend(option, this.defaultOption, paramOption);
        $('.datepicker').datepicker(option);
    },

    /**
     * input, textarea selectにjQueryUIスタイルを自動適用
     *
     */
    setInputField: function() {
        $('input[type=text],textarea').addClass('ui-textfield ui-widget ui-widget-content ui-corner-all');

        // 削除モーダル内「削除」、「キャンセル」ボタン
        $('.dialog-button').button();

        $('input[type=radio]').checkboxradio();

        $('select').selectmenu();
    },

    /**
     * ファイル選択ボタン設定
     *
     * @param btnId
     *           クリックイベント発火用のボタンID
     *
     * @param uploadId
     *           ファイル選択ボタンID
     *
     * @param fileNameId
     *           ファイル名を表示するテキストボックスID
     */
    setInputFile: function(btnId, uploadId, fileNameId) {
        // アップロードボタン
        $(uploadId).change(function() {
            var val = $(this).val();
            var path = val.replace(/\\/g, '/');
            var match = path.lastIndexOf('/');
            $(fileNameId).css('display', 'inline-block');
            $(fileNameId).val(match !== -1 ? val.substring(match + 1) : val);
        });
        $(fileNameId).bind('keyup, keydown, keypress', function() {
            return false;
        });
        $(btnId).click(function() {
            $(uploadId).trigger('click');
        });
    }
};

/**
 * 入力チェック（JS）の共通ユーティリティ
 */
var InputCheckUtil = {
    /**
     * 入力名チェック<br>
     * @param targetId
     *           入力チェック対象のID
     * @param checkVal
     *           入力チェック対象の名前
     * @param checkLegth
     *           入力チェック対象の長さ
     */
    checkInputValue : function(checkTarget, checkVal, checkLegth) {
        var self = this;

        // チェック結果
        var result = {};

        // 未入力チェック
        result = InputCheckUtil.checkBlank(checkTarget, checkVal);

        if (!result.ret) {
            InputCheckUtil.showErrMsg(checkTarget, result.msg);
            return false;
        }

        // 入力文字長さチェック
        result = InputCheckUtil.checkMaxLength(checkTarget, checkVal, checkLegth);

        if (!result.ret) {
            InputCheckUtil.showErrMsg(checkTarget, result.msg);
            return false;
        }

        // チェックOK
        return true
    },
    /**
     * 未入力チェック<br>
     *
     * @param targetId
     *           入力チェック対象のID
     *
     * @param label
     *           エラーメッセージ用可変文言
    */
    checkBlank: function(targetId, label) {

        // チェック結果
        var result = {
            'ret' : true,
            'msg' : ''
        };
    
        var checkTarget = $(targetId);
        var targetValue = checkTarget.val();
    
        if (!targetValue) {
            result.ret = false;
            result.msg = (label+'を入力してください。');
    
            return result;
        }
    
        return result;
    
    },

    /**
     * 日付入力形式チェック<br>
     *
     * @param targetId
     *           入力チェック対象のID
     *
     * @param label
     *           エラーメッセージ用可変文言
     *
     */
   checkDate: function(targetId, label) {

    // チェック結果
    var result = {
        'ret' : true,
        'msg' : ''
    };

    var checkTarget = $(targetId);
    var targetValue = checkTarget.val();

    if (!targetValue.match(/^\d{4}\/\d{2}\/\d{2}$/)){
        result.ret = false;
        result.msg = (label+ 'はYYYY/MM/DD形式で入力してください。')
        return result;
    }

    var date = new Date(targetValue);  
    if(date.getFullYear() !=  targetValue.split("/")[0] 
        || date.getMonth() != targetValue.split("/")[1] - 1 
        || date.getDate() != targetValue.split("/")[2]
    ){
        result.ret = false;
        result.msg = ('不正な日付が入力されています。')
        return result;
    }
    return result;
    },

    /**
     * 日付比較チェック<br>
     *
     * @param fromId
     *           入力チェック対象のID
     *
     * @param toId
     *           入力チェック対象のID
     *
     * @param label
     *           エラーメッセージ用可変文言
     *
     * @param label2
     *           エラーメッセージ用可変文言2
     *
     */
   checkDatePeriod: function(fromId, toId, label, label2) {

    // チェック結果
    var result = {
        'ret' : true,
        'msg' : ''
    };

    var targetValue = $(fromId).val();
    var checkValue = $(toId).val();

    // 日付
    if ((targetValue > checkValue)){
        result.ret = false;
        result.msg = (label+'には'+label2+'以降の日付を入力してください。')
        return result;
    }

    return result;
    },
    /**
     * 桁数チェック(完全一致)<br>
     *
     * @param targetId
     *           入力チェック対象のID
     *
     * @param label
     *           エラーメッセージ用可変文言
     *
     * @param length
     *           桁数
     */
    checkLength: function(targetId, label, length) {

        // チェック結果
        var result = {
            'ret' : true,
            'msg' : ''
        };
    
        var checkTarget = $(targetId);
        var targetValue = checkTarget.val();
    
        if (length !== targetValue.length) {
            result.ret = false;
            result.msg = (label+'は'+length+'桁で入力してください。');
            return result;
        }
    
        return result;
    
    },

    /**
     * 桁数チェック(最大値)<br>
     *
     * @param targetId
     *           入力チェック対象のID
     *
     * @param label
     *           エラーメッセージ用可変文言
     *
     * @param maxLength
     *           最大桁
     */
    checkMaxLength: function(targetId, label, maxLength) {

        // チェック結果
        var result = {
            'ret' : true,
            'msg' : ''
        };
    
        var checkTarget = $(targetId);
        var targetValue = checkTarget.val()
    
        if (maxLength < targetValue.length) {
            result.ret = false;
            result.msg = (label +'は' + maxLength + '文字以内で入力してください。');
    
            return result;
        }
    
        return result;
    
    },

    /**
     * 半角数字チェック<br>
     *
     * @param targetId
     *           入力チェック対象のID
     *
     * @param label
     *           エラーメッセージ用可変文言
    */
    checkNum: function(targetId, label) {

        // チェック結果
        var result = {
            'ret' : true,
            'msg' : ''
        };

        var checkTarget = $(targetId);
        var targetValue = checkTarget.val();

        if (isNaN(targetValue)) {
            result.ret = false;
            result.msg = (label+'は半角数字で入力してください。')
            return result;
        }

        return result;
    },

    /**
     * 入力エラーメッセージ表示<br>
     */
    showErrMsg: function(targetId, msg) {

    var errMsg = $('<div class="input-err-msg"></div>');
    errMsg.text(msg);
    $(targetId).addClass('input-err');
    $(targetId).parent().prepend(errMsg);

    }
}
