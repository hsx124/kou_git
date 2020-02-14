from admin_app.dao.dao_main import DaoMain

class DaoMTwitter(DaoMain):

    """アカウント名をもとに、twitterデータ検索"""
    def selectByTwitterName(self, param):
        sql =   """
                SELECT
                twitter_code
                , user_name
                , account_name
                , main_account_flg
                , update_user
                , update_time
                FROM m_twitter
                WHERE invalid_flg = false
                AND account_name LIKE %(twitter_name)s
                ORDER BY twitter_code ASC
                """
        return self.selectWithParam(sql, param)

    """Twitterに紐付け作品データ取得""" 
    def selectTwitterBySakuhinCode(self, param):
        sql =   """
                SELECT
	                twitter.twitter_code
	                , twitter.user_name
	                , twitter.account_name
	                , twitter.main_account_flg
	                , sakuhin_map.update_user
	                , sakuhin_map.update_time
                    , sakuhin_map.sakuhin_map_id
                FROM
                 m_twitter twitter 
                INNER JOIN m_sakuhin_map sakuhin_map 
                    ON twitter.twitter_code = sakuhin_map.title_code
                    AND twitter.invalid_flg = FALSE 
                INNER JOIN m_sakuhin sakuhin
                    ON sakuhin_map.sakuhin_code = sakuhin.sakuhin_code
                    AND sakuhin_map.invalid_flg = FALSE 
                WHERE
                sakuhin.sakuhin_code = %(sakuhin_code)s
                AND sakuhin.invalid_flg = FALSE
                ORDER BY sakuhin_map.update_time DESC
                """
        return self.selectWithParam(sql, param)