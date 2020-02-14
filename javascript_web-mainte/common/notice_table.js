//////////////////////////////////////////////////////////
// 更新履歴情報ユーティリティクラス
//////////////////////////////////////////////////////////
var NoticeTableUtil = {

    /**
     * ローディング開始
     * @param msg
     *        読み込み中表示メッセージ
     * @param target
     *        基準要素
     */
    setDLArea: function() {
        // DatePicker設定
        InputUtil.setDataPicker();

        // 更新履歴日付初期値設定
        var date = new Date();
        $('#date-end').datepicker('setDate', date.setMonth(date.getMonth() - 1));
        $('#date-start').datepicker('setDate', date);
        $('.datepicker').datepicker('option', 'disabled', true);
        $('#date-end, #date-start').addClass('input-disabled');

        $('select[name=filter]').selectmenu({
            width: 200
        });

        $('select[name=filter]').on('selectmenuchange', function() {
            // エラーメッセージ削除
            $('.input-err').removeClass('input-err');
            $('.input-err-msg').remove();

            if ($(this).val() === 'all') {
                $('#date-end, #date-start').addClass('input-disabled');
                $('.datepicker').datepicker('option', 'disabled', true);
            } else if ($(this).val() === 'date') {
                $('#date-end, #date-start').removeClass('input-disabled');

                $('.datepicker').datepicker('option', 'disabled', false);
            }
        });
    },

    /**
     * 更新履歴CSVダウンロード
     * 
     */
    downloadTableCsv: function(tableName, csvTitle) {

        // ダウンロードボタン押下
        $('#csv-change-table').on('click', function(){

            var selectVal = $('select[name=filter]').val()

            // 更新履歴CSV（全件）
            if ('all' === selectVal){

                var param = {
                    'table-name':tableName
                }
                // GET通信でテーブル名渡す
                AjaxUtil.get('/admin_app/change_csv_download/', param, function(data) {
                    var fileName = '更新履歴_' + csvTitle + '.csv';
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
                    'date-start':start,
                    'date-end':end
                }
                // GET通信でテーブル名渡す
                AjaxUtil.get('/admin_app/change_csv_download/', param, function(data) {
                    var fileName = '更新履歴_'+ csvTitle +'_'+start+'_'+end+'.csv';
                    FileUtil.outputCsv(data, fileName);
                });
            }
        })
    },

    /**
     * ダウンロード期間（開始）入力チェック
     * 
     */
    checkDateStart:function(){

    // チェック結果
    var result = {};

    // チェック対象
    var checkTarget = '#date-start';

    // 未入力チェック
    result = InputCheckUtil.checkBlank(checkTarget, 'ダウンロード期間（開始）');

    if (!result.ret) {
        InputCheckUtil.showErrMsg(checkTarget, result.msg);
        return false;
    }

    // 日付形式チェック
    // 日付妥当性チェック
    result = InputCheckUtil.checkDate(checkTarget, 'ダウンロード期間（開始）');

    if (!result.ret) {
        InputCheckUtil.showErrMsg(checkTarget, result.msg);
        return false;
    }

    return true
    },

    /**
     * ダウンロード期間（終了）入力チェック
     * 
     */
    checkDateEnd:function(){

    // チェック結果
    var result = {};

    // チェック対象
    var checkTarget = '#date-end';

    // 未入力チェック
    result = InputCheckUtil.checkBlank(checkTarget, 'ダウンロード期間（終了）');

    if (!result.ret) {
        InputCheckUtil.showErrMsg(checkTarget, result.msg);
        return false;
    }

    // 日付形式チェック
    // 日付妥当性チェック
    result = InputCheckUtil.checkDate(checkTarget, 'ダウンロード期間（終了）');

    if (!result.ret) {
        InputCheckUtil.showErrMsg(checkTarget, result.msg);
        return false;
    }

    // 日付比較
    result = InputCheckUtil.checkDatePeriod('#date-start', checkTarget, 'ダウンロード期間（終了）', 'ダウンロード期間（開始）');
    if (!result.ret) {
        InputCheckUtil.showErrMsg(checkTarget, result.msg);
        return false;
    }

    return true
    },
}