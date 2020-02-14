from ipdds_app.dao.dao_main import DaoMain

class DaoTMobileApp(DaoMain):

    """アプリランキングデータの取得"""
    def selectRankingApp(self):

        sql =   """
                SELECT
                  rank() OVER (ORDER BY sum(download_count) DESC) AS rank
                  , COALESCE(m_ip.key_visual_file_name, '')
                  , t1.ip_code
                  , t1.app_name
                  , to_char(sum(download_count), '999,999,999') as download_count 
                FROM
                  ( 
                    ( 
                      SELECT
                        m_mobile_app.app_name
                        , m_mobile_app.ip_code
                        , COALESCE(t_mobile_app.download_count,0) as download_count
                      FROM
                        t_mobile_app 
                        INNER JOIN m_mobile_app 
                          ON m_mobile_app.app_id_ios = t_mobile_app.app_id 
                             and m_mobile_app.is_invalid = false
                      WHERE
                        t_mobile_app.result_yyyymm >= to_char(current_timestamp + '-3 months', 'yyyymm') 
                        and t_mobile_app.result_yyyymm < to_char(current_timestamp, 'yyyymm')
                    ) 
                    UNION ALL ( 
                      SELECT
                        m_mobile_app.app_name
                        , m_mobile_app.ip_code
                        , COALESCE(t_mobile_app.download_count,0) as download_count
                      FROM
                        t_mobile_app 
                      INNER JOIN m_mobile_app 
                        ON m_mobile_app.app_id_android = t_mobile_app.app_id 
                           and m_mobile_app.is_invalid = false
                      WHERE
                        t_mobile_app.result_yyyymm >= to_char(current_timestamp + '-3 months', 'yyyymm') 
                        and t_mobile_app.result_yyyymm < to_char(current_timestamp, 'yyyymm')
                    )
                  ) AS t1 
                  INNER JOIN m_ip 
                    ON t1.ip_code = m_ip.ip_code 
                       and m_ip.is_invalid = false
                       and valid_start_date <= now() and now() <= valid_end_date
                WHERE
                  m_ip.ip_code IS NOT NULL
                GROUP BY
                  t1.app_name
                  , t1.ip_code
                  , m_ip.key_visual_file_name 
                ORDER BY
                  sum(download_count) DESC 
                LIMIT
                  5
                """

        return self.select(sql)

    """アプリIDをもとにアプリデータを取得"""
    def selectGraphData(self,app_id_ios,app_id_android,select_item):

        sql = """
              SELECT
                left(t_mobile_app.result_yyyymm,4) || '-' || right(t_mobile_app.result_yyyymm,2) AS result_yyyymm
                , sum(t_mobile_app.{select_item})::numeric::integer AS result_data
              FROM
                t_mobile_app
              WHERE
                (t_mobile_app.app_id = %s
                or t_mobile_app.app_id = %s)
                and to_char(current_timestamp - interval '1 years','yyyymm') <= t_mobile_app.result_yyyymm
                and t_mobile_app.result_yyyymm < to_char(current_timestamp,'yyyymm')
              GROUP BY t_mobile_app.result_yyyymm
              """
        return self.selectWithParam(sql.format(select_item=select_item),[app_id_ios,app_id_android])

    """アプリIDをもとに直近3ヶ月の月商を取得"""
    def selectLastThreeMonthsSalesDataByAppId(self, app_id_ios,app_id_android):
        sql = """
              SELECT
              sum(monthly_sales)::numeric::integer
              FROM t_mobile_app
              WHERE
              t_mobile_app.result_yyyymm >= to_char(current_timestamp + '-3 months', 'yyyymm') 
              and t_mobile_app.result_yyyymm < to_char(current_timestamp, 'yyyymm')
              and (
                t_mobile_app.app_id = %s
                or t_mobile_app.app_id = %s
              )
              GROUP BY result_yyyymm
              """
        return self.selectWithParam(sql,[app_id_ios,app_id_android])

    """アプリIDをもとにアプリデータ（累計売上（発売日からNか月）と累計ダウンロード数（発売日からNか月））を取得"""
    def selectTotalDataFromFirstDayGraphData(self,app_name):

        sql = """
		        SELECT
              left(t2.result_yyyymm,4) || '-' || right(t2.result_yyyymm,2) AS result_yyyymm
              , round(( 
                  SELECT
                    sum(t1.monthly_sales)
                  FROM
                    t_mobile_app t1 
                  WHERE
                    t1.app_name = t2.app_name 
                    AND t1.result_yyyymm <= t2.result_yyyymm), 0 )::numeric::integer first_total_sales
              , round(( 
                  SELECT
                    sum(t1.download_count)
                  FROM
                    t_mobile_app t1 
                  WHERE
                    t1.app_name = t2.app_name 
                    AND t1.result_yyyymm <= t2.result_yyyymm), 0)::numeric::integer first_total_count
            FROM
              t_mobile_app t2 
            WHERE
              t2.app_name = %s
                AND t2.result_yyyymm >= to_char(
					        (SELECT
  						      min(service_start_date)
						      FROM
						        m_mobile_app 
						      WHERE
						        app_name = %s
						        AND m_mobile_app.is_invalid = FALSE) ,'yyyymm')
              	  AND t2.result_yyyymm < to_char(
			  		        (SELECT
					            min(service_start_date)
					          FROM
					            m_mobile_app 
					          WHERE
					            app_name = %s
					            AND m_mobile_app.is_invalid = FALSE ) + interval '1 years','yyyymm')
            GROUP BY
              t2.result_yyyymm
              , t2.app_name 
            ORDER BY
              t2.result_yyyymm
            """
        return self.selectWithParam(sql,[app_name,app_name,app_name])

    """アプリの平均売上グラフと平均ダウンロード数グラフのデータを取得"""
    def selectAppAvgSalesAndDownloadGraphData(self,app_name):

        sql = """
            SELECT
              left(t2.result_yyyymm,4) || '-' || right(t2.result_yyyymm,2) AS result_yyyymm
              , round(( 
                  SELECT
                    sum(t1.monthly_sales) / count(DISTINCT result_yyyymm) 
                  FROM
                    t_mobile_app t1 
                  WHERE
                    t1.app_name = t2.app_name 
                    AND t1.result_yyyymm <= t2.result_yyyymm), 0 )::numeric::integer avg_sales
              , round(( 
                  SELECT
                    sum(t1.download_count) / count(DISTINCT result_yyyymm) 
                  FROM
                    t_mobile_app t1 
                  WHERE
                    t1.app_name = t2.app_name 
                    AND t1.result_yyyymm <= t2.result_yyyymm), 0)::numeric::integer avg_count
            FROM
              t_mobile_app t2 
            WHERE
              t2.app_name = %s
              AND t2.result_yyyymm >= to_char(current_timestamp - interval '1 years', 'yyyymm')
              AND t2.result_yyyymm < to_char(current_timestamp, 'yyyymm')
            GROUP BY
              t2.result_yyyymm
              , t2.app_name 
            ORDER BY
              t2.result_yyyymm
            """
        return self.selectWithParam(sql,[app_name])

    """アプリの累計売上グラフと累計ダウンロード数グラフのデータを取得"""
    def selectAppTotalSalesAndDownloadGraphData(self,app_name):

        sql = """
            SELECT
              left(t2.result_yyyymm,4) || '-' || right(t2.result_yyyymm,2) AS result_yyyymm
              , round(( 
                  SELECT
                    sum(t1.monthly_sales)
                  FROM
                    t_mobile_app t1 
                  WHERE
                    t1.app_name = t2.app_name 
                    AND t1.result_yyyymm <= t2.result_yyyymm), 0 )::numeric::integer total_sales
              , round(( 
                  SELECT
                    sum(t1.download_count)
                  FROM
                    t_mobile_app t1 
                  WHERE
                    t1.app_name = t2.app_name 
                    AND t1.result_yyyymm <= t2.result_yyyymm), 0)::numeric::integer total_count
            FROM
              t_mobile_app t2 
            WHERE
              t2.app_name = %s
              AND t2.result_yyyymm >= to_char(current_timestamp - interval '1 years', 'yyyymm')
              AND t2.result_yyyymm < to_char(current_timestamp, 'yyyymm')
            GROUP BY
              t2.result_yyyymm
              , t2.app_name 
            ORDER BY
              t2.result_yyyymm
            """
        return self.selectWithParam(sql,[app_name])

