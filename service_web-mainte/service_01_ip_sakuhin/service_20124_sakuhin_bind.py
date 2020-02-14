from admin_app.service.service_list import ServiceList

from admin_app.dao.dao_m_sakuhin_map import DaoMSakuhinMap
from admin_app.dao.dao_m_sakuhin import DaoMSakuhin
from admin_app.dao.dao_m_manga_title import DaoMMangaTitle
from admin_app.dao.dao_m_novel_title import DaoMNovelTitle
from admin_app.dao.dao_m_anime_title import DaoMAnimeTitle
from admin_app.dao.dao_m_app_title import DaoMAppTitle
from admin_app.dao.dao_m_media_report import DaoMMediaReport

from admin_app.dao.dao_m_twitter import DaoMTwitter
from admin_app.dao.dao_m_game_title import DaoMGameTitle

from admin_app.dao.dao_t_update_history import DaoTUpdateHistory
from admin_app.dto.dto_01_ip_sakuhin.dto_20124_sakuhin_bind import DtoSakuhinBind

class SakuhinBindService(ServiceList): 

    # 作品紐付けマスタテーブル用DAO
    dao_m_sakuhin_map = DaoMSakuhinMap()
    # 作品マスタテーブル用DAO
    dao_m_sakuhin = DaoMSakuhin()
    # マンガタイトルマスタテーブル用DAO
    dao_m_manga_title = DaoMMangaTitle()
    # 小説タイトルマスタテーブル用DAO
    dao_m_novel_title = DaoMNovelTitle()
    # アニメタイトルマスタテーブル用DAO
    dao_m_anime_title = DaoMAnimeTitle()
    # アプリタイトルマスタテーブル用DAO
    dao_m_app_title = DaoMAppTitle()
    # メディアレポートマスタテーブル用DAO
    dao_m_media_report = DaoMMediaReport()
    # Twitterマスタテーブル用DAO
    dao_m_twitter = DaoMTwitter()
    # Gameマスタテーブル用DAO
    dao_m_game_title = DaoMGameTitle()
    # 更新履歴テーブル用DAO
    dao_t_update_history = DaoTUpdateHistory()

    '''初期描画'''
    def initialize(self, tableName):
        # 更新履歴
        notice_table = self.getnoticetable(tableName)
        # 領域用DTOを画面DTOに詰める
        dto_list= DtoSakuhinBind.DtoNoticeTableList(notice_table)

        return self.unpack(dto_list)

    """
    作品データを取得する（モーダル）
    """
    def getSakuhinModalData(self, sakuhin_name):
        param = {'sakuhin_name' : '%' + sakuhin_name + '%'}
        sakuhin_list = self.mapping(DtoSakuhinBind.DtoSakuhinModal, self.dao_m_sakuhin.selectBySakuhinName(param))
       
        return self.unpack(sakuhin_list)

    """
    関連タイトル一覧を取得する
    """
    def getTitleBySakuhinCode(self, sakuhin_code):

        param = {'sakuhin_code' : sakuhin_code}
        # # マンガタイトルデータ取得
        # manga_list_tuple = tuple(self.dao_m_sakuhin_map.selectMangaTitle(param))
        # # 小説タイトルデータ取得
        # novel_list_tuple = tuple(self.dao_m_sakuhin_map.selectNovelTitle(param))
        # # アニメタイトルデータ取得
        # anime_list_tuple = tuple(self.dao_m_sakuhin_map.selectAnimeTitle(param))
        # # アプリタイトルデータ取得
        # app_list_tuple = tuple(self.dao_m_sakuhin_map.selectAppTitle(param))
        # # 白書タイトルデータ取得
        # report_list_tuple = tuple(self.dao_m_sakuhin_map.selectReportTitle(param))
        # #タイトル一覧生成 
        # title_list = manga_list_tuple + novel_list_tuple + anime_list_tuple + app_list_tuple + report_list_tuple
        # dto_title_list = self.mapping(DtoSakuhinBind.DtoTitleList, title_list)
        dto_title_list = self.mapping(DtoSakuhinBind.DtoTitleList, self.dao_m_sakuhin_map.selectTitleByCode(param))

        return self.unpack(dto_title_list)

    """
    関連タイトルモーダルを取得する
    """
    def getTitleByName(self, title_name, category_list):

        param = {'title_name' : '%' + title_name + '%'}

        manga_list = []
        novel_list = []
        anime_list = []
        app_list = []
        report_list = []
        for category in category_list:
            if category == "manga":
                # マンガタイトルデータ取得
                manga_list = self.dao_m_manga_title.selectTitleByName(param)
            if category == "novel":
                # 小説タイトルデータ取得
                novel_list = self.dao_m_novel_title.selectTitleByName(param)
            if category == "anime":
                # アニメタイトルデータ取得
                anime_list = self.dao_m_anime_title.selectTitleByName(param)
            if category == "app":
                # アプリタイトルデータ取得
                app_list = self.dao_m_app_title.selectTitleByName(param)
            if category == "report":
                # 白書タイトルデータ取得
                report_list = self.dao_m_media_report.selectTitleByName(param)
        
        #タイトル一覧生成 
        title_list = tuple(manga_list) + tuple(novel_list) + tuple(anime_list) + tuple(app_list) + tuple(report_list)
        dto_title_list = self.mapping(DtoSakuhinBind.DtoTitleModal, title_list)
       
        return self.unpack(dto_title_list)

    """
    関連タイトル紐付けを解除する
    """
    def delConnectionTitle(self, full_name, sakuhin_map_id, sakuhin_code, sakuhin_name, title_name,category_name):
        # 作品紐付け解除の無効フラグを変更
        param = {
            'full_name' : full_name,
            'sakuhin_map_id' : sakuhin_map_id
        }
        # 作品紐付け解除処理を行う
        self.dao_m_sakuhin_map.updateInvalidFlgBy(param)

        # 変更履歴の登録
        # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
        entity = ('m_sakuhin_map', '削除', sakuhin_name, category_name + title_name, full_name)
        self.dao_t_update_history.insert(entity)

        # 最新の関連タイトルデータを取得
        return self.getTitleBySakuhinCode(sakuhin_code)

    """
    関連タイトル追加
    """
    def addConnectionTitle(self, full_name, title_code_list, category_code_list, sakuhin_code, sakuhin_name, title_name_list, category_name_list):

        # 関連作品追加処理を行う
        self.dao_m_sakuhin_map.insertByTitleList(sakuhin_code,full_name,title_code_list,category_code_list)

        # 変更履歴の登録
        # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
        self.dao_t_update_history.insertByTitleList(sakuhin_name,title_name_list,category_name_list,full_name)

        # 最新の関連タイトルデータを取得
        return self.getTitleBySakuhinCode(sakuhin_code)

    """
    Twitterデータを取得する（モーダル）
    """
    def getTwitterModalData(self, twitter_name):
        param = {'twitter_name' : '%' + twitter_name + '%'}
        twitter_list = self.mapping(DtoSakuhinBind.DtoTwitterModal, self.dao_m_twitter.selectByTwitterName(param))
       
        return self.unpack(twitter_list)

    """
    Twitter一覧を取得する
    """
    def getTwitterListData(self, sakuhin_code):
        param = {'sakuhin_code' : sakuhin_code}
        dto_twitter_list = self.mapping(DtoSakuhinBind.DtoTwitterList, self.dao_m_twitter.selectTwitterBySakuhinCode(param))

        return self.unpack(dto_twitter_list)

    """
    twitterに関連作品紐付けを解除する
    """
    def delTwitterSakuhin(self, full_name,sakuhin_map_id,sakuhin_code,account_name,sakuhin_name):
        # 作品紐付け解除の無効フラグを変更
        param = {
            'full_name' : full_name,
            'sakuhin_map_id' : sakuhin_map_id
        }
        # 作品紐付け解除処理を行う
        self.dao_m_sakuhin_map.updateInvalidFlgBy(param)

        # 変更履歴の登録
        # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
        entity = ('m_sakuhin_map', '削除', sakuhin_name, 'Twitter'+ account_name, full_name)
        self.dao_t_update_history.insert(entity)

        # 最新の関連作品データを取得
        return self.getTwitterListData(sakuhin_code)

    """
    Twitter関連作品追加
    """
    def addTwitterSakuhin(self, full_name,sakuhin_code,sakuhin_name,twitter_code,account_name,main_flg):
        # 紐付け登録用パナメーラ
        param ={
            'sakuhin_code' : sakuhin_code,
            'twitter_code' : twitter_code,
            'full_name' : full_name
        }
        # 当作品の紐付けたTwitterが強制解除フラグ
        delflg = False
        # 当作品の紐付けたTwitterが強制解除Twitterのユーザ名
        del_user = ''

        # TwitterのメインフラグがTrueの場合、
        # 当作品の紐付けたTwitter（メインフラグ＝True）を検索し、
        # 存在場合は、当作品紐付けたTwitterを紐付け解除後、当Twitterとの紐付け処理を行う
        if 'true' == main_flg:
            param_code = {'sakuhin_code' : sakuhin_code}
            main_data = self.mapping(DtoSakuhinBind.DtoDelTwitter,self.dao_m_sakuhin_map.selectSakuhinForFlg(param_code))

            #当作品の紐付けたTwitter（メインフラグ＝True）が存在する場合
            if  main_data:
                # 強制解除フラグがTrue設定
                delflg = True
                # 強制解除の作品紐付けID
                map_id = main_data[0].sakuhin_map_id
                del_user = main_data[0].user_name

                param_del ={
                    'full_name' : full_name,
                    'sakuhin_map_id' : map_id
                }

                # 当作品紐付けたTwitterを紐付け解除処理行う
                self.dao_m_sakuhin_map.updateInvalidFlgBy(param_del)

                # 変更履歴の登録
                # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
                entity = ('m_sakuhin_map', '削除', sakuhin_name, 'Twitter'+ del_user, full_name)
                self.dao_t_update_history.insert(entity)

                # Twitter関連作品追加処理を行う
                self.dao_m_sakuhin_map.insertBySakuhinCode(param)
            else:
                # 当作品の紐付けTwitter（メインフラグ＝True）が存在しない場合、
                # Twitter関連作品追加処理を行う
                self.dao_m_sakuhin_map.insertBySakuhinCode(param)
        else:
            # Twitter関連作品追加処理を行う
            self.dao_m_sakuhin_map.insertBySakuhinCode(param)

        # 変更履歴の登録
        # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
        entity = ('m_sakuhin_map', '追加', sakuhin_name, 'Twitter'+ account_name, full_name)
        self.dao_t_update_history.insert(entity)

        # 最新のTwitterリストデータを取得
        param = {'sakuhin_code' : sakuhin_code}
        dto_twitter_list = self.mapping(DtoSakuhinBind.DtoTwitterList, self.dao_m_twitter.selectTwitterBySakuhinCode(param))

        return self.unpack({'delflg':delflg,'del_user':del_user,'twitter_list':dto_twitter_list})

    """
    Gameデータを取得する（モーダル）
    """
    def getGameModalData(self, game_name):
        param = {'game_name' : '%' + game_name + '%'}
        game_list = self.mapping(DtoSakuhinBind.DtoGamerModal, self.dao_m_game_title.selectByGameName(param))
       
        return self.unpack(game_list)

    """
    Game紐付け作品一覧を取得する
    """
    def getGameListData(self, game_code):
        param = {'game_code' : game_code}
        dto_sakuhin_list = self.mapping(DtoSakuhinBind.DtoSakuhinList, self.dao_m_sakuhin.selectSakuhinByGameCode(param))

        return self.unpack(dto_sakuhin_list)

    """
    Gameに関連作品紐付けを解除する
    """
    def delGameSakuhin(self, full_name,sakuhin_map_id,game_code,game_name,sakuhin_name):
        # 作品紐付け解除の無効フラグを変更
        param = {
            'full_name' : full_name,
            'sakuhin_map_id' : sakuhin_map_id
        }
        # 作品紐付け解除処理を行う
        self.dao_m_sakuhin_map.updateInvalidFlgBy(param)

        # 変更履歴の登録
        # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
        entity = ('m_sakuhin_map', '削除', sakuhin_name, 'ゲーム'+ game_name, full_name)
        self.dao_t_update_history.insert(entity)

        # 最新の関連作品データを取得
        return self.getGameListData(game_code)

    """
    Game関連作品追加
    """
    def addGameSakuhin(self, full_name, sakuhin_code_list, game_code, game_name):
        sakuhin_code_list = tuple(sakuhin_code_list)
        # 紐付け登録用パナメーラ
        param ={
            'sakuhin_code_list' : sakuhin_code_list,
            'game_code' : game_code,
            'full_name' : full_name
        }

        # 関連作品追加処理を行う
        self.dao_m_sakuhin_map.insertBySakuhinList(param)

        # 変更履歴の登録
        # (変更テーブル名,操作内容,変更対象,備考,更新者)を設定
        entity = {
            'update_table' : 'm_sakuhin_map',
            'operation' : '追加',
            'sakuhin_code_list' : sakuhin_code_list,
            'remarks' : 'ゲーム' + game_name,
            'full_name' : full_name
        }
        self.dao_t_update_history.insertSakuhinMapBylist(entity)

        # 最新の関連タイトルデータを取得
        return self.getGameListData(game_code)
