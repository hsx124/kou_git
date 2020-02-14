import re
from django import forms
from admin_app.dto.dto_validation_util import ValidationUtil

class DtoStaffCreateForm(forms.Form):

    staff_code = forms.CharField(
        label='スタッフコード',
        required=True,
        error_messages={'required': ValidationUtil.E0000001.format('スタッフコード')},
    )
    staff_name = forms.CharField(
        label='スタッフ名',
        max_length=100,
        required=True,
        error_messages={'required': ValidationUtil.E0000001.format('スタッフ名'),
                        'max_length': ValidationUtil.E0000002.format('スタッフ名','100')},
    )
    past_sakuhin = forms.CharField(
        label='過去作品',
        required=False,
    )
    remarks = forms.CharField(
        label='備考',
        required=False,
    )
