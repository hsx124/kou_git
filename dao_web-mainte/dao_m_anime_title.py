from admin_app.dao.dao_main import DaoMain

class DaoMAnimeTitle(DaoMain):
    def selectAnimeMasterBySakuhinCode(self, sakuhin_code):
        '''
        アニメマスタ情報取得（グリッド表示用）
        '''

        # 作品コードで作品紐づけマスタを検索
        # 作品紐づけマスタから、作品カテゴリがアニメの紐づけコードを取得
        # 作品コード
        param = {'sakuhin_code': sakuhin_code}
        sql = """
                SELECT
                    m_sakuhin.sakuhin_code
                  , m_sakuhin.sakuhin_name
                  , m_anime_title.*
                FROM ip_dds.m_sakuhin
                LEFT JOIN m_sakuhin_map ON (
                    m_sakuhin_map.sakuhin_code = m_sakuhin.sakuhin_code
                    )
                LEFT JOIN ip_dds.m_anime_title ON (
                    anime_title_code = m_sakuhin_map.title_code
                    )
                WHERE m_sakuhin_map.sakuhin_code = '0000000001'
                AND m_sakuhin_map.title_category_code = '03'
                """
        # SELECT
        #   m_sakuhin.sakuhin_code
        # , m_sakuhin.sakuhin_name
        # , m_anime_title.anime_title_name
        # , m_anime_title.broadcast_station
        # , m_anime_title.broadcast_period
        # , m_anime_title.update_user
        # , m_anime_title.update_date
        # FROM m_anime_title
        # INNER JOIN m_anime_title ON (
        #                         SELECT
        #                             m_sakuhin_map.title_code
        #                         FROM ip_dds.m_sakuhin_map
        #                         WHERE m_sakuhin_map.sakuhin_code = '0000000001'
        #                         AND m_sakuhin_map.title_category_code = '03'
        #                         AND m_sakuhin_map.invalid_flg = false
        # )
        # WHERE m_anime_title.invalid_flg = false
        # ORDER BY m_anime_title.anime_title_name ASC

        return self.selectWithParam(sql, param)

    def selectAnimeMasterforCSV(self):
        '''
        アニメマスタ情報取得(CSVダウンロード全件用)
        '''
        sql = """
                SELECT
                  m_anime_title.sakuhin_code
                , m_anime_title.anime_title_name
                , m_anime_title.broadcast_station
                , m_anime_title.broadcast_period
                , m_anime_title.create_user
                , m_anime_title.create_date
                , m_anime_title.update_user
                , m_anime_title.update_date
                FROM m_anime_title
                INNER JOIN m_sakuhin ON (
                    m_anime_title.sakuhin_code = m_sakuhin.sakuhin_code 
                    AND m_sakuhin.invalid_flg = false
                )
                WHERE m_anime_title.invalid_flg = false
                ORDER BY
                  m_anime_title.sakuhin_code ASC
                , m_anime_title.anime_title_name ASC
                """
        return self.select(sql)

    def updateInvalidFlgByTvProgramName(self, anime_title_name, full_name):
        '''
        アプリマスタレコード論理削除
        無効フラグを有効にする
        '''
        sql = """
                UPDATE m_anime_title
                SET invalid_flg = true
                , update_user = %s
                , update_date = now()
                WHERE m_anime_title.anime_title_name = %s
                """

        return self.updateWithParam(sql, (full_name, anime_title_name))

    def insertMAnime(self, entity):
        '''
        新規wikiマスタ（アニメマスタ）レコード作成
        '''

        # 既にアニメ作品が登録されている場合は登録不可とする。
        if 0 < self.selectCountAnimeByIpCode((entity[0])):
            raise DaoMAnime.DuplicateAnimeException

        sql = """
                INSERT INTO m_anime_title
                (
                  sakuhin_code
                , anime_title_name
                , broadcast_station
                , broadcast_period
                , invalid_flg
                , create_user
                , create_date
                , update_user
                , update_date
                )
                VALUES (
                  %s
                , %s
                , %s
                , %s
                , false
                , %s 
                , now()
                , %s
                , now()
                )
                """
        return self.updateWithParam(sql, entity)

    def updateMWiki(self, entity):
        '''
        wikiマスタ（アニメマスタ）レコード編集
        '''

        sql = """
                UPDATE m_anime_title
                SET 
                  anime_title_name = %s
                , broadcast_station = %s
                , broadcast_period = %s
                , update_user = %s
                , update_date = now()
                WHERE sakuhin_code = %s
                AND anime_title_name = %s
                AND invalid_flg = false
                """
        return self.updateWithParam(sql, entity)

    def selectMWikiByIpCodeAnimeName(self, entity):
        '''
        アニメ編集画面表示用
        '''

        sql = """
                SELECT
                  m_anime_title.sakuhin_code
                , m_sakuhin.sakuhin_name
                , m_anime_title.anime_title_name
                , m_anime_title.broadcast_station
                , m_anime_title.broadcast_period
                FROM m_anime_title
                INNER JOIN m_sakuhin ON (
                    m_anime_title.sakuhin_code = m_sakuhin.sakuhin_code 
                    AND m_sakuhin.invalid_flg = false
                )
                WHERE m_anime_title.invalid_Fl = false
                AND m_anime_title.sakuhin_code = %s
                AND m_anime_title.anime_title_name = %s
                LIMIT 1
                """
        return self.selectWithParam(sql, entity)

    def selectCountAnimeByIpCode(self, sakuhin_code):
        '''
        アニメ作品重複チェック
        '''

        param = {'sakuhin_code': sakuhin_code}
        sql = """
                SELECT count(*)
                FROM m_anime_title
                WHERE m_anime_title.invalid_flg = false
                AND m_anime_title.sakuhin_code = %(sakuhin_code)s
                """
        return self.selectWithParam(sql, param)[0][0]

    class DuplicateAnimeException(Exception):
        """
        アニメ作品重複エラー
        """
        pass

    """タイトル名・タイトルかな名をもとにアニメタイトルデータを取得""" 
    def selectTitleByName(self, param):
        sql =   """
			          SELECT
                    anime_title_code
                    , anime_title_name
                    , 'アニメ' AS category_name
                    , '03' AS category_code
                    , update_user
                    , update_time
                FROM m_anime_title
                WHERE invalid_flg = false
                AND anime_title_name LIKE %(title_name)s
                ORDER BY anime_title_code
                """
        return self.selectWithParam(sql, param)