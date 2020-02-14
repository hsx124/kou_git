var MangaListController = function() {};
MangaListController.prototype = new AbstractController();

/**
 * マンガDB登録画面の主処理
 */
MangaListController.prototype.execute = function() {
    var self = this;

    // メッセージ欄表示
    // MockMsgUtil.showStatusMsg('#target-book-name');

    // 更新履歴エリア生成
    self.createNoticeTable();

    return $.Deferred()
        .resolve()
        .promise();
};

/**
 * メニュー選択処理
 */
MangaListController.prototype.selectedMenu = function() {
    return '.menu-manga-master';
};

/**
 * イベント登録処理
 */
MangaListController.prototype.bindEvent = function() {
    var self = this;

    // 更新履歴DLエリアのイベント設定
    NoticeTableUtil.setDLArea();

    // マンガDB登録成功
    $('#save1').on('click', function() {
        // マンガマスタ一覧生成
        self.createMangaList();
    });

    // マンガDB登録失敗
    $('#save2').on('click', function() {
        // マンガマスタ一覧生成
        self.createMangaList2();
    });

    // ファイル選択ボタン設定
    InputUtil.setInputFile('#btn', '#upload', '#uploadname');
    InputUtil.setInputFile('#btn2', '#upload2', '#uploadname2');
    InputUtil.setInputFile('#btn3', '#upload3', '#uploadname3');
    InputUtil.setInputFile('#btn4', '#upload4', '#uploadname4');
    InputUtil.setInputFile('#btn5', '#upload5', '#uploadname5');

    return $.Deferred()
        .resolve()
        .promise();
};
/**
 * 更新履歴表示<br>
 * モック限定の処理を含むので本製造の時に注意。
 */
MangaListController.prototype.createNoticeTable = function() {
    // 更新履歴エリアの生成
    var noticeTable = new MockNoticeTable('2019/08/22', 'メディア部 XXX', '350作品', 1);
    noticeTable.add('2019/03/10', 'メディア部 XXX', '200作品', 1);
    noticeTable.add('2019/02/22', 'メディア部 XXX', '100作品', 1);
    MockNoticeTableUtil.draw(noticeTable.getAll());
};

/**
 * マンガDB一覧（登録成功時）生成<br>
 * jQGridを使用して表を描画する。
 */
MangaListController.prototype.createMangaList = function() {
    var self = this;
    $('.import-error').hide();
    $('.import-success').hide();
    $('#list-grid').GridUnload();
    $('#error-grid').GridUnload();

    $('#status-msg').hide();
    var list = $('#list');
    LoadingUtil.start('一括登録中...', list);

    setTimeout(function() {
        LoadingUtil.stop();
        $('.import-success').show();
        // グリッド生成
        var colModel = self.createColModel();
        $('#status-msg').show();
        var option = {
            colNames: colModel.name,
            colModel: colModel.model,
            data: self.createGridData(),
            pager: '#pager'
        };
        GridUtil.renderNormalGrid('#list-grid', option, true);
    }, 1500);
};
/**
 * マンガDB一覧（登録失敗時）生成<br>
 * jQGridを使用して表を描画する。
 */
MangaListController.prototype.createMangaList2 = function() {
    var self = this;
    $('.import-error').hide();
    $('.import-success').hide();
    $('#list-grid').GridUnload();
    $('#error-grid').GridUnload();
    $('#status-msg2').hide();

    var list = $('#list');
    LoadingUtil.start('一括登録中...', list);

    setTimeout(function() {
        LoadingUtil.stop();
        $('.import-error').show();
        $('#status-msg2').show();
        // グリッドレンダリング
        var colModel = self.createColModel2();
        var option = {
            colNames: colModel.name,
            colModel: colModel.model,
            data: self.createGridData2(),
            pager: '#pager2'
        };
        GridUtil.renderNormalGrid('#error-grid', option, true);
    }, 1500);
};
/**
 * jQGrid用のカラム定義
 */
