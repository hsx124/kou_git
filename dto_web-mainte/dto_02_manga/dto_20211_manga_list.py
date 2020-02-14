from typing import NamedTuple

from admin_app.dto.dto_list import DtoList

class DtoMangaList(NamedTuple):

    class DtoNoticeTableList(NamedTuple):
        """更新履歴一覧"""
        notice_table : DtoList.DtoNoticeTable

    class DtoMangaMasterList(NamedTuple):
        """マンガタイトル基本マスタ一覧"""
        class DtoMangaMasterListData(NamedTuple):
            # マンガタイトルコード
            manga_title_code : str
            # マンガタイトル名
            manga_title_name : str
            # 連載開始年月
            rensai_start_yyyymm : str
            # 掲載媒体
            media_name : str
            # 出版社
            publisher_name : str
            # 更新者
            update_user: str
            # 更新日時
            update_time: str

        """マンガタイトル基本マスタ一覧(CSV用)"""
        class DtoMangaMasterListForCSV(NamedTuple):
            # マンガタイトルコード
            manga_title_code : str
            # マンガタイトル名
            manga_title_name : str
            # 連載開始年月
            rensai_start_yyyymm : str
            # 掲載媒体
            media_name : str
            # 出版社
            publisher_name : str
            # 作成者
            create_user : str
            # 作成日時
            create_time : str
            # 更新者
            update_user: str
            # 更新日時
            update_time: str