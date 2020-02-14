var MangaSeinendaiCreateController = function() {
};
MangaSeinendaiCreateController.prototype = new AbstractController();

/**
 * 性年代マスタ新規登録画面の主処理
 */
MangaSeinendaiCreateController.prototype.execute = function() {
    var self = this;

    // DatePicker設定
    InputUtil.setDataPicker();

    return $.Deferred().resolve().promise();
};

/**
 * メニュー選択処理
 */
MangaSeinendaiCreateController.prototype.selectedMenu = function() {
    return '.manga-seinendai-list';
};

/**
 * イベント登録処理
 */
MangaSeinendaiCreateController.prototype.bindEvent = function() {
    var self = this;

    // ファイル選択ボタン設定
    InputUtil.setInputFile('#btn', '#upload', '#uploadname');

    // ファイルアップロード
    $('#upload').on('change', function(e) {
        self.readFile(e);
    })

    var drop_dom_element = document.getElementById('drop');
    drop_dom_element.addEventListener('drop', function(e) {
        self.handleDrop(e);
    }, false);
    drop_dom_element.addEventListener('dragenter', self.handleDragover, false);
    drop_dom_element.addEventListener('dragover', self.handleDragover, false);

    // 保存ボタン
    $('.save-button ').on('click', function() {
        window.location.href = '/admin_app/manga_seinendai_list/';
    });
    // 一覧に戻るボタン
    $('.back-button ').on('click', function() {
        window.location.href = '/admin_app/manga_seinendai_list/';
    });

    // 保存してもう一つ追加ボタン
    $('.save-more-button ').on('click', function() {
        window.location.href = '/admin_app/manga_seinendai_create/';
    });

    return $.Deferred().resolve().promise();
};

MangaSeinendaiCreateController.prototype.handleDragover = function(e) {
    e.stopPropagation();
    e.preventDefault();
    e.dataTransfer.dropEffect = 'copy';
}

MangaSeinendaiCreateController.prototype.handleDrop = function(e) {
    var self = this;
    e.stopPropagation();
    e.preventDefault();
    var files = e.dataTransfer.files;
    var f = files[0];
    var reader = new FileReader();
    reader.onload = self.onloadFile;
    reader.readAsArrayBuffer(f);
}

MangaSeinendaiCreateController.prototype.readFile = function(e) {
    var self = this;
    var files = e.target.files;
    var f = files[0];
    var reader = new FileReader();
    reader.onload = self.onloadFile;
    reader.readAsArrayBuffer(f);
}

MangaSeinendaiCreateController.prototype.onloadFile = function(e) {
    var self = this;
    var unit8 = new Uint8Array(e.target.result);
    var workbook = XLSX.read(unit8, {
        type : "array"
    });
    console.log(workbook.Sheets['詳細']);

    if (workbook.Sheets['詳細']) {

        // 性年代シート内データ取得
        var seinendai = self.getSeinendai(workbook.Sheets['詳細']);
        // var seinendai = workbook.Sheets['詳細'];
        // 入力フォームにセル内容をセット
        t : type;
        v : value;
        $('#male-1').val(seinendai['A2'].v);
        $('#male-2').val(seinendai['A3'].v);
        $('#male-3').val(seinendai['A4'].v);
        $('#male-4').val(seinendai['A2'].v);
        $('#male-5').val(seinendai['A3'].v);
        $('#male-6').val(seinendai['A4'].v);
        $('#male-7').val(seinendai['A2'].v);
        $('#male-8').val(seinendai['A3'].v);
        $('#male-9').val(seinendai['A4'].v);
        $('#male-10').val(seinendai['A4'].v);
        $('#female-1').val(seinendai['B2'].v);
        $('#female-2').val(seinendai['B3'].v);
        $('#female-3').val(seinendai['B4'].v);
        $('#female-4').val(seinendai['B2'].v);
        $('#female-5').val(seinendai['B3'].v);
        $('#female-6').val(seinendai['B4'].v);
        $('#female-7').val(seinendai['B2'].v);
        $('#female-8').val(seinendai['B3'].v);
        $('#female-9').val(seinendai['B4'].v);
        $('#female-10').val(seinendai['B4'].v);

        var maleSum = 0;
        maleSum += parseInt($('#male-1').val());
        maleSum += parseInt($('#male-2').val());
        maleSum += parseInt($('#male-3').val());
        maleSum += parseInt($('#male-4').val());
        maleSum += parseInt($('#male-5').val());
        maleSum += parseInt($('#male-6').val());
        maleSum += parseInt($('#male-7').val());
        maleSum += parseInt($('#male-8').val());
        maleSum += parseInt($('#male-9').val());
        maleSum += parseInt($('#male-10').val());
        $('#male-total').val(maleSum);

        var femaleSum = 0;
        femaleSum += parseInt($('#female-1').val());
        femaleSum += parseInt($('#female-2').val());
        femaleSum += parseInt($('#female-3').val());
        femaleSum += parseInt($('#female-4').val());
        femaleSum += parseInt($('#female-5').val());
        femaleSum += parseInt($('#female-6').val());
        femaleSum += parseInt($('#female-7').val());
        femaleSum += parseInt($('#female-8').val());
        femaleSum += parseInt($('#female-9').val());
        femaleSum += parseInt($('#female-10').val());
        $('#female-total').val(femaleSum);

        $('#total').val(maleSum + femaleSum);

    }
}

