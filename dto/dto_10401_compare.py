<<<<<<< HEAD:web/web-front/ipdds/ipdds_app/dto/dto_04_compare.py
from typing import NamedTuple
from typing import List
from typing import Dict
from collections import OrderedDict

class DtoIpCompare(NamedTuple):

    #画面用DTO 全体
    class DtoIpCompareForDisp(NamedTuple):

        #画面用DTO 年代別男女比
        class DtoIpCompareForGenderRatio(NamedTuple):
            #IPコード
            ip_code : str
            #IP名
            ip_name : str
            #総人数
            total : str
            #男性(%)
            male_under_10 : str
            male_11_15 : str
            male_16_20 : str
            male_21_25 : str
            male_26_30 : str
            male_31_35 : str
            male_36_40 : str
            male_41_45 : str
            male_46_50 : str
            male_51_over : str
            #女性(%)
            female_under_10 : str
            female_11_15 : str
            female_16_20 : str
            female_21_25 : str
            female_26_30 : str
            female_31_35 : str
            female_36_40 : str
            female_41_45 : str
            female_46_50 : str
            female_51_over : str

        #画面用DTO Twitter
        class DtoIpCompareForTwitter(NamedTuple):
            #IPコード
            ip_code : str
            #IP名
            ip_name : str
            #最新のフォロワー数
            followers_latest : str
            #3か月前のフォロワー数
            followers_3months_ago : str
            #1年前のフォロワー数
            followers_1year_ago : str
            #Twitterユーザ
            user_name: str
            #TwitterID
            twitter_id : str

        #画面用DTO マンガ
        class DtoIpCompareForBook(NamedTuple):
            #IPコード
            ip_code : str
            #IP名
            ip_name : str
            #累計発行部数
            cumulative : str
            #累計発行部数（１巻）
            cumulative_first : str
            #累計発行部数（最新刊）
            cumulative_latest : str
            #平均発行部数（単巻あたり）
            average_1book : str
            #１巻のISBN
            firstisbn : str
            # 最新刊のISBN
            latestisbn : str

        #画面用DTO ゲーム
        class DtoIpCompareForGame(NamedTuple):
            #IPコード
            ip_code : str
            #IP名
            ip_name : str
            #アプリ名
            pkg_soft_name : str
            #対応機種
            platform_name : str
            #発売元
            distributor_name : str
            #発売日
            release_date : str
            #累計売上本数
            qty_total_sales : str
            #パッケージソフト名
            pkg_soft_code : str

        #画面用DTO アプリ
        class DtoIpCompareForApp(NamedTuple):
            #IPコード
            ip_code : str
            #IP名
            ip_name : str
            #アプリ名
            app_name : str           
            #プラットフォーム
            platform : str
            #発売元
            distributor_name : str
            #発売日
            release_date : str
            #累計売上
            total_sales : str
            #累計ダウンロード数
            total_download_count : str
            #平均売上
            avg_sales : str
            #平均ダウンロード数
            avg_download_count : str
            #app_id_ios
            app_id_ios : str
            #app_id_android
            app_id_android : str 
            # サービス開始年月日
            service_start_date : str  

        #画面用DTO アプリ
        class DtoIpCompareForIpName(NamedTuple):
            #IPコード
            ip_code : str
            #IP名
            ip_name : str
 
        #年代別男女比情報
        gender_ratio : List[DtoIpCompareForGenderRatio]
        #Twitter情報
        twitter : List[DtoIpCompareForTwitter]
        #マンガ情報
        book : List[DtoIpCompareForBook]
        #ゲーム情報
        game : List[DtoIpCompareForGame]
        #アプリ情報
        app : List[DtoIpCompareForApp]
        #比較画面IP名情報
        ip_name : List[DtoIpCompareForIpName]

    #DAO用DTO
    class DtoIpCompareForDao(NamedTuple):

        #DAO用DTO　年代別男女比
        class DtoGenderRatioForDao(NamedTuple):
            #IPコード
            ip_code : str
            #IP名
            ip_name : str
            #男性
            male : int
            #女性
            female : int
            #全体
            total : int
            #男性人数
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
            #女性人数
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

        #DAO用DTO　Twitter
        class DtoTwitterForDao(NamedTuple):
            #IPコード
            ip_code : str
            #IP名
            ip_name : str
            #最新のフォロワー数
            followers_latest : int
            #3か月前のフォロワー数
            followers_3months_ago : int
            #1年前のフォロワー数
            followers_1year_ago : int
            #Twitterユーザ
            user_name: str
            #TwitterID
            twitter_id : str

        #DAO用DTO マンガ
        class DtoBookForDao(NamedTuple):
            #IPコード
            ip_code : str
            #IP名
            ip_name : str
            #累計発行部数
            cumulative : str
            #累計発行部数（１巻）
            cumulative_first : str
            #累計発行部数（最新刊）
            cumulative_latest : str
            #平均発行部数（単巻あたり）
            average_1book : str
            #１巻のISBN
            firstisbn : str
            # 最新刊のISBN
            latestisbn : str

        #DAO用DTO ゲーム
        class DtoGameForDao(NamedTuple):
            #IPコード
            ip_code : str
            #IP名
            ip_name : str
            #アプリ名
            pkg_soft_name : str
            #対応機種
            platform_name : str
            #発売元
            distributor_name : str
            #発売日
            release_date : str
            #累計売上本数
            qty_total_sales : str
            # パッケージソフトコード
            pkg_soft_code : str

        #DTO用DTO アプリ
        class DtoAppForDao(NamedTuple):
            #IPコード
            ip_code : str
            #IP名
            ip_name : str
            #アプリ名
            app_name : str   
            #プラットフォーム
            platform : str
            #発売元
            distributor_name : str
            #発売日
            release_date : str
            #累計売上
            total_sales : str
            #累計ダウンロード数
            total_download_count : str
            #平均売上
            avg_sales : str
            #平均ダウンロード数
            avg_download_count : str
            #app_id_ios
            app_id_ios : str
            #app_id_android
            app_id_android : str 
            # サービス開始年月日
            service_start_date : str     

        #DTO用DTO 発売日
        class DtoFirstDayForDao(NamedTuple):
            #発売日
            firstday : str

        #DTO用DTO 1巻のISBN
        class DtoFirstIsbnForDao(NamedTuple):
            #1巻のISBN
            firstisbn : str
            # 1巻の発行年月日
            book_issue_date : str

        #DTO用DTO 最新刊巻のISBN
        class DtolatestIsbnForDao(NamedTuple):
            #最新刊巻のISBN
            latestisbn : str
            # 最新巻の発行年月日
            book_issue_date : str

        #DTO用DTO 比較画面Ip名取得
        class DtoIpCompareForIpNameDao(NamedTuple):
            #IPコード
            ip_code : str
            #IP名
            ip_name : str

        #DTO用DTO グラフ用データ処理するため（データはNullある場合）
        class DtoIpCompareForDateNotNullDao(NamedTuple):
            #グラフ表示用年月
            result_yyyymm : str
            #グラフ表示用データ
            result_data : str

        #DTO用DTO グラフ用データ処理するため（データはNullある場合）アプリグラフ５とグラフ６用
        class DtoIpCompareForDateNotNullAppSalesDao(NamedTuple):
            #グラフ表示用年月
            result_yyyymm : str
            #アプリ平均売上
            avg_sales : str
            #アプリ平均ダウンロード数
            avg_count : str
