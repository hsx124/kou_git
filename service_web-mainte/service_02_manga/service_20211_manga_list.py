from admin_app.service.service_main import ServiceMain
from admin_app.service.service_list import ServiceList

from admin_app.dao.dao_m_manga_title import DaoMMangaTitle
from admin_app.dto.dto_02_manga.dto_20211_manga_list import DtoMangaList

class MangaListService(ServiceList):

    dao_m_manga_title = DaoMMangaTitle()

    """初期描画"""
    def initialize(self, tableName):
        # 更新履歴
        notice_table = self.getnoticetable(tableName)
        # 領域用DTOを画面DTOに詰める
        dto_manga_list= DtoMangaList.DtoNoticeTableList(notice_table)

        return self.unpack(dto_manga_list)

    """マンガのデータを取得する"""
    def getMangaList(self):
        dto_manga_list = self.mapping(DtoMangaList.DtoMangaMasterList.DtoMangaMasterListData, self.dao_m_manga_title.selectAll())

        return self.unpack(dto_manga_list)

    """マンガの削除処理"""
    def deleteMangaData(self, manga_title_code, manga_title_name, full_name):

        # 削除する前に該当データの無効フラグを確認
        param_code = {'manga_title_code': manga_title_code}
        invalid_flg = self.dao_m_manga_title.selectInvalidFlg(param_code)

        # 削除フラグ（当削除対象が既に削除したかフラグ）
        delete_flg = False

        # 既に削除した場合はエラーメッセージを表示
        if invalid_flg :
            delete_flg = True
        else:
            # マンガコードに合致するレコードを論理削除
            param = {
                'manga_title_code': manga_title_code,
                'full_name': full_name
            }
            self.dao_m_manga_title.updateInvalidFlgByMangaCode(param)

            # 変更履歴の登録
            # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
            entity = ('m_manga_title', '削除', manga_title_name, '', full_name)
            self.dao_t_update_history.insert(entity)

        # マンガタイトル基本マスタ一覧グリッドを更新のため、マンガタイトル基本マスタデータ再検索
        dto_manga_list = self.mapping(DtoMangaList.DtoMangaMasterList.DtoMangaMasterListData, self.dao_m_manga_title.selectAll())

        return self.unpack({'is_error':delete_flg,'manga_list':dto_manga_list})

    """CSV出力用マンガ情報取得"""
    def getMangaCsvData(self):
        manga_list_for_CSV = {}

        # マンガ情報(CSV出力用)を全件取得
        manga_list_for_CSV = self.mapping(DtoMangaList.DtoMangaMasterList.DtoMangaMasterListForCSV, self.dao_m_manga_title.selectCsvData())

        return self.unpack(manga_list_for_CSV)