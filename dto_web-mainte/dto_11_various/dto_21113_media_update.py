from typing import NamedTuple
from django import forms
from typing import List

from admin_app.dto.dto_11_various.dto_21112_media_create import DtoMediaCreateForm
from admin_app.dto.dto_validation_util import ValidationUtil

class DtoMediaUpdate(NamedTuple):

    '''掲載媒体マスタ 編集画面連携用'''
    class DtoMediaUpdateData(NamedTuple):
        # 掲載媒体コード
        media_code: str
        # 掲載媒体名
        media_name: str
        # 表示フラグ
        show_flg: str
        # 優先順位
        priority: str