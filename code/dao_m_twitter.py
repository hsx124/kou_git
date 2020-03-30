from admin_app.dao.dao_main import DaoMain

class DaoMTwitter(DaoMain):

    def selectAll(self):
        """
        Twitterマスタ全件取得
        """
        sql =   """
                SELECT
                  m_twitter.twitter_code
                , m_twitter.account_name
                , m_twitter.user_name
                , m_twitter.main_account_flg
                , m_twitter.update_user
                , m_twitter.update_time
                FROM m_twitter
                WHERE invalid_flg = false
                ORDER BY 
                m_twitter.update_time DESC,
                m_twitter.twitter_code ASC
                """
        return self.select(sql)

    def selectCsvData(self):
        """
        Twitterマスタ全件取得(CSV出力用)
        """
        sql =   """
                SELECT
                  m_twitter.twitter_code
                , m_twitter.account_name
                , m_twitter.user_name
                , m_twitter.main_account_flg
                , m_twitter.twitter_id
                , m_twitter.account_create_time
                , m_twitter.create_user
                , m_twitter.create_time
                , m_twitter.update_user
                , m_twitter.update_time
                FROM m_twitter
                WHERE invalid_flg = false
                ORDER BY
                m_twitter.twitter_code ASC
                """
        return self.select(sql)

    """削除する前に該当データの無効フラグ確認""" 
    def selectInvalidFlg(self, param):
        sql =   """
                SELECT
                    invalid_flg
                FROM m_twitter
                WHERE twitter_code = %(twitter_code)s
                """
        return self.selectWithParam(sql, param)[0][0]

    """Twitterコード最大値取得"""
    def selectMaxTwitterCode(self):

        sql =   """
                SELECT
                  coalesce(max(right(twitter_code,9)),'FMT000000000')
                FROM m_twitter
                """
        return self.select(sql)[0][0]

    """Twitterデータを倫理削除""" 
    def deleteTwitterData(self, param):
        sql =   """
                UPDATE m_twitter
                SET invalid_flg = true
                  , update_user = %(full_name)s
                  , update_time = now()
                WHERE twitter_code = %(title_code)s
                """
        return self.updateWithParam(sql, param)

    """アカウント名をもとに、twitterデータ検索"""
    def selectByTwitterName(self, param):
        sql =   """
                SELECT
                m_twitter.twitter_code
                , m_twitter.user_name
                , m_twitter.account_name
                , m_twitter.main_account_flg
                , m_twitter.update_user
                , m_twitter.update_time
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

    #重複チェック
    """Twitterコード重複エラー"""
    class DuplicateTwitterCodeException(Exception):
        pass

    """ユーザー名重複エラー"""
    class DuplicateUserNameException(Exception):
        pass

    #インサート
    """新規Twitterマスタ作成"""
    def insert(self, param):

        # Twitterコード重複チェック
        twitter_code = {
            'twitter_code': param['twitter_code']
        }
        if 0 < self.selectSameCode(twitter_code):
            raise DaoMTwitter.DuplicateTwitterCodeException

        # ユーザー名重複チェック
        user_name = {
            'user_name': param['user_name'],
            'twitter_code': param['twitter_code']
        }
        if 0 < self.selectSameUserName(user_name):
          raise DaoMTwitter.DuplicateUserNameException

        sql =   """
                INSERT INTO m_twitter(
                    twitter_code
                    , twitter_id
                    , account_name
                    , user_name
                    , main_account_flg
                    , auto_collect_flg
                    , invalid_flg
                    , create_user
                    , create_time
                    , update_user
                    , update_time
                    ) VALUES(%(twitter_code)s, %(twitter_id)s, %(account_name)s, %(user_name)s, %(main_account_flg)s, true, false, %(full_name)s , now(), %(full_name)s , now())
                """
        return self.updateWithParam(sql, param)

    """ツイッターマスタ編集画面表示用"""
    def selectUpdateData(self, param):
        sql =   """
                SELECT
                  m_twitter.twitter_code
                , m_twitter.account_name
                , m_twitter.user_name
                , m_twitter.main_account_flg
                FROM m_twitter
                WHERE m_twitter.invalid_flg = false
                AND m_twitter.twitter_code = %(twitter_code)s
                """
        return self.selectWithParam(sql, param)
 
    """同一ユーザー名を検索"""
    def selectSameUserName(self, param):

        sql =   """
                SELECT count(*)
                FROM m_twitter
                WHERE user_name = %(user_name)s
                AND twitter_code <> %(twitter_code)s
                AND invalid_flg = false
                """
        return self.selectWithParam(sql, param)[0][0]

    """同一Twitterコードを検索"""
    def selectSameCode(self, param):
        sql =   """
                SELECT count(*)
                FROM m_twitter
                WHERE twitter_code = %(twitter_code)s
                """
        return self.selectWithParam(sql, param)[0][0]

    """ツイッターマスタ更新"""
    def update(self, param):
        # ユーザー名重複チェック
        check_param = {
            'user_name': param['user_name'],
            'twitter_code': param['twitter_code']
        }
        if 0 < self.selectSameUserName(check_param):
          raise DaoMTwitter.DuplicateUserNameException

        sql =   """
                UPDATE m_twitter
                SET
                  account_name = %(account_name)s
                , user_name = %(user_name)s
                , main_account_flg = %(main_account_flg)s
                , update_user = %(full_name)s
                , update_time = now()
                WHERE twitter_code = %(twitter_code)s
                """
        return self.updateWithParam(sql,param)

    def selectMapSakuhinByTwitterCode(self,param):
        sql =   """
                SELECT
                    sakuhin_map.sakuhin_map_id
                    , twitter.twitter_code
                    , twitter.account_name 
                    , twitter.user_name
                FROM
                    m_twitter twitter 
                INNER JOIN m_sakuhin_map sakuhin_map 
                    ON twitter.twitter_code = sakuhin_map.title_code 
                    AND twitter.invalid_flg = FALSE 
                    AND twitter.main_account_flg = TRUE 
                INNER JOIN m_sakuhin sakuhin 
                    ON sakuhin_map.sakuhin_code = sakuhin.sakuhin_code 
                    AND sakuhin_map.invalid_flg = FALSE 
                WHERE
                    sakuhin.sakuhin_code in ( 
                    select
                    mp.sakuhin_code 
                    from
                    m_sakuhin_map mp 
                    inner join m_twitter tw 
                        on tw.twitter_code = mp.title_code 
                        and tw.invalid_flg = mp.invalid_flg 
                    where
                        tw.twitter_code = %(twitter_code)s
                        
                    ) 
                    AND sakuhin.invalid_flg = FALSE
                """
        return self.selectWithParam(sql, param)
    
    """削除する前に該当データの無効フラグ確認""" 
    def selectInvalidFlg(self, param):
        sql =   """
                SELECT
                invalid_flg
                FROM m_sakuhin_map
                WHERE sakuhin_map_id = %(sakuhin_map_id)s
                """
        return self.selectWithParam(sql, param)[0][0]