from ipdds_app.dao.dao_main import DaoMain

class DaoTApp(DaoMain):

    """アプリランキングデータの取得"""
    def selectRankingApp(self):

        sql =   """
                SELECT
                  rank() OVER (ORDER BY sum(download_cnt) DESC) AS rank
                  , COALESCE(m_sakuhin.key_visual_file_name, '')
                  , t1.sakuhin_code
                  , t1.app_title_name
                  , to_char(sum(download_cnt), '999,999,999') as download_cnt 
                FROM
                  ( 
                    ( 
                      SELECT
                        m_app_title.app_title_name
                        , m_sakuhin.sakuhin_code
                        , COALESCE(t_app.download_cnt,0) as download_cnt
                      FROM
                        t_app 
                        INNER JOIN m_app_title 
                          ON m_app_title.app_id_ios = t_app.app_id 
                             and m_app_title.invalid_flg = false

                        INNER JOIN m_sakuhin_map
                          ON m_app_title.app_title_code = m_sakuhin_map.title_code
                             and m_sakuhin_map.invalid_flg = false
                             
                        INNER JOIN m_sakuhin 
                          ON m_sakuhin_map.sakuhin_code = m_sakuhin.sakuhin_code 
                             and m_sakuhin.invalid_flg = false
                             and TO_DATE(valid_start_yyyymmdd, 'YYYYMMDD') <= now() and now() <= TO_DATE(valid_end_yyyymmdd, 'YYYYMMDD')
                      WHERE
                        t_app.result_yyyymm >= to_char(current_timestamp + '-3 months', 'yyyymm') 
                        and t_app.result_yyyymm < to_char(current_timestamp, 'yyyymm')
                    ) 
                    UNION ALL ( 
                      SELECT
                        m_app_title.app_title_name
                        , m_sakuhin.sakuhin_code
                        , COALESCE(t_app.download_cnt,0) as download_cnt
                      FROM
                        t_app 
                      INNER JOIN m_app_title 
                        ON m_app_title.app_id_android = t_app.app_id 
                           and m_app_title.invalid_flg = false
                      INNER JOIN m_sakuhin_map
                        ON m_app_title.app_title_code = m_sakuhin_map.title_code
                            and m_sakuhin_map.invalid_flg = false            
                      INNER JOIN m_sakuhin 
                        ON m_sakuhin_map.sakuhin_code = m_sakuhin.sakuhin_code 
                            and m_sakuhin.invalid_flg = false
                            and TO_DATE(valid_start_yyyymmdd, 'YYYYMMDD') <= now() and now() <= TO_DATE(valid_end_yyyymmdd, 'YYYYMMDD')                          
                      WHERE
                        t_app.result_yyyymm >= to_char(current_timestamp + '-3 months', 'yyyymm') 
                        and t_app.result_yyyymm < to_char(current_timestamp, 'yyyymm')
                    )
                  ) AS t1 
                  INNER JOIN m_sakuhin 
                    ON t1.sakuhin_code = m_sakuhin.sakuhin_code 
                       and m_sakuhin.invalid_flg = false
                       and TO_DATE(valid_start_yyyymmdd, 'YYYYMMDD') <= now() and now() <= TO_DATE(valid_end_yyyymmdd, 'YYYYMMDD')
                WHERE
                  m_sakuhin.sakuhin_code IS NOT NULL
                GROUP BY
                  t1.app_title_name
                  , t1.sakuhin_code
                  , m_sakuhin.key_visual_file_name 
                ORDER BY
                  sum(download_cnt) DESC 
                LIMIT
                  5
                """

        return self.select(sql)

    """アプリIDをもとにアプリデータを取得"""
    def selectGraphData(self,app_id_ios,app_id_android,select_item):
        sql = """
              SELECT
                m_app_title.app_title_code
                , m_app_title.app_title_name
                , left (result_app.result_yyyymm, 4) || '-' || right (result_app.result_yyyymm, 2) AS result_yyyymm
                , sum(result_app.{select_item}) ::numeric ::integer AS result_data
              FROM
                m_app_title
                INNER JOIN (
                  SELECT
                    m_app_title.app_title_code
                    , m_app_title.app_title_name
                    , t_app.result_yyyymm
                    , t_app.{select_item}
                  FROM
                    t_app
                    LEFT JOIN m_app_title
                      ON t_app.app_id = m_app_title.app_id_ios
                  WHERE
                    t_app.app_id = %s
                    and to_char(
                      current_timestamp - interval '1 years'
                      , 'yyyymm'
                    ) <= t_app.result_yyyymm
                    and t_app.result_yyyymm < to_char(current_timestamp, 'yyyymm')
                  UNION ALL
                  SELECT
                    m_app_title.app_title_code
                    , m_app_title.app_title_name
                    , t_app.result_yyyymm
                    , t_app.{select_item}
                  FROM
                    t_app
                    LEFT JOIN m_app_title
                      ON t_app.app_id = m_app_title.app_id_android
                  WHERE
                    t_app.app_id = %s
                    and to_char(
                      current_timestamp - interval '1 years'
                      , 'yyyymm'
                    ) <= t_app.result_yyyymm
                    and t_app.result_yyyymm < to_char(current_timestamp, 'yyyymm')
                ) AS result_app
                  ON m_app_title.app_title_code = result_app.app_title_code
              GROUP BY
                m_app_title.app_title_code
                , m_app_title.app_title_name
                , result_app.result_yyyymm
              """
        return self.selectWithParam(sql.format(select_item=select_item),[app_id_ios,app_id_android])

    """アプリの発売日を取得(グラフ用)"""
    def selectAppServiceStartDate(self,app_title_code):
        sql = """
          SELECT
  				  LEFT(min(service_start_yyyymmdd),6)
					FROM m_app_title
					WHERE
					  app_title_code = %s
					  AND invalid_flg = FALSE
          LIMIT 1
          """
        return self.selectWithParam(sql,[app_title_code])

    """アプリ名をもとにアプリデータ（累計売上（発売日からNか月）を取得"""
    def selectAppFromServiceStartDateSalesGraphData(self,firstDate,app_title_name,app_id_ios,app_id_android):
        sql = """
		        SELECT
              left(t2.result_yyyymm,4) || '-' || right(t2.result_yyyymm,2) AS result_yyyymm
              , round(( 
                  SELECT
                    sum(t1.monthly_sales_gaku)
                  FROM t_app t1 
                  WHERE
                    t1.app_title_name = t2.app_title_name
                    AND t1.result_yyyymm <= t2.result_yyyymm), 0 )::numeric::integer first_total_sales
            FROM t_app t2 
            WHERE
              	t2.app_title_name = %s
                AND t2.result_yyyymm >= %s
              	AND t2.result_yyyymm < to_char((TO_DATE(%s, 'YYYYMMDD') + interval '1 years'),'yyyymm')
                AND t2.result_yyyymm < to_char(current_timestamp,'yyyymm')
                AND (t2.app_id = %s OR t2.app_id = %s)  
            GROUP BY
              t2.result_yyyymm
              , t2.app_title_name 
            ORDER BY
              t2.result_yyyymm
            """
        return self.selectWithParam(sql,[app_title_name,firstDate,firstDate,app_id_ios,app_id_android])

    """アプリ名をもとに累計ダウンロード数（発売日からNか月））を取得"""
    def selectAppFromServiceStartDateDownloadGraphData(self,firstDate,app_title_name,app_id_ios,app_id_android):
        sql = """
		        SELECT
              left(t2.result_yyyymm,4) || '-' || right(t2.result_yyyymm,2) AS result_yyyymm
              , round(( 
                  SELECT
                    sum(t1.download_cnt)
                  FROM t_app t1
                  WHERE
                    t1.app_title_name = t2.app_title_name 
                    AND t1.result_yyyymm <= t2.result_yyyymm), 0)::numeric::integer first_total_count
            FROM t_app t2
            WHERE
              	t2.app_title_name = %s
                AND t2.result_yyyymm >= %s
              	AND t2.result_yyyymm < to_char((TO_DATE(%s, 'YYYYMMDD') + interval '1 years'),'yyyymm')
                AND t2.result_yyyymm < to_char(current_timestamp,'yyyymm')
                AND (t2.app_id = %s OR t2.app_id = %s)  
            GROUP BY
              t2.result_yyyymm
              , t2.app_title_name 
            ORDER BY
              t2.result_yyyymm
            """
        return self.selectWithParam(sql,[app_title_name,firstDate,firstDate,app_id_ios,app_id_android])

    """アプリ名をもとにアプリの累計売上グラフのデータを取得"""
    def selectAppTotalSalesGraphData(self,firstDate,app_title_name,app_id_ios,app_id_android):
        sql = """
            SELECT
              left(t2.result_yyyymm,4) || '-' || right(t2.result_yyyymm,2) AS result_yyyymm
              , round(( 
                  SELECT
                    sum(t1.monthly_sales_gaku)
                  FROM t_app t1
                  WHERE
                    t1.app_title_name = t2.app_title_name
                    AND t1.result_yyyymm <= t2.result_yyyymm), 0 )::numeric::integer total_sales
            FROM t_app t2 
            WHERE
              t2.app_title_name = %s
              AND t2.result_yyyymm >= to_char(current_timestamp - interval '1 years', 'yyyymm')
              AND t2.result_yyyymm < to_char(current_timestamp, 'yyyymm')
              AND t2.result_yyyymm >= %s
              AND (t2.app_id = %s OR t2.app_id = %s) 
            GROUP BY
              t2.result_yyyymm
              , t2.app_title_name 
            ORDER BY
              t2.result_yyyymm
            """
        return self.selectWithParam(sql,[app_title_name,firstDate,app_id_ios,app_id_android])

    """アプリ名を累計ダウンロード数グラフのデータを取得"""
    def selectAppTotalDownloadGraphData(self,firstDate,app_title_name,app_id_ios,app_id_android):
        sql = """
            SELECT
            left(t2.result_yyyymm,4) || '-' || right(t2.result_yyyymm,2) AS result_yyyymm
              , round(( 
                  SELECT
                    sum(t1.download_cnt)
                  FROM t_app t1 
                  WHERE
                    t1.app_title_name = t2.app_title_name
                    AND t1.result_yyyymm <= t2.result_yyyymm), 0)::numeric::integer total_count
            FROM t_app t2 
            WHERE
              t2.app_title_name = %s
              AND t2.result_yyyymm >= to_char(current_timestamp - interval '1 years', 'yyyymm')
              AND t2.result_yyyymm < to_char(current_timestamp, 'yyyymm')
              AND t2.result_yyyymm >= %s
              AND (t2.app_id = %s OR t2.app_id = %s) 
            GROUP BY
              t2.result_yyyymm
              , t2.app_title_name
            ORDER BY
              t2.result_yyyymm
            """
        return self.selectWithParam(sql,[app_title_name,firstDate,app_id_ios,app_id_android])

    """アプリの平均売上グラフと平均ダウンロード数グラフのデータを取得"""
    def selectAppAvgSalesAndDownloadGraphData(self,firstDate,app_title_name,app_id_ios,app_id_android):
        sql = """
            SELECT
              left(t2.result_yyyymm,4) || '-' || right(t2.result_yyyymm,2) AS result_yyyymm
              , round(( 
                  SELECT
                    sum(t1.monthly_sales_gaku) / count(DISTINCT result_yyyymm) 
                  FROM t_app t1 
                  WHERE
                    t1.app_title_name = t2.app_title_name 
                    AND t1.result_yyyymm <= t2.result_yyyymm), 0 )::numeric::integer avg_sales
              , round(( 
                  SELECT
                    sum(t1.download_cnt) / count(DISTINCT result_yyyymm) 
                  FROM t_app t1 
                  WHERE
                    t1.app_title_name = t2.app_title_name
                    AND t1.result_yyyymm <= t2.result_yyyymm), 0)::numeric::integer avg_count
            FROM t_app t2 
            WHERE
              t2.app_title_name = %s
              AND t2.result_yyyymm >= to_char(current_timestamp - interval '1 years', 'yyyymm')
              AND t2.result_yyyymm < to_char(current_timestamp, 'yyyymm')
              AND t2.result_yyyymm >= %s
              AND (t2.app_id = %s OR t2.app_id = %s) 
            GROUP BY
              t2.result_yyyymm
              , t2.app_title_name
            ORDER BY
              t2.result_yyyymm
            """
        return self.selectWithParam(sql,[app_title_name,firstDate,app_id_ios,app_id_android])