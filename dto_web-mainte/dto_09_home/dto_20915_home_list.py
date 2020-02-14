from typing import NamedTuple

from admin_app.dto.dto_list import DtoList

from django import forms

from admin_app.dto.dto_validation_util import ValidationUtil
from django.core import validators
class NewsCreateForm(forms.Form):

    news_subject = forms.CharField(
        label='タイトル',
        max_length=50,
        required=True,
        error_messages={'required': ValidationUtil.E0000001.format('タイトル'),
                        'max_length': ValidationUtil.E0000002.format('タイトル','50')},
    )
    news_headline  = forms.CharField(
        label='概要',
        max_length=50,
        required=True,
        error_messages={'required': ValidationUtil.E0000001.format('概要'),
                        'max_length': ValidationUtil.E0000002.format('概要','50')},
    )
    news_info_detail = forms.CharField(
        label='詳細',
        required=True,
        error_messages={'required': ValidationUtil.E0000001.format('詳細')},
    )
    news_link_url = forms.CharField(
        label='遷移先',
        required=True,
        validators=[validators.URLValidator(schemes=['http', 'https'])],
        error_messages={'required': ValidationUtil.E0000001.format('遷移先'),
                        'invalid': ValidationUtil.E0000010},
    )

class DtoHomelist(NamedTuple):
    

    class DtoBanner(NamedTuple):
        '''バナーリンク'''
        is_invalid : str
        tumbnail_file_name : str
        title : str
        details : str
        position : str

    class DtoNews(NamedTuple):
        '''お知らせ'''
        # ID
        id : str
        # タイトル
        subject : str
        # 概要
        headline : str
        # 詳細
        article : str
        # 遷移先
        link_url : str

    notice_table : DtoList.DtoNoticeTable
    banner : DtoBanner
    news : DtoNews