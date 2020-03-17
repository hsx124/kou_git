from admin_app.dao.dao_main import DaoMain

class DaoNews(DaoMain):
    def selectNews(self):
        """お知らせ"""

        sql =   """
                SELECT
                  news_id
                , subject
                , headline
                , details
                , link_url
                FROM m_top_news 
                ORDER BY update_time DESC
                LIMIT 1
                """
    
        return self.select(sql)

    def updateNews(self,entity):

        sql =   """
                UPDATE m_top_news
                SET
                  subject = %s
                , headline = %s
                , details = %s
                , link_url = %s
                , update_user = %s
                , update_time = now()
                WHERE
                news_id = %s
                """
        return self.updateWithParam(sql, entity)

    def createNews(self,entity):

        sql =   """
                INSERT INTO m_top_news (
                    subject
                  , headline
                  , details
                  , link_url
                  , update_user
                  , update_time
                  ) 
                VALUES (%s, %s, %s, %s, %s, now())
                """
        return self.updateWithParam(sql, entity)



    
  
