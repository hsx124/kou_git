from django import forms
from admin_app.dto.dto_validation_util import ValidationUtil

class AnimeCreateForm(forms.Form):
    ip_code = forms.CharField(
        label='IPコード',
        max_length=10,
        required=True,
        error_messages={'required': ValidationUtil.E0000001.format('IPコード'),
                        'max_length': ValidationUtil.E0000002.format('IPコード','10')}
    )

    ip_name = forms.CharField(
        label='IP名',
        max_length=100,
        required=True,
        error_messages={'required': ValidationUtil.E0000001.format('IP名'),
                    'max_length': ValidationUtil.E0000002.format('IP名','100')}
    )
    tv_program_name = forms.CharField(
        label='Wikipedia - アニメタイトル',
        max_length=100,
        required=True,
        error_messages={'required': ValidationUtil.E0000001.format('Wikipedia - アニメタイトル'),
                        'max_length': ValidationUtil.E0000002.format('Wikipedia - アニメタイトル','100')}
    )
    period = forms.CharField(
        label='放送期間',
        required=False,
    )
    broadcaster = forms.CharField(
        label='放送局',
        max_length=100,
        required=False,
        error_messages={'max_length': ValidationUtil.E0000002.format('放送局','100')}
    )