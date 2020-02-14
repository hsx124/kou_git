from admin_app.service.service_list import ServiceList

from admin_app.dao.dao_m_publisher import DaoMPublisher
from admin_app.dto.dto_11_various.dto_21121_publisher_list import DtoPublisherList

class PublisherListService(ServiceList):

    # 出版社マスタテーブル用DAO
    dao_m_publisher = DaoMPublisher()

    '''初期描画'''
    def initialize(self, tableName):
        # 更新履歴
        notice_table = self.getnoticetable(tableName)
        # 領域用DTOを画面DTOに詰める
        dto_publisher_list= DtoPublisherList.DtoNoticeTableList(notice_table)

        return self.unpack(dto_publisher_list)

    """
    出版社のデータを取得する
    """
    def getPublisherList(self):
        publisher_list = self.mapping(DtoPublisherList.DtoPublisherMasterList.DtoPublisherMasterListData, self.dao_m_publisher.selectAll())

        return self.unpack(publisher_list)

    """出版社の削除処理"""
    def deletePublisherData(self, publisher_code, publisher_name, full_name):

        # 削除する前に当該データの無効フラグを確認
        paramCode = {'publisher_code':publisher_code}
        invalid_flg =  self.dao_m_publisher.selectInvalidFlg(paramCode)
        
        #削除フラグ（当削除対象が既に削除したかフラグ）
        delflg = False

        # 既に削除した場合はエラーメッセージを表示
        if invalid_flg :
            delflg = True
        else:
            # 出版社コードに合致するレコードを論理削除
            param = {
                'publisher_code':publisher_code,
                'full_name':full_name
            }
            self.dao_m_publisher.updateInvalidFlgByPublisherCode(param)

            # 変更履歴の登録
            # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
            entity = ('m_publisher', '削除', publisher_name, '', full_name)
            self.dao_t_update_history.insert(entity)

        # 出版社マスタ一覧グリッドを更新
        publisher_list = self.mapping(DtoPublisherList.DtoPublisherMasterList.DtoPublisherMasterListData, self.dao_m_publisher.selectAll())

        return self.unpack({'is_error':delflg,'publisherlist':publisher_list})

    def getPublisherCsvData(self):
        """
        CSV出力用出版社情報取得
        """
        publisher_list_for_CSV = {}

        # 出版社情報(CSV出力用)を全件取得
        publisher_list_for_CSV = self.mapping(DtoPublisherList.DtoPublisherMasterList.DtoPublisherMasterListForCSV, self.dao_m_publisher.selectCsvData())

        return self.unpack(publisher_list_for_CSV)