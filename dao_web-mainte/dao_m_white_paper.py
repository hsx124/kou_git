from admin_app.dao.dao_main import DaoMain

class DaoTWhitePaper(DaoMain):
    """白書領域データの取得"""
    def selectWhitePaper(self):

        sql =   """
                SELECT
                  id
                , file_name
                , whitepaper_category
                , instructions
                , year
                , related_ip
                , update_user
                , update_date 
                FROM m_white_paper
                WHERE is_invalid = false
                ORDER BY year ASC
                , update_date ASC
                """

        return self.select(sql)
