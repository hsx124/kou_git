from ipdds_app.service.service_main import ServiceMain

from ipdds_app.dao.dao_m_ip import DaoMIp
from ipdds_app.dao.dao_m_core import DaoMCore
from ipdds_app.dao.dao_m_media import DaoMMedia
from ipdds_app.dao.dao_m_imp import DaoMImp
from ipdds_app.dao.dao_m_fact_tag import DaoMFactTag

from ipdds_app.dto.dto_05_search_result import DtoSearchResult
from ipdds_app.dto.dto_06_similar_search import DtoSimilarSearch

from ipdds_app.service.service_06_similar_search import SimilarSearchService

import datetime
from dateutil.relativedelta import relativedelta
from operator import itemgetter
from itertools import groupby
from collections import OrderedDict

class SearchResultService(ServiceMain):

    # m_coreテーブル用DAO
    dao_m_core = DaoMCore()
    # m_mediaテーブル用DAO
    dao_m_media = DaoMMedia()
    # m_impテーブル用DAO
    dao_m_imp = DaoMImp()
    # m_fact_tagテーブル用DAO
    dao_m_fact_tag = DaoMFactTag()

    # m_ipテーブル用DAO
    dao_m_ip = DaoMIp()

    # 書籍データ（巻毎）の表示数
    book_volume_num = 5

    # service_06_similar_search
    similarSearchService = SimilarSearchService()

    """
    業務処理
    @param request リクエスト
    @return 検索結果一覧画面DTO（フォーム情報、ユーザインプット情報、検索結果情報）
    """
    def bizProcess(self,request):
        
        '''
        類似検索フォームの要素の情報をDBから取得し、DTOに設定する。
        '''
        formElm = self.similarSearchService.bizProcess()
        
        '''
        ユーザインプット情報をDTOに設定する。
        '''
        # キーワード
        ipt_keyword = [ keyword for keyword in request.getlist("name_keyword") ]
        # 分類
        ipt_category = [ category for category in request.getlist("name_category") ]
        # コア
        ipt_core = [ core for core in request.getlist("name_core") ]
        # 掲載媒体
        ipt_media = [ media for media in request.getlist("name_media") ]
        # 印象
        ipt_imp = [ imp for imp in request.getlist("name_imp") ]
        # 現実/非現実フラグ
        ipt_fiction_flag = [ fiction for fiction in request.getlist("name_fiction_flag") ]
        # 事実タグ
        ipt_fact_tag = [ fact_tag for fact_tag in request.getlist("name_fact_tag") ]
        # 展開時期(開始)
        ipt_start_date = [ start_date for start_date in request.getlist("name_start_date") ]
        # 展開時期(終了)
        ipt_end_date = [ end_date for end_date in request.getlist("name_end_date") ]

        inputContents = DtoSearchResult.InputContents(ipt_keyword,ipt_category,ipt_core,ipt_media,ipt_imp,ipt_fiction_flag,ipt_fact_tag,ipt_start_date,ipt_end_date)

        '''
        検索処理
        '''
        search_result_keyword = []
        search_result_keyword_result = []

        # 印象マスタの件数の取得
        imp_cnt = self.dao_m_imp.selectImpCounntMax()

        ## キーワード検索
        for keyword in request.getlist("name_keyword"):
            if keyword == '':
                continue
            search_result_keyword_result += self.dao_m_ip.selectByKeyword(keyword,imp_cnt,self.book_volume_num)

        # キーワード検索で該当したIPリストを元に検索結果情報を取得
        for ip in search_result_keyword_result:
            search_result_keyword += self.dtoMapping(ipt_fact_tag, ip,imp_cnt)

        # キーワード検索の重複削除
        search_result_keyword = list({result.ip_code: result for result in search_result_keyword}.values())
        
        ## 類似検索
        search_result_similar = []
        search_result_similar_result = []
        search_result_similar_result += self.dao_m_ip.selectBySimilarCondition(inputContents,imp_cnt,self.book_volume_num)
        for ip in search_result_similar_result:
            search_result_similar += self.dtoMapping(ipt_fact_tag, ip, imp_cnt)

        ## キーワード検索に存在するIPは類似検索結果より削除する
        for keywordResult in search_result_keyword:
            search_result_similar = [ similarResult 
                                    for similarResult in search_result_similar
                                    if keywordResult.ip_code != similarResult.ip_code]

        dto_search_result = DtoSearchResult(formElm,  # フォーム情報
                                            inputContents,  # ユーザ入力情報
                                            search_result_keyword,  # 検索結果（キーワード検索）
                                            search_result_similar,  # 検索結果（類似検索）
                                            len(search_result_keyword + search_result_similar)) # 検索結果件数

        return self.unpack(dto_search_result)

    """
    検索結果をdtoにマッピングする処理
    @param ipt_fact_tag ユーザ入力の事実タグ情報
    @param resultIp 検索結果(1IP)
    @param imp_cnt 印象テーブルの件数
    @return 検索結果情報
    """
    def dtoMapping(self, ipt_fact_tag, resultIp,imp_cnt):
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
        # 書籍データ(IP毎)
        book_series = [DtoSearchResult.SearchResultContents.BookSeries(ip_name,resultIp[29],resultIp[30])]
        # 印象
        tag_imp = list(resultIp[31:31+imp_cnt])
        tag_imp = [ DtoSearchResult.SearchResultContents.Tag.PairCodeName(tag_imp[i],tag_imp[i+1]) 
                    for i in range(0,len(tag_imp),2) 
                    if tag_imp[i] and tag_imp[i+1] ]


        # 類似率の計算
        similar_rate = self.calcSimilarRate(tag_fact_tag,ipt_fact_tag)
        
        tag = DtoSearchResult.SearchResultContents.Tag(tag_category, tag_core, tag_media, tag_imp, tag_fiction_flag, tag_fact_tag)
        
        return [DtoSearchResult.SearchResultContents(keyvisual_file_name # キービジュアルファイル名
                                                    ,ip_code # IPコード
                                                    ,ip_name # IP名
                                                    ,ip_kana_name # IPかな名
                                                    ,overview # あらすじ
                                                    ,tag # タグ情報
                                                    ,book_series # 書籍データ（部毎）
                                                    ,similar_rate # 類似率
                                                    ,release_date # 発表年月日
                                                    ,update_date)] # 更新日付
    
    """
    類似度を計算する処理
    @param tag_fact_tag 計算対象のIPが持つ事実タグ
    @param ipt_fact_tag ユーザが入力した事実タグ
    @return 類似度
    """
    def calcSimilarRate(self,tag_fact_tag,ipt_fact_tag):
        if(not ipt_fact_tag):
            return ""
        similar_rate = ""
        fact_tag_code_list = [fact_tag.code for fact_tag in tag_fact_tag]
        for tmp in ipt_fact_tag:
            if tmp in fact_tag_code_list :
                similar_rate += "1"
            else:
                similar_rate += "0"
        similar_rate = str(similar_rate.count("1")) + similar_rate
        return similar_rate