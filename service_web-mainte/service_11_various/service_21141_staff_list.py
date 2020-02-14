from admin_app.service.service_main import ServiceMain
from admin_app.service.service_list import ServiceList

from admin_app.dao.dao_m_staff import DaoMStaff
from admin_app.dto.dto_11_various.dto_21141_staff_list import DtoStaffList

class StaffListService(ServiceList):

    dao_m_staff = DaoMStaff()

    '''初期描画'''
    def initialize(self, table_name):

        # 更新履歴
        notice_table = self.getnoticetable(table_name)

        # 領域用DTOを画面DTOに詰める
        dto_staff_list= DtoStaffList.DtoNoticeTableList(notice_table)
        return self.unpack(dto_staff_list)

    """スタッフのデータを取得する"""
    def getStaffList(self):
        dto_staff_list = self.mapping(DtoStaffList.DtoStaffMasterList.DtoStaffMasterListData, self.dao_m_staff.selectStaffList())
        return self.unpack(dto_staff_list)

    """スタッフの削除処理"""
    def deleteStaffData(self, staff_code, staff_name, full_name):

        # 削除する前に該当データの無効フラグを確認
        param_code = {'staff_code': staff_code}
        invalid_flg = self.dao_m_staff.selectInvalidFlg(param_code)
        # 削除フラグ（当削除対象が既に削除したかフラグ）
        delete_flg = False

        # 既に削除した場合はエラーメッセージを表示
        if invalid_flg :
            delete_flg = True
        else:
            # スタッフコードに合致するレコードを論理削除
            param = {
                'staff_code': staff_code,
                'full_name': full_name
            }
            self.dao_m_staff.updateInvalidFlgByStaffCode(param)

            # 変更履歴の登録
            # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
            entity = ('m_staff', '削除', staff_name, '', full_name)
            self.dao_t_update_history.insert(entity)

        # スタッフマスタ一覧グリッドを更新のため、スタッフマスタデータ再検索
        dto_staff_list = self.mapping(DtoStaffList.DtoStaffMasterList.DtoStaffMasterListData, self.dao_m_staff.selectStaffList())

        return self.unpack({'is_error':delete_flg,'staff_list':dto_staff_list})

    """CSV出力用マンガ情報取得"""
    def getStaffCsvData(self):
        staff_list_for_CSV = {}

        # スタッフ情報(CSV出力用)を全件取得
        staff_list_for_CSV = self.mapping(DtoStaffList.DtoStaffMasterList.DtoStaffMasterListForCSV, self.dao_m_staff.selectCsvData())

        return self.unpack(staff_list_for_CSV)