from typing import NamedTuple
from typing import List
from admin_app.dto.dto_list import DtoList

class DtoSakuhinTagList(NamedTuple):

    class DtoNoticeTableList(NamedTuple):
        # 更新履歴一覧
        notice_table : DtoList.DtoNoticeTable


    class DtoSakuhinTagMasterList(NamedTuple):
        # 作品タグマスタの取得
        sakuhin_tag_code : str
        sakuhin_tag_category_name : str
        sakuhin_tag_name : str
        update_user : str
        update_time : str

    class DtoSakuhinTagCategoryAll(NamedTuple):
        # プルダウン：カテゴリマスタの取得
         sakuhin_tag_category_code : str
         sakuhin_tag_category_name : str

    class DtoTagMasterListForCSV(NamedTuple):
        # タグマスタ一覧(CSV用)
        sakuhin_tag_code : str
        sakuhin_tag_category_name : str
        sakuhin_tag_name : str
        create_user : str
        create_time : str
        update_user : str
        update_time : str

    notice_table : DtoList.DtoNoticeTable
    sakuhin_tag_category_list : List[DtoSakuhinTagCategoryAll]
