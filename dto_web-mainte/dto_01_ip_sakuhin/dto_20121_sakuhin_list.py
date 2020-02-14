from typing import NamedTuple

from admin_app.dto.dto_list import DtoList

class DtoSakuhinList(NamedTuple):

    '''作品マスタ一覧'''
    class DtosakuhinMasterList(NamedTuple):
        sakuhin_code : str
        sakuhin_name : str
        overview: str
        keyvisual_file_name: str
        keyword: str
        release_date: str
        update_user : str
        update_date : str

    '''作品マスタ一覧(CSV用)'''
    class DtosakuhinMasterListForCSV(NamedTuple):
        sakuhin_code:str
        sakuhin_name:str
        sakuhin_kana_name:str
        key_visual_file_name:str
        release_yyyymm:str
        valid_start_yyyymmdd:str
        valid_end_yyyymmdd:str
        foreign_window:str
        domestic_window:str
        memo:str
        overview:str
        keyword:str
        invalid_flg:str
        create_user:str
        create_time:str
        update_user:str
        update_time:str

    notice_table : DtoList.DtoNoticeTable
    sakuhin_master_list : DtosakuhinMasterList
    sakuhin_master_list_for_CSV: DtosakuhinMasterListForCSV
