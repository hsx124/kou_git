from typing import NamedTuple
from django import forms

class DtoMangaUpdate(NamedTuple):

    '''マンガタイトル基本マスタ 編集画面連携用'''
    class DtoMangaUpdateData(NamedTuple):
        manga_title_code: str
        manga_title_name: str
        rensai_start_yyyymm : str
        published_cnt : int
        rensai_end_flg : str
        award_history : str
        media_code : str
        media_name : str
        publisher_code : str
        publisher_name : str
        staff_map_code : str
        staff_role_code1 : str
        staff_role_name1 : str
        staff_role_code2 : str
        staff_role_name2 : str
        staff_role_code3 : str
        staff_role_name3 : str
        staff_role_code4 : str
        staff_role_name4 : str
        staff_role_code5 : str
        staff_role_name5 : str
        staff_code1 : str
        staff_name1 : str
        staff_code2 : str
        staff_name2 : str
        staff_code3 : str
        staff_name3 : str
        staff_code4 : str
        staff_name4 : str
        staff_code5 : str
        staff_name5 : str