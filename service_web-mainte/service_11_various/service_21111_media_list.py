from admin_app.service.service_list import ServiceList

from admin_app.dao.dao_m_media import DaoMMedia
from admin_app.dto.dto_11_various.dto_21111_media_list import DtoMediaList

class MediaListService(ServiceList):

    # 掲載媒体マスタテーブル用DAO
    dao_m_media = DaoMMedia()

    '''初期描画'''
    def initialize(self, tableName):
        # 更新履歴
        notice_table = self.getnoticetable(tableName)
        # 領域用DTOを画面DTOに詰める
        dto_media_list= DtoMediaList.DtoNoticeTableList(notice_table)

        return self.unpack(dto_media_list)

    """
    掲載媒体のデータを取得する
    """
    def getMediaList(self):
        dto_mediaList = self.mapping(DtoMediaList.DtoMediaMasterList.DtoMediaMasterListData, self.dao_m_media.selectAll())
        
        return self.unpack(dto_mediaList)

    """掲載媒体の削除処理"""
    def deleteMediaData(self, media_code, media_name, full_name):
    
        # 削除する前に該当データの無効フラグを確認
        paramCode = {'media_code':media_code}
        invalid_flg = self.dao_m_media.selectInvalidFlg(paramCode)
        
        #削除フラグ（当削除対象が既に削除したかフラグ）
        delflg = False

        # 既に削除した場合はエラーメッセージを表示
        if invalid_flg :
            delflg = True
        else:
            # 掲載媒体コードに合致するレコードを論理削除
            param = {
                'media_code':media_code,
                'full_name':full_name
            }
            self.dao_m_media.updateInvalidFlgByMediaCode(param)

            # 変更履歴の登録
            # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
            entity = ('m_media', '削除', media_name, '', full_name)
            self.dao_t_update_history.insert(entity)

        # 掲載媒体マスタ一覧グリッドを更新のため、掲載媒体マスタデータ再検索
        dto_mediaList = self.mapping(DtoMediaList.DtoMediaMasterList.DtoMediaMasterListData, self.dao_m_media.selectAll())

        return self.unpack({'is_error':delflg,'mediaList':dto_mediaList})

    def getMediaCsvData(self):
        """
        CSV出力用掲載媒体情報取得
        """
        media_list_for_CSV = {}

        # 掲載媒体情報(CSV出力用)を全件取得
        media_list_for_CSV = self.mapping(DtoMediaList.DtoMediaMasterList.DtoMediaMasterListForCSV, self.dao_m_media.selectCsvData())

        return self.unpack(media_list_for_CSV)