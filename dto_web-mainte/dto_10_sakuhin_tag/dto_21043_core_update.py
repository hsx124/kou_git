from typing import NamedTuple
from django import forms
from typing import List

from admin_app.dto.dto_10_sakuhin_tag.dto_21042_core_create import DtoCoreCreateForm
from admin_app.dto.dto_validation_util import ValidationUtil

class DtoCoreUpdate(NamedTuple):

    '''コアマスタ 編集画面連携用'''
    class DtoCoreUpdateData(NamedTuple):
        # コアコード
        core_code: str
        # コア名
        core_name: str