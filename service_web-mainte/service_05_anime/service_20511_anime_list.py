import csv

from admin_app.service.service_list import ServiceList

from admin_app.dao.dao_m_sakuhin import DaoMSakuhin
from admin_app.dao.dao_m_anime_title import DaoMAnimeTitle

from admin_app.dto.dto_main import DtoMain
from admin_app.dto.dto_05_anime.dto_20511_anime_list import DtoAnimeList

class AnimeListService(ServiceList):
    # 作品マスタテーブル用DAO
    dao_m_sakuhin = DaoMSakuhin()

    # アニメタイトル基本マスタテーブル用DAO
    dao_m_anime_title = DaoMAnimeTitle()

    '''初期描画'''
    def bizProcess(self, tableName):

        # 更新履歴
        notice_table = self.getnoticetable(tableName)

        # 領域用DTOを画面DTOに詰める
        dto_anime_list= DtoAnimeList(notice_table, {})

        return self.unpack(dto_anime_list)

    def getGridDataProcess(self, sakuhin_code):
        '''
        グリッド表示用アニメ情報取得
        ----------
        sakuhin_code : str
                作品コード
        '''

        grid_date = self.mapping(DtoAnimeList.DtoAnimeMasterList, self.dao_m_anime_title.selectAnimeMasterBySakuhinCode(sakuhin_code))
        return self.unpack(grid_date)
    
    def getCsvDataProcess(self):
        '''
        CSV出力用書籍情報取得
        ----------
        sakuhin_code : str
                作品コード
        '''

        csv_date = {}

        # アニメタイトル情報(CSV出力用)を全件取得
        csv_date = self.dao_m_anime_title.selectAnimeMasterforCSV()

        return csv_date

    def deleteAnimeProcess(self, sakuhin_code, anime_title_name, full_name):
        '''
        アプリ削除プロセス
        '''

        # 作品コードに合致するレコードを論理削除
        self.dao_m_anime_title.updateIsInvalidByTvProgramName(anime_title_name,full_name)

        # 変更履歴の登録
        # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
        entity = ('m_anime_title', '削除', anime_title_name, '', full_name)
        self.dao_t_update_history.insertTUpdateHistory(entity)

        # アプリマスタ一覧グリッドを更新
        grid_date = self.mapping(DtoAnimeList.DtoAnimeMasterList, self.dao_m_anime_title.selectAnimeMasterBySakuhinCode(sakuhin_code))

        return self.unpack(grid_date)


