import re
from django import forms
from admin_app.dto.dto_validation_util import ValidationUtil

class DtoMediaCreateForm(forms.Form):

    media_code = forms.CharField(
        label='掲載媒体コード',
        max_length=5,
        required=True,
        error_messages={'max_length': ValidationUtil.E0000018.format('掲載媒体コード','5')},
    )
    media_name = forms.CharField(
        label='掲載媒体名',
        max_length=30,
        required=True,
        error_messages={'required': ValidationUtil.E0000001.format('掲載媒体名'),
                        'max_length': ValidationUtil.E0000002.format('掲載媒体名','30')},
    )
    show_flg = forms.CharField(
        label='表示/非表示',
        required=True,
        error_messages={'required': ValidationUtil.E0000001.format('表示/非表示')},
    )
    priority = forms.CharField(
        label='優先順位',
        max_length=4,
        required=True,
        validators=[ValidationUtil.validate_halfwidth_num],
        error_messages={'required': ValidationUtil.E0000001.format('優先順位'),
                    'max_length': ValidationUtil.E0000018.format('優先順位','4'),
                    'halfwidth_num': ValidationUtil.E0000013.format('優先順位')},
    )