MangaListController.prototype.createColModel = function() {
    var width = $('#list').width();

    var medelArray = [];
    medelArray.push(
        GridUtil.createColModel({
            name: 'ipName',
            width: width * 0.07
        })
    );
    medelArray.push(
        GridUtil.createColModel({
            name: 'author',
            width: width * 0.05
        })
    );
    medelArray.push(
        GridUtil.createColModel({
            name: 'core1',
            width: width * 0.05
        })
    );
    medelArray.push(
        GridUtil.createColModel({
            name: 'core2',
            width: width * 0.05
        })
    );
    medelArray.push(
        GridUtil.createColModel({
            name: 'classification',
            align: 'center',
            width: width * 0.05
        })
    );
    medelArray.push(
        GridUtil.createColModel({
            name: 'dorodoro',
            align: 'center',
            width: width * 0.1
        })
    );
    medelArray.push(
        GridUtil.createColModel({
            name: 'odoroki',
            align: 'center',
            width: width * 0.07
        })
    );
    medelArray.push(
        GridUtil.createColModel({
            name: 'kanasimi',
            align: 'center',
            width: width * 0.07
        })
    );
    medelArray.push(
        GridUtil.createColModel({
            name: 'kowai',
            align: 'center',
            width: width * 0.05
        })
    );
    medelArray.push(
        GridUtil.createColModel({
            name: 'realistic',
            align: 'center',
            width: width * 0.1
        })
    );
    medelArray.push(
        GridUtil.createColModel({
            name: 'tag',
            width: width * 0.2
        })
    );
    return {
        model: medelArray,
        name: ['IP名', '作者名', 'コア1', 'コア2', '印象分類', 'ドロドロ／さわやか', '驚き／平穏', '悲しみ／感動', '怖／楽', '非現実的／現実的', '事実タグ']
    };
};
/**
 * jQGrid用のカラム定義
 */
MangaListController.prototype.createColModel2 = function() {
    var width = $('#list').width();

    var medelArray = [];
    medelArray.push(
        GridUtil.createColModel({
            name: 'ipName',
            width: width * 0.07
        })
    );
    medelArray.push(
        GridUtil.createColModel({
            name: 'author',
            width: width * 0.07
        })
    );
    medelArray.push(
        GridUtil.createColModel({
            name: 'core1',
            width: width * 0.05
        })
    );
    medelArray.push(
        GridUtil.createColModel({
            name: 'core2',
            width: width * 0.05
        })
    );
    medelArray.push(
        GridUtil.createColModel({
            name: 'classification',
            align: 'center',
            width: width * 0.05
        })
    );
    medelArray.push(
        GridUtil.createColModel({
            name: 'dorodoro',
            align: 'center',
            width: width * 0.1
        })
    );
    medelArray.push(
        GridUtil.createColModel({
            name: 'odoroki',
            align: 'center',
            width: width * 0.07
        })
    );
    medelArray.push(
        GridUtil.createColModel({
            name: 'kanasimi',
            align: 'center',
            width: width * 0.07
        })
    );
    medelArray.push(
        GridUtil.createColModel({
            name: 'kowai',
            align: 'center',
            width: width * 0.05
        })
    );
    medelArray.push(
        GridUtil.createColModel({
            name: 'realistic',
            align: 'center',
            width: width * 0.1
        })
    );
    medelArray.push(
        GridUtil.createColModel({
            name: 'tag'
        })
    );
    medelArray.push(
        GridUtil.createColModel({
            name: 'error-msg',
            classes: 'error-column',
            width: width * 0.3
        })
    );
    return {
        model: medelArray,
        name: ['IP名', '作者名', 'コア1', 'コア2', '印象分類', 'ドロドロ／さわやか', '驚き／平穏', '悲しみ／感動', '怖／楽', '非現実的／現実的', '事実タグ', 'エラー内容']
    };
};

/**
 * jQGrid用のデータ定義
 */
