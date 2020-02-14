from typing import NamedTuple
from typing import List
from admin_app.dto.dto_list import DtoList

class DtoSakuhinTagBind(NamedTuple):

    class DtoSakuhinTagMasterList(NamedTuple):
        # 作品タグマスタの取得
        sakuhin_tag_code : str
        sakuhin_tag_category_name : str
        sakuhin_tag_name : str
        update_user : str
        update_time : str

    class CoreAll(NamedTuple):
        # プルダウン：カテゴリマスタの取得
         core_code : str
         core_name : str

    class SakuhinTagCategoryAll(NamedTuple):
        # プルダウン：カテゴリマスタの取得
         sakuhin_tag_category_code : str
         sakuhin_tag_category_name : str


    notice_table : DtoList.DtoNoticeTable
    core : List[CoreAll]
    sakuhin_tag_category_list : List[SakuhinTagCategoryAll]
