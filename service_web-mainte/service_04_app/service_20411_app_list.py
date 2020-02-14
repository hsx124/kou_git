import csv

from admin_app.service.service_list import ServiceList

from admin_app.dao.dao_m_sakuhin import DaoMSakuhin
from admin_app.dao.dao_m_mobile_app import DaoMMobileApp

from admin_app.dto.dto_main import DtoMain
from admin_app.dto.dto_04_app.dto_20411_app_list import DtoAppList

class AppListService(ServiceList):

    # IPマスタテーブル用DAO
    dao_m_sakuhin = DaoMSakuhin()

    # アプリマスタテーブル用DAO
    dao_m_mobile_app = DaoMMobileApp()

    '''初期描画'''
    def bizProcess(self, tableName):

        # 更新履歴
        notice_table = self.getnoticetable(tableName)

        # 領域用DTOを画面DTOに詰める
        dto_app_list= DtoAppList(notice_table, {})

        return self.unpack(dto_app_list)

    def getGridDataProcess(self, sakuhin_code):
        '''
        グリッド表示用アプリ情報取得
        ----------
        sakuhin_code : str
                IPコード
        '''

        grid_date = self.mapping(DtoAppList.DtoAppMasterList, self.dao_m_mobile_app.selectAppMasterByIpCode(sakuhin_code))
        return self.unpack(grid_date)
    
    def getCsvDataProcess(self, sakuhin_code=None):
        '''
        CSV出力用書籍情報取得
        ----------
        sakuhin_code : str
                IPコード
        '''

        csv_date = {}

        if sakuhin_code != None:
            # 選択IPに紐づくアプリ情報(CSV出力用)を取得
            csv_date = self.dao_m_mobile_app.selectAppMasterforCSVByIpCode(sakuhin_code)
        else:
            # アプリ情報(CSV出力用)を全件取得
            csv_date = self.dao_m_mobile_app.selectAppMasterforCSV()

        return csv_date

    def deleteAppProcess(self, sakuhin_code, appName, full_name):
        '''
        アプリ削除プロセス
        '''

        # IPコードに合致するレコードを論理削除
        self.dao_m_mobile_app.updateIsInvalidByAppName(appName,full_name)

        # 変更履歴の登録
        # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
        entity = ('m_mobile_app', '削除', appName, '', full_name)
        self.dao_t_update_history.insertTChangeManagement(entity)

        # アプリマスタ一覧グリッドを更新
        grid_date = self.mapping(DtoAppList.DtoAppMasterList, self.dao_m_mobile_app.selectAppMasterByIpCode(sakuhin_code))

        return self.unpack(grid_date)


