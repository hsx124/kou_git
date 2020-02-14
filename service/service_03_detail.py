from ipdds_app.service.service_main import ServiceMain

from ipdds_app.dao.dao_m_imp import DaoMImp
from ipdds_app.dao.dao_m_ip import DaoMIp
from ipdds_app.dao.dao_m_wiki import DaoMWiki
from ipdds_app.dao.dao_m_manga_db import DaoMMangaDb
from ipdds_app.dao.dao_m_white_paper import DaoMWhitePaper
from ipdds_app.dao.dao_t_twitter import DaoTTwitter
from ipdds_app.dao.dao_t_book import DaoTBook
from ipdds_app.dao.dao_m_pkg_soft import DaoMPkgSoft
from ipdds_app.dao.dao_t_pkg_soft import DaoTPkgSoft
from ipdds_app.dao.dao_m_mobile_app import DaoMMobileApp
from ipdds_app.dao.dao_t_mobile_app import DaoTMobileApp

from ipdds_app.dto.dto_main import DtoGraphData
from ipdds_app.dto.dto_05_search_result import DtoSearchResult
from ipdds_app.dto.dto_03_detail import DtoDetail

import datetime
from dateutil.relativedelta import relativedelta

class DetailService(ServiceMain):

    # m_impテーブル用DAO
    dao_m_imp = DaoMImp()
    # m_ipテーブル用DAO
    dao_m_ip = DaoMIp()
    # m_wikiテーブル用DAO
    dao_m_wiki = DaoMWiki()
    # m_manga_dbテーブル用DAO
    dao_m_manga_db = DaoMMangaDb()
    # m_white_paperテーブル用DAO
    dao_m_white_paper = DaoMWhitePaper()
    
    # t_twitterテーブル用DAO
    dao_t_twitter = DaoTTwitter()
    # t_bookテーブル用DAO
    dao_t_book = DaoTBook()
    # m_pkg_softテーブル用DAO
    dao_m_pkg_soft = DaoMPkgSoft()
    # t_pkg_softテーブル用DAO
    dao_t_pkg_soft = DaoTPkgSoft()
    # m_mobile_appテーブル用DAO
    dao_m_mobile_app = DaoMMobileApp()
    # t_mobile_appテーブル用DAO
    dao_t_mobile_app = DaoTMobileApp()
    
    """
    業務処理
    @param ip_code IPコード
    @return 詳細画面DTO
    """
    def bizProcess(self,ip_code):
        
        '''
        各画面領域のデータを取得し領域用DTOに詰める
        '''
        if not self.dao_m_ip.selectCountByIpCode(ip_code)[0][0]:
            return {'ip_not_found':True}
        
        # 印象マスタの件数の取得
        imp_cnt = self.dao_m_imp.selectImpCounntMax()
        # IP概要
        tmp_ip_data = self.dao_m_ip.selectDetailByIpCode(ip_code, imp_cnt)[0]
        ip_data = self.dtoMapping(tmp_ip_data, imp_cnt)
        broadcast = self.mapping(DtoDetail.DtoBroadcast, self.dao_m_wiki.selectBroadCastByIpCode(ip_code))
        # 類似IP
        fact_tag_code = [ tmp.code for tmp in ip_data.tag.fact_tag ]
        similar_ip = self.mapping(DtoDetail.DtoSimilarIp, self.dao_m_manga_db.selectSimilarIpByFactCode(fact_tag_code,ip_code))
        # 関連文書
        related_documents = self.mapping(DtoDetail.DtoRelatedDocuments, self.dao_m_white_paper.selectRelatedDocumentsByIpCode(ip_code))
        # Twtterデータ
        twitter_graph_data = self.mapping(DtoGraphData, self.dao_t_twitter.selectGraphData(ip_data.detail_indivisual_item.twitter_id))
        # マンガデータ
        isbn = ip_data.book_volume[0].isbn
        manga_first_graph_data = self.mapping(DtoGraphData, self.dao_t_book.selectGraphData(isbn))
        isbn = ip_data.book_volume[1].isbn
        manga_latest_graph_data = self.mapping(DtoGraphData, self.dao_t_book.selectGraphData(isbn))
        # ゲームデータ
        game_area = []
        game_data = self.mapping(DtoDetail.DtoGameArea.DtoGameData,self.dao_m_pkg_soft.selectGameData(ip_code))
        for data in game_data:
            graph = self.mapping(DtoGraphData, self.dao_t_pkg_soft.selectGraphData(data.pkg_soft_code))
            game_area.append(DtoDetail.DtoGameArea(data,graph))
        # アプリデータ
        app_area = []
        app_data = self.mapping(DtoDetail.DtoAppArea.DtoAppData,self.dao_m_mobile_app.selectAppData(ip_code))
        for data in app_data:
            last_three_months_sales = self.getLastThreeMonthsSales(data)
            graph1 = self.mapping(DtoGraphData, self.dao_t_mobile_app.selectGraphData(data.app_id_ios,data.app_id_android,'download_count'))
            graph2 = self.mapping(DtoGraphData, self.dao_t_mobile_app.selectGraphData(data.app_id_ios,data.app_id_android,'monthly_sales'))
            app_area.append(DtoDetail.DtoAppArea(data,last_three_months_sales,graph1,graph2))
        
        # 領域用DTOを画面DTOに詰める
        dto_detail = DtoDetail( ip_data # IP単位のデータ
                                ,broadcast # 放送期間・放送局
                                ,related_documents # 関連文書
                                ,similar_ip # 類似IP領域
                                ,twitter_graph_data # Twitterグラフデータ
                                ,manga_first_graph_data # マンガ1巻グラフデータ
                                ,manga_latest_graph_data # マンガ最新刊グラフデータ
                                ,game_area # ゲームデータ
                                ,app_area # アプリデータ
                                )
        return self.unpack(dto_detail)

    """
    取得結果をdtoにマッピングする処理
    @param resultIp 検索結果(1IP)
    @param imp_cnt 印象テーブルの件数
    @return 詳細情報（IP単位のデータ)
    """
    def dtoMapping(self, resultIp,imp_cnt):
        keyvisual_file_name = resultIp[0]  # キービジュアルファイル名
        ip_code = resultIp[1] # IPコード
        ip_name =  resultIp[2] # IP名
        ip_kana_name = resultIp[3] # IPかな名
        overview = resultIp[4] # あらすじ
        # 分類タグ
        tag_category = list(resultIp[5:10])
        tag_category = [ str(category) for category in tag_category ]
        #  ジャンルタグ
        tag_core = list(resultIp[10:14])
        tag_core = [    DtoSearchResult.SearchResultContents.Tag.PairCodeName(tag_core[i],tag_core[i+1]) 
                        for i in range(0,len(tag_core),2) 
                        if tag_core[i] and tag_core[i+1]    ]
        #  掲載媒体
        tag_media = DtoSearchResult.SearchResultContents.Tag.PairCodeName( resultIp[14], resultIp[15])
        #  現実フラグ
        tag_fiction_flag = resultIp[16]
        #  事実メタ
        tag_fact_tag = list(resultIp[17:27])
        tag_fact_tag = [    DtoSearchResult.SearchResultContents.Tag.PairCodeName(tag_fact_tag[i],tag_fact_tag[i+1]) 
                            for i in range(0,len(tag_fact_tag),2) 
                            if tag_fact_tag[i] and tag_fact_tag[i+1]    ]
        release_date = resultIp[27] # 発表年月日
        update_date = resultIp[28] # 更新日付

        # 印象
        tmp_idx_before = 31
        tmp_idx_after = 31+imp_cnt
        tag_imp = list(resultIp[tmp_idx_before:tmp_idx_after])
        tag_imp = [ DtoSearchResult.SearchResultContents.Tag.PairCodeName(tag_imp[i],tag_imp[i+1]) 
                    for i in range(0,len(tag_imp),2) 
                    if tag_imp[i] and tag_imp[i+1] ]
        # 書籍データ(巻毎)
        tmp_idx_before = tmp_idx_after
        tmp_idx_after = tmp_idx_before + 6
        book_volume = list(resultIp[tmp_idx_before:tmp_idx_after])
        book_volume = [ DtoDetail.DtoIpData.BookVolume(book_volume[i],book_volume[i+1],book_volume[i+2]) 
                        for i in range(0,len(book_volume),3) ]
        # 併買
        tmp_idx_before = tmp_idx_after
        tmp_idx_after = tmp_idx_before + 15
        buy_together_ip_code = list(resultIp[tmp_idx_before:tmp_idx_after])
        manga_db = self.mapping(DtoDetail.DtoIpData.DtoBuyTogether,self.dao_m_manga_db.selectAuthorAndPublisherByIpList(buy_together_ip_code))
        buy_together = []
        for v in buy_together_ip_code:
            if v == "":
                continue
            matchedMangaDb = [tmp for tmp in manga_db if v == tmp.ip_code]
            if matchedMangaDb:
                buy_together.append(matchedMangaDb[0])
            else:
                buy_together.append(DtoDetail.DtoIpData.DtoBuyTogether("",v,"-","-"))
        # 詳細画面個別項目（併売以外）
        tmp_idx_before = tmp_idx_after
        tmp_idx_after = tmp_idx_before + 63
        detailIndividualItem = self.mapping( DtoDetail.DtoIpData.DtoDetailIndivisualItem ,[resultIp[tmp_idx_before:tmp_idx_after]])[0]

        published_num = detailIndividualItem.published_num # 既刊数
        # 書籍データ(IP毎)
        book_series = [DtoDetail.DtoIpData.BookSeries(ip_name,published_num,resultIp[29],resultIp[30])]

        tag = DtoSearchResult.SearchResultContents.Tag(tag_category, tag_core, tag_media, tag_imp, tag_fiction_flag, tag_fact_tag)
        
        return DtoDetail.DtoIpData(keyvisual_file_name # キービジュアルファイル名
                                                    ,ip_code # IPコード
                                                    ,ip_name # IP名
                                                    ,ip_kana_name # IPかな名
                                                    ,overview # あらすじ
                                                    ,tag # タグ情報
                                                    ,book_volume # 書籍データ（巻毎）
                                                    ,book_series # 書籍データ（部毎）
                                                    ,release_date # 発表年月日
                                                    ,update_date # 更新日付
                                                    ,buy_together # 併売
                                                    ,detailIndividualItem # 詳細画面個別項目（併売以外）
                                                    ) 

    """
    アプリ月商平均の導出
    @param data app_id用のアプリデータ
    @return アプリ月商平均
    """
    def getLastThreeMonthsSales(self,data):
        sales = self.dao_t_mobile_app.selectLastThreeMonthsSalesDataByAppId(data.app_id_ios,data.app_id_android)
        if not sales or not sales[0][0]:
            return
        else:
            sales = [ v[0] for v in sales ]
            return str('{:,}'.format(round(sum(sales)/len(sales))))
