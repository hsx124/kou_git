from ipdds_app.dao.dao_main import DaoMain

class DaoMWhitePaper(DaoMain):

    """関連文書の取得"""
    def selectRelatedDocumentsByIpCode(self,ip_code):

        sql =   """
                SELECT
                  id
                  , file_name
                  , whitepaper_category
                  , year
                FROM
                  m_white_paper 
                WHERE
                  is_invalid = false
                  and related_ip LIKE %s
                ORDER BY
                  year DESC
                """

        return self.selectWithParam(sql,['%' + ip_code + '%'])
    
    """白書を全件取得する"""
    def selectAll(self):

        sql = """
              SELECT
                id
                , file_name
                , whitepaper_category
                , instructions
                , year
              FROM
                m_white_paper
              WHERE
                is_invalid = false
              """
              
        return self.select(sql)