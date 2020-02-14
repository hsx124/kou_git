from admin_app.service.service_main import ServiceMain
from admin_app.service.service_list import ServiceList

from admin_app.dao.dao_m_core import DaoMCore
from admin_app.dto.dto_10_sakuhin_tag.dto_21041_core_list import DtoCoreList

class CoreListService(ServiceList):

    dao_m_core = DaoMCore()

    '''初期描画'''
    def initialize(self, table_name):

        # 更新履歴
        notice_table = self.getnoticetable(table_name)

        # 領域用DTOを画面DTOに詰める
        dto_core_list= DtoCoreList.DtoNoticeTableList(notice_table)
        return self.unpack(dto_core_list)

    """コアのデータを取得する"""
    def getCoreList(self):
        dto_core_list = self.mapping(DtoCoreList.DtoCoreMasterList.DtoCoreMasterListData, self.dao_m_core.selectCoreList())
        return self.unpack(dto_core_list)

    """コアの削除処理"""
    def deleteCoreData(self, core_code, core_name, full_name):

        # 削除する前に該当データの無効フラグを確認
        param_code = {'core_code': core_code}
        invalid_flg = self.dao_m_core.selectInvalidFlg(param_code)
        # 削除フラグ（当削除対象が既に削除したかフラグ）
        delete_flg = False

        # 既に削除した場合はエラーメッセージを表示
        if invalid_flg :
            delete_flg = True
        else:
            # コアコードに合致するレコードを論理削除
            param = {
                'core_code': core_code,
                'full_name': full_name
            }
            self.dao_m_core.updateInvalidFlgByCoreCode(param)

            # 変更履歴の登録
            # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
            entity = ('m_core', '削除', core_name, '', full_name)
            self.dao_t_update_history.insert(entity)

        # コアマスタ一覧グリッドを更新のため、コアマスタデータ再検索
        dto_core_list = self.mapping(DtoCoreList.DtoCoreMasterList.DtoCoreMasterListData, self.dao_m_core.selectCoreList())

        return self.unpack({'is_error':delete_flg,'core_list':dto_core_list})

    """CSV出力用マンガ情報取得"""
    def getCoreCsvData(self):
        core_list_for_CSV = {}

        # コア情報(CSV出力用)を全件取得
        core_list_for_CSV = self.mapping(DtoCoreList.DtoCoreMasterList.DtoCoreMasterListForCSV, self.dao_m_core.selectCsvData())

        return self.unpack(core_list_for_CSV)