MangaListController.prototype.createGridData = function() {
    var colNames = ['ipName', 'author', 'core1', 'core2', 'classification', 'dorodoro', 'odoroki', 'kanasimi', 'kowai', 'realistic', 'tag'];
    var gridData = [
        ['進撃の巨人', '諫山創', 'アクション', '', 'A', 'ドロドロ', '驚き（事件）', '悲しみ', '怖', '非現実的', '謎/巨人/戦闘・対決のもの/残酷・流血・グロテスク'],
        ['ＯＮＥ　ＰＩＥＣＥ', '尾田栄一郎', 'バトル', '', 'A', 'さわやか', '驚き（事件）', '感動', '楽', '非現実的', '海賊/仲間/冒険/友情/宝'],
        ['弱虫ペダル', '渡辺航', 'スポーツ', '', 'A', 'さわやか', '驚き（事件）', '感動', '楽', '現実的', '自転車/部活/オタク/高校生'],
        ['ＨＵＮＴＥＲ×ＨＵＮＴＥＲ', '冨樫義博', 'バトル', '', 'A', 'さわやか', '驚き（事件）', '感動', '楽', '非現実的', 'ハンター/冒険'],
        ['ＮＡＲＵＴＯ', '岸本斉史', 'バトル', '', 'B', 'さわやか', '驚き（事件）', '感動', '楽', '非現実的', '仲間/忍者/戦闘・対決/落ちこぼれ'],
        ['北斗の拳', '原作：武論尊／作画：原哲夫', 'バトル', '', 'B', 'ドロドロ', '驚き（事件）', '感動', '怖', '非現実的', '戦闘・対決/暴力/世紀末/ディストピア'],
        ['七つの大罪', '鈴木央', 'バトル', '', 'B', 'さわやか', '驚き（事件）', '感動', '楽', '非現実的', '罪人/騎士団/戦闘・対決/旅'],
        ['鋼の錬金術師', '荒川弘', 'バトル', '', 'B', 'さわやか', '驚き（事件）', '感動', '楽', '非現実的', '錬金術/兄弟/旅/戦闘・対決'],
        ['ベイビーステップ', '勝木光', 'スポーツ', '', 'B', 'さわやか', '驚き（事件）', '感動', '楽', '現実的', 'テニス/主人公の成長/高校生'],
        ['鬼滅の刃', '吾峠呼世晴', 'バトル', '', 'B', 'ドロドロ', '驚き（事件）', '悲しみ', '怖', '非現実的', '鬼/大正時代/刀/残酷・流血・グロテスク'],
        ['テニスの王子様', '許斐たけし', 'スポーツ', '', 'A', 'さわやか', '驚き（事件）', '感動', '楽', '現実的', 'テニス/中学生/帰国子女'],
        ['呪術廻戦', '芥見下々', 'バトル', '', 'B', 'ドロドロ', '驚き（事件）', '悲しみ', '怖', '非現実的', '呪術師/残酷・流血・グロテスク'],
        ['さよなら絶望先生', '久米田康次', 'ギャグコメディ', '', 'B', 'さわやか', '驚き（事件）', '悲しみ', '怖', '現実的', 'ハーレム/教師/生徒/時事ネタ'],
        ['ＧＡＮＧＳＴＡ．', 'コースケ', 'バトル', '', 'B', 'ドロドロ', '驚き（事件）', '悲しみ', '怖', '非現実的', '便利屋/銃/スラム街/アウトロー'],
        ['僕のヒーローアカデミア', '堀越耕平', 'バトル', '', 'B', 'さわやか', '驚き（事件）', '感動', '楽', '非現実的', '個性/ヒーロー/高校生'],
        ['異世界おじさん', 'ほとんど死んでいる', 'ギャグコメディ', '', 'D', 'さわやか', '驚き（事件）', '感動', '楽', '現実的', '異世界/叔父/ツンデレ/エルフ/セガ'],
        ['ハイキュー', '古舘春一', 'スポーツ', '', 'B', 'さわやか', '驚き（事件）', '感動', '楽', '非現実的', 'バレーボール/高校生/仙台/低身長'],
        ['あせとせっけん', '山田金鉄', 'ラブロマンス', '', 'B', 'さわやか', '平穏（ほのぼの）', '感動', '楽', '現実的', '汗っかき/コンプレックス/職場恋愛/眼鏡']
    ];
    return GridUtil.createGridData(colNames, gridData);
};

