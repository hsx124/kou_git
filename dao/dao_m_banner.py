from ipdds_app.dao.dao_main import DaoMain

class DaoMBanner(DaoMain):

    """バナーリンクデータの取得"""
    def selectAll(self):

        sql =   """
                SELECT
                is_checked
                , external_site 
                , m_banner.white_paper
                , m_white_paper.file_name
                , '/static/ipdds_app/image/banner/' || position || '/' || thumbnail_file_name
                , title
                , details
                FROM
                  m_banner 
                LEFT JOIN
                  m_white_paper
                ON m_white_paper.id = to_number(case m_banner.white_paper when '' then '0' else m_banner.white_paper end, '9999999999999999999')
                   and m_white_paper.is_invalid = false
                WHERE
                  position in ('1', '2', '3') 
                  and m_banner.is_invalid = false 
                ORDER BY
                  position
                """

        return self.select(sql)