MangaSeinendaiCreateController.prototype.handleDrop = function(e) {
    e.stopPropagation();
    e.preventDefault();
    var files = e.dataTransfer.files, f = files[0];
    var reader = new FileReader();
    reader.onload = function(e) {
        var unit8 = new Uint8Array(e.target.result);
        var workbook = XLSX.read(unit8, {
            type : "array"
        });
        console.log(workbook);

        if (workbook.Sheets['詳細']) {

            // 性年代シート内データ取得
            var seinendai = workbook.Sheets['詳細'];

            // 入力フォームにセル内容をセット
            t : type;
            v : value;
            $('#male-1').val(seinendai['A2'].v);
            $('#male-2').val(seinendai['A3'].v);
            $('#male-3').val(seinendai['A4'].v);
            $('#male-4').val(seinendai['A2'].v);
            $('#male-5').val(seinendai['A3'].v);
            $('#male-6').val(seinendai['A4'].v);
            $('#male-7').val(seinendai['A2'].v);
            $('#male-8').val(seinendai['A3'].v);
            $('#male-9').val(seinendai['A4'].v);
            $('#male-10').val(seinendai['A4'].v);
            $('#female-1').val(seinendai['B2'].v);
            $('#female-2').val(seinendai['B3'].v);
            $('#female-3').val(seinendai['B4'].v);
            $('#female-4').val(seinendai['B2'].v);
            $('#female-5').val(seinendai['B3'].v);
            $('#female-6').val(seinendai['B4'].v);
            $('#female-7').val(seinendai['B2'].v);
            $('#female-8').val(seinendai['B3'].v);
            $('#female-9').val(seinendai['B4'].v);
            $('#female-10').val(seinendai['B4'].v);

            var maleSum = 0;
            maleSum += parseInt($('#male-1').val());
            maleSum += parseInt($('#male-2').val());
            maleSum += parseInt($('#male-3').val());
            maleSum += parseInt($('#male-4').val());
            maleSum += parseInt($('#male-5').val());
            maleSum += parseInt($('#male-6').val());
            maleSum += parseInt($('#male-7').val());
            maleSum += parseInt($('#male-8').val());
            maleSum += parseInt($('#male-9').val());
            maleSum += parseInt($('#male-10').val());
            $('#male-total').val(maleSum);

            var femaleSum = 0;
            femaleSum += parseInt($('#female-1').val());
            femaleSum += parseInt($('#female-2').val());
            femaleSum += parseInt($('#female-3').val());
            femaleSum += parseInt($('#female-4').val());
            femaleSum += parseInt($('#female-5').val());
            femaleSum += parseInt($('#female-6').val());
            femaleSum += parseInt($('#female-7').val());
            femaleSum += parseInt($('#female-8').val());
            femaleSum += parseInt($('#female-9').val());
            femaleSum += parseInt($('#female-10').val());
            $('#female-total').val(femaleSum);

            $('#total').val(maleSum + femaleSum);

        }
    };
    reader.readAsArrayBuffer(f);
}

MangaSeinendaiCreateController.prototype.getSeinendai = function(sheet) {

    var seinendai = [];

    var male = 0;
    var female = 0;
    // 10歳以下
    for (var i = 0; i < 10; i++) {
        male += parseInt(sheet[''].v);
        female += parseInt(sheet[''].v);
    }
    return seinendai;
}

$(function() {
    var controller = new MangaSeinendaiCreateController();
    controller.init();
});
