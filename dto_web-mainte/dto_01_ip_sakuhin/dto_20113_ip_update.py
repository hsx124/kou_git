from typing import NamedTuple
from django import forms
from typing import List

from admin_app.dto.dto_01_ip_sakuhin.dto_20112_ip_create import DtoIpCreateForm
from admin_app.dto.dto_validation_util import ValidationUtil

class DtoIpUpdate(NamedTuple):

    '''IPマスタ 編集画面連携用'''
    class DtoIpUpdateData(NamedTuple):
        # IPコード
        ip_code: str
        # IP名
        ip_name: str
        # IPかな名
        ip_kana_name: str
        # IP管理フラグ
        ip_control_flg: str