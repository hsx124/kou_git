from typing import NamedTuple
from admin_app.dto.dto_list import DtoList

class DtoStaffList(NamedTuple):

    class DtoNoticeTableList(NamedTuple):
        # 更新履歴一覧
        notice_table : DtoList.DtoNoticeTable

    class DtoStaffMasterList(NamedTuple):

        class DtoStaffMasterListData(NamedTuple):
            # スタッフマスタの取得
            staff_code : str
            staff_name : str
            past_sakuhin : str
            remarks : str
            update_user : str
            update_time : str

        class DtoStaffMasterListForCSV(NamedTuple):
            # スタッフマスタ一覧(CSV用)
            staff_code : str
            staff_name : str
            past_sakuhin : str
            remarks : str
            create_user : str
            create_time : str
            update_user : str
            update_time : str