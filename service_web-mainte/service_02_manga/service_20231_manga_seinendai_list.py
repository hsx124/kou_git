from admin_app.service.service_main import ServiceMain
from admin_app.service.service_list import ServiceList

from admin_app.dao.dao_m_seinendai import DaoMSeinendai
from admin_app.dto.dto_02_manga.dto_20231_manga_seinendai_list import DtoMangaSeinendaiList

class MangaSeinendaiListService(ServiceList):

    dao_m_seinendai = DaoMSeinendai()

    """初期描画"""
    def initialize(self, tableName):
        # 更新履歴
        notice_table = self.getnoticetable(tableName)
        # 領域用DTOを画面DTOに詰める
        dto_manga_seinendai_list= DtoMangaSeinendaiList.DtoNoticeTableList(notice_table)

        return self.unpack(dto_manga_seinendai_list)

    """性年代のデータを取得する"""
    def getMangaSeinendaiList(self):
        dto_manga_seinendai_list = self.mapping(DtoMangaSeinendaiList.DtoMangaSeinendaiMasterList.DtoMangaSeinendaiMasterListData, self.dao_m_seinendai.selectAll())

        return self.unpack(dto_manga_seinendai_list)

    """性年代の削除処理"""
    def deleteMangaSeinendaiData(self, seinendai_code, manga_title_name, full_name):

        # 削除する前に該当データの無効フラグを確認
        param_code = {'seinendai_code': seinendai_code}
        invalid_flg = self.dao_m_seinendai.selectInvalidFlg(param_code)

        # 削除フラグ（当削除対象が既に削除したかフラグ）
        delete_flg = False

        # 既に削除した場合はエラーメッセージを表示
        if invalid_flg :
            delete_flg = True
        else:
            # 性年代に合致するレコードを論理削除
            param = {
                'seinendai_code': seinendai_code,
                'full_name': full_name
            }
            self.dao_m_seinendai.updateInvalidFlgByMangaSeinendaiCode(param)
            self.dao_m_seinendai.updateInvalidFlgByMangaTitleCode(param)

            # 変更履歴の登録
            # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
            entity = ('m_seinendai', '削除', manga_title_name, '', full_name)
            self.dao_t_update_history.insert(entity)

        # グリッドを更新の為、性年代マスタデータ再検索
        dto_manga_seinendai_list = self.mapping(DtoMangaSeinendaiList.DtoMangaSeinendaiMasterList.DtoMangaSeinendaiMasterListData, self.dao_m_seinendai.selectAll())

        return self.unpack({'is_error':delete_flg,'manga_seinendai_list':dto_manga_seinendai_list})

    """CSV出力用性年代情報取得"""
    def getMangaSeinendaiCsvData(self):
        manga_list_for_CSV = {}

        # 性年代情報(CSV出力用)を全件取得
        manga_list_for_CSV = self.mapping(DtoMangaSeinendaiList.DtoMangaSeinendaiMasterList.DtoMangaSeinendaiMasterListForCSV, self.dao_m_seinendai.selectCsvData())

        return self.unpack(manga_list_for_CSV)