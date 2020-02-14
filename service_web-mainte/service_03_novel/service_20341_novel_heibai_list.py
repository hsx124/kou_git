from admin_app.service.service_main import ServiceMain
from admin_app.service.service_list import ServiceList

from admin_app.dao.dao_m_heibai import DaoMHeibai
from admin_app.dto.dto_03_novel.dto_20341_novel_heibai_list import DtoNovelHeibaiList

class NovelHeibaiListService(ServiceList):

    dao_m_heibai = DaoMHeibai()

    """初期描画"""
    def initialize(self, tableName):
        # 更新履歴
        notice_table = self.getnoticetable(tableName)
        # 領域用DTOを画面DTOに詰める
        dto_novel_heibai_list= DtoNovelHeibaiList.DtoNoticeTableList(notice_table)

        return self.unpack(dto_novel_heibai_list)

    """併売のデータを取得する"""
    def getNovelHeibaiList(self):
        dto_novel_heibai_list = self.mapping(DtoNovelHeibaiList.DtoNovelHeibaiMasterList.DtoNovelHeibaiMasterListData, self.dao_m_heibai.selectNovelAll())

        return self.unpack(dto_novel_heibai_list)

    """併売の削除処理"""
    def deleteNovelHeibaiData(self, heibai_code, novel_title_name, full_name):

        # 削除する前に該当データの無効フラグを確認
        param_code = {'heibai_code': heibai_code}
        invalid_flg = self.dao_m_heibai.selectInvalidFlg(param_code)

        # 削除フラグ（当削除対象が既に削除したかフラグ）
        delete_flg = False

        # 既に削除した場合はエラーメッセージを表示
        if invalid_flg :
            delete_flg = True
        else:
            # 併売に合致するレコードを論理削除
            param = {
                'heibai_code': heibai_code,
                'full_name': full_name
            }
            self.dao_m_heibai.updateInvalidFlgByHeibaiCode(param)
            self.dao_m_heibai.updateInvalidFlgByNovelTitleCode(param)

            # 変更履歴の登録
            # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
            entity = ('m_heibai(novel)', '削除', novel_title_name, '', full_name)
            self.dao_t_update_history.insert(entity)

        # グリッドを更新の為、併売マスタデータ再検索
        dto_novel_heibai_list = self.mapping(DtoNovelHeibaiList.DtoNovelHeibaiMasterList.DtoNovelHeibaiMasterListData, self.dao_m_heibai.selectNovelAll())

        return self.unpack({'is_error':delete_flg,'novel_heibai_list':dto_novel_heibai_list})

    """CSV出力用併売情報取得"""
    def getNovelHeibaiCsvData(self):
        novel_heibai_list_for_CSV = {}

        # 併売情報(CSV出力用)を全件取得
        novel_heibai_for_CSV = self.mapping(DtoNovelHeibaiList.DtoNovelHeibaiMasterList.DtoNovelHeibaiMasterListForCSV, self.dao_m_heibai.selectNovelCsvData())

        return self.unpack(novel_heibai_for_CSV)