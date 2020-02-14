/**
 * loadingの共通ユーティリティ
 */
var LoadingUtil = {
    /**
     * ローディング開始
     *
     * @param msg
     *            読み込み中表示メッセージ
     * @param target
     *            基準要素
     */
    start : function(msg, target) {
        if (msg == undefined) {
            msg = '';
        }
        var dispMsg = "<div class='loadingMsg'>" + msg + '</div>';
        if ($('#loading').length == 0) {
            target.append("<div id='loading'>" + dispMsg + '</div>');
        }
    },

    /**
     * ローディング停止
     */
    stop : function() {
        $('#loading').remove();
    }
};
