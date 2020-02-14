from typing import NamedTuple
from django import forms
from typing import List

from admin_app.dto.dto_10_sakuhin_tag.dto_21022_sakuhin_tag_create import DtoSakuhinTagCreateForm
from admin_app.dto.dto_validation_util import ValidationUtil

class DtoSakuhinTagUpdate(NamedTuple):

    '''タグマスタ 編集画面連携用'''
    class DtoSakuhinTagUpdateData(NamedTuple):
        # タグコード
        tag_code: str
        # タグ名
        tag_name: str
        # タグカテゴリ名
        sakuhin_tag_category_code: str