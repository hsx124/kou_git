from typing import NamedTuple
from django import forms
from typing import List

from admin_app.dto.dto_11_various.dto_21152_staff_role_create import DtoStaffRoleCreateForm
from admin_app.dto.dto_validation_util import ValidationUtil

class DtoStaffRoleUpdate(NamedTuple):

    '''スタッフ役割マスタ 編集画面連携用'''
    class DtoStaffRoleUpdateData(NamedTuple):
        # スタッフ役割コード
        staff_role_code: str
        # スタッフ役割名
        staff_role_name: str