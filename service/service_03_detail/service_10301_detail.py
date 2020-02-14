from ipdds_app.service.service_main import ServiceMain

from ipdds_app.dao.dao_m_sakuhin import DaoMSakuhin
from ipdds_app.dao.dao_m_anime_title import DaoMAnime
from ipdds_app.dao.dao_m_manga_title import DaoMMangaTitle
from ipdds_app.dao.dao_m_manga_isbn import DaoMMangaIsbn
from ipdds_app.dao.dao_m_media_report import DaoMMediaReport
from ipdds_app.dao.dao_m_seinendai import DaoMSeinendai
from ipdds_app.dao.dao_m_heibai import DaoMHeibai
from ipdds_app.dao.dao_m_sakuhin_tag import DaoMSakuhinTag
from ipdds_app.dao.dao_m_core import DaoMCore
from ipdds_app.dao.dao_m_media import DaoMMedia
from ipdds_app.dao.dao_t_twitter import DaoTTwitter
from ipdds_app.dao.dao_t_isbn import DaoTIsbn
from ipdds_app.dao.dao_m_game_title import DaoMGame
from ipdds_app.dao.dao_t_game import DaoTGame
from ipdds_app.dao.dao_m_app_title import DaoMApp
from ipdds_app.dao.dao_t_app import DaoTApp

from ipdds_app.dto.dto_main import DtoGraphData
from ipdds_app.dto.dto_05_search.dto_10502_search_result import DtoSearchResult
from ipdds_app.dto.dto_03_detail.dto_10301_detail import DtoDetail

import datetime
from dateutil.relativedelta import relativedelta

