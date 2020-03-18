var SakuhinTagBindController = function() {};
SakuhinTagBindController.prototype = new AbstractController();

/**
 * タグ情報一覧画面の主処理
 */
SakuhinTagBindController.prototype.execute = function() {
    var self = this;

    return $.Deferred().resolve().promise();
};

/**
 * メニュー選択処理
 */
SakuhinTagBindController.prototype.selectedMenu = function() {
    return '.tag-bind';
};
/**
 * イベント登録処理
 */
SakuhinTagBindController.prototype.bindEvent = function() {
    var self = this;
    

    // 更新履歴DLエリアのイベント設定
    NoticeTableUtil.setDLArea();

    // 更新履歴CSVダウンロード
    NoticeTableUtil.downloadTableCsv('m_sakuhin_tag_map', 'タグ紐付け情報');

    // タイトル検索モーダルイベント
    $('.title-search-button').on('click', function() {
        self.searchTitle();
    });
    // TODO:タグソート、ドラッグイベント
    // self.setTagEvent();

    $('.moveUp,.moveDown').on('click',function(){
        var id = this.id;
        if(id == 'tag1_5_moveUp' || id == 'tag1_5_moveDown'){
            id = 'tag-1-5';
        }else if(id == 'tag6_10_moveUp' || id == 'tag6_10_moveDown'){
            id = 'tag-6-10';
        }else{
            id = 'tag-11-20'
        }
        
        if($(this).hasClass('moveUp')){
            self.tagMoveUp(id);
        }else{
            self.tagMoveDown(id);
        }
    })

    // タグ設定ボタンイベント
    $('.setting-btn').on('click',function(){
        self.tagSettingBtn(this.id);
    })
    
    // タグ削除ボタンイベント
    $('.delete-btn').on('click',function(){
        self.tagDeleteBtn(this.id);
    })

    // タグをクリアボタンイベント
    $('.clear-button').on('click', function() {
        // $('.jquery-ui-sortable').empty();
        self.createDummyTag();
    });

    // タグ候補表示
    $('.tag-select-button').on('click', function() {
        $('.input-err-msg').remove();
        if($('#tag_select').val()==""){
            InputCheckUtil.showErrMsg('#tag_select', 'タグを選択してください。');
            return
        }
        self.selectTagArea();
    });

    // タグ名より該当タグを取得
    $('.tag-search-button').on('click',function(){
        var tag_name = $('.tag_name').val();
        self.likeSearchTag(tag_name);
    })

    // タグ保存ボタンのクリックイベント
    $('.tag-save-button').on('click', function() {
        self.saveTagBtn();
    });
    return $.Deferred().resolve().promise();
};

/**
 * カテゴリーマスタ検索
 */
SakuhinTagBindController.prototype.likeSearchTag = function(tag_name) {
    var self = this;
    var param ={
        'tag_like_search':'tag_like_search',
        'tag_name':tag_name
    }

    AjaxUtil.get('/admin_app/sakuhin_tag_bind/', param).then(function(xhr, status){
        // ajax実行成功する場合、カテゴリー名を表示する
        if(status == 'success'){
            // データを取得
            var result = JSON.parse(xhr.responseText);
            // タグ選択要素生成
            $('.tag-list-area')
                .children()
                .remove();

            self.CreateTagList(result);
        }
    });

}

SakuhinTagBindController.prototype.CreateTagList = function(result) {
    var tagSelectList = $('<ul class="tag-select-list"></ul>');
    if (result) {
        $(result).each(function(i,val){
            var tag_name = val['sakuhin_tag_name'];
            var tagElem = $('<li class="jquery-ui-draggable" sakuhin-tag-code =' +val['sakuhin_tag_code'] + '>' + tag_name + '</li>');

            tagElem.on('click',function(){
                $(this).toggleClass('button-pushed');
                
            })
            tagSelectList.append(tagElem);
        })
    }
    // タグリスト
    if(result.length > 0){
        $('.tag-list-area').append(tagSelectList);
    }
}

/**
 * タイトル検索
 */
