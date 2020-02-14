from django import forms
from typing import NamedTuple
from dateutil.parser import parse

from admin_app.dto.dto_list import DtoList
from admin_app.dto.dto_validation_util import ValidationUtil

class DtoMangaHeibaiCreateForm(forms.Form):

    ''' 新規画面連携用'''
    class DtoMangaHeibaiCreateData(NamedTuple):
        manga_title_code: str
        manga_title_name: str