class DetailService(ServiceMain):

    # m_sakuhinテーブル用DAO
    dao_m_sakuhin = DaoMSakuhin()
    # m_anime_titleテーブル用DAO
    dao_m_anime_title = DaoMAnime()
    # m_mangaテーブル用DAO
    dao_m_manga_title = DaoMMangaTitle()
    # m_manga_isbnテーブル用DAO
    dao_m_manga_isbn = DaoMMangaIsbn()
    # m_media_reportテーブル用DAO
    dao_m_media_report = DaoMMediaReport()
    # dao_m_seinendaiテーブル用DAO
    dao_m_seinendai = DaoMSeinendai()
    # dao_m_heibaiテーブル用DAO
    dao_m_heibai = DaoMHeibai()
    dao_m_sakuhin_tag = DaoMSakuhinTag()
    dao_m_core = DaoMCore()
    dao_m_media = DaoMMedia()

    # t_twitterテーブル用DAO
    dao_t_twitter = DaoTTwitter()
    # t_isbnテーブル用DAO
    dao_t_isbn = DaoTIsbn()
    # m_game_titleテーブル用DAO
    dao_m_game_title = DaoMGame()
    # t_gameテーブル用DAO
    dao_t_game = DaoTGame()
    # m_app_titleテーブル用DAO
    dao_m_app_title = DaoMApp()
    # t_appテーブル用DAO
    dao_t_app = DaoTApp()

    """
    業務処理
    @param sakuhin_code 作品コード
    @return 詳細画面DTO
    """
    def bizProcess(self,sakuhin_code):

        '''
        各画面領域のデータを取得し領域用DTOに詰める
        '''
        if not self.dao_m_sakuhin.selectCountBySakuhinCode(sakuhin_code)[0][0]:
            return {'sakuhin_not_found':True}

        # 作品概要
        tmp_sakuhin_data = self.dao_m_sakuhin.selectDetailBySakuhinCode(sakuhin_code)[0]
        sakuhin_data = self.dtoMapping(tmp_sakuhin_data)

        # 領域用DTOを画面DTOに詰める
        dto_detail = DtoDetail(
                                sakuhin_data #作品単位のデータ
                            )
        return self.unpack(dto_detail)

    """
    取得結果をdtoにマッピングする処理
    @param resultSakuhin 検索結果(1Sakuhin)
    @return 詳細情報（作品単位のデータ)
    """
    def dtoMapping(self, resultSakuhin):
        return DtoDetail.DtoSakuhinData(resultSakuhin[0] # キービジュアルファイル名
                                        ,resultSakuhin[1] # 作品コード
                                        ,resultSakuhin[2] # 作品名
                                        ,resultSakuhin[3] # 作品かな名
                                        ,resultSakuhin[4] # あらすじ
                                        ,resultSakuhin[5] # 発表年月日
                                        ,resultSakuhin[6] # 更新日付
                                        ,resultSakuhin[7] # 国外窓口
                                        ,resultSakuhin[8] # 国内窓口
                                        ,resultSakuhin[9] # メモ
                                        )

    """
    作品コードをもとにアニメ情報を取得
    @param sakuhin_code 作品コード
    @return アニメ情報
    """
    def getAnime(self,sakuhin_code):
        # アニメ情報の取得(アニメタイトル名,放送期間,放送局)
        return self.dao_m_anime_title.selectBroadCastBySakuhinCode(sakuhin_code)

    def getBunrui(self,sakuhin_code):
        # 分類タグ
        return self.dao_m_sakuhin.selectBunruiTag(sakuhin_code)

    def getMedia(self,sakuhin_code):
        # 掲載媒体：全件表示
        return self.dao_m_media.selectMediaBySakuhinCode(sakuhin_code)

    def getCore(self,sakuhin_code):
        # コアタグ：メインとなるデータのみ表示
        return self.dao_m_core.selectCore(sakuhin_code)

    def getTag(self,sakuhin_code):
        # 事実タグ：出現回数の多い5要素のみ表示する
        return self.dao_m_sakuhin_tag.selectTag(sakuhin_code)

    def getRuiji(self,sakuhin_code,tag_code_list):
        # 類似作品：
        return self.dao_m_manga_title.selectSimilarSakuhinByFactCode(tag_code_list,sakuhin_code)


    """
    作品コードをもとに値を合計した年代別男女比情報を取得する
    @param sakuhin_code 作品コード
    @return 年代別男女比情報
    """
    def getGenderRatio(self,sakuhin_code):
        # 年代別男女比情報の取得
        return self.dao_m_seinendai.selectDetailBySakuhinCode(sakuhin_code)

    """
    作品コードをもとにタイトルコードを取得する
    """
    def getHeibai(self,sakuhin_code):
        return self.dao_m_manga_title.selectMangaCode(sakuhin_code)

    """
    タイトルコードをもとに併売データを全件取得する
    """
    def getHeibaiData(self,title_code):
        # 併売情報の取得
        heibai_data = []
        for i in range(1,16,1):
            heibai_data += self.dao_m_heibai.selectHeibaiDataByTitleCode(title_code,i)
        return heibai_data
    """
    作品コードをもとに関連文書情報を取得
    @param sakuhin_code 作品コード
    @return 関連文書情報
    """
    def getRelatedDocuments(self,sakuhin_code):
        # 関連文書の取得(年代,カテゴリ,出版社)
        return self.dao_m_media_report.selectRelatedDocumentsBySakuhinCode(sakuhin_code)

    """
    作品コードをもとにマンガコードを取得
    @param sakuhin_code 作品コード
    @returnマンガコード
    """
    def getManga(self,sakuhin_code):
        # マンガコードの取得
        return self.dao_m_manga_title.selectMangaCode(sakuhin_code)

    """
    マンガタイトルコードをもとにGrid用のデータを取得
    @param title_coide マンガタイトルコード
    @return Grid用マンガ基本情報
    """
    def getMangaData(self,title_code):
        # マンガ基本情報の取得
        return self.dao_m_manga_title.selectMangaData(title_code)

    """
    マンガタイトルコードをもとにGrid用のデータを取得
    @param title_coide マンガタイトルコード
    @return Grid用マンガ実績情報
    """
    def getMangaIsbnData(self,title_code):
        # マンガ実績情報の取得
        return self.dao_m_manga_isbn.selectMangaIsbn(title_code)

    """
    マンガタイトルコードをもとにplot用のデータを取得
    @param title_coide マンガタイトルコード
    @return plot用マンガ売上
    """
    def getMangaGraphData(self,title_code):
        # マンガグラフ用データの取得
        # return self.dao_m_manga_isbn.selectGraphData(title_code)
        return self.dao_m_manga_isbn.selectGraphDataForTotalSales(title_code)

    """
    作品コードをもとにtwitterコードを取得
    @param sakuhin_code 作品コード
    @return twitterコード
    """
    def getTwitterDataBySakuhinCode(self,sakuhin_code):
        # twitterコードの取得
        return self.dao_t_twitter.selectTwitterData(sakuhin_code)

    """
    twitter_idをもとにGrid用のデータを取得
    @param twitter_id ツイッターID
    @return Grid用twitter実績
    """
    def getTwitterDataByTwitterId(self,twitter_id):
        # twitter実績データの取得
        return self.dao_t_twitter.selectTwitterZissekiData(twitter_id)

    """
    twitter_idをもとにPlot用のデータを取得
    @param twitter_id ツイッターID
    @return Plot用twitter実績
    """
    def getTwitterGraphDataByTwitterId(self,twitter_id):
        # twitter実績データの取得
        return self.dao_t_twitter.selectGraphData(twitter_id)

    """
    作品コードをもとにゲームタイトルコードを取得
    @param sakuhin_code 作品コード
    @return ゲームタイトルコード
    """
    def getGameBySakuhinCode(self,sakuhin_code):
        # ゲームタイトルコードの取得
        return self.dao_m_game_title.selectGame(sakuhin_code)

    """
    ゲームタイトルコードをもとにGrid用のデータを取得
    @param title_code ゲームタイトルコード
    @return Grid用ゲーム実績
    """
    def getGameDataByTitleCode(self,title_code):
        # ゲームデータの取得
        return self.dao_m_game_title.selectGameDataByTitleCode(title_code)

    """
    ゲームタイトルコードをもとにPlot用のデータを取得
    @param title_code ゲームタイトルコード
    @return Plot用ゲーム実績
    """
    def getGameGraphDataByTitleCode(self,title_code):
        # ゲームデータの取得
        return self.dao_t_game.selectGraphData(title_code)

    """
    作品コードをもとにアプリタイトルコードを取得
    @param sakuhin_code 作品コード
    @return アプリタイトルコード
    """
    def getAppBySakuhinData(self,sakuhin_code):
        # アプリ情報の取得
        return self.dao_m_app_title.selectApp(sakuhin_code)

    """
    アプリタイトルコードをもとにGrid用データを取得
    @param title_code アプリタイトルコード
    @return Grid用アプリ基本情報
    """
    def getAppDataByTitleCode(self,title_code,app_id_ios,app_id_android):
        # アプリ基本情報の取得
        return self.dao_m_app_title.selectAppData(title_code,app_id_ios,app_id_android)

    """
    アプリIDをもとにPlot用のダウンロード数データを取得
    @param app_id_ios アプリID_ios
    @param app_id_android アプリID_android
    @return Plot用ダウンロード数
    """
    def getAppGraphDataForDownload(self,app_id_ios,app_id_android):
        # アプリIDと紐づくアプリのダウンロード数を取得する
        return self.dao_t_app.selectGraphData(app_id_ios,app_id_android,'download_cnt')

    """
    アプリIDをもとにPlot用の収益データを取得
    @param app_id_ios アプリID_ios
    @param app_id_android アプリID_android
    @return Plot用収益データ
    """
    def getAppGraphDataForMonthlySales(self,app_id_ios,app_id_android):
        # アプリIDと紐づくアプリの収益データを取得する
        return self.dao_t_app.selectGraphData(app_id_ios,app_id_android,'monthly_sales_gaku')
