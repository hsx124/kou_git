from admin_app.service.service_main import ServiceMain
from admin_app.service.service_list import ServiceList

from admin_app.dao.dao_m_seisaku_company import DaoMSeisakuCompany
from admin_app.dto.dto_11_various.dto_21131_seisaku_company_list import DtoSeisakuCompanyList

class SeisakuCompanyListService(ServiceList):

    # 制作会社マスタテーブル用DAO
    dao_m_seisaku_company = DaoMSeisakuCompany()
    # serviceMain = ServiceMain()

    '''初期描画'''
    def initialize(self, tableName):
        # 更新履歴
        notice_table = self.getnoticetable(tableName)
        # 領域用DTOを画面DTOに詰める
        dto_update_list= DtoSeisakuCompanyList.DtoNoticeTableList(notice_table)

        return self.unpack(dto_update_list)

    """
    制作会社のデータを取得する
    """
    def getSeisakuCompanyList(self):
        seisaku_company_list = self.mapping(DtoSeisakuCompanyList.DtoSeisakuCompanyMasterList.DtoSeisakuCompanyMasterListData, self.dao_m_seisaku_company.selectAll())
        
        return self.unpack(seisaku_company_list)

    """制作会社の削除処理"""
    def delete(self, seisaku_company_code, seisaku_company_name, full_name):

        # 削除する前に当該データの無効フラグを確認
        param_code = {'seisaku_company_code':seisaku_company_code}
        invalid_flg = self.dao_m_seisaku_company.selectInvalidFlg(param_code)

        #削除フラグ（当削除対象が既に削除したかフラグ）
        delflg = False

        # 既に削除した場合はエラーメッセージを表示
        if invalid_flg :
            delflg = True
        else:
            # 制作会社コードに合致するレコードを論理削除
            param = {
                'seisaku_company_code':seisaku_company_code,
                'full_name':full_name
            }
            self.dao_m_seisaku_company.updateInvalidFlg(param)

            # 変更履歴の登録
            # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
            entity = ('m_seisaku_company', '削除', seisaku_company_name, '', full_name)
            self.dao_t_update_history.insert(entity)

        # 制作会社マスタ一覧グリッドを更新
        seisaku_company_list = self.mapping(DtoSeisakuCompanyList.DtoSeisakuCompanyMasterList.DtoSeisakuCompanyMasterListData, self.dao_m_seisaku_company.selectAll())

        return self.unpack({'is_error':delflg,'seisakucompanylist':seisaku_company_list})

    def getCsvData(self):
        """
        CSV出力用制作会社情報取得
        """
        seisaku_company_CSV = {}

        # 制作会社情報(CSV出力用)を全件取得
        seisaku_company_CSV = self.mapping(DtoSeisakuCompanyList.DtoSeisakuCompanyMasterList.DtoSeisakuCompanyMasterListForCSV, self.dao_m_seisaku_company.selectCsvData())

        return self.unpack(seisaku_company_CSV)