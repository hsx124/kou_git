from typing import NamedTuple
from admin_app.dto.dto_list import DtoList

class DtoSakuhinTagCategoryList(NamedTuple):

    class DtoNoticeTableList(NamedTuple):
        # 更新履歴一覧
        notice_table : DtoList.DtoNoticeTable

    class DtoSakuhinTagCategoryMasterList(NamedTuple):

        class DtoSakuhinTagCategoryMasterListData(NamedTuple):
            # タグカテゴリマスタの取得
            sakuhin_tag_category_code : str
            sakuhin_tag_category_name : str
            update_user : str
            update_time : str

        class DtoSakuhinTagCategoryMasterListForCSV(NamedTuple):
            # タグカテゴリマスタ一覧(CSV用)
            sakuhin_tag_category_code : str
            sakuhin_tag_category_name : str
            create_user : str
            create_time : str
            update_user : str
            update_time : str