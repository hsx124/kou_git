/**
 * キービジュアル制御クラス
 */
var KeyVisualUtil = {
    execute : function() {

        // キービジュアルのDOM要素
        var keyvisual = $(event.target);

        // オーバレイ用の羅別
        var keyvisualLabel = $('<div class="keyvisualLabel">SAMPLE</div>');
        $('.contents').css('display', 'block');
        keyvisualLabel.css({
            'margin' : 'auto',
            'width' : '1000px',
            'height' : '70px',
            'position' : 'absolute',
            'top' : '0px',
            'left' : -(1000 / 2 - keyvisual.width() / 2),
            'right' : '0',
            'bottom' : '0',
            'color' : 'black',
            'text-align' : 'center',
            'transform' : 'rotate(57deg)',
            'background' : 'white',
            'line-height' : '70px'
        });

        // オーバレイ
        var keyvisualOverlay = $('<div oncontextmenu="return false;" class="keyvisualOverlay"></div>');
        keyvisualOverlay.css({
            'position' : 'absolute',
            'width' : keyvisual.width(),
            'height' : keyvisual.height(),
            'overflow' : 'hidden',
            'opacity' : '0.7',
            'color' : 'orange',
            'font-size' : '50px'
        });
        // imgタグのonclickイベントをオーバーレイに付ける
        keyvisualOverlay.on('click',keyvisual.get(0).onclick);
        // オーバレイ適用
        keyvisual.before(keyvisualOverlay.append(keyvisualLabel));

        // 注意文言表示
        if (keyvisual.data('attention')) {

            // 注意文言領域をキービジュアルの幅に合わせる
            var attention = $('<div style="background:#f4e0e4;border:1px #e60012 solid;display:block;text-align: center;margin-top:4px;"><i class="icon-warning-sign"></i>画像の転用はお控えください。</div>');
            attention.css('width', keyvisual.width() + 'px');
            keyvisual.after(attention);
        }
    },
    notFound : function() {
        var obj = event.target;
        obj.src = "/static/ipdds_app/image/keyvisual/NO_IMAGE.png";
        obj.onload = "";
        obj.onerror = "";
    }
}