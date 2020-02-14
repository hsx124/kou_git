from ipdds_app.service.service_main import ServiceMain

from ipdds_app.dao.dao_m_core import DaoMCore
from ipdds_app.dao.dao_m_media import DaoMMedia
from ipdds_app.dao.dao_m_imp import DaoMImp
from ipdds_app.dao.dao_m_fact_tag import DaoMFactTag


from ipdds_app.dto.dto_06_similar_search import DtoSimilarSearch

import datetime
from dateutil.relativedelta import relativedelta
from operator import itemgetter
from itertools import groupby

class SimilarSearchService(ServiceMain):

    # m_coreテーブル用DAO
    dao_m_core = DaoMCore()
    # m_mediaテーブル用DAO
    dao_m_media = DaoMMedia()
    # m_impテーブル用DAO
    dao_m_imp = DaoMImp()
    # m_fact_tagテーブル用DAO
    dao_m_fact_tag = DaoMFactTag()

    def bizProcess(self):
        
        '''
        類似検索フォームの要素の情報をDBから取得し、DTOに設定する。
        '''
        # コアマスタの取得
        core_dto = self.mapping(DtoSimilarSearch.DtoCore, self.dao_m_core.selectAll())
        # 掲載媒体マスタの取得
        media_dto = self.mapping(DtoSimilarSearch.DtoMedia, self.dao_m_media.selectAll())
        # 印象マスタの取得
        imp_dto = self.mapping(DtoSimilarSearch.DtoImp, self.dao_m_imp.selectAll())
        imp_dto = [ imp_dto[i:i+2] for i in range(0,len(imp_dto),2) ]
        # 事実タグマスタの取得
        fact_tag_dto = self.mapping(DtoSimilarSearch.DtoFactTag, self.dao_m_fact_tag.selectAll())
        fact_tag_dto = sorted(fact_tag_dto, key=itemgetter(0))
        fact_tag_dto = { key:list(group) for key,group in groupby(fact_tag_dto, key=itemgetter(0)) }
        
        dto_similar_search = DtoSimilarSearch(core_dto,media_dto,imp_dto,fact_tag_dto)
        return self.unpack(dto_similar_search)