SakuhinTagBindController.prototype.searchTitle = function() {
    var self = this;
    $('.status-msg').remove();
    $('.input-err-msg').remove();
    // 入力チェックエラーの場合、検索を行わない
    if (!InputCheckUtil.checkInputValue('#input-title-name','タイトル名',100)) {
        return;
    }

    // タイトルカテゴリを取得
    var categoryList = [];
    $('input[name=checkbox]:checked').each(function(){
                categoryList.push($(this).val());
    });
    
    if(categoryList.length == 0){
        InputCheckUtil.showErrMsg('#input-title-name', '検索カテゴリを選択してください。');
        return;
    }  
    // タイトル選択モーダル
    self.openTitleModal();

};

/**
 * タイトル選択モーダル
 */
SakuhinTagBindController.prototype.openTitleModal = function() {
    var self = this;
    modal = $('#title-search-dialog');

    // タイトルカテゴリを取得
    var categoryList = [];
    $('input[name=checkbox]:checked').each(function(){
        categoryList.push($(this).val());
    });  

    // パラメータを設定する
    var param = {
        'title-modal' : 'title-modal',
        'title-name' : $('#input-title-name').val(),
        'category' : JSON.stringify(categoryList)
    };
    // 検索処理（非同期）
    AjaxUtil.get('/admin_app/sakuhin_tag_bind/', param).then(function(xhr, status){
        // ajax実行成功する場合、作品モーダルグリッドを描画する
        if(status == 'success'){
            // データを取得
            var result = JSON.parse(xhr.responseText);
            if(result.length > 100){
                InputCheckUtil.showErrMsg('#input-title-name', '検索結果が100件以上のため、検索条件を絞って、もう一度検索してください。');
                return;
            }

            // データを取得後、グリッド設定処理
            self.setTitleSeatchModelGrid(result);
        }else{
            // ajax実行失敗する場合、エラーメッセージを表示する
            $('#errorMsg').show();
        }
        
    });

};

SakuhinTagBindController.prototype.setTitleSeatchModelGrid = function(result) {
        var self = this;
        // 一覧データが10以下の場合は高さ自動調整
        var height = 'auto';
        if (result.length >= 10) {
            height = 450;
        }
         // グリッドを再描画
        $('#list-grid').jqGrid('clearGridData')
        .jqGrid("GridUnload");
        
        // グリッド生成
        var colModel = self.createColModel();
        var option = {
            colNames: colModel.name,
            colModel: colModel.model,
            data: result,
            width: $('#list').width(),
            height : height,
            pager: '#pager',
            loadComplete: function(){
                self.gridBtnEvent(result)
            },
            pgbuttons : false,
            pginput : false,
            viewrecords : true,
            rowList : result.length,
            rowNum : result.length
        };
        GridUtil.renderNormalGrid('#list-grid', option, true);
    
        // モーダル生成
        modal.dialog({
            title: 'タイトルを選択',
            resizable: false,
            modal: true,
            width: 'auto',
            height: 'auto',
        });

        // モーダルを閉じる
        $('.cancel-button').on('click', function() {
            modal.dialog('close');
        });
};
/**
 * タグ候補表示エリア
 */
SakuhinTagBindController.prototype.selectTagArea = function() {
    var self = this;

    var selectValue = $('#tag_select').val();
    var param = {
        'category_select' : 'category_select',
        'category_code':selectValue
    }

    AjaxUtil.get('/admin_app/sakuhin_tag_bind/', param).then(function(xhr, status){
        // ajax実行成功する場合、カテゴリー名を表示する
        if(status == 'success'){
            // データを取得
            var result = JSON.parse(xhr.responseText);
            if(result.length > 100){
                InputCheckUtil.showErrMsg('#input-title-name', '検索結果が100件以上のため、検索条件を絞って、もう一度検索してください。');
                return;
            }

            // タグ選択要素生成
            $('.tag-list-area')
                .children()
                .remove();

            self.CreateTagList(result);

            // ドラッグ付与
            // self.setDragEvent('.jquery-ui-draggable');
        }else{
            // ajax実行失敗する場合、エラーメッセージを表示する
            $('#errorMsg').show();
        }
    });
    
};

