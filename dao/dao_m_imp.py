from ipdds_app.dao.dao_main import DaoMain

class DaoMImp(DaoMain):

    """印象マスタの取得"""
    def selectAll(self):

        sql =   """
                SELECT
                  imp_code
                  , imp_name 
                FROM
                  m_imp 
                WHERE
                  is_invalid = false 
                ORDER BY
                  imp_code
                """

        return self.select(sql)

    """印象マスタの件数の取得"""
    def selectImpCounntMax(self):
            sql =   """
                SELECT
                  count(*)
                FROM
                  m_imp 
                WHERE
                  is_invalid = false 
                """
            return self.select(sql)[0][0]