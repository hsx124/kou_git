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
from admin_app.dao.dao_m_sakuhin_tag_bind import DaoMTagBind
from admin_app.dao.dao_t_update_history import DaoTUpdateHistory

from admin_app.dto.dto_10_sakuhin_tag.dto_21011_sakuhin_tag_bind import DtoSakuhinTagBind

class SakuhinTagBindService(ServiceList):

    # コアマスタテーブル用DAO
    dao_m_core = DaoMCore()
    # 作品タグマスタテーブル用DAO
    dao_m_sakuhin_tag = DaoMSakuhinTag()
    # 作品タグカテゴリマスタテーブル用DAO
    dao_m_sakuhin_tag_category = DaoMSakuhinTagCategory()
    dao_m_sakuhin_tag_bind = DaoMTagBind()
    dao_t_update_history = DaoTUpdateHistory()

    '''初期描画'''
    def initialize(self, table_name):

        # 更新履歴
        notice_table = self.getnoticetable(table_name)
        dto_core = self.mapping(DtoSakuhinTagBind.CoreAll, self.dao_m_core.selectCoreList())
        dto_sakuhin_tag_category = self.mapping(DtoSakuhinTagBind.SakuhinTagCategoryAll, self.dao_m_sakuhin_tag_category.selectSakuhinTagCategoryAll())
        # 領域用DTOを画面DTOに詰める
        dto_sakuhin_tag_bind= DtoSakuhinTagBind(notice_table, dto_core, dto_sakuhin_tag_category)
        return self.unpack(dto_sakuhin_tag_bind)

    def getTitleByName(self, title_name, category_list):
        '''
        @param  title_name 検索タイトル
                category_list 検索カテゴリ（マンガ、小説、アニメ）
        '''
        param = {'title_name' : '%' + title_name + '%'}

        manga_list = []
        novel_list = []
        anime_list = []
        
        for category in category_list:
            if category == 'manga':
                # マンガタイトルデータ取得
                manga_list = self.dao_m_sakuhin_tag_bind.selectMangaTagByTitleName(param)
            if category == 'novel':
                # 小説タイトルデータ取得
                novel_list = self.dao_m_sakuhin_tag_bind.selectNovelTagByTitleName(param)
            if category == 'anime':
                # アニメタイトルデータ取得
                anime_list = self.dao_m_sakuhin_tag_bind.selectAnimeTagByTitleName(param)

        # タイトル一覧生成
        title_list = tuple(manga_list) + tuple(novel_list) + tuple(anime_list)
        dto_title_list = self.mapping(DtoSakuhinTagBind.TitleSearchModal, title_list)
        return self.unpack(dto_title_list)
    def getTagNameByCode(self,tag_code_list):
        
        tag_code_list = tuple(tag_code_list.values())
        param = {
            'tag_code_list':tag_code_list
        }
        dto_tag_name_list = self.dao_m_sakuhin_tag_bind.getTagNameByCode(param)
        
        return self.unpack(dto_tag_name_list)
    
    def createInsertOrUpdateData(self,param,full_name):
        tag_map_code = param['tag_map_code']
        param_list ={
            'tag_map_code' :param['tag_map_code'],          
            'title_category_code':param['title_category_code'],
            'title_code':param['title_code'],
            'core_code1':param['core_code1'],
            'core_code2':param['core_code2'],
            'tag_1':param['sakuhin_tagArea1']['tag-1'],
            'tag_2':param['sakuhin_tagArea1']['tag-2'],
            'tag_3':param['sakuhin_tagArea1']['tag-3'],
            'tag_4':param['sakuhin_tagArea1']['tag-4'],
            'tag_5':param['sakuhin_tagArea1']['tag-5'],
            'tag_6':param['sakuhin_tagArea2']['tag-6'],
            'tag_7':param['sakuhin_tagArea2']['tag-7'],
            'tag_8':param['sakuhin_tagArea2']['tag-8'],
            'tag_9':param['sakuhin_tagArea2']['tag-9'],
            'tag_10':param['sakuhin_tagArea2']['tag-10'],
            'tag_11':param['sakuhin_tagArea3']['tag-11'],
            'tag_12':param['sakuhin_tagArea3']['tag-12'],
            'tag_13':param['sakuhin_tagArea3']['tag-13'],
            'tag_14':param['sakuhin_tagArea3']['tag-14'],
            'tag_15':param['sakuhin_tagArea3']['tag-15'],
            'tag_16':param['sakuhin_tagArea3']['tag-16'],
            'tag_17':param['sakuhin_tagArea3']['tag-17'],
            'tag_18':param['sakuhin_tagArea3']['tag-18'],
            'tag_19':param['sakuhin_tagArea3']['tag-19'],
            'tag_20':param['sakuhin_tagArea3']['tag-20'],
            'full_name' : full_name
        }

        if tag_map_code == '' or tag_map_code == 'null':
            # m_sakuhin_tap_mapに存在するtag_map_codeの最大値を取得
            new_code = self.dao_m_sakuhin_tag_bind.selectMaxTagMapCode()
            # 最大値+1を0埋めする（新規tag_map_code）
            max_code = str(int(new_code[2:])+1).zfill(10)
            param_list['tag_map_code'] = max_code
            self.dao_m_sakuhin_tag_bind.insert(param_list)

            # タイトルマスタのタグマップコードを更新
            self.dao_m_sakuhin_tag_bind.updateTagCodeByTitleCode(param_list)
            # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
            entity = ('m_sakuhin_tag_map','追加',param['title_name'],'',full_name)
            self.dao_t_update_history.insert(entity)
            return 'create'

        else:
            entity = ('m_sakuhin_tag_map','編集',param['title_name'],'',full_name)
            self.dao_t_update_history.insert(entity)
            self.dao_m_sakuhin_tag_bind.update(param_list)
            return 'update'

    def getSakuhinTag(self,tag_name):
        dto_tag = self.mapping(DtoSakuhinTagBind.SakuhinTagList,self.dao_m_sakuhin_tag_bind.selectSakuhinTagByName(tag_name))
        return self.unpack(dto_tag)