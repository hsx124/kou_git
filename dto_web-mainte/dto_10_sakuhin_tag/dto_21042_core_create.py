import re
from django import forms
from admin_app.dto.dto_validation_util import ValidationUtil

class DtoCoreCreateForm(forms.Form):

    core_code = forms.CharField(
        label='コアコード',
        required=True,
        error_messages={'required': ValidationUtil.E0000001.format('コアコード')},
    )
    core_name = forms.CharField(
        label='コア名',
        max_length=15,
        required=True,
        error_messages={'required': ValidationUtil.E0000001.format('コア名'),
                        'max_length': ValidationUtil.E0000002.format('コア名','15')},
    )


