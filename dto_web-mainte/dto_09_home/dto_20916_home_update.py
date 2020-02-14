from typing import NamedTuple

from admin_app.dto.dto_main import DtoMain
from django import forms

from admin_app.dto.dto_validation_util import ValidationUtil
from django.core import validators
from django.core.exceptions import ValidationError

class HomeUpdateForm(forms.Form):
    banner_title = forms.CharField(
        label='タイトル',
        max_length=100,
        required=True,
        error_messages={'required': ValidationUtil.E0000001.format('タイトル'),
                        'max_length': ValidationUtil.E0000002.format('タイトル','100')},
    )
    banner_detail = forms.CharField(
        label='詳細',
        required=True,
        error_messages={'required': ValidationUtil.E0000001.format('詳細')}
    )
    thumbnail_file_name = forms.CharField(
        label='サムネイルファイル名',
        max_length=100,
        required=True,
        error_messages={'required': ValidationUtil.E0000011.format('サムネイル','ファイル'),
                        'max_length': ValidationUtil.E0000005.format('サムネイルファイル名','100')},
    )
    thumbnail = forms.ImageField(
        label='サムネイル',
        required=False,
    )
    banner_url = forms.CharField(
        label='外部リンク',
        required=False,
        validators=[validators.URLValidator(schemes=['http', 'https'])]
    )
    banner_hakusho = forms.CharField(
        label='白書',
        required=False,
    )
    url_checkbox = forms.BooleanField(
        initial = False,
        required=False,
    )

    # 複合項目チェック
    def clean(self):
        cleaned_data = super().clean()

        # 遷移先入力チェック
        if cleaned_data['url_checkbox']:
            if 'banner_url' in cleaned_data and cleaned_data['banner_url'] in validators.EMPTY_VALUES:
                self.add_error('banner_url',ValidationError(ValidationUtil.E0000011.format('遷移先','外部サイト'),code='required'))
        else:
            if cleaned_data['banner_hakusho'] in validators.EMPTY_VALUES:
                self.add_error('banner_hakusho',ValidationError(ValidationUtil.E0000011.format('遷移先','白書'),code='required'))

        return cleaned_data

class DtoHomeupdate(NamedTuple):

    class DtoBanner(NamedTuple):
        '''バナーリンク'''
        position : str
        tumbnail_file_name : str
        title : str
        details :str
        external_site :str
        is_checked :str
        white_paper : str
        white_paper_file_name : str

    class DtoTWhitePaper(NamedTuple):
        '''白書'''
        id : str
        file_name : str
        whitepaper_category :str
        instructions : str
        year : str
        related_ip : str
        update_user : str
        update_date : str

    banner : DtoBanner
    whitepaper : DtoTWhitePaper

