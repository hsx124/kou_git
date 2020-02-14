from ipdds_app.dao.dao_main import DaoMain

class DaoMFactTag(DaoMain):

    """事実メタマスタの取得"""
    def selectAll(self):

        sql =   """
                SELECT
                  m_fact_tag_category.fact_tag_category_name
                  , fact_tag_code
                  , fact_tag_name 
                FROM
                  m_fact_tag 
                  LEFT OUTER JOIN m_fact_tag_category 
                    ON m_fact_tag_category.fact_tag_category_code = m_fact_tag.fact_tag_category_code 
                    AND m_fact_tag_category.is_invalid = false 
                WHERE
                  m_fact_tag.is_invalid = false 
                ORDER BY
                  m_fact_tag_category.fact_tag_category_code
                  , fact_tag_code
                """

        return self.select(sql)
