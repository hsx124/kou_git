var IpUpdateController = function() {
};

IpUpdateController.prototype = new AbstractController();

IpUpdateController.prototype.execute = function() {

    // キービジュアル設定
    $('#upload').uploadThumbs({
        position : '#preview'
    });

    // DatePicker設定
    InputUtil.setDataPicker();

    // clear thumbnail images
    $.fn.uploadThumbs.clear = function (option) {
        $('#preview > img').remove();
        $('.input-err-msg').remove();
        // clear file names
        typeof  this.data('alternate').attr('value') == 'undefined' ?
                this.data('alternate').hide().text('') :
                this.data('alternate')       . val('');

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

IpUpdateController.prototype.selectedMenu = function() {
    return '.menu-ip-master';
}

IpUpdateController.prototype.bindEvent = function() {

    $('.back-button').on('click', function() {
        window.location.href = '/admin_app/sakuhin_list/';
    });

    // ファイル選択ボタン設定
    InputUtil.setInputFile('#btn', '#upload', '#uploadname');

    // CLEditor生成
    CLEditorUtil.createCLEditor('#overview');
    // CLEditorにdjangoから連携されたあらすじを設定
    if(!(typeof djangoObj.form.overview === 'undefined')){
        CLEditorUtil.updateEditor('#overview', djangoObj.form.overview);
    }

    return $.Deferred().resolve().promise();
}

$(function() {
    var controller = new IpUpdateController();
    controller.init();
});