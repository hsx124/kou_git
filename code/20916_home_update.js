var HomeUpdateController = function() {};

HomeUpdateController.prototype = new AbstractController();


HomeUpdateController.prototype.execute = function() {
    var self = this;
    // キービジュアル設定
    $('#upload').uploadThumbs({
        position: '#preview'
    });

    // DatePicker設定
    InputUtil.setDataPicker();
    $('#datepicker-from').datepicker('setDate', new Date('2019/10/25'));
    $('#datepicker-to').datepicker('setDate', new Date('2035/08/25'));
    self.isChecked();

    //オーバーレイ制御（初期表示時）
    if ( djangoObj.dto.banner.external_site_flg) {
        $('#url-checkbox').prop('checked',true);
        $('#hakusho-checkbox').prop('checked',false);
        $('#url-overlay').css('display', 'none');
        $('#hakusho-overlay').css('display', 'block');
    } else {
        $('#hakusho-checkbox').prop('checked',true);
        $('#url-checkbox').prop('checked',false);
        $('#url-overlay').css('display', 'block');
        $('#hakusho-overlay').css('display', 'none');
    }

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
                InputCheckUtil.showErrMsg("#key-visual-area","サムネイルのファイルサイズは1MB未満としてください。");
                inputElem.value = '';
                break;
            }
        }
    };

    return $.Deferred()
        .resolve()
        .promise();
};

/**
 * メニュー選択処理
 */
HomeUpdateController.prototype.selectedMenu = function() {
    return '.home-list';
};

/**
 * イベント登録処理
 */
HomeUpdateController.prototype.bindEvent = function() {
    var self = this;
    // 元々あるキービジュアルを削除
    $('#upload').on('change', function() {
        $('#preview > img').remove();
    });

    // 更新ボタン
    self.homeUpdateButton();

    // ファイル選択ボタン設定
    InputUtil.setInputFile('#btn', '#upload', '#uploadname');

    // 外部URLCB
    $('#url-checkbox').on('click', function() {
        if ($('#url-checkbox').prop('checked')) {
            $('#hakusho-checkbox').prop('checked', false);
        } else {
            $('#url-checkbox').prop('checked', true);
        }
        self.isChecked();
    });
    
    // 白書CB
    $('#hakusho-checkbox').on('click', function() {
        if ($('#hakusho-checkbox').prop('checked')) {
            $('#url-checkbox').prop('checked', false);
        } else {
            $('#hakusho-checkbox').prop('checked', true);
        }
        self.isChecked();
    });

    // 白書選択モーダル
    $('.select-hakusho-button').click(function() {
        self.selectHakusho(djangoObj.dto.media_report);
    });

    return $.Deferred()
        .resolve()
        .promise();
};

// 更新ボタン
HomeUpdateController.prototype.homeUpdateButton = function() {
    var self = this;

    $('.save-button').click(function(event) {
        $('#banner-submit').submit();
    });
}

/**
 * 白書選択モーダル
 */
HomeUpdateController.prototype.selectHakusho = function(hakusho_list) {
    var self = this;

    modal = $('#hakusho-dialog');
    // グリッド生成
    var colModel = self.createColModel();
    var option = {
        colNames: colModel.name,
        colModel: colModel.model,
        data: hakusho_list,
        pager: '#pager',
        loadComplete: self.gridBtnEvent
    };
    GridUtil.renderNormalGrid('#list-grid', option, true);
    // モーダル生成
    modal.dialog({
        title: '白書を選択',
        resizable: false,
        modal: true,
        width: 'auto',
        height: 'auto'
    });
};

/**
 * オーバーレイ制御
 */
HomeUpdateController.prototype.isChecked = function() {
    if ($('#url-checkbox').is(':checked')) {
        $('#url-overlay').css('display', 'none');
        $('#hakusho-overlay').css('display', 'block');
    } else {
        $('#url-overlay').css('display', 'block');
        $('#hakusho-overlay').css('display', 'none');
    }
};

/**
 * jQGrid用のカラム定義
 */
HomeUpdateController.prototype.createColModel = function() {
    var width = 1500;

    var modelArray = [];
    modelArray.push(
        GridUtil.createColModel({
            name: 'media_report_name',
            width: width * 0.22
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'media_report_category',
            width: width * 0.1
        })
    );

    modelArray.push(
        GridUtil.createColModel({
            name: 'year',
            width: width * 0.05
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'update_user',
            width: width * 0.1
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'update_date',
            width: width * 0.07,
            formatter : 'date',
            formatoptions : {
                srcformat : 'ISO8601Long',
                newformat : 'Y/m/d',
                defaultValue:null 
            }
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            title: false,
            name: 'operation',
            width: width * 0.07,
            align: 'center',
            formatter: function(val, opt, rdt) {
                return "<button type='button' class='grid-btn-update' data-document-name='" + rdt.media_report_name + "' id-num='" + rdt.media_report_code + "'>" + '選択する' + '</button>';
            },
            sortable: false
        })
    );
    return {
        model: modelArray,
        name: ['ドキュメント名', 'カテゴリ', '年度', '最終更新者', '最終更新日時', '選択']
    };
};

HomeUpdateController.prototype.createGridData = function() {
    var colNames = ['documentName', 'category', 'year', 'updateUser', 'updateDate', 'operation'];
    
    return GridUtil.createGridData(colNames, gridData);
};
HomeUpdateController.prototype.gridBtnEvent = function() {
    $('.grid-btn-update').button();
    $('.grid-btn-update').on('click', function() {
        modal.dialog('close');
        var button = $(this);
        $('.hakusho-doc').text(button.attr('data-document-name'));
        $('#banner-hakusho_num').val(button.attr('id-num'));
        $('#banner-hakusho').val(button.attr('data-document-name'));
    });
};

$(function() {
    var controller = new HomeUpdateController();
    controller.init();
});
