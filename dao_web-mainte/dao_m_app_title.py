from admin_app.dao.dao_main import DaoMain

class DaoMAppTitle(DaoMain):
    """タイトル名・タイトルかな名をもとにアプリタイトルデータを取得""" 
    def selectTitleByName(self, param):
        sql =   """
				SELECT
                    app_title_code
                    , app_title_name
                    , 'アプリ' AS category_name
                    , '04' AS category_code
                    , update_user
                    , update_time
                FROM m_app_title
                WHERE invalid_flg = false
                AND app_title_name LIKE %(title_name)s
                ORDER BY app_title_code
                """
        return self.selectWithParam(sql, param)