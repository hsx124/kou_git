from typing import NamedTuple

from admin_app.dto.dto_list import DtoList

class DtoPublisherList(NamedTuple):

    class DtoNoticeTableList(NamedTuple):
        """更新履歴一覧"""
        notice_table : DtoList.DtoNoticeTable

    class DtoPublisherMasterList(NamedTuple):
        """出版社マスタ一覧"""
        class DtoPublisherMasterListData(NamedTuple):
            # 出版社コード
            publisher_code : str
            # 出版社名
            publisher_name : str
            # 更新者
            update_user: str
            # 更新日時
            update_time: str

        """出版社マスタ一覧(CSV用)"""
        class DtoPublisherMasterListForCSV(NamedTuple):
            # 出版社コード
            publisher_code : str
            # 出版社名
            publisher_name : str
            # 作成者
            create_user : str
            # 作成日時
            create_time : str
            # 更新者
            update_user: str
            # 更新日時
            update_time: str
