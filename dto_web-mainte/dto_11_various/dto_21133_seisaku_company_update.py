from typing import NamedTuple
from django import forms
from typing import List

from admin_app.dto.dto_11_various.dto_21132_seisaku_company_create import DtoSeisakuCompanyCreateForm
from admin_app.dto.dto_validation_util import ValidationUtil

class DtoSeisakuCompanyUpdate(NamedTuple):

    '''制作会社マスタ 編集画面連携用'''
    class DtoSeisakuCompanyUpdateData(NamedTuple):
        # 制作会社コード
        seisaku_company_code: str
        # 制作会社名
        seisaku_company_name: str