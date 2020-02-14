from admin_app.service.service_main import ServiceMain
from admin_app.service.service_list import ServiceList

from admin_app.dao.dao_m_sakuhin_tag_category import DaoMSakuhinTagCategory
from admin_app.dto.dto_10_sakuhin_tag.dto_21031_sakuhin_tag_category_list import DtoSakuhinTagCategoryList

class SakuhinTagCategoryListService(ServiceList):

    dao_m_sakuhin_tag_category = DaoMSakuhinTagCategory()

    '''初期描画'''
    def initialize(self, table_name):

        # 更新履歴
        notice_table = self.getnoticetable(table_name)

        # 領域用DTOを画面DTOに詰める
        dto_sakuhin_tag_category_list= DtoSakuhinTagCategoryList.DtoNoticeTableList(notice_table)
        return self.unpack(dto_sakuhin_tag_category_list)

    """タグカテゴリのデータを取得する"""
    def getSakuhinTagCategoryList(self):
        dto_sakuhin_tag_category_list = self.mapping(DtoSakuhinTagCategoryList.DtoSakuhinTagCategoryMasterList.DtoSakuhinTagCategoryMasterListData, self.dao_m_sakuhin_tag_category.selectSakuhinTagCategoryList())
        return self.unpack(dto_sakuhin_tag_category_list)

    """タグカテゴリの削除処理"""
    def deleteSakuhinTagCategoryData(self, sakuhin_tag_category_code, sakuhin_tag_category_name, full_name):

        # 削除する前に該当データの無効フラグを確認
        param_code = {'sakuhin_tag_category_code': sakuhin_tag_category_code}
        invalid_flg = self.dao_m_sakuhin_tag_category.selectInvalidFlg(param_code)
        # 削除フラグ（当削除対象が既に削除したかフラグ）
        delete_flg = False

        # 既に削除した場合はエラーメッセージを表示
        if invalid_flg :
            delete_flg = True
        else:
            # タグカテゴリコードに合致するレコードを論理削除
            param = {
                'sakuhin_tag_category_code': sakuhin_tag_category_code,
                'full_name': full_name
            }
            self.dao_m_sakuhin_tag_category.updateInvalidFlgBySakuhinTagCategoryCode(param)

            # 変更履歴の登録
            # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
            entity = ('m_sakuhin_tag_category', '削除', sakuhin_tag_category_name, '', full_name)
            self.dao_t_update_history.insert(entity)

        # タグカテゴリマスタ一覧グリッドを更新のため、タグカテゴリマスタデータ再検索
        dto_sakuhin_tag_category_list = self.mapping(DtoSakuhinTagCategoryList.DtoSakuhinTagCategoryMasterList.DtoSakuhinTagCategoryMasterListData, self.dao_m_sakuhin_tag_category.selectSakuhinTagCategoryList())

        return self.unpack({'is_error':delete_flg,'sakuhin_tag_category_list':dto_sakuhin_tag_category_list})

    """CSV出力用マンガ情報取得"""
    def getSakuhinTagCategoryCsvData(self):
        sakuhin_tag_category_list_for_CSV = {}

        # タグカテゴリ情報(CSV出力用)を全件取得
        sakuhin_tag_category_list_for_CSV = self.mapping(DtoSakuhinTagCategoryList.DtoSakuhinTagCategoryMasterList.DtoSakuhinTagCategoryMasterListForCSV, self.dao_m_sakuhin_tag_category.selectCsvData())

        return self.unpack(sakuhin_tag_category_list_for_CSV)