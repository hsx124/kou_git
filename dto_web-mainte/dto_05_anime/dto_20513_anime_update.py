from typing import NamedTuple
from admin_app.dto.dto_validation_util import ValidationUtil

class DtoAnimeUpdate(NamedTuple):

    class DtoAnimeUpdateData(NamedTuple):
        '''
        アプリマスタ 編集画面連携用
        '''
        ip_code: str
        ip_name: str
        tv_program_name: str
        broadcaster: str
        period: str

    anime_update_form : DtoAnimeUpdateData