var MangaCreateController = function() {
};
MangaCreateController.prototype = new AbstractController();

/**
 * メニュー選択処理
 */
MangaCreateController.prototype.selectedMenu = function() {
    return '.manga-list';
};

/**
 * イベント登録処理
 */
MangaCreateController.prototype.bindEvent = function() {
    var self = this;

    // モーダルを開くイベント群
    self.openModalEvent();

    // ボタン削除イベント群
    self.deleteBtnEvent();

    // マンガ一覧に戻る
    $('.back-button').on('click', function() {
        window.location.href = '/admin_app/manga_list/';
    });

    return $.Deferred().resolve().promise();
};

MangaCreateController.prototype.openModalEvent = function() {
    var self = this;

    // 掲載媒体モーダルを開く
    $('.media').on('selectmenuopen', function() {
        self.openMediaModal();
    });

    // 出版社モーダルを開く
    $('.publisher').on('selectmenuopen', function() {
        self.openPublisherModal();
    });

    // スタッフ役割モーダルを開く
    $('.staff-role').on('selectmenuopen', function() {
        var select = $(this).attr('data-select-staff-role');
        self.openStaffRoleModal(select);
    });

    // スタッフモーダルを開く
    $('.staff').on('selectmenuopen', function() {
        var select = $(this).attr('data-select-staff');
        self.openStaffModal(select);
    });
};

MangaCreateController.prototype.deleteBtnEvent = function(){
    // 掲載媒体データ削除ボタン
    $('.media-delete-button').on('click',function(){
        $('#media-code').val('');
        $('#media-name').val('');
        $('#media-name').text('掲載雑誌を選択');
        // セレクトボックスを再読み込みする
        $('.media').selectmenu('refresh');
    });

    // 出版社データ削除ボタン
    $('.publisher-delete-button').on('click',function(){
        $('#publisher-code').val('');
        $('#publisher-name').val('');
        $('#publisher-name').text('出版社を選択');
        // セレクトボックスを再読み込みする
        $('.publisher').selectmenu('refresh');
    });

    // スタッフ役割削除ボタン
    $('.staff-delete-button').on('click',function(){
        var select = $(this).attr('data-delete-button');
        if(select == '01'){
            $('#staff-role-code1').val('');
            $('#staff-role-name1').val('');
            $('#staff-role-name1').text('スタッフ役割1を選択');
            $('#staff-code1').val('');
            $('#staff-name1').val('');
            $('#staff-name1').text('スタッフ1を選択');
        }else if(select == '02'){
            $('#staff-role-code2').val('');
            $('#staff-role-name2').val('');
            $('#staff-role-name2').text('スタッフ役割2を選択');
            $('#staff-code2').val('');
            $('#staff-name2').val('');
            $('#staff-name2').text('スタッフ2を選択');
        }else if(select == '03'){
            $('#staff-role-code3').val('');
            $('#staff-role-name3').val('');
            $('#staff-role-name3').text('スタッフ役割3を選択');
            $('#staff-code3').val('');
            $('#staff-name3').val('');
            $('#staff-name3').text('スタッフ3を選択');
        }else if(select == '04'){
            $('#staff-role-code4').val('');
            $('#staff-role-name4').val('');
            $('#staff-role-name4').text('スタッフ役割4を選択');
            $('#staff-code4').val('');
            $('#staff-name4').val('');
            $('#staff-name4').text('スタッフ4を選択');
        }else if(select == '05'){
            $('#staff-role-code5').val('');
            $('#staff-role-name5').val('');
            $('#staff-role-name5').text('スタッフ役割5を選択');
            $('#staff-code5').val('');
            $('#staff-name5').val('');
            $('#staff-name5').text('スタッフ5を選択');
        }

        // セレクトボックスを再読み込みする
        $('.staff').selectmenu('refresh');
        $('.staff-role').selectmenu('refresh');
    });
};

// モーダル検索
MangaCreateController.prototype.searchModal = function(param, callback, modal) {
    // ajaxでデータ取得
    AjaxUtil.get('/admin_app/manga_create/', param).then(function(xhr,status) {
        if(status == 'success'){
            var result = JSON.parse(xhr.responseText);
            // 取得したデータを表示する。
            callback(result, modal);
        }else{
            $('#errorMsg').show();
            modal.dialog('close');
        }
    });
}

