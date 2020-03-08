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

    class TitleSearchModal(NamedTuple):
        # タグ紐づけ編集タイトル検索
        # タイトルコード
        title_code : str
        # タイトル名
        title_name : str
        # タイトルカテゴリ名
        title_category_name : str
        # タイトルカテゴリコード
        title_category_code : str
        # # プラットフォーム名
        # platform_name : str
        # # 発売日
        # result_yyyymmdd : str
        # # 販売社
        # hanbai_company_name : str
        # 更新者
        update_user: str
        # 更新日時
        update_time: str
        # core_code1 : str
        # core_code2 : str
        tag_code1 : str
        tag_code2 : str
        tag_code3 : str
        tag_code4 : str
        tag_code5 : str
        tag_code6 : str
        tag_code7 : str
        tag_code8 : str
        tag_code9 : str
        tag_code10 : str
        tag_code11 : str
        tag_code12 : str
        tag_code13 : str
        tag_code14 : str
        tag_code15 : str
        tag_code16 : str
        tag_code17 : str
        tag_code18 : str
        tag_code19 : str
        tag_code20 : str
        tag_map_code : str
        # # 作品紐付けID
        # sakuhin_map_id : str

    notice_table : DtoList.DtoNoticeTable
    core : List[CoreAll]
    sakuhin_tag_category_list : List[SakuhinTagCategoryAll]