/**
 * jQGrid用のカラム定義
 */
SakuhinTagBindController.prototype.createColModel = function() {
    var width = 1700;

    var modelArray = [];
    modelArray.push(
        GridUtil.createColModel({
            name: 'title_name',
            width: width * 0.24,
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'title_category_name',
            width: width * 0.05,
        })
    );
    
    modelArray.push(
        GridUtil.createColModel({
            name: 'update_user',
            width: width * 0.07,
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            name: 'update_time',
            width: width * 0.06,
            formatter : 'date',
            formatoptions : {
                srcformat : 'ISO8601Long',
                newformat : 'Y/m/d'
            }
        })
    );
    modelArray.push(
        GridUtil.createColModel({
            title: false,
            name: 'operation',
            width: width * 0.05,
            align: 'center',
            formatter: function(val, opt, rdt) {
                return (
                    '</button>' +
                    "<button type='button' class='grid-btn-update grid-btn-connectionIpDel update-button' data-titleName='" +
                    rdt.title_name.replace(/[&'`"<>]/g, function(match) {
                        return {
                        '&': '&amp;',
                        "'": '&#x27;',
                        '`': '&#x60;',
                        '"': '&quot;',
                        '<': '&lt;',
                        '>': '&gt;',
                        }[match]
                    }) +
                    "'title-code='" +
                    rdt.title_code +
                    "'data-category='" +
                    rdt.title_category_name +
                    "'data-category_code='" +
                    rdt.title_category_code +
                    "'tag_map_code='" +
                    rdt.tag_map_code  +
                    "'data-row-id='" +
                    opt.rowId +
                    "'>" +
                    '編集' +
                    '</button>'
                );
            },
            sortable: false,
        })
    );
    return {
        model: modelArray,
        name: ['タイトル名', '種別','更新者', '更新日時', '編集'],
    };
};

/**
 * jQGrid用のボタンイベント定義
 */
SakuhinTagBindController.prototype.gridBtnEvent = function(data) {
    var self = this;
    $('.grid-btn-update').on('click', function() {
        var tag_code_list = {};
        var core_code =[];
        var button = $(this);
        $(data).each(function(i,val){
            if(button.attr('title-code') == val['title_code']){
                core_code.push(val['core_code1']);
                core_code.push(val['core_code2']);
                tag_code_list['tag_code1'] = val['tag_code1'];
                tag_code_list['tag_code2'] = val['tag_code2'];
                tag_code_list['tag_code3'] = val['tag_code3'];
                tag_code_list['tag_code4'] = val['tag_code4'];
                tag_code_list['tag_code5'] = val['tag_code5'];
                tag_code_list['tag_code6'] = val['tag_code6'];
                tag_code_list['tag_code7'] = val['tag_code7'];
                tag_code_list['tag_code8'] = val['tag_code8'];
                tag_code_list['tag_code9'] = val['tag_code9'];
                tag_code_list['tag_code10'] = val['tag_code10'];
                tag_code_list['tag_code11'] = val['tag_code11'];
                tag_code_list['tag_code12'] = val['tag_code12'];
                tag_code_list['tag_code13'] = val['tag_code13'];
                tag_code_list['tag_code14'] = val['tag_code14'];
                tag_code_list['tag_code15'] = val['tag_code15'];
                tag_code_list['tag_code16'] = val['tag_code16'];
                tag_code_list['tag_code17'] = val['tag_code17'];
                tag_code_list['tag_code18'] = val['tag_code18'];
                tag_code_list['tag_code19'] = val['tag_code19'];
                tag_code_list['tag_code20'] = val['tag_code20'];
            }
        })
        var param = {
            'tag_name_select':'tag_name_select',
            'tag_code_list':JSON.stringify(tag_code_list)
        }
        AjaxUtil.get('/admin_app/sakuhin_tag_bind/', param).then(function(xhr, status){
            // ajax実行成功する場合、カテゴリー名を表示する
            if(status == 'success'){
                // データを取得
                var result = JSON.parse(xhr.responseText);

                var resultArr = []
                for (let i in result) {
                    let o = {};
                    o[i] = result[i];
                    resultArr.push(o)
             
                }

                var tagArea1 = resultArr.slice(0,5);
                var tagArea2 = resultArr.slice(5,10);
                var tagArea3 = resultArr.slice(10,20);
                
                var uiTag1 = $('#tag-1-5 ');
                var uiTag2 = $('#tag-6-10');
                var uiTag3 = $('#tag-11-20');
               
                $('.jquery-ui-sortable').empty();
                self.makeLiTag(uiTag1,tagArea1,1);
                self.makeLiTag(uiTag2,tagArea2,6);
                self.makeLiTag(uiTag3,tagArea3,11);

            }
        });


        // タイトル
        var select_title = $('.select-title');
        select_title.text($(this).attr('data-titleName'));
        select_title.attr('tag_map_code',$(this).attr('tag_map_code'));
        select_title.attr('data-category_code',$(this).attr('data-category_code'));
        select_title.attr('title_code',$(this).attr('title-code'));

        $('.tag-select-area').slideDown('slow');
        var modal = $('#title-search-dialog');
        modal.dialog('close');

        // コア名設定
        var options ={};
        $('#core-1 option').each(function(){
            options = $(this);
            if(options.val() == core_code[0]){
                $(this).attr('selected','selected');
            }
        })

        $('#core-2 option').each(function(){
            options = $(this);
            if(options.val() == core_code[1]){
                $(this).attr('selected','selected');
            }
        })
        
        $('#core-1').selectmenu("refresh");
        $('#core-2').selectmenu("refresh");
    });

    $('.title-select-cancel-button').on('click', function() {
        modal.dialog('close');
    });
};

