from typing import NamedTuple
from django import forms
from admin_app.dto.dto_01_ip_sakuhin.dto_20122_sakuhin_create import SakuhinCreateForm
from admin_app.dto.dto_validation_util import ValidationUtil

class DtoSakuhinUpdate(NamedTuple):

    '''IPマスタ 編集画面連携用'''
    class DtoSakuhinUpdateDate(NamedTuple):
        sakuhin_code: str
        sakuhin_name: str
        sakuhin_kana_name: str
        key_visual_file_name: str
        release_yyyymm: str
        valid_start_yyyymmdd: str
        valid_end_yyyymmdd: str
        domestic_window: str
        foreign_window: str
        memo: str
        overview: str
        keyword: str

    sakuhin_update_form : DtoSakuhinUpdateDate