=======
from typing import NamedTuple
from typing import List
from typing import Dict
from collections import OrderedDict

class DtoSakuhinCompare(NamedTuple):

    #画面用DTO 全体
    class DtoSakuhinCompareForDisp(NamedTuple):

        #画面用DTO 年代別男女比
        class DtoSakuhinCompareForGenderRatio(NamedTuple):
            #作品コード
            sakuhin_code : str
            #作品名
            sakuhin_name : str
            #総人数
            total : str
            #男性(%)
            male_under_10 : str
            male_11_15 : str
            male_16_20 : str
            male_21_25 : str
            male_26_30 : str
            male_31_35 : str
            male_36_40 : str
            male_41_45 : str
            male_46_50 : str
            male_51_over : str
            #女性(%)
            female_under_10 : str
            female_11_15 : str
            female_16_20 : str
            female_21_25 : str
            female_26_30 : str
            female_31_35 : str
            female_36_40 : str
            female_41_45 : str
            female_46_50 : str
            female_51_over : str

        #画面用DTO Twitter
        class DtoSakuhinCompareForTwitter(NamedTuple):
            #作品コード
            sakuhin_code : str
            #作品名
            sakuhin_name : str
            #最新のフォロワー数
            followers_latest : str
            #3か月前のフォロワー数
            followers_3months_ago : str
            #1年前のフォロワー数
            followers_1year_ago : str
            #Twitterユーザ
            user_name: str
            #TwitterID
            twitter_id : str

        #画面用DTO マンガ
        class DtoSakuhinCompareForManga(NamedTuple):
            #作品コード
            sakuhin_code : str
            #作品名
            sakuhin_name : str
            #累計発行部数
            cumulative : str
            #累計発行部数（１巻）
            cumulative_first : str
            #累計発行部数（最新刊）
            cumulative_latest : str
            #平均発行部数（単巻あたり）
            average_1manga : str
            #１巻のISBN
            firstisbn : str
            # 最新刊のISBN
            latestisbn : str
            #マンガ名
            manga_name : str
            #マンガコード
            manga_code : str

        #画面用DTO ゲーム
        class DtoSakuhinCompareForGame(NamedTuple):
            #作品コード
            sakuhin_code : str
            #作品名
            sakuhin_name : str
            #ゲーム名
            game_title_name : str
            #対応機種
            platform_name : str
            #発売元
            hanbai_company_name : str
            #発売日
            release_yyyymmdd : str
            #累計売上本数
            total_sales_cnt : str
            #ゲーム名
            game_title_code : str

        #画面用DTO アプリ
        class DtoSakuhinCompareForApp(NamedTuple):
            #作品コード
            sakuhin_code : str
            #作品名
            sakuhin_name : str
            #アプリ名
            app_title_name : str           
            #プラットフォーム
            platform : str
            #発売元
            hanbai_company_name : str
            #発売日
            service_start_yyyymmdd : str
            #累計売上
            total_sales : str
            #累計ダウンロード数
            total_download_cnt : str
            #平均売上
            avg_sales : str
            #平均ダウンロード数
            avg_download_cnt : str
            #アプリコード
            app_title_code : str
            #app_id_ios
            app_id_ios : str
            #app_id_android
            app_id_android : str

        #画面用DTO アプリ
        class DtoSakuhinCompareForSakuhinName(NamedTuple):
            #作品コード
            sakuhin_code : str
            #作品名
            sakuhin_name : str
 
        #年代別男女比情報
        gender_ratio : List[DtoSakuhinCompareForGenderRatio]
        #Twitter情報
        twitter : List[DtoSakuhinCompareForTwitter]
        #マンガ情報
        manga : List[DtoSakuhinCompareForManga]
        #ゲーム情報
        game : List[DtoSakuhinCompareForGame]
        #アプリ情報
        app : List[DtoSakuhinCompareForApp]
        #比較画面作品名情報
        sakuhin_name : List[DtoSakuhinCompareForSakuhinName]

    #DAO用DTO
    class DtoSakuhinCompareForDao(NamedTuple):

        #DAO用DTO　年代別男女比
        class DtoGenderRatioForDao(NamedTuple):
            #作品コード
            sakuhin_code : str
            #作品名
            sakuhin_name : str
            #男性
            male : int
            #女性
            female : int
            #全体
            total : int
            #男性人数
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
            #女性人数
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

        #DAO用DTO　Twitter
        class DtoTwitterForDao(NamedTuple):
            #作品コード
            sakuhin_code : str
            #作品名
            sakuhin_name : str
            #最新のフォロワー数
            followers_latest : int
            #3か月前のフォロワー数
            followers_3months_ago : int
            #1年前のフォロワー数
            followers_1year_ago : int
            #Twitterユーザ
            user_name: str
            #TwitterID
            twitter_id : str

        #DAO用DTO マンガ
        class DtoMangaForDao(NamedTuple):
            #作品コード
            sakuhin_code : str
            #作品名
            sakuhin_name : str
            #累計発行部数
            cumulative : str
            #累計発行部数（１巻）
            cumulative_first : str
            #累計発行部数（最新刊）
            cumulative_latest : str
            #平均発行部数（単巻あたり）
            average_1manga : str
            #１巻のISBN
            firstisbn : str
            # 最新刊のISBN
            latestisbn : str
            #マンガ名
            manga_name : str
            #マンガコード
            manga_code : str

        #DAO用DTO ゲーム
        class DtoGameForDao(NamedTuple):
            #作品コード
            sakuhin_code : str
            #作品名
            sakuhin_name : str
            #アプリ名
            game_title_name : str
            #対応機種
            platform_name : str
            #発売元
            hanbai_company_name : str
            #発売日
            release_yyyymmdd : str
            #累計売上本数
            total_sales_cnt : str
            # ゲームコード
            game_title_code : str

        #DAO用DTO アプリ
        class DtoAppForDao(NamedTuple):
            #作品コード
            sakuhin_code : str
            #作品名
            sakuhin_name : str
            #アプリ名
            app_title_name : str   
            #アプリID_IOS
            app_id_ios : str
            #アプリID_Android
            app_id_android : str
            #発売元
            hanbai_company_name : str
            #発売日
            service_start_yyyymmdd : str
            #累計売上
            total_sales : str
            #累計ダウンロード数
            total_download_cnt : str
            #平均売上
            avg_sales : str
            #平均ダウンロード数
            avg_download_cnt : str
            #アプリ名
            app_title_code : str   

        #DAO用DTO 1巻のISBN
        class DtoFirstIsbnForDao(NamedTuple):
            #1巻のISBN
            firstisbn : str
            # 1巻の発行年月日
            manga_issue_date : str

        #DAO用DTO 最新刊巻のISBN
        class DtolatestIsbnForDao(NamedTuple):
            #最新刊巻のISBN
            latestisbn : str
            # 最新巻の発行年月日
            manga_issue_date : str

        #DAO用DTO 比較画面作品名取得
        class DtoSakuhinCompareForSakuhinNameDao(NamedTuple):
            #作品コード
            sakuhin_code : str
            #作品名
            sakuhin_name : str

        #DAO用DTO グラフ用データ処理するため（データはNullある場合）
        class DtoForDate2NotNullDao(NamedTuple):
            #グラフ表示用年月
            result_yyyymm : str
            #グラフ表示用データ
            result_data : str

        #DAO用DTO グラフ用データ処理するため（データはNullある場合）
        class DtoForDate3NotNullDao(NamedTuple):
            #グラフ表示用年月
            result_yyyymm : str
            #アプリ平均売上
            avg_sales : str
            #アプリ平均ダウンロード数
            avg_count : str

        #DAO用DTO ゲームグラフ表示用発売年月日
        class DtoForServiceStartDate(NamedTuple):
            #ゲームグラフ表示用発売年月日
            service_date : str
>>>>>>> remotes/origin/feature/ph1.3:web/web-front/ipdds/ipdds_app/dto/dto_10401_compare.py
