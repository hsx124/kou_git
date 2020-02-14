from typing import NamedTuple

from admin_app.dto.dto_list import DtoList

class DtoIpList(NamedTuple):

    class DtoNoticeTableList(NamedTuple):
        """更新履歴一覧"""
        notice_table : DtoList.DtoNoticeTable

    class DtoIpMasterList(NamedTuple):
        """IPマスタ"""
        class DtoIpMasterListData(NamedTuple):
            ip_code : str
            ip_name : str
            ip_kana_name: str
            ip_control_flg: str
            update_user : str
            update_time : str

        """IPマスタ一覧(CSV用)"""
        class DtoIpListForCSV(NamedTuple):
            ip_code : str
            ip_name : str
            ip_kana_name: str
            ip_control_flg: str
            create_user: str
            create_time: str
            update_user: str
            update_time: str
