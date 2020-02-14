from admin_app.dao.dao_main import DaoMain

class DaoMGameTitle(DaoMain):

    """ゲーム名をもとに、Gameデータ検索"""
    def selectByGameName(self, param):
        sql =   """
                SELECT
                game_title_code
                , game_title_name
                , hanbai_company_name
                , platform_name
                , release_yyyymmdd
                , update_user
                , update_time
                FROM m_game_title
                WHERE invalid_flg = false
                AND game_title_name LIKE %(game_name)s
                ORDER BY game_title_code ASC
                """
        return self.selectWithParam(sql, param)