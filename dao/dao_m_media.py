from ipdds_app.dao.dao_main import DaoMain

class DaoMMedia(DaoMain):

    """掲載媒体マスタの取得"""
    def selectAll(self):

        sql =   """
                SELECT
                  media_code
                  , media_name 
                FROM
                  m_media 
                WHERE
                  is_invalid = false
                ORDER BY
                  media_code
                """

        return self.select(sql)

    """
    作品コードに紐づく掲載媒体を取得
    """
    def selectMediaBySakuhinCode(self,sakuhin_code):
      sql = """
            SELECT DISTINCT
              m_sakuhin_map.sakuhin_code
              , m_media.media_code
              , media_name
            FROM
              m_media
              INNER JOIN m_manga_title
                ON m_manga_title.media_code = m_media.media_code
                AND m_manga_title.invalid_flg = false
              INNER JOIN m_sakuhin_map
                ON m_manga_title.manga_title_code = m_sakuhin_map.title_code
                AND m_sakuhin_map.invalid_flg = false
            WHERE
              m_sakuhin_map.sakuhin_code = %s
              AND m_media.invalid_flg = false
            ORDER BY
              m_media.media_code
            """
      return self.selectWithParam(sql,[sakuhin_code])