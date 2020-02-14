from typing import NamedTuple
from django import forms
from typing import List

from admin_app.dto.dto_11_various.dto_21142_staff_create import DtoStaffCreateForm
from admin_app.dto.dto_validation_util import ValidationUtil

class DtoStaffUpdate(NamedTuple):

    '''スタッフマスタ 編集画面連携用'''
    class DtoStaffUpdateData(NamedTuple):
        # スタッフコード
        staff_code: str
        # スタッフ名
        staff_name: str
        # 過去作品
        past_sakuhin : str
        # 備考
        remarks : str