SakuhinTagBindController.prototype.makeLiTag = function(ele,metaData,cnt) {
    $(metaData).each(function(i,val){
        if(val['tag_code' + (i + cnt)] == ""|| val['tag_code' + (i + cnt)] == null){
            ele.append($('<li id="" class="set-tag-btn">'+ '<span>タグを設定できます</span></li>').on('click',SakuhinTagBindController.prototype.switchTagSelect));
        }else{

            ele.append($('<li id='+'"'+val['tag_code' + (i + cnt)][0] + '"' + '><span>' +val['tag_code'+ (i + cnt)][1] + '</span></li>').on('click',SakuhinTagBindController.prototype.switchTagSelect));
        }
    });
}

/**
 * タグ要素削除イベント
 */
// SakuhinTagBindController.prototype.clickTagDeleteButton = function() {
//     //
//     $('.tag-delete-button').on('click', function() {
//         $('#tag-1-5 li').off('click');
//         // 親要素のliを削除
//         $(this)
//             .parent()
//             .parent()
//             .remove();
//     });
// };

// SakuhinTagBindController.prototype.setDragEvent = function(elem) {
//     var self = this;
//     $(elem).draggable({
//         connectToSortable: '.jquery-ui-sortable',
//         revert: 'invalid',
//         zIndex: '100',
//     });
// };
// /**
//  * ソート機能、ドラッグ付与
//  */
// SakuhinTagBindController.prototype.setTagEvent = function() {
//     var self = this;
//     $('.jquery-ui-sortable').sortable({
//         revert: 'invalid',
//         // ドラッグ要素が上に乗った時のイベント
//         receive: function(event, ui) {
//             $(ui.item)
//                 .children('span')
//                 .removeClass('display-none');
//         },
//     });

//     self.setDragEvent('.jquery-ui-draggable');
// };

