from admin_app.dao.dao_main import DaoMain

class DaoBanner(DaoMain):
    """バナーリンク"""
    def selectbanner(self,position):

        param = {'position': position}
        sql =   """
                SELECT
                  position
                , thumbnail_file_name
                , title
                , details
                , external_site
                , is_checked
                , white_paper
                , CASE is_checked 
                    WHEN TRUE THEN ''
                    ELSE ( 
                            SELECT file_name 
                            FROM m_white_paper 
                            WHERE id = to_number(COALESCE(m_banner.white_paper,'0'), '9999999999999999999')
                          )
                  END AS white_paper_file_name
                FROM m_banner 
                WHERE position = %(position)s
                AND is_invalid = false 
                ORDER BY
                  position
                """

        return self.selectWithParam(sql, param)

    def selectbannerpreview(self):
        sql = """
              SELECT
                is_invalid
              , thumbnail_file_name
              , title
              , details
              , position
              FROM m_banner
              ORDER BY position ASC
              LIMIT 3
              """
        return self.select(sql)
    
    def updateBanner(self,position,title,details,thumbnail_file_name,external_site,white_paper,is_checked,full_name):
        '''
        バナーリンク更新
        '''
        param = {
                    'position': position,
                    'title': title,
                    'details': details,
                    'thumbnail_file_name': thumbnail_file_name,
                    'external_site': external_site,
                    'white_paper': white_paper,
                    'is_checked': is_checked,
                    'full_name': full_name
                 }
        sql =   """
                UPDATE m_banner
                SET
                  title = %(title)s
                , details = %(details)s
                , thumbnail_file_name = %(thumbnail_file_name)s
                , external_site = %(external_site)s
                , white_paper = %(white_paper)s
                , is_checked = %(is_checked)s
                , update_user = %(full_name)s
                , update_date = now()
                WHERE position = %(position)s
                """

        return self.updateWithParam(sql, param)

    def bannerDisable(self, is_invalid, full_name):
        '''
        バナー表示/非表示切り替え
        '''
        param = {
                    'is_invalid': is_invalid,
                    'full_name': full_name,
                 }
        sql =   """
                UPDATE m_banner
                SET
                  is_invalid = %(is_invalid)s
                , update_user = %(full_name)s
                , update_date = now()
                WHERE position in ('1', '2', '3')
                """
        return self.updateWithParam(sql, param)