from admin_app.dao.dao_main import DaoMain

class DaoNews(DaoMain):
    def selectNews(self):
        """お知らせ"""

        sql =   """
                SELECT
                  id
                , subject
                , headline
                , article
                , link_url
                FROM t_top_news 
                ORDER BY update_date DESC
                LIMIT 1
                """
    
        return self.select(sql)

    def updateNews(self,entity):

        sql =   """
                UPDATE t_top_news
                SET
                  subject = %s
                , headline = %s
                , article = %s
                , link_url = %s
                , update_user = %s
                , update_date = now()
                WHERE
                id = %s
                """
        return self.updateWithParam(sql, entity)

    def createNews(self,entity):

        sql =   """
                INSERT INTO t_top_news (
                    subject
                  , headline
                  , article
                  , link_url
                  , update_user
                  , update_date
                  ) 
                VALUES (%s, %s, %s, %s, %s, now())
                """
        return self.updateWithParam(sql, entity)



    
  