SakuhinTagBindController.prototype.tagSettingBtn = function(id) {
    var self = this;
    $('.input-err-msg').remove();
    var tag_list = $('.tag-select-list .button-pushed');
    var tag1_5 = $('#tag-1-5');
    var tag6_10 = $('#tag-6-10');
    var tag11_20 = $('#tag-11-20');
    
    if($('#tag-list-area').children().length == 0){
        InputCheckUtil.showErrMsg('#tag_select', 'タグを選択してください。');
        $("html,body").animate({ scrollTop: $('.input-err-msg').offset().top}, 1000);
        return
    }

    // タグ選択を行わない場合
    if(tag_list.length == 0 ){
        InputCheckUtil.showErrMsg('#tag-list-area', '追加タグを選択してください。');
        $("html,body").animate({ scrollTop: $('.input-err-msg').offset().top}, 1000);
        return
    }
    // var tag_max_size = 5;
    
    if(tag_list.length <= 5 && id == 'tag-area1'){
        self.addTagToList(tag_list,tag1_5);
    }

    if(tag_list.length <= 5 && id == 'tag-area2'){
        self.addTagToList(tag_list,tag6_10);
    }

    if(tag_list.length <= 10 && id == 'tag-area3'){
        self.addTagToList(tag_list,tag11_20);
    }

    // タグボタンの背景色を元に戻す
    tag_list.each(function(){
        $(this).removeClass('button-pushed').removeClass('set-tag-btn');
    });
}

/**
 *  タグを追加する
 */
SakuhinTagBindController.prototype.addTagToList = function(target_list,tag_list) {
    var canSet_tag_list = tag_list.children().filter(function(index,ele){
        return $(ele).text().indexOf("設定") > 0;
    })

    target_list.each(function(i,outVal){
        var $outVal =$(outVal);
        var selectedTag = tag_list.find('.selected')

        // 設定先が選択されている場合
        if(selectedTag.length > 0){
            
            selectedTag.removeClass('set-tag-btn');
            selectedTag.html('<span>' + $outVal.html() + '</span>');
            selectedTag.id = $outVal.attr('sakuhin-tag-code');
            return false
        }

        // タグを設定できますのボタンがある場合
        if(canSet_tag_list.length > 0){
            var setTag = $(canSet_tag_list[i])
            setTag.removeClass('set-tag-btn');
            setTag.html('<span>' + $outVal.html() + '</span>');
            setTag.attr("id",$outVal.attr('sakuhin-tag-code'));
        }else{
            tag_list.each(function(j,innerVal){
                $(innerVal.children[i]).removeClass('set-tag-btn');
                innerVal.children[i].innerHTML = '<span>' + $outVal.html() + '</span>';
                innerVal.children[i].id = $outVal.attr('sakuhin-tag-code');
            })
        }

        // $(this)
        // .remove();
        
    })
    
}

/**
 *  タグを削除する
 */
SakuhinTagBindController.prototype.tagDeleteBtn = function(id) {
    var ulId ="";
    if(id == 'tag-area1-del'){
        ulId = 'tag-1-5';
    }else if(id == 'tag-area2-del'){
        ulId = 'tag-6-10';
    }else{
        ulId = 'tag-11-20';
    }

    var tag_selected = $('#' + ulId + ' .selected');
    
    if (tag_selected.length == 1) {
        tag_selected.remove();
        $('<li id="" class="set-tag-btn"><span>タグを設定できます</span></li>').on('click',this.switchTagSelect).appendTo($('#'+ulId));
    }

}

/**
 *  タグ要素を上へ移動    
 */
SakuhinTagBindController.prototype.tagMoveUp = function(id) {

    var ul_selected = $('#' +id + ' .selected');
    var selectedContent = ul_selected.children('span').html();
    var selectedEleId = ul_selected.attr('id');
    var selectedEleClass = ul_selected.attr('class');
    var prevContent = ul_selected.prev().children('span').html();
    var prev = ul_selected.prev();
    var prevEleId = ul_selected.prev().attr('id');
    var preEleClass = ul_selected.prev().attr('class');
    if (ul_selected.length == 1) {
        if (prev.length) {
            ul_selected.children('span').html(prevContent);
            ul_selected.attr('id',prevEleId);
            ul_selected.attr('class',preEleClass);
            prev.children('span').html(selectedContent);
            prev.attr('id',selectedEleId);
            prev.attr('class',selectedEleClass);
            prev.addClass('selected').siblings().removeClass('selected');
        } 
    } 
        
}

/**
 *  タグ要素を下へ移動    
 */
