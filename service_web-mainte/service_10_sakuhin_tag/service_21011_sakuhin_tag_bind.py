from admin_app.service.service_main import ServiceMain
from admin_app.service.service_list import ServiceList

from admin_app.dao.dao_m_core import DaoMCore
from admin_app.dao.dao_m_sakuhin_tag import DaoMSakuhinTag
from admin_app.dao.dao_m_sakuhin_tag_category import DaoMSakuhinTagCategory

from admin_app.dao.dao_m_manga_title import DaoMMangaTitle
from admin_app.dao.dao_m_novel_title import DaoMNovelTitle
from admin_app.dao.dao_m_anime_title import DaoMAnimeTitle
from admin_app.dao.dao_m_app_title import DaoMAppTitle
from admin_app.dao.dao_m_game_title import DaoMGameTitle

from admin_app.dto.dto_10_sakuhin_tag.dto_21011_sakuhin_tag_bind import DtoSakuhinTagBind

class SakuhinTagBindService(ServiceList):

    # コアマスタテーブル用DAO
    dao_m_core = DaoMCore()
    # 作品タグマスタテーブル用DAO
    dao_m_sakuhin_tag = DaoMSakuhinTag()
    # 作品タグカテゴリマスタテーブル用DAO
    dao_m_sakuhin_tag_category = DaoMSakuhinTagCategory()
    # マンガタイトルマスタテーブル用DAO
    dao_m_manga_title = DaoMMangaTitle()
    # 小説タイトルマスタテーブル用DAO
    dao_m_novel_title = DaoMNovelTitle()
    # アニメタイトルマスタテーブル用DAO
    dao_m_anime_title = DaoMAnimeTitle()
    # アプリタイトルマスタテーブル用DAO
    dao_m_app_title = DaoMAppTitle()
    # ゲームタイトルマスタテーブル用DAO
    dao_m_game_title = DaoMGameTitle()

    '''初期描画'''
    def initialize(self, table_name):

        # 更新履歴
        notice_table = self.getnoticetable(table_name)
        dto_core = self.mapping(DtoSakuhinTagBind.CoreAll, self.dao_m_core.selectAll())
        dto_sakuhin_tag_category = self.mapping(DtoSakuhinTagBind.SakuhinTagCategoryAll, self.dao_m_sakuhin_tag_category.selectSakuhinTagCategoryAll())
        # 領域用DTOを画面DTOに詰める
        dto_sakuhin_tag_bind= DtoSakuhinTagBind(notice_table, dto_core, dto_sakuhin_tag_category)
        return self.unpack(dto_sakuhin_tag_bind)
