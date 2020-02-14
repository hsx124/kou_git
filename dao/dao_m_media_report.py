from ipdds_app.dao.dao_main import DaoMain

class DaoMMediaReport(DaoMain):

    
    """メディアレポートを全件取得する"""
    def selectAll(self):

        sql = """
              SELECT
                media_report_code
                , media_report_name
                , media_report_category
                , details
                , year
              FROM
                m_media_report
              WHERE
                invalid_flg = false
              """
              
        return self.select(sql)


    """関連文書の取得"""
    def selectRelatedDocumentsBySakuhinCode(self,sakuhin_code):

        sql =   """
                SELECT
                  year
                  , media_report_category
                  , media_report_code || '_' || media_report_name
                FROM
                  m_media_report LEFT JOIN m_sakuhin_map ON m_media_report.media_report_code = m_sakuhin_map.title_code
                WHERE
                  m_media_report.invalid_flg = false
                  AND m_sakuhin_map.sakuhin_code = %s
                ORDER BY
                  year DESC
                """

        return self.selectWithParam(sql,[sakuhin_code])