// モーダル(掲載媒体)
MangaCreateController.prototype.openMediaModal = function() {
    var self = this;
    $('#errorMsg').hide();
    var modal = $('#media-confirm-dialog');

    // 全体検索を表示しておく
    self.searchMediaInit(modal);

    // 検索処理
    $('.search-media-botton').on('click', function() {
        self.searchMedia(modal);
    });

    // 初期化処理
    $('.clear-botton').on('click', function() {
        $('#media-keyword').val('');
        $('.media-btn-list').empty();
        self.searchMediaInit(modal);
    });

    // キャンセル処理
    $('.cancel-botton').on('click', function() {
        modal.dialog('close');
    });

    modal.dialog({
        modal: true,
        width: '1150px',
    });
}

// 掲載媒体マスタ検索（初期化）
MangaCreateController.prototype.searchMediaInit = function(modal) {
    var self = this;
    var param = {
        'process_code' : 'media',
        'keyword' : ''
    };
    self.searchModal(param, self.drawMediaList, modal);
}

// 掲載媒体マスタ検索
MangaCreateController.prototype.searchMedia = function(modal) {
    var self = this;
    var param = {
        'process_code' : 'media',
        'keyword' : document.getElementById('media-keyword').value
    };
    self.searchModal(param, self.drawMediaList, modal);
}

// 掲載媒体マスタ検索結果を描画する
MangaCreateController.prototype.drawMediaList = function(mediaData,modal) {
    $('.media-btn-list').empty();
    for(var i=0;i<mediaData.length;i++){
        media = mediaData[i];
        mediaButton = "<button type='button' class='media-btn-select' data-media-code='" + media[0] + "' data-media-name='" + media[1] + "'>" + media[1] + "</button>"
        $('.media-btn-list').append(mediaButton);
    }
    // クリックイベント
    $('.media-btn-select').on('click', function() {
        var button = $(this);

        // 選択したデータをformに適用してモーダルを閉じる
        $('#media-code').val(button.attr('data-media-code'));
        $('#media-name').val(button.attr('data-media-name'));
        $('#media-name').text(button.attr('data-media-name'));

        // セレクトボックスを再読み込みする
        $('.media').selectmenu('refresh');
        modal.dialog('close');

        // モーダル内を初期化しておく
        $('#media-keyword').val('');
        $('.media-btn-list').empty();
    });
}

// モーダル(出版社)
MangaCreateController.prototype.openPublisherModal = function() {
    var self = this;
    $('#errorMsg').hide();

    var modal = $('#publisher-confirm-dialog');

    // 全体検索を表示しておく
    self.searchPublisherInit(modal);

    // 検索処理
    $('.search-publisher-botton').on('click', function() {
        self.searchPublisher(modal);
    });

    // 初期化処理
    $('.clear-botton').on('click', function() {
        $('#publisher-keyword').val('');
        $('.publisher-btn-list').empty();
        self.searchPublisherInit(modal);
    });

    // キャンセル処理
    $('.cancel-botton').on('click', function() {
        modal.dialog('close');
    });

    modal.dialog({
        modal: true,
        width: '1150px'
    });
}

// 出版社マスタ検索（初期化）
MangaCreateController.prototype.searchPublisherInit = function(modal) {
    var self = this;
    var param = {
        'process_code' : 'publisher',
        'keyword' : ''
    };
    self.searchModal(param, self.drawPublisherList, modal);
}

// 出版社マスタ検索
MangaCreateController.prototype.searchPublisher = function(modal) {
    var self = this;
    var param = {
        'process_code' : 'publisher',
        'keyword' : document.getElementById('publisher-keyword').value
    };
    self.searchModal(param, self.drawPublisherList, modal);
}

