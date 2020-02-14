import json
from admin_app.dao.dao_m_heibai import DaoMHeibai
from admin_app.dao.dao_m_manga_title import DaoMMangaTitle
from admin_app.service.service_main import ServiceMain

from admin_app.dao.dao_t_update_history import DaoTUpdateHistory

from admin_app.dto.dto_list import DtoList
from admin_app.dto.dto_02_manga.dto_20242_manga_heibai_create import DtoMangaHeibaiCreateForm
from admin_app.dto.dto_02_manga.dto_20211_manga_list import DtoMangaList

class MangaHeibaiCreateService(ServiceMain):

    # テーブル用DAO
    dao_m_heibai = DaoMHeibai()
    dao_m_manga_title = DaoMMangaTitle()

    # 変更履歴用DAO
    dao_t_update_history = DaoTUpdateHistory()

    '''初期描画'''
    def initialize(self,manga_title_code):
        manga_heibai_create_form = self.unpack(self.mapping(DtoMangaHeibaiCreateForm.DtoMangaHeibaiCreateData, self.dao_m_manga_title.selectMangaTitle(manga_title_code)))

        if manga_heibai_create_form:
            return self.unpack({'value_not_found':False,'form':manga_heibai_create_form[0]})
        else:
            return self.unpack({'value_not_found':True,'form':''})

    '''マンガタイトル名を検索してマンガ情報を取得する。'''
    def getSakuhinByTitleName(self,keyword):
        if len(keyword) == 0:
            dto_manga_list = self.mapping(DtoMangaList.DtoMangaMasterList.DtoMangaMasterListData, self.dao_m_manga_title.selectAll())
        else:
            dto_manga_list = self.mapping(DtoMangaList.DtoMangaMasterList.DtoMangaMasterListData, self.dao_m_manga_title.selectMangaByKeyword(keyword))
        return dto_manga_list