from typing import List
from ipdds_app.service.service_main import ServiceMain
from ipdds_app.dao.dao_m_ip import DaoMIp
from ipdds_app.dao.dao_m_gender_ratio import DaoGenderRatio
from ipdds_app.dao.dao_t_twitter import DaoTTwitter
from ipdds_app.dao.dao_t_book import DaoTBook
from ipdds_app.dao.dao_t_pkg_soft import DaoTPkgSoft
from ipdds_app.dao.dao_t_mobile_app import DaoTMobileApp

from ipdds_app.dto.dto_04_compare import DtoIpCompare

import datetime
from builtins import round

class IpCompareService(ServiceMain):

    # m_ipテーブル用DAO
    dao_m_ip = DaoMIp()
    # dao_m_gender_ratioテーブル用DAO
    dao_m_gender_ratio = DaoGenderRatio()
    # dao_t_twitterテーブル用DAO
    dao_t_twitter = DaoTTwitter()
    # dao_t_bookテーブル用DAO
    dao_t_book = DaoTBook()
    # dao_t_pkg_softテーブル用DAO
    dao_t_pkg_soft = DaoTPkgSoft()
    # dao_t_mobile_appテーブル用DAO
    dao_t_mobile_app = DaoTMobileApp()


    def bizProcess(self,ip_code_list):

        '''
        各画面領域のデータを取得し領域用DTOに詰める
        '''
        if len(ip_code_list) == 0 or not self.dao_m_ip.selectCompareCountByIpCode(ip_code_list)[0][0]:
            return {'ip_not_found':True}


        #年代別男女比情報取得
        dto_genderRatioDispList = []
        for dto_ratioForDao in self.mapping(DtoIpCompare.DtoIpCompareForDao.DtoGenderRatioForDao, self.dao_m_gender_ratio.selectCompareAgeAll(ip_code_list)):
            genderRatio = self.createGenderRatioForDisp(dto_ratioForDao)
            dto_genderRatioDispList.append(genderRatio)

        #Twitter情報取得
        dto_twitterDispList = []
        for dto_twitterForDao in self.mapping(DtoIpCompare.DtoIpCompareForDao.DtoTwitterForDao, self.dao_m_ip.selectCompareTwitter(ip_code_list)):
            twitter = self.createTwitterForDisp(dto_twitterForDao)
            dto_twitterDispList.append(twitter)

        #マンガ情報取得
        dto_bookDispList = []
        for dto_bookForDao in self.mapping(DtoIpCompare.DtoIpCompareForDao.DtoBookForDao, self.dao_m_ip.selectCompareBook(ip_code_list)):
            book = self.createBookForDisp(dto_bookForDao)
            dto_bookDispList.append(book)

        #ゲーム情報取得
        dto_gameDispList = []
        for dto_gameForDao in self.mapping(DtoIpCompare.DtoIpCompareForDao.DtoGameForDao, self.dao_m_ip.selectCompareGame(ip_code_list)):
            game = self.createGameForDisp(dto_gameForDao)
            dto_gameDispList.append(game)

        #アプリ情報取得
        dto_appDispList = []
        for dto_appForDao in self.mapping(DtoIpCompare.DtoIpCompareForDao.DtoAppForDao, self.dao_m_ip.selectCompareApp(ip_code_list)):
            app = self.createAppForDisp(dto_appForDao)
            dto_appDispList.append(app)

        #比較画面Ip名取得
        dto_compareIpNameDispList = []
        for dto_ipNameDao in self.mapping(DtoIpCompare.DtoIpCompareForDao.DtoIpCompareForIpNameDao, self.dao_m_ip.selectCompareIpName(ip_code_list)):
            ipName = self.createIpNameForDisp(dto_ipNameDao)
            dto_compareIpNameDispList.append(ipName)


        #画面用のDTOにデータを取り込む
        dto_IpCompareForDisp = DtoIpCompare.DtoIpCompareForDisp(dto_genderRatioDispList,dto_twitterDispList,dto_bookDispList,dto_gameDispList,dto_appDispList,dto_compareIpNameDispList)

        return self.unpack(dto_IpCompareForDisp)

    """
    画面表示用の年代別男女比情報を生成する
    @param dto_ratioForDao データベースから取得した年代別男女比情報:
    @return 画面表示用の年代別男女比情報
    """
    def createGenderRatioForDisp(self, dto_ratioForDao):

        #画面表示用の年代別男女比情報

        ip_code = dto_ratioForDao.ip_code
        ip_name = dto_ratioForDao.ip_name
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

        genderRatio = DtoIpCompare.DtoIpCompareForDisp.DtoIpCompareForGenderRatio(ip_code,ip_name,total,male_under_10,male_11_15,male_16_20,male_21_25,male_26_30,male_31_35,male_36_40,male_41_45,male_46_50,male_51_over,female_under_10,female_11_15,female_16_20,female_21_25,female_26_30,female_31_35,female_36_40,female_41_45,female_46_50,female_51_over)
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
        ip_code = dto_twitterForDao.ip_code
        ip_name = dto_twitterForDao.ip_name
        followers_latest = dto_twitterForDao.followers_latest
        followers_3months_ago = dto_twitterForDao.followers_3months_ago
        followers_1year_ago = dto_twitterForDao.followers_1year_ago
        user_name = dto_twitterForDao.user_name
        twitter_id = dto_twitterForDao.twitter_id

        twitter = DtoIpCompare.DtoIpCompareForDisp.DtoIpCompareForTwitter(ip_code,ip_name,followers_latest,followers_3months_ago,followers_1year_ago,user_name,twitter_id)
        return twitter

    """
    画面表示用のBook情報を生成する
    @param dto_bookForDao データベースから取得したBook情報:
    @return 画面表示用のBook情報
    """
    def createBookForDisp(self, dto_bookForDao):
        ip_code = dto_bookForDao.ip_code
        ip_name = dto_bookForDao.ip_name
        cumulative = dto_bookForDao.cumulative
        cumulative_first = dto_bookForDao.cumulative_first
        cumulative_latest = dto_bookForDao.cumulative_latest
        average_1book = dto_bookForDao.average_1book
        firstisbn = dto_bookForDao.firstisbn
        latestisbn = dto_bookForDao.latestisbn

        book = DtoIpCompare.DtoIpCompareForDisp.DtoIpCompareForBook(ip_code,ip_name,cumulative,cumulative_first,cumulative_latest,average_1book,firstisbn,latestisbn)
        return book

    """
    画面表示用のGame情報を生成する
    @param dto_gameForDao データベースから取得したGame情報:
    @return 画面表示用のGame情報
    """
    def createGameForDisp(self, dto_gameForDao):
        ip_code = dto_gameForDao.ip_code
        ip_name = dto_gameForDao.ip_name
        pkg_soft_name = dto_gameForDao.pkg_soft_name
        platform_name = dto_gameForDao.platform_name
        distributor_name = dto_gameForDao.distributor_name
        release_date = dto_gameForDao.release_date
        qty_total_sales = dto_gameForDao.qty_total_sales
        pkg_soft_code = dto_gameForDao.pkg_soft_code

        book = DtoIpCompare.DtoIpCompareForDisp.DtoIpCompareForGame(ip_code,ip_name,pkg_soft_name,platform_name,distributor_name,release_date,qty_total_sales,pkg_soft_code)
        return book

    """
    画面表示用のApp情報を生成する
    @param dto_appForDao データベースから取得したApp情報:
    @return 画面表示用のApp情報
    """
    def createAppForDisp(self, dto_appForDao):
        ip_code = dto_appForDao.ip_code
        ip_name = dto_appForDao.ip_name
        app_name = dto_appForDao.app_name
        platform = dto_appForDao.platform
        distributor_name = dto_appForDao.distributor_name
        release_date = dto_appForDao.release_date
        total_sales = dto_appForDao.total_sales
        total_download_count = dto_appForDao.total_download_count
        avg_sales = dto_appForDao.avg_sales
        avg_download_count = dto_appForDao.avg_download_count
        app_id_ios = dto_appForDao.app_id_ios
        app_id_android = dto_appForDao.app_id_android
        service_start_date = dto_appForDao.service_start_date

        app = DtoIpCompare.DtoIpCompareForDisp.DtoIpCompareForApp(ip_code,ip_name,app_name,platform,distributor_name,release_date,total_sales,total_download_count,avg_sales,avg_download_count,app_id_ios,app_id_android,service_start_date)
        return app

        """
    画面表示用のIpName情報を生成する
    @param dto_IpNameForDao データベースから取得したIpName情報:
    @return 画面表示用のIpName情報
    """
    def createIpNameForDisp(self, dto_IpNameForDao):
        ip_code = dto_IpNameForDao.ip_code
        ip_name = dto_IpNameForDao.ip_name

        ipName = DtoIpCompare.DtoIpCompareForDisp.DtoIpCompareForIpName(ip_code,ip_name)
        return ipName

    """
    年代別男女比のグラフ表示用のデータを取得する
    """
    def get_gender_ratio(self,ip_code):
        return self.dao_m_gender_ratio.selectCompareAgeByIpCode(ip_code)
    
    """
    Twitterのグラフ表示用のデータを取得する
    """
    def get_twitter(self,twitter_id):
        dto_resultGraphDataList = []
        for graph_data in self.mapping(DtoIpCompare.DtoIpCompareForDao.DtoIpCompareForDateNotNullDao,self.dao_t_twitter.selectGraphData(twitter_id)):
            result_graphdata = self.checkGraphDataIsNotNull(graph_data)
            dto_resultGraphDataList.append(result_graphdata)
        return dto_resultGraphDataList

    """
    マンガのグラフ1（累計発行部数（発売日からNか月））とグラフ２（平均発行部数（単巻あたり）（発売日からNか月））表示用のデータを取得する
    """
    def get_book1(self,ip_code):
        # 発売日を取得
        firstDay = self.mapping(DtoIpCompare.DtoIpCompareForDao.DtoFirstDayForDao,self.dao_t_book.selectFirstDayData(ip_code))
        tmp = firstDay[0].firstday
        if tmp is None :
            return []
        # 累計発行部数（発売日からN月）と平均発行部数（単巻あたり）（発売日からNか月）のデータを取得
        dto_resultGraphDataList = []
        for graph_data in self.mapping(DtoIpCompare.DtoIpCompareForDao.DtoIpCompareForDateNotNullAppSalesDao,self.dao_t_book.selectBookTotalAndAvgFirstDayGraphData(ip_code,tmp)):
            result_graphdata = self.checkAppGraph5DataIsNotNull(graph_data)
            dto_resultGraphDataList.append(result_graphdata)
        print(dto_resultGraphDataList)
        return dto_resultGraphDataList

    """
    マンガのグラフ3（累計発行部数）とグラフ6平均発行部数（単巻あたり）（直近一年間）表示用のデータを取得する
    """
    def get_book3(self,ip_code):
        # 発売日を取得
        firstDay = self.mapping(DtoIpCompare.DtoIpCompareForDao.DtoFirstDayForDao,self.dao_t_book.selectFirstDayData(ip_code))
        tmp = firstDay[0].firstday
        if tmp is None :
            return []
        # 累計発行部数と平均発行部数（単巻あたり）のデータを取得
        dto_resultGraphDataList = []
        for graph_data in self.mapping(DtoIpCompare.DtoIpCompareForDao.DtoIpCompareForDateNotNullAppSalesDao,self.dao_t_book.selectBookTotalAndAvgNowDayGraphData(ip_code,tmp)):
            result_graphdata = self.checkAppGraph5DataIsNotNull(graph_data)
            dto_resultGraphDataList.append(result_graphdata)
        return dto_resultGraphDataList

    """
    マンガのグラフ4（累計発行部数）（1巻）表示用のデータを取得する
    """
    def get_book4(self,ip_code):
        # 1巻のIsbnを取得
        firstisbn = self.mapping(DtoIpCompare.DtoIpCompareForDao.DtoFirstIsbnForDao,self.dao_t_book.selectFirstIsbnData(ip_code))
        if not firstisbn:
            return []
        tmpfirstisbn = firstisbn[0].firstisbn
        tmpfirstbookissuedate = firstisbn[0].book_issue_date
        # 累計発行部数（1巻）のデータを取得
        dto_resultGraphDataList = []
        for graph_data in self.mapping(DtoIpCompare.DtoIpCompareForDao.DtoIpCompareForDateNotNullDao,self.dao_t_book.selectCompareGraphData(tmpfirstisbn,tmpfirstbookissuedate)):
            result_graphdata = self.checkGraphDataIsNotNull(graph_data)
            dto_resultGraphDataList.append(result_graphdata)
        return dto_resultGraphDataList

    """
    マンガのグラフ5（累計発行部数）（最新巻）表示用のデータを取得する
    """
    def get_book5(self,ip_code):
        # 最新巻のIsbnを取得
        latestisbn = self.mapping(DtoIpCompare.DtoIpCompareForDao.DtolatestIsbnForDao,self.dao_t_book.selectLatestIsbnData(ip_code))
        if not latestisbn:
            return []
        tmplatestisbn = latestisbn[0].latestisbn
        tmpbookissuedate = latestisbn[0].book_issue_date
        # 累計発行部数（最新巻）のデータを取得
        dto_resultGraphDataList = []
        for graph_data in self.mapping(DtoIpCompare.DtoIpCompareForDao.DtoIpCompareForDateNotNullDao,self.dao_t_book.selectCompareGraphData(tmplatestisbn,tmpbookissuedate)):
            result_graphdata = self.checkGraphDataIsNotNull(graph_data)
            dto_resultGraphDataList.append(result_graphdata)
        return dto_resultGraphDataList

    """
    ゲームのグラフ1（累計売上本数）（発売日からNか月）表示用のデータを取得する
    """
    def get_game1(self,pkg_soft_code):
        # 累計売上本数(発売日からNか月)のデータを取得
        dto_resultGraphDataList = []
        for graph_data in self.mapping(DtoIpCompare.DtoIpCompareForDao.DtoIpCompareForDateNotNullDao,self.dao_t_pkg_soft.selectFromFirstDayGraphData(pkg_soft_code)):
            result_graphdata = self.checkGraphDataIsNotNull(graph_data)
            dto_resultGraphDataList.append(result_graphdata)
        return dto_resultGraphDataList

    """
    ゲームのグラフ2（累計売上本数）表示用のデータを取得する
    """
    def get_game2(self,pkg_soft_code):
        # 累計売上本数のデータを取得
        dto_resultGraphDataList = []
        for graph_data in self.mapping(DtoIpCompare.DtoIpCompareForDao.DtoIpCompareForDateNotNullDao,self.dao_t_pkg_soft.selectGraphData(pkg_soft_code)):
            result_graphdata = self.checkGraphDataIsNotNull(graph_data)
            dto_resultGraphDataList.append(result_graphdata)
        return dto_resultGraphDataList

    """
    アプリの累計売上グラフ1（累計売上（発売日からNか月））表示用のデータを取得する
    """
    def get_appSales1(self,app_name):
        # 累計売上(発売日からNか月)のデータを取得
        dto_resultAppGraph5DataList = []
        for graph_data in self.mapping(DtoIpCompare.DtoIpCompareForDao.DtoIpCompareForDateNotNullAppSalesDao,self.dao_t_mobile_app.selectTotalDataFromFirstDayGraphData(app_name)):
            result_graphdata = self.checkAppGraph5DataIsNotNull(graph_data)
            print(result_graphdata)
            dto_resultAppGraph5DataList.append(result_graphdata)
        return dto_resultAppGraph5DataList

    """
    アプリの累計売上グラフ2（累計売上）表示用のデータを取得する
    """
    def get_appSales2(self,app_name):
        dto_resultAppGraph5DataList = []
        for graph_data in self.mapping(DtoIpCompare.DtoIpCompareForDao.DtoIpCompareForDateNotNullAppSalesDao,self.dao_t_mobile_app.selectAppTotalSalesAndDownloadGraphData(app_name)):
            result_graphdata = self.checkAppGraph5DataIsNotNull(graph_data)
            dto_resultAppGraph5DataList.append(result_graphdata)
        return dto_resultAppGraph5DataList

    """
    アプリの平均売上グラフと平均ダウンロード数グラフ表示用のデータを取得する
    """
    def get_appAvgSales_download(self,app_name):
        # 平均売上と平均ダウンロード数のデータを取得
        dto_resultAppGraph5DataList = []
        for graph_data in self.mapping(DtoIpCompare.DtoIpCompareForDao.DtoIpCompareForDateNotNullAppSalesDao,self.dao_t_mobile_app.selectAppAvgSalesAndDownloadGraphData(app_name)):
            result_graphdata = self.checkAppGraph5DataIsNotNull(graph_data)
            dto_resultAppGraph5DataList.append(result_graphdata)
        return dto_resultAppGraph5DataList

    """
    アプリの累計ダウンロードグラフ（ダウンロード（発売日からNか月））表示用のデータを取得する
    """
    def get_appDownload1(self,app_name):
        # 累計ダウンロード(発売日からNか月)のデータを取得
        dto_resultAppGraph5DataList = []
        for graph_data in self.mapping(DtoIpCompare.DtoIpCompareForDao.DtoIpCompareForDateNotNullAppSalesDao,self.dao_t_mobile_app.selectTotalDataFromFirstDayGraphData(app_name)):
            result_graphdata = self.checkAppGraph5DataIsNotNull(graph_data)
            dto_resultAppGraph5DataList.append(result_graphdata)
        return dto_resultAppGraph5DataList

    """
    アプリの累計ダウンロードグラフ表示用のデータを取得する
    """
    def get_appDownload2(self,app_name):
        # 累計ダウンロードのデータを取得
        dto_resultAppGraph5DataList = []
        for graph_data in self.mapping(DtoIpCompare.DtoIpCompareForDao.DtoIpCompareForDateNotNullAppSalesDao,self.dao_t_mobile_app.selectAppTotalSalesAndDownloadGraphData(app_name)):
            result_graphdata = self.checkAppGraph5DataIsNotNull(graph_data)
            dto_resultAppGraph5DataList.append(result_graphdata)
        return dto_resultAppGraph5DataList

    """
    グラフデータがnullがある場合、「0」に変更する
    @param graph_data データベースから取得したデータ
    @return グラフ表示用データ
    """       
    def checkGraphDataIsNotNull(self, graph_data):
        result_yyyymm = graph_data.result_yyyymm
        if graph_data.result_data is None:
            result_data  = 0
        else:
            result_data = graph_data.result_data
            
        result_graphdata = DtoIpCompare.DtoIpCompareForDao.DtoIpCompareForDateNotNullDao(result_yyyymm,result_data)
        return result_graphdata

    """
    グラフデータがnullがある場合、「0」に変更する(アプリグラフ５とアプリグラフ６用))
    @param graph_data データベースから取得したデータ
    @return グラフ表示用データ
    """       
    def checkAppGraph5DataIsNotNull(self, graph_data):
        result_yyyymm = graph_data.result_yyyymm
        if graph_data.avg_sales is None:
            avg_sales  = 0
        else:
            avg_sales = graph_data.avg_sales

        if graph_data.avg_count is None:
            avg_count  = 0
        else:
            avg_count = graph_data.avg_count

        result_graphdata = DtoIpCompare.DtoIpCompareForDao.DtoIpCompareForDateNotNullAppSalesDao(result_yyyymm,avg_sales,avg_count)
        return result_graphdata