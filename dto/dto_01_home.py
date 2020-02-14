from typing import NamedTuple

class DtoHome(NamedTuple):
    class DtoKeyVisual(NamedTuple):
        ip_code : str
        keyvisual_file_name : str
        fact_1_code : str
        fact_1 : str
        fact_2_code : str
        fact_2 : str
        fact_3_code : str
        fact_3 : str
        fact_4_code : str
        fact_4 : str
        fact_5_code : str
        fact_5 : str

    class DtoBanner(NamedTuple):
        is_checked : str
        external_site : str
        white_paper_id : str
        white_paper_file_name : str
        tumbnail_file_name : str
        title : str
        details :str

    class DtoLatestNotice(NamedTuple):
        release_date : str
        subject : str
        article : str
        link_url : str

    class DtoNews(NamedTuple):
        category : str
        datetime : str
        headline : str
        link_url : str

    class DtoRankingManga(NamedTuple):
        rank : str
        keyvisual_file_name : str
        ip_code : str
        book_name : str
        isbn : str
        qty_sales : str

    class DtoRankingApp(NamedTuple):
        rank : str
        keyvisual_file_name : str
        ip_code : str
        app_name : str
        download_count : str

    class DtoRankingTwitter(NamedTuple):
        rank : str
        keyvisual_file_name : str
        ip_code : str
        account_name : str
        follower_count : str

    class DtoTagInfo(NamedTuple):
        sakuhin_code : str
        tag_name1 : str
        tag_code1 : str
        tag_name2 : str
        tag_code2 : str
        tag_name3 : str
        tag_code3 : str
        tag_name4 : str
        tag_code4 : str
        tag_name5 : str
        tag_code5 : str

    key_visual : DtoKeyVisual
    banner : DtoBanner
    latest_notice : DtoLatestNotice
    news : DtoNews
    ranking_manga : DtoRankingManga
    ranking_app : DtoRankingApp
    ranking_twitter : DtoRankingTwitter
    agg_period : str
