from admin_app.service.service_main import ServiceMain
from admin_app.service.service_list import ServiceList

from admin_app.dao.dao_m_ip import DaoMIp
from admin_app.dto.dto_01_ip_sakuhin.dto_20111_ip_list import DtoIpList

class IpListService(ServiceList):

    # IPマスタテーブル用DAO
    dao_m_ip = DaoMIp()

    """初期描画"""
    def initialize(self, tableName):
        # 更新履歴
        notice_table = self.getnoticetable(tableName)
        # 領域用DTOを画面DTOに詰める
        dto_ip_list= DtoIpList.DtoNoticeTableList(notice_table)

        return self.unpack(dto_ip_list)

    """IPマスタのデータを取得する"""
    def getIpList(self):
        ip_list = self.mapping(DtoIpList.DtoIpMasterList.DtoIpMasterListData, self.dao_m_ip.selectAll())

        return self.unpack(ip_list)

    """IPの削除処理"""
    def deleteIpData(self, ip_code, ip_name, full_name):

        # 削除する前に当該データの無効フラグを確認
        param_code = {'ip_code':ip_code}
        invalid_flg =  self.dao_m_ip.selectInvalidFlg(param_code)
        
        #削除フラグ（当削除対象が既に削除したかフラグ）
        delflg = False

        # 既に削除した場合はエラーメッセージを表示
        if invalid_flg :
            delflg = True
        else:
            # IPコードに合致するレコードを論理削除
            param = {
                'ip_code':ip_code,
                'full_name':full_name
            }
            self.dao_m_ip.updateInvalidFlgByIpCode(param)

            # 変更履歴の登録
            # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
            entity = ('m_ip', '削除', ip_name, '', full_name)
            self.dao_t_update_history.insert(entity)

        # IPマスタ一覧グリッドを更新
        ip_list = self.mapping(DtoIpList.DtoIpMasterList.DtoIpMasterListData, self.dao_m_ip.selectAll())

        return self.unpack({'is_error':delflg,'ip_list':ip_list})

    """CSV出力用IP情報取得"""
    def getIpCsvData(self):
        ip_master_list_for_CSV = {}

        # IP情報(CSV出力用)を全件取得
        ip_master_list_for_CSV = self.mapping(DtoIpList.DtoIpMasterList.DtoIpListForCSV, self.dao_m_ip.selectCsvData())

        return self.unpack(ip_master_list_for_CSV)