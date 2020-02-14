/**
 * テキストフォローのユーティリティ
 */
var TextfollowUtil = {
    execute: function () {
        $('[data-tooltip]').each(function (idx, elm) {
            var $elm = $(elm);
            var constants = text_follow_list[$elm.attr('data-id')];

            var title = constants.title || 'タイトルがありません';
            var body = constants.body || 'ボディがありません';
            var width = constants.width || 400;
            var position = constants.position || 'center';
            var left;
            if(position == 'center'){
                left = width/2
            }else if(position == 'left'){
                left = width/5
            }else if(position == 'right'){
                left = width*0.65
            }

            var html = '' +
                '<div class="tooltip-util">' +
                '    <div class="tooltip-before"></div>' +
                '    <div class="tooltip-after"></div>' +
                '    <div class="text '+ $elm.attr('data-id') +'">' +
                '        <div class="tooltip-title">' + title + '</div>' +
                '        <div class="tooltip-body">' + body + '</div>' +
                '    </div>' +
                '</div>'

            $elm.append(html);
            $elm.children('.tooltip-util').css('width', width+'px');
            $elm.children('.tooltip-util').css('left', -(left)+'px');

            var before = {
                content: "",
                position: "absolute",
                top: "-23px",
                left: left + "px",
                marginLeft: "-15px",
                border: "12px solid transparent",
                borderBottom: "12px solid #FFF",
                zIndex: "2"
            }
            var after = {
                content: "",
                position: "absolute",
                top: "-26px",
                left: left + "px",
                marginLeft: "-17px",
                border: "14px solid transparent",
                borderBottom: "12px solid rgb(255, 210, 150)",
                zIndex: "1"
            }

            $elm.children('.tooltip-util').children('.tooltip-before').css(before);
            $elm.children('.tooltip-util').children('.tooltip-after').css(after);
        });
    }
}