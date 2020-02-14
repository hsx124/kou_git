import re
from django import forms
from admin_app.dto.dto_validation_util import ValidationUtil

class DtoSeisakuCompanyCreateForm(forms.Form):

    seisaku_company_code = forms.CharField(
        label='制作会社コード',
        max_length=5,
        required=True,
        error_messages={'max_length': ValidationUtil.E0000018.format('制作会社コード','5')},
    )
    seisaku_company_name = forms.CharField(
        label='制作会社名',
        max_length=100,
        required=True,
        error_messages={'required': ValidationUtil.E0000001.format('制作会社名'),
                        'max_length': ValidationUtil.E0000002.format('制作会社名','100')},
    )
