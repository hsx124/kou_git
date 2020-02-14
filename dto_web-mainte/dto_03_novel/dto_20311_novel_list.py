from typing import NamedTuple

from admin_app.dto.dto_list import DtoList

class DtoNovelList(NamedTuple):

    class DtoNoticeTableList(NamedTuple):
        """更新履歴一覧"""
        notice_table : DtoList.DtoNoticeTable

    class DtoNovelMasterList(NamedTuple):
        """小説タイトル基本マスタ一覧"""
        class DtoNovelMasterListData(NamedTuple):
            # 小説タイトルコード
            novel_title_code : str
            # 小説タイトル名
            novel_title_name : str
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

        """小説タイトル基本マスタ一覧(CSV用)"""
        class DtoNovelMasterListForCSV(NamedTuple):
            # 小説タイトルコード
            novel_title_code : str
            # 小説タイトル名
            novel_title_name : str
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