import re
from django import forms
from admin_app.dto.dto_validation_util import ValidationUtil

class DtoPublisherCreateForm(forms.Form):

    publisher_code = forms.CharField(
        label='出版社コード',
        max_length=5,
        required=True,
        error_messages={'max_length': ValidationUtil.E0000018.format('出版社コード','5')},
    )
    publisher_name = forms.CharField(
        label='出版社名',
        max_length=100,
        required=True,
        error_messages={'required': ValidationUtil.E0000001.format('出版社名'),
                        'max_length': ValidationUtil.E0000002.format('出版社名','100')},
    )
