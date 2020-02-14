import re
from django import forms
from admin_app.dto.dto_validation_util import ValidationUtil

class DtoSakuhinTagCategoryCreateForm(forms.Form):

    sakuhin_tag_category_code = forms.CharField(
        label='タグカテゴリコード',
        required=True,
        error_messages={'required': ValidationUtil.E0000001.format('タグカテゴリコード')},
    )
    sakuhin_tag_category_name = forms.CharField(
        label='タグカテゴリ名',
        max_length=15,
        required=True,
        error_messages={'required': ValidationUtil.E0000001.format('タグカテゴリ名'),
                        'max_length': ValidationUtil.E0000002.format('タグカテゴリ名','30')},
    )


