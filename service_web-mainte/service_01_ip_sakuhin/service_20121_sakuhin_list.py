from admin_app.service.service_main import ServiceMain
from admin_app.service.service_list import ServiceList

from admin_app.dao.dao_m_sakuhin import DaoMSakuhin

from admin_app.dto.dto_01_ip_sakuhin.dto_20121_sakuhin_list import DtoSakuhinList

class SakuhinListService(ServiceList):

    # 作品マスタテーブル用DAO
    dao_m_sakuhin = DaoMSakuhin()

    '''初期描画'''
    def initialize(self, tableName):

        # 更新履歴
        notice_table = self.getnoticetable(tableName)

        # 作品マスタ一覧グリッド
        sakuhin_master_list = self.mapping(DtoSakuhinList.DtosakuhinMasterList, self.dao_m_sakuhin.selectAll())

        # 領域用DTOを画面DTOに詰める
        dto_sakuhin_list= DtoSakuhinList(notice_table,sakuhin_master_list,{})

        return self.unpack(dto_sakuhin_list)

    """作品マスタのデータを取得する"""
    def getSakuhinList(self):
        sakuhin_list = self.mapping(DtoSakuhinList.DtosakuhinMasterList, self.dao_m_sakuhin.selectAll())
        return self.unpack(sakuhin_list)

    '''作品削除プロセス'''
    def deleteSakuhinData(self, sakuhinCode, sakuhinName, full_name):

        # 削除する前に当該データの無効フラグを確認
        param_code = {'sakuhin_code':sakuhinCode}
        invalid_flg =  self.dao_m_sakuhin.selectInvalidFlg(param_code)

        #削除フラグ（当削除対象が既に削除したかフラグ）
        delflg = False

        # 既に削除した場合はエラーメッセージを表示
        if invalid_flg :
            delflg = True
        else:
            # 作品コードに合致するレコードを論理削除
            self.dao_m_sakuhin.updateInvalidFlgBySakuhinCode(sakuhinCode, full_name)

            # 変更履歴の登録
            # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
            entity = ('m_sakuhin', '削除', sakuhinName, '', full_name)
            self.dao_t_update_history.insert(entity)

        # 作品マスタ一覧グリッドを更新
        sakuhin_list = self.mapping(DtoSakuhinList.DtosakuhinMasterList, self.dao_m_sakuhin.selectAll())

        return self.unpack({'is_error':delflg,'sakuhin_list':sakuhin_list})

    def getSakuhinCsvData(self):
        '''
        CSV出力用sakuhin情報取得
        '''

        sakuhin_master_list_for_CSV = {}

        # 作品情報(CSV出力用)を全件取得
        sakuhin_master_list_for_CSV = self.mapping(DtoSakuhinList.DtosakuhinMasterListForCSV, self.dao_m_sakuhin.selectsakuhinMasterForCSV())

        return self.unpack(sakuhin_master_list_for_CSV)
