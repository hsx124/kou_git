from typing import NamedTuple

from admin_app.dto.dto_list import DtoList

class DtoMangaHeibaiList(NamedTuple):

    class DtoNoticeTableList(NamedTuple):
        """更新履歴一覧"""
        notice_table : DtoList.DtoNoticeTable

    class DtoMangaHeibaiMasterList(NamedTuple):
        """併売マスタ一覧"""
        class DtoMangaHeibaiMasterListData(NamedTuple):
            heibai_code : str
            manga_title_code : str
            manga_title_name : str
            heibai_name_1 : str
            heibai_name_2 : str
            heibai_name_3 : str
            heibai_name_4 : str
            heibai_name_5 : str
            update_user : str
            update_time : str

        """併売マスタ一覧(CSV用)"""
        class DtoMangaHeibaiMasterListForCSV(NamedTuple):
            manga_title_code : str
            manga_title_name : str
            heibai_code : str
            heibai_name_1 : str
            heibai_1 : str
            heibai_name_2 : str
            heibai_2 : str
            heibai_name_3 : str
            heibai_3 : str
            heibai_name_4 : str
            heibai_4 : str
            heibai_name_5 : str
            heibai_5 : str
            create_user : str
            create_time : str
            update_user : str
            update_time : str