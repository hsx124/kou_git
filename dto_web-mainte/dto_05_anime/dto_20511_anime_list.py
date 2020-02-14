from typing import NamedTuple

from admin_app.dto.dto_list import DtoList

class DtoAnimeList(NamedTuple):

    class DtoAnimeMasterList(NamedTuple):
        '''
        アニメマスタ一覧表示用
        '''
        ip_code : str
        ip_name : str
        tv_program_name : str
        broadcaster : str
        period : str
        update_user : str
        update_date : str

    notice_table : DtoList.DtoNoticeTable
    anime_master_list : DtoAnimeMasterList