from typing import NamedTuple
from admin_app.dto.dto_list import DtoList

class DtoStaffRoleList(NamedTuple):

    class DtoNoticeTableList(NamedTuple):
        # 更新履歴一覧
        notice_table : DtoList.DtoNoticeTable

    class DtoStaffRoleMasterList(NamedTuple):

        class DtoStaffRoleMasterListData(NamedTuple):
            # スタッフ役割マスタの取得
            staff_role_code : str
            staff_role_name : str
            update_user : str
            update_time : str

        class DtoStaffRoleMasterListForCSV(NamedTuple):
            # スタッフ役割マスタ一覧(CSV用)
            staff_role_code : str
            staff_role_name : str
            create_user : str
            create_time : str
            update_user : str
            update_time : str