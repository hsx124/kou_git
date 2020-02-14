from django import forms

from admin_app.dto.dto_validation_util import ValidationUtil
import re

class SakuhinCreateForm(forms.Form):

    ip_code = forms.CharField(
        label='IPコード',
        max_length=10,
        required=True,
    )
    ip_name = forms.CharField(
        label='IP名',
        max_length=100,
        required=True,
        error_messages={'required': ValidationUtil.E0000001.format('IP名'),
                        'max_length': ValidationUtil.E0000002.format('IP名','100')},
    )
    ip_kana_name = forms.CharField(
        label='IPかな名',
        max_length=100,
        required=True,
        validators=[ValidationUtil.validate_fullwidth_hiragana],
        error_messages={'required': ValidationUtil.E0000001.format('IPかな名'),
                        'max_length': ValidationUtil.E0000002.format('IPかな名','100'),
                        'fullwidth_hiragana': ValidationUtil.E0000004.format('IPかな名')},
    )
    overview_wiki_title = forms.CharField(
        label='Wikipedia - ページタイトル',
        max_length=100,
        required=False,
        error_messages={'max_length': ValidationUtil.E0000002.format('Wikipedia - ページタイトル','100')},
    )
    overview = forms.CharField(
        label='あらすじ',
        required=False,
    )
    key_visual_file_name = forms.CharField(
        label='キービジュアルファイル名',
        max_length=100,
        required=False,
        error_messages={'max_length': ValidationUtil.E0000005.format('キービジュアルファイル名','100')},
    )
    key_visual = forms.ImageField(
        required=False,
    )
    keyword1 = forms.CharField(
        label='キーワード1',
        required=False,
    )
    keyword2 = forms.CharField(
        label='キーワード2',
        required=False,
    )
    keyword3 = forms.CharField(
        label='キーワード3',
        required=False,
    )
    keyword4 = forms.CharField(
        label='キーワード4',
        required=False,
    )
    keyword5 = forms.CharField(
        label='キーワード5',
        required=False,
    )
    keyword6 = forms.CharField(
        label='キーワード6',
        required=False,
    )
    keyword7 = forms.CharField(
        label='キーワード7',
        required=False,
    )
    keyword8 = forms.CharField(
        label='キーワード8',
        required=False,
    )
    keyword9 = forms.CharField(
        label='キーワード9',
        required=False,
    )
    keyword10 = forms.CharField(
        label='キーワード10',
        required=False,
    )
    keyword11 = forms.CharField(
        label='キーワード11',
        required=False,
    )
    keyword12 = forms.CharField(
        label='キーワード12',
        required=False,
    )
    keyword13 = forms.CharField(
        label='キーワード13',
        required=False,
    )
    keyword14 = forms.CharField(
        label='キーワード14',
        required=False,
    )
    keyword15 = forms.CharField(
        label='キーワード15',
        required=False,
    )
    domestic_window = forms.CharField(
        label='国内窓口',
        max_length=250,
        required=False,
        error_messages={'max_length': ValidationUtil.E0000002.format('国内窓口','250')},
    )
    foreign_window = forms.CharField(
        label='国外窓口',
        max_length=250,
        required=False,
        error_messages={'max_length': ValidationUtil.E0000002.format('国外窓口','250')},
    )
    release_date = forms.DateTimeField(
        label='展開開始年月日',
        required=True,
        widget=forms.DateInput(attrs={"type": "date"}),
        input_formats=['%Y/%m/%d'],
        error_messages={'required': ValidationUtil.E0000001.format('展開開始年月日'),
                        'invalid': ValidationUtil.E0000008},
    )
    valid_start_date = forms.DateTimeField(
        label='IP公開開始',
        required=True,
        widget=forms.DateInput(attrs={"type": "date"}),
        input_formats=['%Y/%m/%d'],
        error_messages={'required': ValidationUtil.E0000001.format('IP公開有効期限（開始）'),
                        'invalid': ValidationUtil.E0000008},
    )
    valid_end_date = forms.DateTimeField(
        label='IP公開終了',
        required=True,
        widget=forms.DateInput(attrs={"type": "date"}),
        input_formats=['%Y/%m/%d'],
        error_messages={'required': ValidationUtil.E0000001.format('IP公開有効期限（終了）'),
                        'invalid': ValidationUtil.E0000008},
    )
    memo = forms.CharField(
        label='メモ',
        max_length=250,
        required=False,
        error_messages={'max_length': ValidationUtil.E0000002.format('メモ','250')},
    )

    # 複合項目チェック
    def clean(self):
        cleaned_data = super().clean()

        # キーワードの文字数チェック
        if (len(cleaned_data['keyword1']) > 30
            or len(cleaned_data['keyword2']) > 30
            or len(cleaned_data['keyword3']) > 30
            or len(cleaned_data['keyword4']) > 30
            or len(cleaned_data['keyword5']) > 30
            or len(cleaned_data['keyword6']) > 30
            or len(cleaned_data['keyword7']) > 30
            or len(cleaned_data['keyword8']) > 30
            or len(cleaned_data['keyword9']) > 30
            or len(cleaned_data['keyword10']) > 30
            or len(cleaned_data['keyword11']) > 30
            or len(cleaned_data['keyword12']) > 30
            or len(cleaned_data['keyword13']) > 30
            or len(cleaned_data['keyword14']) > 30
            or len(cleaned_data['keyword15']) > 30
            ):
            self.add_error('keyword1',ValidationUtil.E0000002.format('キーワード','30'))
        else:
            # キーワードの"/"チェック
            keyword1 = self.cleaned_data.get('keyword1')
            keyword2 = self.cleaned_data.get('keyword2')
            keyword3 = self.cleaned_data.get('keyword3')
            keyword4 = self.cleaned_data.get('keyword4')
            keyword5 = self.cleaned_data.get('keyword5')
            keyword6 = self.cleaned_data.get('keyword6')
            keyword7 = self.cleaned_data.get('keyword7')
            keyword8 = self.cleaned_data.get('keyword8')
            keyword9 = self.cleaned_data.get('keyword9')
            keyword10 = self.cleaned_data.get('keyword10')
            keyword11 = self.cleaned_data.get('keyword11')
            keyword12 = self.cleaned_data.get('keyword12')
            keyword13 = self.cleaned_data.get('keyword13')
            keyword14 = self.cleaned_data.get('keyword14')
            keyword15 = self.cleaned_data.get('keyword15')
        
            if not (re.match('^(?!.*\/).*$', keyword1)
                and re.match('^(?!.*\/).*$', keyword2)
                and re.match('^(?!.*\/).*$', keyword3)
                and re.match('^(?!.*\/).*$', keyword4)
                and re.match('^(?!.*\/).*$', keyword5)
                and re.match('^(?!.*\/).*$', keyword6)
                and re.match('^(?!.*\/).*$', keyword7)
                and re.match('^(?!.*\/).*$', keyword8)
                and re.match('^(?!.*\/).*$', keyword9)
                and re.match('^(?!.*\/).*$', keyword10)
                and re.match('^(?!.*\/).*$', keyword11)
                and re.match('^(?!.*\/).*$', keyword12)
                and re.match('^(?!.*\/).*$', keyword13)
                and re.match('^(?!.*\/).*$', keyword14)
                and re.match('^(?!.*\/).*$', keyword15)):
                self.add_error('keyword1',ValidationUtil.E0000017.format('キーワード'))

        # IP公開開始とIP公開終了の整合性チェック
        if ('valid_start_date' in cleaned_data
            and 'valid_end_date' in cleaned_data
            and cleaned_data['valid_start_date'] > cleaned_data['valid_end_date']):
            self.add_error('valid_start_date',ValidationUtil.E0000009.format('IP公開有効期限（終了）','IP公開有効期限（開始）'))
        return cleaned_data
