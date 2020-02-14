/**
 * CLEditor共通ユーティリティ
 */
var CLEditorUtil = {
    /**
     * CLEditorのデフォルトオプション
     */
    defaultEditorOption: {
        // ツールバーで利用する機能
        controls: 'removeformat | ' + 'bold italic underline strikethrough | ' + 'size color highlight | ' + 'bullets numbering | ' + 'outdent indent  | ' + 'cut copy paste pastetext  | ' + 'source',

        // 高さ
        height: 400
    },

    /**
     * エディタ初期表示内容
     */
    defaultHtml: '',

    /**
     * CLEditor更新
     *
     *  @param editorId
     *            エディターID
     *  @param paramHtml
     *            エディターに表示するhtml
     */
    updateEditor: function(editorId, paramHtml) {
        var html = '';
        if (paramHtml) {
            html = paramHtml;
        }
        $(editorId).val(html);
        $(editorId)
            .cleditor()[0]
            .updateFrame();
    },

    // エディター設定
    createCLEditor: function(editorId, paramHtml, paramOption) {
        // ボタン説明を日本語化
        $.cleditor.buttons.bold.title = '太字';
        $.cleditor.buttons.italic.title = '斜体';
        $.cleditor.buttons.underline.title = '下線';
        $.cleditor.buttons.strikethrough.title = '打消し線';
        $.cleditor.buttons.size.title = 'フォントサイズ';
        $.cleditor.buttons.color.title = 'フォントカラー';
        $.cleditor.buttons.highlight.title = '背景色';
        $.cleditor.buttons.removeformat.title = '文字の装飾を解除';
        $.cleditor.buttons.bullets.title = 'リスト';
        $.cleditor.buttons.numbering.title = '数字リスト';
        $.cleditor.buttons.outdent.title = 'インデント解除';
        $.cleditor.buttons.indent.title = 'インデント';
        $.cleditor.buttons.rule.title = '水平線を挿入';
        $.cleditor.buttons.cut.title = '切り取り';
        $.cleditor.buttons.copy.title = 'コピー';
        $.cleditor.buttons.paste.title = '貼り付け';
        $.cleditor.buttons.pastetext.title = 'テキストとして貼り付け';
        $.cleditor.buttons.source.title = 'htmlソースに切り替え';

        // エディター生成
        var option = {};
        $.extend(option, this.defaultEditorOption, paramOption);
        $(editorId).cleditor(option);

        // エディター内容を更新
        CLEditorUtil.updateEditor(editorId, paramHtml);
    }
};
