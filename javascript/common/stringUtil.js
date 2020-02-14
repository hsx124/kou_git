/**
 * 文字列関連のユーティリティ
 */
var StringUtil = {
    // 第一引数で与えられた数を第二引数で与えられた桁数で左0埋めする
    lpad : function(num, length) {
        return ('0000000000' + num).slice(-length);
    },

    // 第一引数で与えられた値がundefinedである場合、第二引数で与えられれた代替文字列を返却する
    coalesce : function(val, str) {
        return (val != undefined ? val : str)
    },
    // 第一引数で与えられた数値を3桁カンマ区切り
    comma_separated : function(val){
        if(val){
            return val.toString().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,") 
        }else{
            return ''
        }
    }
}