// 出版社マスタ検索結果を描画する
MangaCreateController.prototype.drawPublisherList = function(publisherData) {
    $('.publisher-btn-list').empty();
    for(var i=0;i<publisherData.length;i++){
        publisher = publisherData[i];
        publisherButton = "<button type='button' class='publisher-btn-select' data-publisher-code='" + publisher[0] + "' data-publisher-name='" + publisher[1] + "'>" + publisher[1] + "</button>"
        $('.publisher-btn-list').append(publisherButton);
    }

    // クリックイベント
    $('.publisher-btn-select').on('click', function() {
        var modal = $('#publisher-confirm-dialog');
        var button = $(this);

        // 選択したデータをformに適用してモーダルを閉じる
        $('#publisher-code').val(button.attr('data-publisher-code'));
        $('#publisher-name').val(button.attr('data-publisher-name'));
        $('#publisher-name').text(button.attr('data-publisher-name'));

        // セレクトボックスを再読み込みする
        $('.publisher').selectmenu('refresh');
        modal.dialog('close');

        // モーダル内を初期化しておく
        $('#publisher-keyword').val('');
        $('.publisher-btn-list').empty();
    });
}

// モーダル検索(スタッフ)
MangaCreateController.prototype.searchModalStaff = function(param, callback, modal, select) {
    // ajaxでデータ取得
    AjaxUtil.get('/admin_app/manga_create/', param).then(function(xhr,status) {
        if(status == 'success'){
            var result = JSON.parse(xhr.responseText);
            // 取得したデータを表示する。
            callback(result, modal, select);
        }else{
            $('#errorMsg').show();
            modal.dialog('close');
        }
    });
}

// モーダル(スタッフ役割)
MangaCreateController.prototype.openStaffRoleModal = function(select) {
    var self = this;
    $('#errorMsg').hide();
    var modal = $('#staff-role-confirm-dialog');

    // 全体検索を表示しておく
    self.searchStaffRoleInit(modal, select);

    // 検索処理
    $('.search-staff-role-botton').on('click', function() {
        self.searchStaffRole(modal, select);
    });

    // 初期化処理
    $('.clear-botton').on('click', function() {
        $('#staff-role-keyword').val('');
        $('.staff-role-btn-list').empty();
        self.searchStaffRoleInit(modal, select);
    });

    // キャンセル処理
    $('.cancel-botton').on('click', function() {
        modal.dialog('close');
    });

    modal.dialog({
        modal: true,
        width: '1150px'
    });
}

// スタッフマスタ検索（初期化）
MangaCreateController.prototype.searchStaffRoleInit = function(modal,select) {
    var self = this;
    var param = {
        'process_code' : 'staff_role',
        'keyword' : ''
    };
    self.searchModalStaff(param, self.drawStaffRoleList, modal, select);
}

// スタッフ役割マスタ検索
MangaCreateController.prototype.searchStaffRole = function(modal,select) {
    var self = this;
    var param = {
        'process_code' : 'staff_role',
        'keyword' : document.getElementById('staff-role-keyword').value
    };
    self.searchModalStaff(param, self.drawStaffRoleList, modal, select);
}
// スタッフ役割マスタ検索結果を描画する
MangaCreateController.prototype.drawStaffRoleList = function(staffRoleData,modal,select) {
    $('.staff-role-btn-list').empty();
    for(var i=0;i<staffRoleData.length;i++){
        staffRole = staffRoleData[i];
        staffRoleButton = "<button type='button' class='staff-role-btn-select' data-staff-role-code='" + staffRole[0] + "' data-staff-role-name='" + staffRole[1] + "'>" + staffRole[1] + "</button>"
        $('.staff-role-btn-list').append(staffRoleButton);
    }

    // クリックイベント
    $('.staff-role-btn-select').on('click', function() {
        var button = $(this);

        // 選択したデータをformに適用してモーダルを閉じる
        if(select == '001-01'){
            $('#staff-role-code1').val(button.attr('data-staff-role-code'));
            $('#staff-role-name1').val(button.attr('data-staff-role-name'));
            $('#staff-role-name1').text(button.attr('data-staff-role-name'));
        }else if(select == '002-01'){
            $('#staff-role-code2').val(button.attr('data-staff-role-code'));
            $('#staff-role-name2').val(button.attr('data-staff-role-name'));
            $('#staff-role-name2').text(button.attr('data-staff-role-name'));
        }else if(select == '003-01'){
            $('#staff-role-code3').val(button.attr('data-staff-role-code'));
            $('#staff-role-name3').val(button.attr('data-staff-role-name'));
            $('#staff-role-name3').text(button.attr('data-staff-role-name'));
        }else if(select == '004-01'){
            $('#staff-role-code4').val(button.attr('data-staff-role-code'));
            $('#staff-role-name4').val(button.attr('data-staff-role-name'));
            $('#staff-role-name4').text(button.attr('data-staff-role-name'));
        }else if(select == '005-01'){
            $('#staff-role-code5').val(button.attr('data-staff-role-code'));
            $('#staff-role-name5').val(button.attr('data-staff-role-name'));
            $('#staff-role-name5').text(button.attr('data-staff-role-name'));
        }

        // セレクトボックスを再読み込みする
        $('.staff-role').selectmenu('refresh');
        modal.dialog('close');

        // モーダル内を初期化しておく
        $('#staff-role-keyword').val('');
        $('.staff-role-btn-list').empty();
    });
}