SakuhinTagBindController.prototype.tagMoveDown = function(id) {
    var ul_selected = $('#' +id + ' .selected');
    var selectedContent = ul_selected.children('span').html();
    var selectedEleId = ul_selected.attr('id');
    var selectedEleClass = ul_selected.attr('class');
    var nextContent = ul_selected.next().children('span').html();
    var next = ul_selected.next();
    var nextEleId = ul_selected.next().attr('id');
    var nextEleClass = ul_selected.next().attr('class');
    if (ul_selected.length == 1) {
        if (next.length) {
            ul_selected.children('span').html(nextContent);
            ul_selected.attr('id',nextEleId);
            ul_selected.attr('class',nextEleClass);
            next.children('span').html(selectedContent);
            next.attr('id',selectedEleId);
            next.attr('class',selectedEleClass);
            next.addClass('selected').siblings().removeClass('selected');
        } 
    } 
}

/**
 * タグを保存するイベント
 */
SakuhinTagBindController.prototype.saveTagBtn = function() {
    var select_title = $('.select-title');
    var tag_map_code = select_title.attr('tag_map_code');
    var title_category_code = select_title.attr('data-category_code');
    var title_code = select_title.attr('title_code');
    var core_code1 = $('#core-1').val();
    var core_code2 = $('#core-2').val();
    var sakuhin_tagArea1 = {};
    var sakuhin_tagArea2 = {};
    var sakuhin_tagArea3 = {};

    $('#tag-1-5 li').each(function(i,val){
        sakuhin_tagArea1['tag-'+ parseInt(i + 1)] = val.id
    })
    
    $('#tag-6-10 li').each(function(i,val){
        sakuhin_tagArea2['tag-'+ parseInt(i + 6)] = val.id
    })
   
    $('#tag-11-20 li').each(function(i,val){
        sakuhin_tagArea3['tag-'+ parseInt(i + 11)] = val.id
    })

    var param = {
        'tag_save':'tag_save',
        'title_name': $('.select-title').text(),
        'title_code': title_code,
        'tag_map_code':tag_map_code,
        'title_category_code':title_category_code,
        'core_code1':core_code1,
        'core_code2':core_code2,
        'sakuhin_tagArea1':sakuhin_tagArea1,
        'sakuhin_tagArea2':sakuhin_tagArea2,
        'sakuhin_tagArea3':sakuhin_tagArea3,
    }

    var form = $('form');
    $('<input>').attr({
                'type': 'hidden',
                'name': 'param',
                'value': JSON.stringify(param)
            }).appendTo(form);
    form.submit();
}

/**
 * 新たなタグを生成する
 */
SakuhinTagBindController.prototype.createDummyTag = function() {
    $('.jquery-ui-sortable li').remove();
    var tag1_5 = $('#tag-1-5');
    var tag6_10 = $('#tag-6-10');
    var tag11_20 = $('#tag-11-20'); 
    var dummyTag;
    for(var index = 1; index <= 20;index++){
        dummyTag = $('<li class="set-tag-btn"><span>タグを設定できます</span></li>').on('click',this.switchTagSelect);
        if(index <= 5){
            tag1_5.append(dummyTag);
        }else if(index > 5 && index <= 10){
            tag6_10.append(dummyTag);
        }else {
            tag11_20.append(dummyTag);
        }
       
    }
}

SakuhinTagBindController.prototype.switchTagSelect = function() {
    $(this).toggleClass('selected').siblings().removeClass('selected');
}

$(function() {
    var controller = new SakuhinTagBindController();
    controller.init();

    $(window).scroll(function () {  
        var offsetTop = $(window).scrollTop()-620 + "px";  
        var scrollTop = $(this).scrollTop();

        if($('.tag-list-area').children().length == 0 || $('.tag-list-area').height() > 1500){
            return
        }
        if(scrollTop > 600 && scrollTop < 1200){
            
            $(".tag-select-table").animate({ top: offsetTop }, { duration: 600, queue: false });  
        }
        if(scrollTop == 0){
            $(".tag-select-table").css("top",0);
        }

        if ($(document).scrollTop() >= $(document).height() - $(window).height()) {
            $(".tag-select-table").css("top",$(window).height()+210+'px');
        }
    }); 
});
