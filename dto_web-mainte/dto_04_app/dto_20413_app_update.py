from typing import NamedTuple
from django import forms
from admin_app.dto.dto_04_app.dto_20412_app_create import AppCreateForm
from admin_app.dto.dto_validation_util import ValidationUtil

class DtoAppUpdate(NamedTuple):

    class DtoAppUpdateData(NamedTuple):
        '''
        アプリマスタ 編集画面連携用
        '''
        ip_code: str
        ip_name: str
        app_name: str
        app_id_ios: str
        app_id_android: str
        distributor_name : str
        service_start_date: str
        service_end_date: str

    app_update_form : DtoAppUpdateData