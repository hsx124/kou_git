from ipdds_app.service.service_main import ServiceMain

from ipdds_app.dao.dao_m_ip import DaoMIp
from ipdds_app.dto.dto_07_age_search import DtoSearchAge

from operator import itemgetter
from itertools import groupby


class SearchAgeService(ServiceMain):

    # m_ipテーブル用DAO
    dao_m_ip = DaoMIp()

    def bizProcess(self):
        
        # 年代画面領域のデータを取得し領域用DTOに詰める
        search_age_dto = self.mapping(DtoSearchAge.DtoAgeName, self.dao_m_ip.selectAgeNameAll())
        search_age_dto = {key:list(group) for key,group in groupby(search_age_dto, key=itemgetter(0))}

        # 領域用DTOを画面DTOに詰める
        dto_age = DtoSearchAge(search_age_dto)

        return self.unpack(dto_age)