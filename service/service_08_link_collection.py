from ipdds_app.service.service_main import ServiceMain

from ipdds_app.dao.dao_m_white_paper import DaoMWhitePaper
from ipdds_app.dto.dto_08_link_collection import DtoLinkCollection

from operator import attrgetter
from operator import itemgetter
from itertools import groupby

import pprint


class LinkCollectionService(ServiceMain):

    # m_white_paperテーブル用DAO
    dao_m_white_paper = DaoMWhitePaper()


    def bizProcess(self):
        
        # 白書テーブルより全件取得
        link_dto = self.mapping(DtoLinkCollection.DtoLink, self.dao_m_white_paper.selectAll())
        # 後続のグルーピング用に年度、カテゴリ順でソート
        link_dto = sorted(link_dto,key=attrgetter('year','whitepaper_category'),reverse=True)
        # 年度毎にグルーピング
        link_dto = {key:list(group) for key,group in groupby(link_dto, key=attrgetter('year'))}
        # 年度内はカテゴリ毎にグルーピング
        for k, v in link_dto.items():
            link_dto[k] =  {key:list(group) for key,group in groupby(v, key=attrgetter('whitepaper_category'))}
        
         # 領域用DTOを画面DTOに詰める
        dto_link_collection = DtoLinkCollection(link_dto)

        return self.unpack(dto_link_collection)