from ipdds_app.service.service_main import ServiceMain

from ipdds_app.dao.dao_m_sakuhin import DaoMSakuhin
from ipdds_app.dao.dao_m_banner import DaoMBanner
from ipdds_app.dao.dao_t_top_news import DaoMTopNews
from ipdds_app.dao.dao_t_isbn import DaoTIsbn
from ipdds_app.dao.dao_t_app import DaoTApp
from ipdds_app.dao.dao_t_twitter import DaoTTwitter

from ipdds_app.dto.dto_01_home.dto_10101_home import DtoHome

import datetime
from dateutil.relativedelta import relativedelta


class HomeService(ServiceMain):

    # m_sakuhinテーブル用DAO
    dao_m_sakuhin = DaoMSakuhin()
    # m_bannerテーブル用DAO
    dao_m_banner = DaoMBanner()
    # m_top_newsテーブル用DAO
    dao_m_top_news = DaoMTopNews()
    # t_mangaテーブル用DAO
    dao_t_isbn = DaoTIsbn()
    # t_appテーブル用DAO
    dao_t_app = DaoTApp()
    # t_twitterテーブル用DAO
    dao_t_twitter = DaoTTwitter()

    def bizProcess(self):

        '''
        各画面領域のデータを取得し領域用DTOに詰める
        '''
        # キービジュアルエリア
        key_visual = self.mapping(DtoHome.DtoKeyVisual, self.dao_m_sakuhin.selectRandomKeyVisual())
        # キーヴィジュアルの重複削除
        key_visual = list({result.sakuhin_code: result for result in key_visual}.values())
        # バナーエリア
        banner = self.mapping(DtoHome.DtoBanner, self.dao_m_banner.selectAll())
        # メディア部からのお知らせエリア
        latest_notice = self.mapping(DtoHome.DtoLatestNotice, self.dao_m_top_news.selectLatestNotice())
        # NEWSエリア
        news = self.mapping(DtoHome.DtoNews, self.dao_m_top_news.selectNews())
        # ランキングエリア（マンガ）
        ranking_manga = self.mapping(DtoHome.DtoRankingManga, self.dao_t_isbn.selectRankingManga())
        # ランキングエリア（アプリ）
        ranking_app = self.mapping(DtoHome.DtoRankingApp, self.dao_t_app.selectRankingApp())
        # ランキングエリア（Twitter）
        ranking_twitter = self.mapping(DtoHome.DtoRankingTwitter, self.dao_t_twitter.selectRankingTwitter())

        # ランキングエリアの集計期間の導出
        now = datetime.datetime.now()
        dt_from = now - relativedelta(months=3)
        dt_to = now - relativedelta(months=1)
        agg_period = dt_from.strftime('%Y/%m') + '-' + dt_to.strftime('%m')

        # 領域用DTOを画面DTOに詰める
        dto_home = DtoHome(key_visual, banner, latest_notice, news, ranking_manga, ranking_app, ranking_twitter, agg_period)

        return self.unpack(dto_home)

    def getTagInfo(self, sakuhin_code):

        # 一旦固定値で返却
        dto_tag = DtoHome.DtoTagInfo(sakuhin_code, 'タグ1', '0000000001', 'タグ2', '0000000002', 'タグ3', '0000000003', 'タグ4', '0000000004', 'タグ5', '0000000005');
        return self.unpack(dto_tag)

