from ipdds_app.dao.dao_main import DaoMain

class DaoTTwitter(DaoMain):
    """Twitterランキングの取得"""
    def selectRankingTwitter(self):

        sql =   """
                SELECT
                  rank() OVER ( 
                    ORDER BY
                      t2.follower_cnt - t1.follower_cnt DESC
                  ) 
                  , COALESCE(m_sakuhin.key_visual_file_name, '')
                  , m_sakuhin.sakuhin_code
                  , m_twitter.account_name
                  , to_char( 
                    t2.follower_cnt - t1.follower_cnt
                    , '999,999,999'
                  ) AS follower_cnt 
                FROM
                  ( 
                    SELECT
                      twitter_id
                      , COALESCE(follower_cnt,0) as follower_cnt
                    FROM
                      t_twitter 
                    WHERE
                      (twitter_id, result_yyyymm) IN ( 
                        SELECT
                          t_twitter.twitter_id
                          , MIN(t_twitter.result_yyyymm) as result_yyyymm 
                        FROM
                          t_twitter 
                        WHERE
                          t_twitter.result_yyyymm >= to_char(current_timestamp + '-3 months', 'yyyymm')
                        GROUP BY
                          t_twitter.twitter_id
                      )
                  ) AS t1 
                  LEFT OUTER JOIN ( 
                    SELECT
                      twitter_id
                      , COALESCE(follower_cnt,0) as follower_cnt
                    FROM
                      t_twitter 
                    WHERE
                      (twitter_id, result_yyyymm) IN ( 
                        SELECT
                          t_twitter.twitter_id
                          , MAX(t_twitter.result_yyyymm) as result_yyyymm 
                        FROM
                          t_twitter 
                        WHERE
                          t_twitter.result_yyyymm < to_char(current_timestamp, 'yyyymm') 
                        GROUP BY
                          t_twitter.twitter_id
                      )
                  ) AS t2 
                    ON t1.twitter_id = t2.twitter_id 
                  INNER JOIN m_twitter 
                    ON t2.twitter_id = m_twitter.twitter_id
                       and m_twitter.invalid_flg = false 
                  INNER JOIN m_sakuhin_map
                    ON m_twitter.twitter_code = m_sakuhin_map.title_code
                       and m_sakuhin_map.invalid_flg = false
                  INNER JOIN m_sakuhin 
                    ON m_sakuhin.sakuhin_code = m_sakuhin_map.sakuhin_code
                       and m_sakuhin.invalid_flg = false
                       and TO_DATE(valid_start_yyyymmdd, 'YYYYMMDD') <= now() and now() <= TO_DATE(valid_end_yyyymmdd, 'YYYYMMDD')
                ORDER BY
                  t2.follower_cnt - t1.follower_cnt DESC 
                LIMIT
                  5
                """

        return self.select(sql)

    """ツイッターIDをもとにフォロワー数取得（グラフ用）"""
    def selectTwitterGraphData(self,twitter_id):
        sql = """
			    SELECT
				      left (t_twitter.result_yyyymm, 4) || '-' || right (t_twitter.result_yyyymm, 2)
            , t_twitter.follower_cnt::numeric::integer
          FROM t_twitter
          WHERE
            t_twitter.twitter_id = %s
            AND to_char(current_timestamp - interval '1 years','yyyymm') <= t_twitter.result_yyyymm
            AND t_twitter.result_yyyymm < to_char(current_timestamp, 'yyyymm')
          """
        return self.selectWithParam(sql,[twitter_id])


    """作品コードに紐づくtwitterIDを取得"""
    def selectTwitterData(self,sakuhin_code):
        sql = """
      			  SELECT
                twitter_id
              FROM m_sakuhin_map INNER JOIN m_twitter
                ON m_sakuhin_map.title_code = m_twitter.twitter_code
              WHERE m_sakuhin_map.sakuhin_code = %s

              """
        return self.selectWithParam(sql,[sakuhin_code])

    """ツイッターIDをもとに実績データを取得"""
    def selectTwitterZissekiData(self,twitter_id):
        sql = """
              SELECT
                  m_twitter.twitter_id
                , account_name
                , twitter_latest.follower_cnt
                , twitter_3months_ago.follower_cnt
                , twitter_1year_ago.follower_cnt
                , user_name
              FROM m_twitter
              	INNER JOIN (SELECT
                    t_twitter.twitter_id
              	  , t_twitter.follower_cnt
                  FROM
                    t_twitter
                    LEFT JOIN m_twitter
                      ON t_twitter.twitter_id = m_twitter.twitter_id
                      AND t_twitter.result_yyyymm < to_char(current_timestamp, 'yyyymm')
                      AND m_twitter.invalid_flg = false
                  WHERE
                    t_twitter.twitter_id = %s
                  ORDER BY
                    m_twitter.twitter_create_time
                    , t_twitter.result_yyyymm DESC
                  LIMIT
                    1
              )  twitter_latest
              ON m_twitter.twitter_id = twitter_latest.twitter_id
              INNER JOIN (
              SELECT
                    t_twitter.twitter_id
              	  , t_twitter.follower_cnt
                  FROM
                    t_twitter
                    LEFT JOIN m_twitter
                      ON t_twitter.twitter_id = m_twitter.twitter_id
                      AND t_twitter.result_yyyymm = to_char(current_timestamp - interval '3 months' , 'yyyymm') 
                      AND m_twitter.invalid_flg = false
                  WHERE
                    t_twitter.twitter_id = %s
                  ORDER BY
                    m_twitter.twitter_create_time
                    , t_twitter.result_yyyymm DESC
                  LIMIT
                    1) twitter_3months_ago
              	  ON m_twitter.twitter_id = twitter_3months_ago.twitter_id
              INNER JOIN
              (
              SELECT
                    t_twitter.twitter_id
              	  , t_twitter.follower_cnt
                  FROM
                    t_twitter
                    LEFT JOIN m_twitter
                      ON t_twitter.twitter_id = m_twitter.twitter_id
                      AND t_twitter.result_yyyymm = to_char(current_timestamp - interval '1 years', 'yyyymm')
                      AND m_twitter.invalid_flg = false
              		WHERE
                    t_twitter.twitter_id = %s
                  ORDER BY
                    m_twitter.twitter_create_time
                  LIMIT
                    1
              	  ) twitter_1year_ago
              	ON m_twitter.twitter_id = twitter_1year_ago.twitter_id
              """
        return self.selectWithParam(sql,[twitter_id,twitter_id,twitter_id])

    """ツイッターIDをもとにフォロワー数取得"""
    def selectGraphData(self,twitter_id):
        sql = """
			    SELECT
              m_twitter.twitter_code
            , m_twitter.account_name
				    , left (t_twitter.result_yyyymm, 4) || '-' || right (t_twitter.result_yyyymm, 2)
            , t_twitter.follower_cnt::numeric::integer
          FROM t_twitter
            INNER JOIN m_twitter
              ON t_twitter.twitter_id = m_twitter.twitter_id
              AND m_twitter.invalid_flg = false
          WHERE
            t_twitter.twitter_id = %s
            AND to_char(current_timestamp - interval '1 years','yyyymm') <= t_twitter.result_yyyymm
            AND t_twitter.result_yyyymm < to_char(current_timestamp, 'yyyymm')
          """
        return self.selectWithParam(sql,[twitter_id])