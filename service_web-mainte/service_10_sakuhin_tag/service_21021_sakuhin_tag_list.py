from admin_app.service.service_main import ServiceMain
from admin_app.service.service_list import ServiceList

from admin_app.dao.dao_m_sakuhin_tag import DaoMSakuhinTag
from admin_app.dao.dao_m_sakuhin_tag_category import DaoMSakuhinTagCategory

from admin_app.dto.dto_10_sakuhin_tag.dto_21021_sakuhin_tag_list import DtoSakuhinTagList

class SakuhinTagListService(ServiceList):

    # タグマスタテーブル用DAO
    dao_m_sakuhin_tag = DaoMSakuhinTag()
    dao_m_sakuhin_tag_category = DaoMSakuhinTagCategory()

    '''初期描画'''
    def initialize(self, table_name):

        # 更新履歴
        notice_table = self.getnoticetable(table_name)
        dto_sakuhin_category_tag = self.mapping(DtoSakuhinTagList.DtoSakuhinTagCategoryAll, self.dao_m_sakuhin_tag_category.selectSakuhinTagCategoryAll())
        # 領域用DTOを画面DTOに詰める
        dto_sakuhin_tag_list= DtoSakuhinTagList(notice_table,dto_sakuhin_category_tag)
        return self.unpack(dto_sakuhin_tag_list)

    """
    タグマスタのデータを取得する
    """
    def getSakuhinTagList(self,category_code):

        if 'all-category' == category_code:
            # 全カテゴリ選択時
            sakuhin_tag_list = self.mapping(DtoSakuhinTagList.DtoSakuhinTagMasterList, self.dao_m_sakuhin_tag.selectSakuhinTagAll())
        else:
            param = {
                'category_code' : category_code        
            }
            self.dao_m_sakuhin_tag.selectSakuhinTagCategoryByCategoryCode(param)
            # 各種カテゴリ選択時
            sakuhin_tag_list = self.mapping(DtoSakuhinTagList.DtoSakuhinTagMasterList, self.dao_m_sakuhin_tag.selectSakuhinTagCategoryByCategoryCode(param))
        
        return self.unpack(sakuhin_tag_list)

    """
    タグマスタの削除処理
    """
    def deleteTagData(self, tag_code, tag_name, full_name,category_code):

        # 削除する前に該当データの無効フラグを確認
        paramCode = {'tag_code':tag_code}
        invalid_flg =  self.dao_m_sakuhin_tag.selectInvalidFlg(paramCode)

        #削除フラグ（当削除対象が既に削除したかフラグ）
        delflg = False
       # 既に削除した場合はエラーメッセージを表示
        if invalid_flg:
            delflg = True
        else:
            param = {
            'tag_code' : tag_code,
            'full_name' : full_name,
            'category_code' : category_code              
            }
            # 作品タグコードに合致するレコードを論理削除
            self.dao_m_sakuhin_tag.updateInvalidFlgByTagCode(param)
            # 更新履歴の登録
            # (変更テーブル名,操作内容,更新対象,備考,更新者)を設定
            entity = ('m_sakuhin_tag', '削除', tag_name, '', full_name)
            self.dao_t_update_history.insert(entity)
        if 'all-category' == category_code:
            # 全カテゴリ選択時
            sakuhin_tag_list = self.mapping(DtoSakuhinTagList.DtoSakuhinTagMasterList, self.dao_m_sakuhin_tag.selectSakuhinTagAll())
        else:
            param = {
                'category_code' : category_code        
            }
            self.dao_m_sakuhin_tag.selectSakuhinTagCategoryByCategoryCode(param)
            # 各種カテゴリ選択時
            sakuhin_tag_list = self.mapping(DtoSakuhinTagList.DtoSakuhinTagMasterList, self.dao_m_sakuhin_tag.selectSakuhinTagCategoryByCategoryCode(param))

        return self.unpack({'is_error':delflg,'sakuhin_list':sakuhin_tag_list})
        
    """
    CSV出力用タグマスタ情報取得
    """
    def getTagCsvData(self):

        tag_list_for_csv = self.mapping(DtoSakuhinTagList.DtoTagMasterListForCSV, self.dao_m_sakuhin_tag.selectTagMasterForCSV())

        return self.unpack(tag_list_for_csv)