/**
 * jQGrid用のデータ定義
 */
MangaListController.prototype.createGridData2 = function() {
    var colNames = ['ipName', 'author', 'core1', 'core2', 'classification', 'dorodoro', 'odoroki', 'kanasimi', 'kowai', 'realistic', 'tag', 'error-msg'];
    var gridData = [
        ['鬼滅の刃', '吾峠呼世晴', '', '', 'B', 'ドロドロ', '驚き（事件）', '悲しみ', '怖', '非現実的', '鬼/大正時代/刀/残酷・流血・グロテスク', '『コア1』が未入力です'],
        [
            'テニスの王子様',
            '許斐たけし',
            'スポーツ',
            '',
            'A',
            'さわやか',
            '驚き（事件）',
            '泣ける',
            '楽',
            '現実的',
            'テニス/中学生/帰国子女',
            '<span class="bold">泣ける</span>は印象マスタに定義されていません'
        ],
        [
            '呪術廻戦',
            '芥見下々',
            'バトル',
            'ヒューマンドラマ',
            'B',
            'ドロドロ',
            '驚き（事件）',
            '悲しみ',
            '怖',
            '非現実的',
            '呪術師/残酷・流血・グロテスク',
            '<span class="bold">ヒューマンドラマ</span>は『コア2』に設定できません'
        ],
        ['さよなら絶望先生', '久米田康次', 'ギャグコメディ', '', 'B', 'さわやか', '驚き（事件）', '悲しみ', '怖', '', 'ハーレム/教師/生徒/時事ネタ', '『現実的／非現実的』が未入力です'],
        ['GANGSTA.', 'コースケ', 'バトル', '', 'B', 'ドロドロ', '驚き（事件）', '悲しみ', '怖', '非現実的', '便利屋/銃/スラム街/アウトロー', '『作品名』は全角で入力してください'],
        [
            '僕のヒーローアカデミア',
            '堀越耕平',
            'バトル',
            '学園もの',
            'B',
            'さわやか',
            '驚き（事件）',
            '感動',
            '楽',
            '非現実的',
            '個性/ヒーロー/高校生',
            '<span class="bold">学園もの</span>はコアマスタに定義されていません'
        ],
        [
            '異世界おじさん',
            'ほとんど死んでいる',
            'ギャグコメディ',
            '',
            'D',
            'さわやか',
            '驚き（事件）',
            '感動',
            '楽',
            '現実的',
            '異世界転生/おじさん/ユーチューバー/ツンデレ/エルフ/セガ',
            '『事実タグ』は5個以内で設定してください'
        ],
        ['ハイキュー', '古舘春一', 'スポーツ', '', 'B', 'さわやか', '驚き（事件）', '感動', '楽', '非現実的', 'バレーボール/高校生/仙台/低身長', '『作品名』が重複しています'],
        ['ハイキュー', '古舘春一', 'スポーツ', '', 'B', 'さわやか', '驚き（事件）', '感動', '楽', '非現実的', 'バレーボール/高校生/仙台/低身長', '『作品名』が重複しています'],
        [
            'あせとせっけん',
            '山田 金鉄',
            'ラブロマンス',
            '',
            'B',
            'さわやか',
            '平穏（ほのぼの）',
            '感動',
            '楽',
            '現実的',
            '汗っかき/コンプレックス/職場恋愛/眼鏡',
            '『作者名』に半角スペースが含まれています'
        ]
    ];
    return GridUtil.createGridData(colNames, gridData);
};

$(function() {
    var controller = new MangaListController();
    controller.init();
});
