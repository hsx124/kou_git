from typing import NamedTuple
from django import forms
from typing import List

from admin_app.dto.dto_10_sakuhin_tag.dto_21032_sakuhin_tag_category_create import DtoSakuhinTagCategoryCreateForm
from admin_app.dto.dto_validation_util import ValidationUtil

class DtoSakuhinTagCategoryUpdate(NamedTuple):

    '''タグカテゴリマスタ 編集画面連携用'''
    class DtoSakuhinTagCategoryUpdateData(NamedTuple):
        # タグカテゴリコード
        sakuhin_tag_category_code: str
        # タグカテゴリ名
        sakuhin_tag_category_name: str