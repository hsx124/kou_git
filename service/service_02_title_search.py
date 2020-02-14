from ipdds_app.service.service_main import ServiceMain

from ipdds_app.dao.dao_m_ip import DaoMIp
from ipdds_app.dto.dto_02_title_search import DtoSearchTitle

from operator import itemgetter
from itertools import groupby


class SearchTitleService(ServiceMain):

    # m_ipテーブル用DAO
    dao_m_ip = DaoMIp()


    def bizProcess(self):
        
        # 各画面領域のデータを取得し領域用DTOに詰める
        search_title_dto = self.mapping(DtoSearchTitle.DtoTitleName, self.dao_m_ip.selectTitleNameAll())
        search_title_dto = sorted(search_title_dto,key=itemgetter(0))
        search_title_dto = {key:list(group) for key,group in groupby(search_title_dto, key=itemgetter(0))}

         # 領域用DTOを画面DTOに詰める
        dto_title = DtoSearchTitle(search_title_dto)

        return self.unpack(dto_title)