from admin_app.dao.dao_main import DaoMain

class DaoBanner(DaoMain):
    """バナーリンク"""
    def selectbanner(self,position):

        param = {'position': position}
        sql =   """
                SELECT
                  position
                , thumbnail_file_name
                , subject
                , details
                , external_site
                , external_site_flg
                , media_report_code
                , CASE external_site_flg 
                    WHEN TRUE THEN ''
                    ELSE ( 
                            SELECT media_report_name 
                            FROM m_media_report 
                            WHERE media_report_code = COALESCE(m_banner.media_report_code,'0')
                          )
                  END AS white_paper_file_name
                FROM m_banner 
                WHERE position = %(position)s
                AND invalid_flg = false 
                ORDER BY
                  position
                """

        return self.selectWithParam(sql, param)

    def selectbannerpreview(self):
        sql = """
              SELECT
                invalid_flg
              , thumbnail_file_name
              , subject
              , details
              , position
              FROM m_banner
              ORDER BY position ASC
              LIMIT 3
              """
        return self.select(sql)
    
    def updateBanner(self,position,title,details,thumbnail_file_name,external_site,media_report_code,is_checked,full_name):
        '''
        バナーリンク更新
        '''
        param = {
                    'position': position,
                    'title': title,
                    'details': details,
                    'thumbnail_file_name': thumbnail_file_name,
                    'external_site': external_site,
                    'media_report_code': media_report_code,
                    'is_checked': is_checked,
                    'full_name': full_name
                 }
        sql =   """
                UPDATE m_banner
                SET
                  subject = %(title)s
                , details = %(details)s
                , thumbnail_file_name = %(thumbnail_file_name)s
                , external_site = %(external_site)s
                , media_report_code = %(media_report_code)s
                , external_site_flg = %(is_checked)s
                , update_user = %(full_name)s
                , update_time = now()
                WHERE position = %(position)s
                """

        return self.updateWithParam(sql, param)

    def bannerDisable(self, invalid_flg, full_name):
        '''
        バナー表示/非表示切り替え
        '''
        param = {
                    'invalid_flg': invalid_flg,
                    'full_name': full_name,
                 }
        sql =   """
                UPDATE m_banner
                SET
                  invalid_flg = %(invalid_flg)s
                , update_user = %(full_name)s
                , update_time = now()
                WHERE position in ('1', '2', '3')
                """
        return self.updateWithParam(sql, param)