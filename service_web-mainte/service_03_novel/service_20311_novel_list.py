from admin_app.service.service_main import ServiceMain
from admin_app.service.service_list import ServiceList

from admin_app.dao.dao_m_novel_title import DaoMNovelTitle
from admin_app.dto.dto_03_novel.dto_20311_novel_list import DtoNovelList

class NovelListService(ServiceList):

    dao_m_novel_title = DaoMNovelTitle()

    """初期描画"""
    def initialize(self, tableName):
        # 更新履歴
        notice_table = self.getnoticetable(tableName)
        # 領域用DTOを画面DTOに詰める
        dto_novel_list= DtoNovelList.DtoNoticeTableList(notice_table)
        return self.unpack(dto_novel_list)

    """小説のデータを取得する"""
    def getNovelList(self):
        dto_novel_list = self.mapping(DtoNovelList.DtoNovelMasterList.DtoNovelMasterListData, self.dao_m_novel_title.selectAll())

        return self.unpack(dto_novel_list)

    """小説の削除処理"""
    def deleteNovelData(self, novel_title_code, novel_title_name, full_name):

        # 削除する前に該当データの無効フラグを確認
        param_code = {'novel_title_code': novel_title_code}
        invalid_flg = self.dao_m_novel_title.selectInvalidFlg(param_code)
        # 削除フラグ（当削除対象が既に削除したかフラグ）
        delete_flg = False

        # 既に削除した場合はエラーメッセージを表示
        if invalid_flg :
            delete_flg = True
        else:
            # 小説コードに合致するレコードを論理削除
            param = {
                'novel_title_code': novel_title_code,
                'full_name': full_name
            }
            self.dao_m_novel_title.updateInvalidFlgByNovelCode(param)

            # 変更履歴の登録
            # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
            entity = ('m_novel_title', '削除', novel_title_name, '', full_name)
            self.dao_t_update_history.insert(entity)

        # 小説タイトル基本マスタ一覧グリッドを更新のため、小説タイトル基本マスタデータ再検索
        dto_novel_list = self.mapping(DtoNovelList.DtoNovelMasterList.DtoNovelMasterListData, self.dao_m_novel_title.selectAll())
        return self.unpack({'is_error':delete_flg,'novel_list':dto_novel_list})

    """CSV出力用小説情報取得"""
    def getNovelCsvData(self):
        novel_list_for_CSV = {}

        # 小説情報(CSV出力用)を全件取得
        novel_list_for_CSV = self.mapping(DtoNovelList.DtoNovelMasterList.DtoNovelMasterListForCSV, self.dao_m_novel_title.selectCsvData())
        return self.unpack(novel_list_for_CSV)