from typing import NamedTuple
from django import forms
from typing import List

from admin_app.dto.dto_11_various.dto_21122_publisher_create import DtoPublisherCreateForm
from admin_app.dto.dto_validation_util import ValidationUtil

class DtoPublisherUpdate(NamedTuple):

    '''出版社マスタ 編集画面連携用'''
    class DtoPublisherUpdateData(NamedTuple):
        # 出版社コード
        publisher_code: str
        # 出版社名
        publisher_name: str