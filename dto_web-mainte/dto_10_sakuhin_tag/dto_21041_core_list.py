from typing import NamedTuple
from admin_app.dto.dto_list import DtoList

class DtoCoreList(NamedTuple):

    class DtoNoticeTableList(NamedTuple):
        # 更新履歴一覧
        notice_table : DtoList.DtoNoticeTable

    class DtoCoreMasterList(NamedTuple):

        class DtoCoreMasterListData(NamedTuple):
            # コアマスタの取得
            core_code : str
            core_name : str
            update_user : str
            update_time : str

        class DtoCoreMasterListForCSV(NamedTuple):
            # コアマスタ一覧(CSV用)
            core_code : str
            core_name : str
            create_user : str
            create_time : str
            update_user : str
            update_time : str