// モーダル(スタッフ)
MangaCreateController.prototype.openStaffModal = function(select) {
    var self = this;
    $('#errorMsg').hide();
    var modal = $('#staff-confirm-dialog');

    // 全体検索を表示しておく
    self.searchStaffInit(modal, select);

    // 検索処理
    $('.search-staff-botton').on('click', function() {
        self.searchStaff(modal, select);
    });

    // 初期化処理
    $('.clear-botton').on('click', function() {
        $('#staff-keyword').val('');
        $('.staff-btn-list').empty();
        self.searchStaffInit(modal, select);
    });

    // キャンセル処理
    $('.cancel-botton').on('click', function() {
        modal.dialog('close');
    });

    modal.dialog({
        modal: true,
        width: '1150px'
    });
}

// スタッフマスタ検索（初期化）
MangaCreateController.prototype.searchStaffInit = function(modal,select) {
    var self = this;
    var param = {
        'process_code' : 'staff',
        'keyword' : ''
    };
    self.searchModalStaff(param, self.drawStaffList, modal, select);
}

// スタッフマスタ検索
MangaCreateController.prototype.searchStaff = function(modal,select) {
    var self = this;
    var param = {
        'process_code' : 'staff',
        'keyword' : document.getElementById('staff-keyword').value
    };
    self.searchModalStaff(param, self.drawStaffList, modal, select);
}

// スタッフマスタ検索結果を描画する
MangaCreateController.prototype.drawStaffList = function(staffData,modal,select) {
    $('.staff-btn-list').empty();
    for(var i=0;i<staffData.length;i++){
        staff = staffData[i];
        staffButton = "<button type='button' class='staff-btn-select' data-staff-code='" + staff[0] + "' data-staff-name='" + staff[1] + "'>" + staff[1] + "</button>"
        $('.staff-btn-list').append(staffButton);
    }

    // クリックイベント
    $('.staff-btn-select').on('click', function() {
        var button = $(this);

        // 選択したデータをformに適用してモーダルを閉じる
        if(select == '001-02'){
            $('#staff-code1').val(button.attr('data-staff-code'));
            $('#staff-name1').val(button.attr('data-staff-name'));
            $('#staff-name1').text(button.attr('data-staff-name'));
        }else if(select == '002-02'){
            $('#staff-code2').val(button.attr('data-staff-code'));
            $('#staff-name2').val(button.attr('data-staff-name'));
            $('#staff-name2').text(button.attr('data-staff-name'));
        }else if(select == '003-02'){
            $('#staff-code3').val(button.attr('data-staff-code'));
            $('#staff-name3').val(button.attr('data-staff-name'));
            $('#staff-name3').text(button.attr('data-staff-name'));
        }else if(select == '004-02'){
            $('#staff-code4').val(button.attr('data-staff-code'));
            $('#staff-name4').val(button.attr('data-staff-name'));
            $('#staff-name4').text(button.attr('data-staff-name'));
        }else if(select == '005-02'){
            $('#staff-code5').val(button.attr('data-staff-code'));
            $('#staff-name5').val(button.attr('data-staff-name'));
            $('#staff-name5').text(button.attr('data-staff-name'));
        }

        // セレクトボックスを再読み込みする
        $('.staff').selectmenu('refresh');
        modal.dialog('close');

        // モーダル内を初期化しておく
        $('#staff-keyword').val('');
        $('.staff-btn-list').empty();
    });
}

$(function() {
    var controller = new MangaCreateController();
    controller.init();
});
