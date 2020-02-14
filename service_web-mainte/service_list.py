import datetime

from admin_app.service.service_main import ServiceMain

from admin_app.dao.dao_t_update_history import DaoTUpdateHistory
from admin_app.dao.dao_m_sakuhin import DaoMSakuhin

from admin_app.dto.dto_main import DtoMain
from admin_app.dto.dto_list import DtoList

class ServiceList(ServiceMain):
    # 変更履歴テーブル用DAO
    dao_t_update_history = DaoTUpdateHistory()
    serviceMain = ServiceMain()

    # IPマスタテーブル用DAO
    dao_m_sakuhin = DaoMSakuhin()
    
    # 更新履歴取得
    def getnoticetable(self, tableName):

        # 更新履歴
        notice_table = self.mapping(DtoList.DtoNoticeTable, self.dao_t_update_history.selectChangeByTableName(tableName))

        return notice_table

    def changecsvdownloadprocess(self, tableName, startDate=datetime.date(1900,1,1), endDate=datetime.date(2099,12,31)):
        '''
        更新履歴CSVダウンロード処理
        '''
        csv_date = ServiceMain.mapping(ServiceMain,DtoList.DtoUpdateHistoryCsv, self.dao_t_update_history.selectChangeRecordByDate(tableName,startDate,endDate))

        return csv_date

    def sakuhinCodeSearchProcess(self, sakuhin_code):
        '''
        IPコードからIPマスタを検索
        '''

        # IPコードからIPを検索
        ip_search_result = self.mapping(DtoList.DtoSakuhinSearchResult, self.dao_m_sakuhin.selectSakuhinMasterBySakuhinCode(sakuhin_code))

        return self.unpack(ip_search_result)

    def sakuhinNameSearchProcess(self, ip_name):
        '''
        IP名からIPマスタを検索
        Parameters
        ----------
        ip_name : str
                IP名
        Returns
        ----------
        obj : {sakuhin_code : str , ip_name : str}
        '''
        
        # IP名からIPを検索
        ip_search_result = self.mapping(DtoList.DtoSakuhinSearchResult, self.dao_m_sakuhin.selectSakuhinMasterBySakuhinName(ip_name))
        return self.unpack(ip_search_result)

