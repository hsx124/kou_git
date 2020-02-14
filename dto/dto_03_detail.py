from typing import NamedTuple
from typing import List
from ipdds_app.dto.dto_05_search_result import DtoSearchResult
from ipdds_app.dto.dto_main import DtoGraphData

class DtoDetail(NamedTuple):
    class DtoIpData(NamedTuple):

        class BookSeries(NamedTuple):
            series_name : str
            published_num : str
            qty_total_sales_2 :str
            avg_per_volume : str

        class BookVolume(NamedTuple):
            isbn : str
            book_name : str
            qty_total_sales_2 : str

        class DtoBuyTogether(NamedTuple):
            ip_code : str
            ip_name : str
            author : str
            publisher : str

        class DtoDetailIndivisualItem(NamedTuple):
            foreign_window : str
            domestic_window : str
            memo : str
            author : str
            artist : str
            original_author : str
            past_series : str
            author_note : str
            publisher : str
            series_start_yyyymm : str
            series_end_flag : str
            award_history : str
            original_auther_past_art : str
            past_series_tv_anime : str
            past_series_live_action_drama : str
            past_series_live_action_film : str
            past_series_anime_film : str
            past_series_stage : str
            past_series_game : str
            past_series_novel : str
            past_series_other : str
            web_app_line_manga : str
            web_app_comico : str
            web_app_manga_one : str
            web_app_manga_one_box : str
            web_app_shounen_jump_plus : str
            web_app_ganma : str
            web_app_gangan_pixiv : str
            web_app_other : str
            twitter_id : str
            user_name : str
            twitter_account_name : str
            twitter_latest_follower_count : str
            twitter_3months_ago_follower_count : str
            twitter_1year_ago_follower_count : str
            is_exist_manga_db : bool
            is_exist_gender_ratio : bool
            is_exist_book : bool
            is_exist_twitter : bool
            published_num : str
            male : int
            female : int
            total : int
            male_lteq10 : int
            male_11to15 : int
            male_16to20 : int
            male_21to25 : int
            male_26to30 : int
            male_31to35 : int
            male_36to40 : int
            male_41to45 : int
            male_46to50 : int
            male_gteq51 : int
            female_lteq10 : int
            female_11to15 : int
            female_16to20 : int
            female_21to25 : int
            female_26to30 : int
            female_31to35 : int
            female_36to40 : int
            female_41to45 : int
            female_46to50 : int
            female_gteq51 : int

        keyvisual_file_name : str
        ip_code : str
        ip_name : str
        ip_kana_name : str
        overview : str
        tag : DtoSearchResult.SearchResultContents.Tag
        book_volume : List[BookVolume]
        book_series : List[BookSeries]
        release_date : str
        update_date : str
        buy_together : List[DtoBuyTogether]
        detail_indivisual_item : DtoDetailIndivisualItem

    class DtoBroadcast(NamedTuple):
        period : str
        broadcaster : str
        
    class DtoRelatedDocuments(NamedTuple):
        id : str
        file_name : str
        whitepaper_category : str
        year : str

    class DtoSimilarIp(NamedTuple):
        ip_code : str
        ip_name : str
        fact_tag_code1 : str
        fact_tag_name1 : str
        fact_tag_code2 : str
        fact_tag_name2 : str
        fact_tag_code3 : str
        fact_tag_name3 : str
        fact_tag_code4 : str
        fact_tag_name4 : str
        fact_tag_code5 : str
        fact_tag_name5 : str
        similar_rate : str

    class DtoGameArea(NamedTuple):
        class DtoGameData(NamedTuple):
            pkg_soft_code : str
            pkg_soft_name : str
            platform_name : str
            distributor_name : str
            release_date : str
            qty_total_sales : str
        game_data : DtoGameData
        game_graph_data : List[DtoGraphData]

    class DtoAppArea(NamedTuple):
        class DtoAppData(NamedTuple):
            app_id_ios : str
            app_id_android : str
            app_name : str
            platform_name : str
            distributor_name : str
            start_date : str
        app_data : DtoAppData
        last_three_months_sales : str
        app_download_count_graph_data : List[DtoGraphData]
        app_monthly_sales_graph_data : List[DtoGraphData]
    
    ip_data : DtoIpData
    broadcast : List[DtoBroadcast]
    related_documents : List[DtoRelatedDocuments]
    similar_ip : List[DtoSimilarIp]
    twitter_graph_data : DtoGraphData
    manga_first_graph_data : DtoGraphData
    manga_latest_graph_data : DtoGraphData
    game_area : List[DtoGameArea]
    app_area : List[DtoAppArea]




