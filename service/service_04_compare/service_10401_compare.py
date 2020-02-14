from typing import List
from ipdds_app.service.service_main import ServiceMain
from ipdds_app.dao.old_dao_m_ip import DaoMIp
from ipdds_app.dao.dao_m_sakuhin import DaoMSakuhin
from ipdds_app.dao.dao_m_seinendai import DaoMSeinendai
from ipdds_app.dao.dao_t_twitter import DaoTTwitter
from ipdds_app.dao.dao_t_isbn import DaoTIsbn
from ipdds_app.dao.dao_t_game import DaoTGame
from ipdds_app.dao.dao_t_app import DaoTApp

from ipdds_app.dto.dto_04_compare.dto_10401_compare import DtoSakuhinCompare

import datetime
from builtins import round

class SakuhinCompareService(ServiceMain):

    # dao_m_sakuhinテーブル用DAO
    dao_m_sakuhin = DaoMSakuhin()
    # dao_m_seinendaiテーブル用DAO
    dao_m_seinendai = DaoMSeinendai()
    # dao_t_twitterテーブル用DAO
    dao_t_twitter = DaoTTwitter()
    # dao_t_isbnテーブル用DAO
    dao_t_isbn = DaoTIsbn()
    # dao_t_gameテーブル用DAO
    dao_t_game = DaoTGame()
    # dao_t_appテーブル用DAO
    dao_t_app = DaoTApp()

    def bizProcess(self,sakuhin_code_list):

        '''
        各画面領域のデータを取得し領域用DTOに詰める
        '''
        if len(sakuhin_code_list) == 0 or not self.dao_m_sakuhin.selectCompareCountBySakuhinCode(sakuhin_code_list)[0][0]:
            return {'sakuhin_not_found':True}


        #年代別男女比情報取得
        dto_genderRatioDispList = []
        for dto_ratioForDao in self.mapping(DtoSakuhinCompare.DtoSakuhinCompareForDao.DtoGenderRatioForDao, self.dao_m_seinendai.selectCompareAgeAll(sakuhin_code_list)):
            genderRatio = self.createGenderRatioForDisp(dto_ratioForDao)
            dto_genderRatioDispList.append(genderRatio)

        #Twitter情報取得
        dto_twitterDispList = []
        for dto_twitterForDao in self.mapping(DtoSakuhinCompare.DtoSakuhinCompareForDao.DtoTwitterForDao, self.dao_m_sakuhin.selectCompareTwitter(sakuhin_code_list)):
            twitter = self.createTwitterForDisp(dto_twitterForDao)
            dto_twitterDispList.append(twitter)

        #マンガ情報取得
        dto_mangaDispList = []
        for dto_mangaForDao in self.mapping(DtoSakuhinCompare.DtoSakuhinCompareForDao.DtoMangaForDao, self.dao_m_sakuhin.selectCompareManga(sakuhin_code_list)):
            manga = self.createMangaForDisp(dto_mangaForDao)
            dto_mangaDispList.append(manga)

        #ゲーム情報取得
        dto_gameDispList = []
        for dto_gameForDao in self.mapping(DtoSakuhinCompare.DtoSakuhinCompareForDao.DtoGameForDao, self.dao_m_sakuhin.selectCompareGame(sakuhin_code_list)):
            game = self.createGameForDisp(dto_gameForDao)
            dto_gameDispList.append(game)

        #アプリ情報取得
        dto_appDispList = []
        for dto_appForDao in self.mapping(DtoSakuhinCompare.DtoSakuhinCompareForDao.DtoAppForDao, self.dao_m_sakuhin.selectCompareApp(sakuhin_code_list)):
            app = self.createAppForDisp(dto_appForDao)
            dto_appDispList.append(app)

        #比較画面作品名取得
        dto_compareSakuhinNameDispList = []
        for dto_sakuhinNameDao in self.mapping(DtoSakuhinCompare.DtoSakuhinCompareForDao.DtoSakuhinCompareForSakuhinNameDao, self.dao_m_sakuhin.selectCompareSakuhinName(sakuhin_code_list)):
            sakuhinName = self.createSakuhinNameForDisp(dto_sakuhinNameDao)
            dto_compareSakuhinNameDispList.append(sakuhinName)

        #画面用のDTOにデータを取り込む
        dto_SakuhinCompareForDisp = DtoSakuhinCompare.DtoSakuhinCompareForDisp(dto_genderRatioDispList,dto_twitterDispList,dto_mangaDispList,dto_gameDispList,dto_appDispList,dto_compareSakuhinNameDispList)

        return self.unpack(dto_SakuhinCompareForDisp)

    """
    画面表示用の年代別男女比情報を生成する
    @param dto_ratioForDao データベースから取得した年代別男女比情報:
    @return 画面表示用の年代別男女比情報
    """
    def createGenderRatioForDisp(self, dto_ratioForDao):

        #画面表示用の年代別男女比情報

        sakuhin_code = dto_ratioForDao.sakuhin_code
        sakuhin_name = dto_ratioForDao.sakuhin_name
        if dto_ratioForDao.total is None:
            total = 0
        else:
            total = "{:,}".format(dto_ratioForDao.total)

        male_under_10 = self.calcPercent(dto_ratioForDao.male_lteq10, dto_ratioForDao.female_lteq10)
        male_11_15 = self.calcPercent(dto_ratioForDao.male_11to15, dto_ratioForDao.female_11to15)
        male_16_20 = self.calcPercent(dto_ratioForDao.male_16to20, dto_ratioForDao.female_16to20)
        male_21_25 = self.calcPercent(dto_ratioForDao.male_21to25, dto_ratioForDao.female_21to25)
        male_26_30 = self.calcPercent(dto_ratioForDao.male_26to30, dto_ratioForDao.female_26to30)
        male_31_35 = self.calcPercent(dto_ratioForDao.male_31to35, dto_ratioForDao.female_31to35)
        male_36_40 = self.calcPercent(dto_ratioForDao.male_36to40, dto_ratioForDao.female_36to40)
        male_41_45 = self.calcPercent(dto_ratioForDao.male_41to45, dto_ratioForDao.female_41to45)
        male_46_50 = self.calcPercent(dto_ratioForDao.male_46to50, dto_ratioForDao.female_46to50)
        male_51_over = self.calcPercent(dto_ratioForDao.male_gteq51, dto_ratioForDao.female_gteq51)

        female_under_10 = self.calcPercent(dto_ratioForDao.female_lteq10,dto_ratioForDao.male_lteq10)
        female_11_15 = self.calcPercent(dto_ratioForDao.female_11to15,dto_ratioForDao.male_11to15)
        female_16_20 = self.calcPercent(dto_ratioForDao.female_16to20,dto_ratioForDao.male_16to20)
        female_21_25 = self.calcPercent(dto_ratioForDao.female_21to25,dto_ratioForDao.male_21to25)
        female_26_30 = self.calcPercent(dto_ratioForDao.female_26to30,dto_ratioForDao.male_26to30)
        female_31_35 = self.calcPercent(dto_ratioForDao.female_31to35,dto_ratioForDao.male_31to35)
        female_36_40 = self.calcPercent(dto_ratioForDao.female_36to40,dto_ratioForDao.male_36to40)
        female_41_45 = self.calcPercent(dto_ratioForDao.female_41to45,dto_ratioForDao.male_41to45)
        female_46_50 = self.calcPercent(dto_ratioForDao.female_46to50,dto_ratioForDao.male_46to50)
        female_51_over = self.calcPercent(dto_ratioForDao.female_gteq51,dto_ratioForDao.male_gteq51)

        genderRatio = DtoSakuhinCompare.DtoSakuhinCompareForDisp.DtoSakuhinCompareForGenderRatio(sakuhin_code,sakuhin_name,total,male_under_10,male_11_15,male_16_20,male_21_25,male_26_30,male_31_35,male_36_40,male_41_45,male_46_50,male_51_over,female_under_10,female_11_15,female_16_20,female_21_25,female_26_30,female_31_35,female_36_40,female_41_45,female_46_50,female_51_over)
        return genderRatio

    """
    パーセント演算
    数位1 ÷ (数値1 + 数値2) をパーセントに変換する
    @param num1 数値1
    @param num2 数値2
    """
    def calcPercent(self, num1, num2):
        if num1 is None:
            num1 = 0
        if num2 is None:
            num2 = 0
        if num1 + num2:
            total = num1 + num2
            quotient = round(num1 / total, 2)
            result = '{:.0%}'.format(quotient)
            return result
        else:
            return "-"

    """
    画面表示用のTwitter情報を生成する
    @param dto_twitterForDao データベースから取得したTwitter情報:
    @return 画面表示用のTwitter情報
    """
    def createTwitterForDisp(self, dto_twitterForDao):
        sakuhin_code = dto_twitterForDao.sakuhin_code
        sakuhin_name = dto_twitterForDao.sakuhin_name
        followers_latest = dto_twitterForDao.followers_latest
        followers_3months_ago = dto_twitterForDao.followers_3months_ago
        followers_1year_ago = dto_twitterForDao.followers_1year_ago
        user_name = dto_twitterForDao.user_name
        twitter_id = dto_twitterForDao.twitter_id

        twitter = DtoSakuhinCompare.DtoSakuhinCompareForDisp.DtoSakuhinCompareForTwitter(sakuhin_code,sakuhin_name,followers_latest,followers_3months_ago,followers_1year_ago,user_name,twitter_id)
        return twitter

    """
    画面表示用のManga情報を生成する
    @param dto_mangaForDao データベースから取得したManga情報:
    @return 画面表示用のManga情報
    """
    def createMangaForDisp(self, dto_mangaForDao):
        sakuhin_code = dto_mangaForDao.sakuhin_code
        sakuhin_name = dto_mangaForDao.sakuhin_name
        cumulative = dto_mangaForDao.cumulative
        cumulative_first = dto_mangaForDao.cumulative_first
        cumulative_latest = dto_mangaForDao.cumulative_latest
        average_1manga = dto_mangaForDao.average_1manga
        firstisbn = dto_mangaForDao.firstisbn
        latestisbn = dto_mangaForDao.latestisbn
        manga_name = dto_mangaForDao.manga_name
        manga_code = dto_mangaForDao.manga_code

        manga = DtoSakuhinCompare.DtoSakuhinCompareForDisp.DtoSakuhinCompareForManga(sakuhin_code,sakuhin_name,cumulative,cumulative_first,cumulative_latest,average_1manga,firstisbn,latestisbn,manga_name,manga_code)
        return manga

    """
    画面表示用のGame情報を生成する
    @param dto_gameForDao データベースから取得したGame情報:
    @return 画面表示用のGame情報
    """
    def createGameForDisp(self, dto_gameForDao):
        sakuhin_code = dto_gameForDao.sakuhin_code
        sakuhin_name = dto_gameForDao.sakuhin_name
        game_title_name = dto_gameForDao.game_title_name
        platform_name = dto_gameForDao.platform_name
        hanbai_company_name = dto_gameForDao.hanbai_company_name
        release_yyyymmdd = self.setDateFromat(dto_gameForDao.release_yyyymmdd)
        total_sales_cnt = dto_gameForDao.total_sales_cnt
        game_title_code = dto_gameForDao.game_title_code

        manga = DtoSakuhinCompare.DtoSakuhinCompareForDisp.DtoSakuhinCompareForGame(sakuhin_code,sakuhin_name,game_title_name,platform_name,hanbai_company_name,release_yyyymmdd,total_sales_cnt,game_title_code)
        return manga

    """
    日付のフォーマットを設定する
    """
    def setDateFromat(self,date):
        if date is None:
            return 'ー'
        else:
            date_yyyy = date[0:4]
            date_mm = date[4:6]
            date_yyyymmdd = date_yyyy + '年' + date_mm + '月'
            return date_yyyymmdd

    """
    画面表示用のApp情報を生成する
    @param dto_appForDao データベースから取得したApp情報:
    @return 画面表示用のApp情報
    """
    def createAppForDisp(self, dto_appForDao):
        sakuhin_code = dto_appForDao.sakuhin_code
        sakuhin_name = dto_appForDao.sakuhin_name
        app_title_name = dto_appForDao.app_title_name

        platform = self.setAppPlatform(dto_appForDao.app_id_ios,dto_appForDao.app_id_android)

        hanbai_company_name = dto_appForDao.hanbai_company_name
        service_start_yyyymmdd = self.setDateFromat(dto_appForDao.service_start_yyyymmdd)
        total_sales = dto_appForDao.total_sales
        total_download_cnt = dto_appForDao.total_download_cnt
        avg_sales = dto_appForDao.avg_sales
        avg_download_cnt = dto_appForDao.avg_download_cnt
        app_title_code = dto_appForDao.app_title_code
        app_id_ios = dto_appForDao.app_id_ios
        app_id_android = dto_appForDao.app_id_android

        app = DtoSakuhinCompare.DtoSakuhinCompareForDisp.DtoSakuhinCompareForApp(sakuhin_code,sakuhin_name,app_title_name,platform,hanbai_company_name,service_start_yyyymmdd,total_sales,total_download_cnt,avg_sales,avg_download_cnt,app_title_code,app_id_ios,app_id_android)
        return app
    
    """
    アプリ一覧プラットフォームの設定
    """
    def setAppPlatform(self,ios,android):
        if ios and android is not None:
            return 'IOS   Android'
        elif ios is not None:
            return 'IOS'
        elif android is not None:
            return 'Android'
        else:
            return 'ー'

    """
    画面表示用のSakuhinName情報を生成する
    @param dto_SakuhinNameForDao データベースから取得したSakuhinName情報:
    @return 画面表示用のSakuhinName情報
    """
    def createSakuhinNameForDisp(self, dto_SakuhinNameForDao):
        sakuhin_code = dto_SakuhinNameForDao.sakuhin_code
        sakuhin_name = dto_SakuhinNameForDao.sakuhin_name

        sakuhinName = DtoSakuhinCompare.DtoSakuhinCompareForDisp.DtoSakuhinCompareForSakuhinName(sakuhin_code,sakuhin_name)
        return sakuhinName

    """
    年代別男女比のグラフ表示用のデータを取得する
    """
    def get_gender_ratio(self,sakuhin_code):
        return self.dao_m_seinendai.selectCompareAgeBySakuhinCode(sakuhin_code)
    
    """
    Twitterのグラフ表示用のデータを取得する
    """
    def get_twitter(self,twitter_id):
        dto_resultGraphDataList = []
        for graph_data in self.mapping(DtoSakuhinCompare.DtoSakuhinCompareForDao.DtoForDate2NotNullDao,self.dao_t_twitter.selectTwitterGraphData(twitter_id)):
            result_graphdata = self.checkData2IsNotNull(graph_data)
            dto_resultGraphDataList.append(result_graphdata)
        return dto_resultGraphDataList

    """
    マンガのグラフ1（累計発行部数（発売日からNか月））とグラフ２（平均発行部数（単巻あたり）（発売日からNか月））表示用のデータを取得する
    """
    def get_manga1(self,manga_code):
        # 発売日を取得
        service_date = self.setMangaServiceStartDate(manga_code)
        # 累計発行部数（発売日からN月）と平均発行部数（単巻あたり）（発売日からNか月）のデータを取得
        dto_resultGraphDataList = []
        for graph_data in self.mapping(DtoSakuhinCompare.DtoSakuhinCompareForDao.DtoForDate3NotNullDao,self.dao_t_isbn.selectMangaTotalAndAvgServiceStartDateGraphData(manga_code,service_date)):
            result_graphdata = self.checkData3IsNotNull(graph_data)
            dto_resultGraphDataList.append(result_graphdata)
        return dto_resultGraphDataList

    """
    マンガのグラフ3（累計発行部数）とグラフ6平均発行部数（単巻あたり）（直近一年間）表示用のデータを取得する
    """
    def get_manga3(self,manga_code):
        # 発売日を取得
        service_date = self.setMangaServiceStartDate(manga_code)
        # 累計発行部数と平均発行部数（単巻あたり）のデータを取得
        dto_resultGraphDataList = []
        for graph_data in self.mapping(DtoSakuhinCompare.DtoSakuhinCompareForDao.DtoForDate3NotNullDao,self.dao_t_isbn.selectMangaTotalAndAvgNowDayGraphData(manga_code,service_date)):
            result_graphdata = self.checkData3IsNotNull(graph_data)
            dto_resultGraphDataList.append(result_graphdata)
        return dto_resultGraphDataList

    """
    マンガのグラフ4（累計発行部数）（1巻）表示用のデータを取得する
    """
    def get_manga4(self,manga_code):
        # 1巻のIsbnを取得
        firstisbn = self.mapping(DtoSakuhinCompare.DtoSakuhinCompareForDao.DtoFirstIsbnForDao,self.dao_t_isbn.selectServiceStartDateIsbnData(manga_code))
        if not firstisbn:
            return []
        tmpfirstisbn = firstisbn[0].firstisbn
        tmpfirstmangaissuedate = firstisbn[0].manga_issue_date
        # 累計発行部数（1巻）のデータを取得
        dto_resultGraphDataList = []
        for graph_data in self.mapping(DtoSakuhinCompare.DtoSakuhinCompareForDao.DtoForDate2NotNullDao,self.dao_t_isbn.selectCompareGraphData(tmpfirstisbn,tmpfirstmangaissuedate)):
            result_graphdata = self.checkData2IsNotNull(graph_data)
            dto_resultGraphDataList.append(result_graphdata)
        return dto_resultGraphDataList

    """
    マンガのグラフ5（累計発行部数）（最新巻）表示用のデータを取得する
    """
    def get_manga5(self,manga_code):
        # 最新巻のIsbnを取得
        latestisbn = self.mapping(DtoSakuhinCompare.DtoSakuhinCompareForDao.DtolatestIsbnForDao,self.dao_t_isbn.selectLatestIsbnData(manga_code))
        if not latestisbn:
            return []
        tmplatestisbn = latestisbn[0].latestisbn
        tmpmangaissuedate = latestisbn[0].manga_issue_date
        # 累計発行部数（最新巻）のデータを取得
        dto_resultGraphDataList = []
        for graph_data in self.mapping(DtoSakuhinCompare.DtoSakuhinCompareForDao.DtoForDate2NotNullDao,self.dao_t_isbn.selectCompareGraphData(tmplatestisbn,tmpmangaissuedate)):
            result_graphdata = self.checkData2IsNotNull(graph_data)
            dto_resultGraphDataList.append(result_graphdata)
        return dto_resultGraphDataList

    """
    ゲームのグラフ1（累計売上本数）（発売日からNか月）表示用のデータを取得する
    """
    def get_game1(self,game_title_code):
        # 発売年月日を取得
        service_date = self.setGameServiceStartDate(game_title_code)
        # 累計売上本数(発売日からNか月)のデータを取得
        dto_resultGraphDataList = []
        for graph_data in self.mapping(DtoSakuhinCompare.DtoSakuhinCompareForDao.DtoForDate2NotNullDao,self.dao_t_game.selectFromServiceStartDateGraphData(service_date,game_title_code)):
            result_graphdata = self.checkData2IsNotNull(graph_data)
            dto_resultGraphDataList.append(result_graphdata)
        return dto_resultGraphDataList

    """
    ゲームのグラフ2（累計売上本数）表示用のデータを取得する
    """
    def get_game2(self,game_title_code):
        # 発売年月日を取得
        service_date = self.setGameServiceStartDate(game_title_code)
        # 累計売上本数のデータを取得
        dto_resultGraphDataList = []
        for graph_data in self.mapping(DtoSakuhinCompare.DtoSakuhinCompareForDao.DtoForDate2NotNullDao,self.dao_t_game.selectGameTotleSalesGraphData(service_date,game_title_code)):
            result_graphdata = self.checkData2IsNotNull(graph_data)
            dto_resultGraphDataList.append(result_graphdata)
        return dto_resultGraphDataList

    """
    アプリの累計売上グラフ1（累計売上（発売日からNか月））表示用のデータを取得する
    """
    def get_appSales1(self,app_title_code,app_title_name,app_id_ios,app_id_android):
        # 発売年月日を取得
        service_date = self.setAppServiceStartDate(app_title_code)
        # 累計売上(発売日からNか月)のデータを取得
        dto_resultGraphDataList = []
        for graph_data in self.mapping(DtoSakuhinCompare.DtoSakuhinCompareForDao.DtoForDate2NotNullDao,self.dao_t_app.selectAppFromServiceStartDateSalesGraphData(service_date,app_title_name,app_id_ios,app_id_android)):
            result_graphdata = self.checkData2IsNotNull(graph_data)
            dto_resultGraphDataList.append(result_graphdata)
        return dto_resultGraphDataList

    """
    アプリの累計売上グラフ2（累計売上）表示用のデータを取得する
    """
    def get_appSales2(self,app_title_code,app_title_name,app_id_ios,app_id_android):
        # 発売年月日を取得
        service_date = self.setAppServiceStartDate(app_title_code)
        dto_resultGraphDataList = []
        for graph_data in self.mapping(DtoSakuhinCompare.DtoSakuhinCompareForDao.DtoForDate2NotNullDao,self.dao_t_app.selectAppTotalSalesGraphData(service_date,app_title_name,app_id_ios,app_id_android)):
            result_graphdata = self.checkData2IsNotNull(graph_data)
            dto_resultGraphDataList.append(result_graphdata)
        return dto_resultGraphDataList

    """
    アプリの平均売上グラフと平均ダウンロード数グラフ表示用のデータを取得する
    """
    def get_appAvgSales_download(self,app_title_code,app_title_name,app_id_ios,app_id_android):
        # 発売年月日を取得
        service_date = self.setAppServiceStartDate(app_title_code)
        # 平均売上と平均ダウンロード数のデータを取得
        dto_resultGraphDataList = []
        for graph_data in self.mapping(DtoSakuhinCompare.DtoSakuhinCompareForDao.DtoForDate3NotNullDao,self.dao_t_app.selectAppAvgSalesAndDownloadGraphData(service_date,app_title_name,app_id_ios,app_id_android)):
            result_graphdata = self.checkData3IsNotNull(graph_data)
            dto_resultGraphDataList.append(result_graphdata)
        return dto_resultGraphDataList

    """
    アプリの累計ダウンロードグラフ（ダウンロード（発売日からNか月））表示用のデータを取得する
    """
    def get_appDownload1(self,app_title_code,app_title_name,app_id_ios,app_id_android):
        # 発売年月日を取得
        service_date = self.setAppServiceStartDate(app_title_code)
        # 累計ダウンロード(発売日からNか月)のデータを取得
        dto_resultGraphDataList = []
        for graph_data in self.mapping(DtoSakuhinCompare.DtoSakuhinCompareForDao.DtoForDate2NotNullDao,self.dao_t_app.selectAppFromServiceStartDateDownloadGraphData(service_date,app_title_name,app_id_ios,app_id_android)):
            result_graphdata = self.checkData2IsNotNull(graph_data)
            dto_resultGraphDataList.append(result_graphdata)
        return dto_resultGraphDataList

    """
    アプリの累計ダウンロードグラフ表示用のデータを取得する
    """
    def get_appDownload2(self,app_title_code,app_title_name,app_id_ios,app_id_android):
        # 発売年月日を取得
        service_date = self.setAppServiceStartDate(app_title_code)
        # 累計ダウンロードのデータを取得
        dto_resultGraphDataList = []
        for graph_data in self.mapping(DtoSakuhinCompare.DtoSakuhinCompareForDao.DtoForDate2NotNullDao,self.dao_t_app.selectAppTotalDownloadGraphData(service_date,app_title_name,app_id_ios,app_id_android)):
            result_graphdata = self.checkData2IsNotNull(graph_data)
            dto_resultGraphDataList.append(result_graphdata)
        return dto_resultGraphDataList

    """
    グラフデータがnullがある場合、「0」に変更する
    @param graph_data データベースから取得したデータ
    @return グラフ表示用データ
    """       
    def checkData2IsNotNull(self, graph_data):
        result_yyyymm = graph_data.result_yyyymm
        if graph_data.result_data is None:
            result_data  = 0
        else:
            result_data = graph_data.result_data
            
        result_graphdata = DtoSakuhinCompare.DtoSakuhinCompareForDao.DtoForDate2NotNullDao(result_yyyymm,result_data)
        return result_graphdata

    """
    グラフデータがnullがある場合、「0」に変更する(アプリグラフ５とアプリグラフ６用))
    @param graph_data データベースから取得したデータ
    @return グラフ表示用データ
    """       
    def checkData3IsNotNull(self, graph_data):
        result_yyyymm = graph_data.result_yyyymm
        if graph_data.avg_sales is None:
            avg_sales  = 0
        else:
            avg_sales = graph_data.avg_sales

        if graph_data.avg_count is None:
            avg_count  = 0
        else:
            avg_count = graph_data.avg_count

        result_graphdata = DtoSakuhinCompare.DtoSakuhinCompareForDao.DtoForDate3NotNullDao(result_yyyymm,avg_sales,avg_count)
        return result_graphdata

    """
    マンガのサービス年月日を取得する
    """
    def setMangaServiceStartDate(self,manga_code):
        # 発売年月日を取得
        service_date = self.mapping(DtoSakuhinCompare.DtoSakuhinCompareForDao.DtoForServiceStartDate,self.dao_t_isbn.selectMangaServiceStartDate(manga_code))
        if not service_date:
            return []
        else:
            tmpDate = service_date[0].service_date
            return tmpDate

    """
    ゲームのサービス年月日を取得する
    """
    def setGameServiceStartDate(self,game_title_code):
        # 発売年月日を取得
        service_date = self.mapping(DtoSakuhinCompare.DtoSakuhinCompareForDao.DtoForServiceStartDate,self.dao_t_game.selectGameServiceStartDate(game_title_code))
        if not service_date:
            return []
        else:
            tmpDate = service_date[0].service_date
            return tmpDate

    """
    アプリのサービス年月日を取得する
    """
    def setAppServiceStartDate(self,app_title_code):
        # 発売年月日を取得
        service_date = self.mapping(DtoSakuhinCompare.DtoSakuhinCompareForDao.DtoForServiceStartDate,self.dao_t_app.selectAppServiceStartDate(app_title_code))
        if not service_date:
            return []
        else:
            tmpDate = service_date[0].service_date
            return tmpDate