from admin_app.service.service_main import ServiceMain
from admin_app.service.service_list import ServiceList

from admin_app.dao.dao_m_staff_role import DaoMStaffRole
from admin_app.dto.dto_11_various.dto_21151_staff_role_list import DtoStaffRoleList

class StaffRoleListService(ServiceList):

    dao_m_staff_role = DaoMStaffRole()

    '''初期描画'''
    def initialize(self, table_name):

        # 更新履歴
        notice_table = self.getnoticetable(table_name)
        # 領域用DTOを画面DTOに詰める
        dto_staff_role_list= DtoStaffRoleList.DtoNoticeTableList(notice_table)
        return self.unpack(dto_staff_role_list)

    """スタッフ役割のデータを取得する"""
    def getStaffRoleList(self):
        dto_staff_role_list = self.mapping(DtoStaffRoleList.DtoStaffRoleMasterList.DtoStaffRoleMasterListData, self.dao_m_staff_role.selectStaffRoleList())
        return self.unpack(dto_staff_role_list)

    """スタッフ役割の削除処理"""
    def deleteStaffRoleData(self, staff_role_code, staff_role_name, full_name):

        # 削除する前に該当データの無効フラグを確認
        param_code = {'staff_role_code': staff_role_code}
        invalid_flg = self.dao_m_staff_role.selectInvalidFlg(param_code)
        # 削除フラグ（当削除対象が既に削除したかフラグ）
        delete_flg = False

        # 既に削除した場合はエラーメッセージを表示
        if invalid_flg :
            delete_flg = True
        else:
            # スタッフ役割コードに合致するレコードを論理削除
            param = {
                'staff_role_code': staff_role_code,
                'full_name': full_name
            }
            self.dao_m_staff_role.updateInvalidFlgByStaffRoleCode(param)

            # 変更履歴の登録
            # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
            entity = ('m_staff_role', '削除', staff_role_name, '', full_name)
            self.dao_t_update_history.insert(entity)

        # スタッフ役割マスタグリッドを更新のため、スタッフ役割マスタデータ再検索
        dto_staff_role_list = self.mapping(DtoStaffRoleList.DtoStaffRoleMasterList.DtoStaffRoleMasterListData, self.dao_m_staff_role.selectStaffRoleList())

        return self.unpack({'is_error':delete_flg,'staff_role_list':dto_staff_role_list})

    """CSV出力用マンガ情報取得"""
    def getStaffRoleCsvData(self):
        staff_role_list_for_CSV = {}

        # スタッフ役割情報(CSV出力用)を全件取得
        staff_role_list_for_CSV = self.mapping(DtoStaffRoleList.DtoStaffRoleMasterList.DtoStaffRoleMasterListForCSV, self.dao_m_staff_role.selectCsvData())

        return self.unpack(staff_role_list_for_CSV)