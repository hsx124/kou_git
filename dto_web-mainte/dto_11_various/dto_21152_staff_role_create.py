import re
from django import forms
from admin_app.dto.dto_validation_util import ValidationUtil

class DtoStaffRoleCreateForm(forms.Form):

    staff_role_code = forms.CharField(
        label='スタッフ役割コード',
        required=True,
        error_messages={'required': ValidationUtil.E0000001.format('スタッフ役割コード')},
    )
    staff_role_name = forms.CharField(
        label='スタッフ役割名',
        max_length=100,
        required=True,
        error_messages={'required': ValidationUtil.E0000001.format('スタッフ役割名'),
                        'max_length': ValidationUtil.E0000002.format('スタッフ役割名','100')},
    )


