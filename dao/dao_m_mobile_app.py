from ipdds_app.dao.dao_main import DaoMain

class DaoMMobileApp(DaoMain):

    """IPコードをもとにアプリデータを取得"""
    def selectAppData(self,ip_code):

        sql = """
              SELECT
                app_id_ios
                , app_id_android
                , m_mobile_app.app_name
                , case when COALESCE(app_id_ios,'') != '' then 'IOS' else '' end
                  || case when COALESCE(app_id_ios,'') != '' and COALESCE(app_id_android,'') != '' then '、' else '' end
                  || case when COALESCE(app_id_android,'') != '' then 'Android' else '' end
                  || case when COALESCE(app_id_ios,'') = '' and COALESCE(app_id_android,'') = '' then 'ー' else '' end
                , distributor_name
                , to_char(service_start_date,'yyyy年MM月')
              FROM m_mobile_app
              WHERE
                is_invalid = false
                and m_mobile_app.ip_code = %s

              """
        return self.selectWithParam(sql,[ip_code])