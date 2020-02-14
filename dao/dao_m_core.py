from ipdds_app.dao.dao_main import DaoMain

class DaoMCore(DaoMain):

    """コアマスタデータの取得"""
    def selectAll(self):

        sql =   """
                SELECT
                  core_code
                  , core_name 
                FROM
                  m_core 
                WHERE
                  is_invalid = false
                ORDER BY
                  core_code
                """

        return self.select(sql)

    def selectCore(self,sakuhin_code):
      sql = """
            SELECT
              sakuhin_code
              , core_code
              , (SELECT core_name FROM m_core WHERE m_core.core_code = core.core_code)
            FROM
              (
                SELECT
                  sakuhin_code
                  , core_code
                  , COUNT(core_code)
                  , ROW_NUMBER() OVER (ORDER BY COUNT(core_code) DESC) AS rank 
                FROM
                  (
                    SELECT
                      core1.sakuhin_code as sakuhin_code
                      , core1.core_code1 as core_code
                      , 1 as count
                    FROM
                      (
                        SELECT
                          sakuhin.sakuhin_code
                          , sakuhin.title_code
                          , manga.manga_title_name
                          , tag_map.core_code1
                          , tag_map.core_code2
                        FROM
                          m_sakuhin_map sakuhin
                          inner JOIN m_manga_title manga
                            ON sakuhin.title_code = manga.manga_title_code
                          LEFT JOIN m_sakuhin_tag_map tag_map
                            ON manga.tag_map_code = tag_map.tag_map_code
                        WHERE
                          sakuhin_code = %s
                          and tag_map.core_code1 is not null
                          and tag_map.core_code1 <> ''
                      ) as core1
                    UNION ALL
                    SELECT
                      core2.sakuhin_code as sakuhin_code
                      , core2.core_code2 as core_code
                      , 1 as count
                    FROM
                      (
                        SELECT
                          sakuhin.sakuhin_code
                          , sakuhin.title_code
                          , manga.manga_title_name
                          , tag_map.core_code1
                          , tag_map.core_code2
                        FROM
                          m_sakuhin_map sakuhin
                          inner JOIN m_manga_title manga
                            ON sakuhin.title_code = manga.manga_title_code
                          LEFT JOIN m_sakuhin_tag_map tag_map
                            ON manga.tag_map_code = tag_map.tag_map_code
                        WHERE
                          sakuhin_code = %s
                          and tag_map.core_code2 is not null
                          and tag_map.core_code2 <> ''
                      ) as core2
                  ) tag_all
                GROUP BY
                  sakuhin_code
                  , core_code
                ORDER BY
                  count desc
                LIMIT
                  1
              ) core
            """
      return self.selectWithParam(sql,[sakuhin_code,sakuhin_code]) 
