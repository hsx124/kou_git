/**
 * jqGridの共通ユーティリティ
 */
var GridUtil = {
    /**
     * jqGrid表示用のデフォルトオプション
     */
    defaultOption: {
        // データの種類('local', 'json', 'xml')
        datatype: 'local',

        // 列のタイトルを指定する（配列で指定）
        colNames: [],

        // 列単位の設定（オブジェクトの配列で指定）
        colModel: [{}],

        // 表示するデータ（オブジェクトの配列で指定）
        data: [{}],

        // 複数選択可否(true:複数選択可 / false：複数選択不可)
        multiselect: false,

        // 1ページに表示する行
        rowNum: 10,

        // 表の高さ（数値または'auto'で指定）
        height: 'auto',

        // 表の幅（数値または'auto'で指定）
        width: 'auto',

        // 行番号（true:表示 / false：非表示）
        rownumbers: true,

        // 列の幅を自動にするかどうか（true:自動 / false：固定）
        autowidth: true,

        // フッターの右下に表示中の行番号を表示するかどうか（true:表示 / false：非表示）
        viewrecords: true,

        // ページャーの選択肢（配列で指定）
        rowList: [10, 20, 50]
    },

    defaultColModel: {
        // インデックス名
        index: '',

        // 項目名
        name: '',

        // 横位置（'left','center','right'）
        align: 'left',

        // 横幅のリサイズ
        resizable: true,

        // 編集の可否
        editable: false,

        // 編集のオプション
        editoptions: [],

        // ソートの可否
        sortable: true,

        // ソートのタイプ（'integer','date','text',function）
        sorttype: 'text',

        // ホバー時に値をツールチップで表示するか
        title: true
    },

    /**
     * jqGrid表示
     *
     * @param target
     *            グリッドを表示させる場所のセレクタ
     * @param paramOption
     *            グリッド用表示用のオプション
     * @param filter
     *            ヘッダーにフィルターを表示するかどうか
     */
    renderNormalGrid: function(target, paramOption, filter) {
        var option = {};
        $.extend(option, this.defaultOption, paramOption);
        $(target).jqGrid(option);

        // フィルター検索
        if (filter) {
            this.setFilterToolbar(target, 'cn');
        }
    },

    /**
     * フィルター表示
     *
     * @param option
     *            検索条件（cn:contain / eq:equal etc...）
     */
    setFilterToolbar: function(target, option) {
        $(target).filterToolbar({
            // cn:contain,eq:equal
            defaultSearch: option
        });
    },

    /**
     * カラム生成
     *
     * @param paramColModel
     *            カラムの設定
     */
    createColModel: function(paramColModel) {
        return $.extend({}, this.defaultColModel, paramColModel);
    },

    /**
     * グリッドデータ生成（全体）
     *
     * @param colNames
     *            カラム名配列
     * @param values
     *            値の配列
     */
    createGridData: function(colNames, values) {
        var data = [];

        for (var i = 0; i < values.length; i++) {
            data.push(GridUtil.createGridDataRow(colNames, values[i]));
        }

        return data;
    },

    /**
     * グリッドデータ生成（1行）
     *
     * @param colNames
     *            カラム名配列
     * @param values
     *            値の配列
     */
    createGridDataRow: function(colNames, values) {
        var ret = {};

        for (var i = 0; i < colNames.length; i++) {
            ret[colNames[i]] = values[i];
        }

        return ret;
    },

    /**
     * フォーマット（〇×表示）
     * セルに値があれば「〇」、なければ「×」で表示
     * null blank undefined は「×」
     * 
     * @param val
     *            セルの値
     */
    formatMaruBatsu: function(val) {
        if (val){
            return '〇';
        } else {
            return '×';
        }
    },

    /**
     * フォーマット
     * セルに値があれば「trueVal」、なければ「falseVal」で表示
     * null blank undefined は「falseVal」
     * 
     * @param val
     *            セルの値
     * @param trueVal
     *            Trueの場合の返却値
     * @param falseVal
     *            Falseの場合の返却値
     */
    formatTrueFalse: function(val,trueVal,falseVal) {
        if (val){
            return trueVal;
        } else {
            return falseVal;
        }
    },
    
};
