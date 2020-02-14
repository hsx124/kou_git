import re
from django import forms
from admin_app.dto.dto_validation_util import ValidationUtil

class DtoSakuhinTagCreateForm(forms.Form):

    tag_code = forms.CharField(
        label='タグコード',
        max_length=10,
        required=True,
        error_messages={'max_length': ValidationUtil.E0000018.format('タグコード','10')},
    )
    tag_name = forms.CharField(
        label='タグ名',
        max_length=15,
        required=True,
        error_messages={'required': ValidationUtil.E0000001.format('タグ名'),
                        'max_length': ValidationUtil.E0000002.format('タグ名','15')},
    )
    sakuhin_tag_category_code = forms.CharField(
        label='タグカテゴリ名',
        max_length=5,
        required=True,
        error_messages={'required': ValidationUtil.E0000019.format('カテゴリ')},
    )


