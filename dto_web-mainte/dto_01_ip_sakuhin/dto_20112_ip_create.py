import re
from django import forms
from admin_app.dto.dto_validation_util import ValidationUtil

class DtoIpCreateForm(forms.Form):

    ip_code = forms.CharField(
        label='IPコード',
        max_length=10,
        required=True,
        error_messages={'max_length': ValidationUtil.E0000018.format('IPコード','10')},
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
    ip_control_flg = forms.CharField(
        label='IP管理フラグ',
        required=True,
        error_messages={'required': ValidationUtil.E0000010},
    )

    # valueの値チェック
    def clean(self):
        cleaned_data = super().clean()

        # trueとfalse以外の時エラーメッセージ
        if 'ip_control_flg' in cleaned_data:
            if (cleaned_data['ip_control_flg'] != 'true' 
                and cleaned_data['ip_control_flg'] != 'false'):
                self.add_error('ip_control_flg',ValidationUtil.E0000010)
