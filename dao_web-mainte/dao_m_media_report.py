from admin_app.dao.dao_main import DaoMain

class DaoMMediaReport(DaoMain):
    """タイトル名・タイトルかな名をもとに白書タイトルデータを取得""" 
    def selectTitleByName(self, param):
        sql =   """
				SELECT
                    media_report_code
                    , media_report_name
                    , 'メディアレポート' AS category_name
                    , '07' AS category_code
                    , update_user
                    , update_time
                FROM m_media_report
                WHERE invalid_flg = false
                AND media_report_name LIKE %(title_name)s
                ORDER BY media_report_code
                """
        return self.selectWithParam(sql, param)