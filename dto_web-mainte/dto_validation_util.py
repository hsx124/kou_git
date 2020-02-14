from django import forms
import re

class ValidationUtil():

    E0000001 = '{0}を入力してください。'
    E0000002 = '{0}は{1}文字以内で入力してください。'
    E0000003 = '{0}は全角文字で入力してください。'
    E0000004 = '{0}はひらがなで入力してください。'
    E0000005 = '{0}は{1}文字以内としてください。'
    E0000006 = '{0}の{1}が正しくありません。'
    E0000007 = '{0}はYYYY/MM/DD形式で入力してください。'
    E0000008 = '不正な日付が入力されています。'
    E0000009 = '{0}には{1}以降の日付を入力してください。'
    E0000010 = '入力形式が正しくありません。'
    E0000011 = '{0}の{1}を選択してください。'
    E0000012 = '{0}は{1}文字または{2}文字で入力してください。'
    E0000013 = '{0}は半角数字で入力してください。'
    E0000014 = 'ファイルサイズは1MB未満としてください。'
    E0000015 = '{0}、{1}のいずれかを入力してください。'
    E0000016 = '{0}は{1}桁で入力してください。'
    E0000017 = '{0}は " / " を入力しないでください。'
    E0000018 = '{0}は{1}桁以内で入力してください。'
    E0000019 = '{0}を選択してください。'
    E0000020 = '{0}と{1}の両方を選択してください。'

    # 全角文字チェック
    def validate_fullwidth(value):
        if not (re.match(r'^[^\x01-\x7E\uFF61-\uFF9F]+$', value) is not None):
            raise forms.ValidationError('全角文字で入力してください。',code='fullwidth')

    # ひらがなチェック（伸ばし棒も許容）
    def validate_fullwidth_hiragana(value):
        if not (re.match(r'^[ぁ-ゟ|ー|・|!|！|?|？]+$', value) is not None):
            raise forms.ValidationError('ひらがなで入力してください。',code='fullwidth_hiragana')

    # 半角数字チェック
    def validate_halfwidth_num(value):
        if not (re.match(r'^[0-9]+$', value) is not None):
            raise forms.ValidationError('半角数字で入力してください。',code='halfwidth_num')
