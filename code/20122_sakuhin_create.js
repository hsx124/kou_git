var SakuhinCreateController = function() {
};

SakuhinCreateController.prototype = new AbstractController();

SakuhinCreateController.prototype.execute = function() {

    // キービジュアル設定
    $('#upload').uploadThumbs({
        position : '#preview',
    });

    var option= {
        // 年プルダウン選択
        changeYear: true,

        // 月プルダウン選択
        changeMonth: true,

        // 年月日フォーマット ex) 2019/02/18
        dateFormat: 'yy/mm/dd'
    }
    
    //DatePicker設定
    $('#datepicker-ymd').datepicker({
        changeMonth: true,
        changeYear: true,
        showButtonPanel: true,
        closeText: '決定',

        beforeShow: function(dateText, inst){
                        $("#ui-datepicker-div").addClass('month');
                },
        onClose: function(dateText, inst) {
            $("#ui-datepicker-div").addClass('month');
              var month = $("#ui-datepicker-div .ui-datepicker-month option:selected").val();
              var year = $("#ui-datepicker-div .ui-datepicker-year option:selected").val();
              if ((parseInt(month)+1)  < 10) {
                  var months = '0'+ (parseInt(month)+1);
              } else {
                  months = (parseInt(month))+1;
              }
              $('#datepicker-ymd').val(year + '/' + months);
              $("#ui-datepicker-div").removeClass('month');
              this.focus();
              $(this).val($.datepicker.formatDate('yy/mm', new Date(year, month, 1))); 
          }
      });

    $('#datepicker-from,#datepicker-to').datepicker(option);

    if(typeof djangoObj.form.valid_start_yyyymmdd === 'undefined'){
        $('#datepicker-from').datepicker('setDate', new Date());
    }
    if(typeof djangoObj.form.valid_end_yyyymmdd === 'undefined'){
        $('#datepicker-to').datepicker('setDate', new Date('2099/12/31'));
    }

    // clear thumbnail images
    $.fn.uploadThumbs.clear = function (option) {
        $('.input-err-msg').remove();
        // clear file names
        typeof  this.data('alternate').attr('value') == 'undefined' ?
                this.data('alternate').hide().text('') :
                this.data('alternate'). val('');

        // find images
        var $images = (typeof option.position == 'number')?  this.siblings('img.thumb'):  $( option.position ).find('img.thumb');

        // remove images
        if ($images.length) {
            $images.not('img.uploaded').next('br').remove().end().remove();
        }
        
        //ファイルサイズを1MBで設定する
        var bigfSize = 1024 * 1024;
        var inputElem = this[0];
        for(var i=0; f = inputElem.files[i];i++){
            if(f.size >= bigfSize){  
                InputCheckUtil.showErrMsg("#key-visual-area","キービジュアルのファイルサイズは1MB未満としてください。");
                inputElem.value = '';
                break;
            }
        }
    };

    return $.Deferred().resolve().promise();
}

SakuhinCreateController.prototype.selectedMenu = function() {
    return '.sakuhin-list';
}

SakuhinCreateController.prototype.bindEvent = function() {
    var self = this;
    $('.back-button').on('click', function() {
        window.location.href = '/admin_app/sakuhin_list/';
    });

    // ファイル選択ボタン設定
    InputUtil.setInputFile('#btn', '#upload', '#uploadname');

    // CLEditor生成
    CLEditorUtil.createCLEditor('#overview');

    $('.key_word_plus_btn').on('click',function(){
        self.addKeyWordInput();
    });

    // CLEditorにdjangoから連携されたあらすじを設定
    if(!(typeof djangoObj.form.overview === 'undefined')){
        CLEditorUtil.updateEditor('#overview', djangoObj.form.overview);
    }

    return $.Deferred().resolve().promise();
}

/**
 *  作品キーワードを追加
 */
SakuhinCreateController.prototype.addKeyWordInput = function() {
    // var div = $('<div>');
    // var keyword_input = $('<input>').attr({
    //     'type': 'text',
    //     'class': 'keyword small ui-textfield ui-widget ui-widget-content ui-corner-all',
    // });
    // div.append(keyword_input)
    // $('.col5').append(div);
    var keyword_area = $('.keyword-area:first');
    // keyword_area.clone(true).appendTo('.plus-div')
    $('.plus-div').before(keyword_area.clone(true)).find("input").val("")
}

$(function() {
    var controller = new SakuhinCreateController();
    controller.init();
});