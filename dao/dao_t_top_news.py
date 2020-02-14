from ipdds_app.dao.dao_main import DaoMain

class DaoMTopNews(DaoMain):

    """最新のお知らせデータを1件取得"""
    def selectLatestNotice(self):

        sql =   """
                SELECT
                  to_char(update_date, 'YYYY/MM/DD') as release_date
                  , subject
                  , article
                  , link_url 
                FROM
                  t_top_news 
                WHERE
                  update_date < now() 
                ORDER BY
                  update_date DESC
                LIMIT
                  1
                """

        return self.select(sql)

    """NEWSデータの取得(最新以外)"""
    def selectNews(self):

        sql =   """
                SELECT
                  category
                  , to_char(datetime, 'YYYY/MM/DD') as datetime
                  , headline 
                  , link_url 
                FROM
                  ( 
                    ( 
                      SELECT
                        'お知らせ' AS category
                        , update_date AS datetime
                        , headline AS headline
                        , link_url as link_url 
                      FROM
                        t_top_news 
                      ORDER BY
                        update_date DESC OFFSET 1
                    ) 
                    UNION ( 
                      SELECT
                        '新着IP' AS category
                        , create_date AS datetime
                        , ip_name AS headline
                        , ip_code as link_url 
                      FROM
                        m_ip 
                      WHERE
                        create_date = update_date
                        and m_ip.is_invalid = false
                        and valid_start_date <= now() and now() <= valid_end_date
                    ) 
                    UNION ( 
                      SELECT
                        '更新情報' AS category
                        , update_date AS datetime
                        , ip_name AS headline
                        , ip_code as link_url 
                      FROM
                        m_ip 
                      WHERE
                        create_date != update_date
                        and m_ip.is_invalid = false
                        and valid_start_date <= now() and now() <= valid_end_date
                    ) 
                    ORDER BY
                      datetime DESC
                  ) as foo
                """

        return self.select(sql)