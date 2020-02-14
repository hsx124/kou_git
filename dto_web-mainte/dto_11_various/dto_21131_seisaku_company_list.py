from typing import NamedTuple

from admin_app.dto.dto_list import DtoList

class DtoSeisakuCompanyList(NamedTuple):

    class DtoNoticeTableList(NamedTuple):
        """更新履歴一覧"""
        notice_table : DtoList.DtoNoticeTable

    class DtoSeisakuCompanyMasterList(NamedTuple):
        """制作会社マスタ一覧"""
        class DtoSeisakuCompanyMasterListData(NamedTuple):
            # 制作会社コード
            seisaku_company_code : str
            # 制作会社名
            seisaku_company_name : str
            # 更新者
            update_user: str
            # 更新日時
            update_time: str

        """制作会社マスタ一覧(CSV用)"""
        class DtoSeisakuCompanyMasterListForCSV(NamedTuple):
            # 制作会社コード
            seisaku_company_code : str
            # 制作会社名
            seisaku_company_name : str
            # 作成者
            create_user : str
            # 作成日時
            create_time : str
            # 更新者
            update_user: str
            # 更新日時
            update_time: str
