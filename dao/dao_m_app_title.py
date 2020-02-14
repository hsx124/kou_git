from ipdds_app.dao.dao_main import DaoMain

class DaoMApp(DaoMain):

    """作品コードをもとにアプリ情報を取得"""
    def selectApp(self,sakuhin_code):

        sql = """
              SELECT
                app_title_code
                , app_id_ios
                , app_id_android
              FROM m_app_title LEFT JOIN m_sakuhin_map ON m_app_title.app_title_code = m_sakuhin_map.title_code
              WHERE
                m_app_title.invalid_flg = false
                AND m_sakuhin_map.sakuhin_code = %s
              """
        return self.selectWithParam(sql,[sakuhin_code])

    """作品コードをもとにアプリデータを取得"""
    def selectAppData(self,app_title_code,app_id_ios,app_id_android):

        sql = """
              SELECT
                  COALESCE(m_app_title.app_id_ios, '') || '/' || COALESCE(m_app_title.app_id_android, '')
                , m_app_title.app_title_name
                , case when COALESCE(app_id_ios,'') != '' then 'IOS' else '' end
                  || case when COALESCE(app_id_ios,'') != '' AND COALESCE(app_id_android,'') != '' then '、' else '' end
                  || case when COALESCE(app_id_android,'') != '' then 'Android' else '' end
                  || case when COALESCE(app_id_ios,'') = '' AND COALESCE(app_id_android,'') = '' then 'ー' else '' end
                , hanbai_company_name
                , TO_CHAR(TO_DATE(service_start_yyyymmdd,'yyyymmdd'),'yyyy年MM月')
                , ROUND(avg(monthly_data.sum_monthly_data),0)::numeric ::integer
              FROM m_app_title
              LEFT JOIN (
                SELECT
                  app_title_name
                  , sum(monthly_sales_gaku) ::numeric ::integer AS sum_monthly_data
                FROM
                  t_app
                WHERE
                  t_app.result_yyyymm >= to_char(current_timestamp + '-3 months', 'yyyymm')
                  AND t_app.result_yyyymm < to_char(current_timestamp, 'yyyymm')
                  AND (
                    t_app.app_id = %s
                    or t_app.app_id = %s
                  )
                GROUP BY
                  app_title_name,result_yyyymm
              ) AS monthly_data
                ON m_app_title.app_title_name = monthly_data.app_title_name
              WHERE
                m_app_title.app_title_code = %s
                AND m_app_title.invalid_flg = false
              GROUP BY
                m_app_title.app_title_code
              """
        return self.selectWithParam(sql,[app_id_ios,app_id_android,app_title_code])