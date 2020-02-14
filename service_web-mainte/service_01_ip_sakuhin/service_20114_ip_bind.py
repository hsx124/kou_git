from admin_app.service.service_list import ServiceList

from admin_app.dao.dao_m_ip import DaoMIp
from admin_app.dao.dao_m_ip_map import DaoMIpMap
from admin_app.dao.dao_m_sakuhin import DaoMSakuhin
from admin_app.dao.dao_t_update_history import DaoTUpdateHistory
from admin_app.dto.dto_01_ip_sakuhin.dto_20114_ip_bind import DtoIpBind

class IpBindService(ServiceList):

    # IPマスタテーブル用DAO
    dao_m_ip = DaoMIp()
    # IP紐付けマスタテーブル用DAO
    dao_m_ip_map = DaoMIpMap()
    # 作品マスタテーブル用DAO
    dao_m_sakuhin = DaoMSakuhin()
    # 更新履歴テーブル用DAO
    dao_t_update_history = DaoTUpdateHistory()

    '''初期描画'''
    def initialize(self, tableName):
        # 更新履歴
        notice_table = self.getnoticetable(tableName)
        # 領域用DTOを画面DTOに詰める
        dto_ip_list= DtoIpBind.DtoNoticeTableList(notice_table)

        return self.unpack(dto_ip_list)

    """
    IPマスタのデータを取得する
    """
    def getIpData(self, ip_name):
        param = {'ip_name':'%' + ip_name + '%'}
        ip_list = self.mapping(DtoIpBind.DtoIpBindList.DtoIpData, self.dao_m_ip.selectByIpName(param))

        return self.unpack(ip_list)

    """
    関連作品データを取得する(IPコード)
    """
    def getConnectionSakuhinListData(self, ip_code):
        param_code = {'ip_code':ip_code}
        sakuhin_list = self.mapping(DtoIpBind.DtoIpBindList.DtoConnectionSakuhin, self.dao_m_ip.selectByIpCode(param_code))
       
        return self.unpack(sakuhin_list)

    """
    関連作品紐付けを解除する
    """
    def delConnectionSakuhin(self, full_name, map_id, ip_code, ip_name, sakuhin_name):
        # 紐付け解除作品の無効フラグを変更
        param = {
            'full_name' : full_name,
            'map_id' : map_id
            }
        # IP紐付け解除処理を行う
        self.dao_m_ip_map.updateInvalidFlgBy(param)

        # 変更履歴の登録
        # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
        entity = ('m_ip_map', '削除', ip_name, sakuhin_name, full_name)
        self.dao_t_update_history.insert(entity)

        # 最新の関連作品データを取得
        return self.getConnectionSakuhinListData(ip_code)

    """
    関連作品データを取得する(モーダル)
    """
    def getConnectionSakuhinModalData(self, sakuhin_name):
        param = {'sakuhin_name':'%' + sakuhin_name + '%'}
        connection_sakuhin_modal = self.mapping(DtoIpBind.DtoIpBindList.DtoConnectionSakuhinModal, self.dao_m_sakuhin.selectBySakuhinName(param))
       
        return self.unpack(connection_sakuhin_modal)

    """
    関連作品追加
    """
    def addConnectionSakuhin(self,sakuhin_code_list,ip_code, ip_name,full_name):
        sakuhin_code_list = tuple(sakuhin_code_list)
        param = {
            'ip_code': ip_code,
            'sakuhin_code_list':sakuhin_code_list,
            'full_name' : full_name
        }
        # 関連作品追加処理を行う
        self.dao_m_ip_map.insertBySakuhinList(param)

        # 変更履歴の登録
        # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
        entity = {
            'update_table' : 'm_ip_map',
            'operation' : '追加',
            'target_name' : ip_name,
            'sakuhin_code_list' : sakuhin_code_list,
            'full_name' : full_name
        }
        self.dao_t_update_history.insertBySakuhinlist(entity)

        # 最新の関連作品データを取得
        return self.getConnectionSakuhinListData(ip_code)

    """
    関連IPデータを取得する(作品コード)
    """
    def getIpBySakuhinCode(self, sakuhin_code):
        param_code = {'sakuhin_code':sakuhin_code}
        ip_list = self.mapping(DtoIpBind.DtoIpBindList.DtoConnectionIpData, self.dao_m_ip.selectBySakuhinCode(param_code))
       
        return self.unpack(ip_list)

    """
    関連IP紐付けを解除する
    """
    def delConnectionIp(self, full_name, map_id, sakuhin_code, ip_name, sakuhin_name):
        # 紐付け解除IPの無効フラグを変更
        param = {
            'full_name' : full_name,
            'map_id' : map_id
        }
        # IP紐付け解除処理を行う
        self.dao_m_ip_map.updateInvalidFlgBy(param)

        # 変更履歴の登録
        # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
        entity = ('m_ip_map', '削除', ip_name, sakuhin_name, full_name)
        self.dao_t_update_history.insert(entity)

        # 最新の関連IPデータを取得
        return self.getIpBySakuhinCode(sakuhin_code)

    """
    関連IP追加
    """
    def addConnectionIp(self,ip_code_list, sakuhin_code, sakuhin_name, full_name):
        ip_code_list = tuple(ip_code_list)
        param = {
            'ip_code_list': ip_code_list,
            'sakuhin_code':sakuhin_code,
            'full_name' : full_name
        }
        # 関連作品追加処理を行う
        self.dao_m_ip_map.insertByIpList(param)

        # 変更履歴の登録
        # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
        entity = {
            'update_table' : 'm_ip_map',
            'operation' : '追加',
            'ip_code_list' : ip_code_list,
            'remarks' : sakuhin_name,
            'full_name' : full_name
        }
        self.dao_t_update_history.insertByIplist(entity)

        return self.getIpBySakuhinCode(sakuhin_code)


