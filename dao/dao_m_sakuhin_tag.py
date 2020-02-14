from ipdds_app.dao.dao_main import DaoMain

class DaoMSakuhinTag(DaoMain):

    """作品タグマスタの取得"""
    def selectAll(self):

        sql =   """
                SELECT
                  COALESCE(m_sakuhin_tag_category.sakuhin_tag_category_name,'')
                  , sakuhin_tag_code
                  , sakuhin_tag_name 
                FROM
                  m_sakuhin_tag 
                  LEFT OUTER JOIN m_sakuhin_tag_category 
                    ON m_sakuhin_tag_category.sakuhin_tag_category_code = m_sakuhin_tag.sakuhin_tag_category_code 
                    AND m_sakuhin_tag_category.invalid_flg = false 
                WHERE
                  m_sakuhin_tag.invalid_flg = false 
                ORDER BY
                  m_sakuhin_tag_category.sakuhin_tag_category_code
                  , sakuhin_tag_code
                """

        return self.select(sql)

    def selectTag(self,sakuhin_code):
      sql = """
            SELECT
              sakuhin_code
              , tag1 as tag1_code
              , (SELECT sakuhin_tag_name as tag1_name FROM m_sakuhin_tag WHERE sakuhin_tag_code = tag1)
              , tag2 as tag2_code
              , (SELECT sakuhin_tag_name as tag2_name FROM m_sakuhin_tag WHERE sakuhin_tag_code = tag2)
              , tag3 as tag3_code
              , (SELECT sakuhin_tag_name as tag3_name FROM m_sakuhin_tag WHERE sakuhin_tag_code = tag3)
              , tag4 as tag4_code
              , (SELECT sakuhin_tag_name as tag4_name FROM m_sakuhin_tag WHERE sakuhin_tag_code = tag4)
              , tag5 as tag5_code
              , (SELECT sakuhin_tag_name as tag5_name FROM m_sakuhin_tag WHERE sakuhin_tag_code = tag5)
            FROM
              ( 
              SELECT
                sakuhin_code
                , MAX(case when rank = 1 then tag_code end) as tag1
                , MAX(case when rank = 2 then tag_code end) as tag2
                , MAX(case when rank = 3 then tag_code end) as tag3
                , MAX(case when rank = 4 then tag_code end) as tag4
                , MAX(case when rank = 5 then tag_code end) as tag5
              FROM
                (
                  SELECT
                    sakuhin_code
                    , tag_code
                    , COUNT(tag_code)
                    , ROW_NUMBER() OVER (ORDER BY COUNT(tag_code) DESC) AS rank
                  FROM
                    (
                      SELECT
                        tag1.sakuhin_code as sakuhin_code
                        , tag1.sakuhin_tag_code1 as tag_code
                        , 1 as count
                      FROM
                        (
                          SELECT
                            sakuhin.sakuhin_code
                            , sakuhin.title_code
                            , manga.manga_title_name
                            , tag_map.sakuhin_tag_code1
                            , tag_map.sakuhin_tag_code2
                            , tag_map.sakuhin_tag_code3
                            , tag_map.sakuhin_tag_code4
                            , tag_map.sakuhin_tag_code5
                          FROM
                            m_sakuhin_map sakuhin
                            inner JOIN m_manga_title manga
                              ON sakuhin.title_code = manga.manga_title_code
                            LEFT JOIN m_sakuhin_tag_map tag_map
                              ON manga.tag_map_code = tag_map.tag_map_code
                          WHERE
                            sakuhin_code = %s
                            and tag_map.sakuhin_tag_code1 is not null
                            and tag_map.sakuhin_tag_code1 <> ''
                        ) tag1
                      UNION ALL
                      SELECT
                        tag2.sakuhin_code as sakuhin_code
                        , tag2.sakuhin_tag_code2 as tag_code
                        , 1 as count
                      FROM
                        (
                          SELECT
                            sakuhin.sakuhin_code
                            , sakuhin.title_code
                            , manga.manga_title_name
                            , tag_map.sakuhin_tag_code1
                            , tag_map.sakuhin_tag_code2
                            , tag_map.sakuhin_tag_code3
                            , tag_map.sakuhin_tag_code4
                            , tag_map.sakuhin_tag_code5
                          FROM
                            m_sakuhin_map sakuhin
                            inner JOIN m_manga_title manga
                              ON sakuhin.title_code = manga.manga_title_code
                            LEFT JOIN m_sakuhin_tag_map tag_map
                              ON manga.tag_map_code = tag_map.tag_map_code
                          WHERE
                            sakuhin_code = %s
                            and tag_map.sakuhin_tag_code2 is not null
                            and tag_map.sakuhin_tag_code2 <> ''
                        ) tag2
                      UNION ALL
                      SELECT
                        tag3.sakuhin_code as sakuhin_code
                        , tag3.sakuhin_tag_code3 as tag_code
                        , 1 as count
                      FROM
                        (
                          SELECT
                            sakuhin.sakuhin_code
                            , sakuhin.title_code
                            , manga.manga_title_name
                            , tag_map.sakuhin_tag_code1
                            , tag_map.sakuhin_tag_code2
                            , tag_map.sakuhin_tag_code3
                            , tag_map.sakuhin_tag_code4
                            , tag_map.sakuhin_tag_code5
                          FROM
                            m_sakuhin_map sakuhin
                            inner JOIN m_manga_title manga
                              ON sakuhin.title_code = manga.manga_title_code
                            LEFT JOIN m_sakuhin_tag_map tag_map
                              ON manga.tag_map_code = tag_map.tag_map_code
                          WHERE
                            sakuhin_code = %s
                            and tag_map.sakuhin_tag_code3 is not null
                            and tag_map.sakuhin_tag_code3 <> ''
                        ) tag3
                      UNION ALL
                      SELECT
                        tag4.sakuhin_code as sakuhin_code
                        , tag4.sakuhin_tag_code4 as tag_code
                        , 1 as count
                      FROM
                        (
                          SELECT
                            sakuhin.sakuhin_code
                            , sakuhin.title_code
                            , manga.manga_title_name
                            , tag_map.sakuhin_tag_code1
                            , tag_map.sakuhin_tag_code2
                            , tag_map.sakuhin_tag_code3
                            , tag_map.sakuhin_tag_code4
                            , tag_map.sakuhin_tag_code5
                          FROM
                            m_sakuhin_map sakuhin
                            inner JOIN m_manga_title manga
                              ON sakuhin.title_code = manga.manga_title_code
                            LEFT JOIN m_sakuhin_tag_map tag_map
                              ON manga.tag_map_code = tag_map.tag_map_code
                          WHERE
                            sakuhin_code = %s
                            and tag_map.sakuhin_tag_code4 is not null
                            and tag_map.sakuhin_tag_code4 <> ''
                        ) tag4
                      UNION ALL
                      SELECT
                        tag5.sakuhin_code as sakuhin_code
                        , tag5.sakuhin_tag_code4 as tag_code
                        , 1 as count
                      FROM
                        (
                          SELECT
                            sakuhin.sakuhin_code
                            , sakuhin.title_code
                            , manga.manga_title_name
                            , tag_map.sakuhin_tag_code1
                            , tag_map.sakuhin_tag_code2
                            , tag_map.sakuhin_tag_code3
                            , tag_map.sakuhin_tag_code4
                            , tag_map.sakuhin_tag_code5
                          FROM
                            m_sakuhin_map sakuhin
                            inner JOIN m_manga_title manga
                              ON sakuhin.title_code = manga.manga_title_code
                            LEFT JOIN m_sakuhin_tag_map tag_map
                              ON manga.tag_map_code = tag_map.tag_map_code
                          WHERE
                            sakuhin_code = %s
                            and tag_map.sakuhin_tag_code5 is not null
                            and tag_map.sakuhin_tag_code5 <> ''
                        ) tag5
                    ) tag_all
                  GROUP BY
                    sakuhin_code
                    , tag_code
                  ORDER BY
                    count desc
                ) tag_rank
              GROUP BY
                sakuhin_code
              ) tag
            """
      return self.selectWithParam(sql,[sakuhin_code,sakuhin_code,sakuhin_code,sakuhin_code,sakuhin_code])

    def selectTagCode(self,sakuhin_code):
      sql = """
            SELECT
                tag1 as tag1_code
              , tag2 as tag2_code
              , tag3 as tag3_code
              , tag4 as tag4_code
              , tag5 as tag5_code
            FROM
              ( 
              SELECT
                sakuhin_code
                , MAX(case when rank = 1 then tag_code end) as tag1
                , MAX(case when rank = 2 then tag_code end) as tag2
                , MAX(case when rank = 3 then tag_code end) as tag3
                , MAX(case when rank = 4 then tag_code end) as tag4
                , MAX(case when rank = 5 then tag_code end) as tag5
              FROM
                (
                  SELECT
                    sakuhin_code
                    , tag_code
                    , COUNT(tag_code)
                    , ROW_NUMBER() OVER (ORDER BY COUNT(tag_code) DESC) AS rank
                  FROM
                    (
                      SELECT
                        tag1.sakuhin_code as sakuhin_code
                        , tag1.sakuhin_tag_code1 as tag_code
                        , 1 as count
                      FROM
                        (
                          SELECT
                            sakuhin.sakuhin_code
                            , sakuhin.title_code
                            , manga.manga_title_name
                            , tag_map.sakuhin_tag_code1
                            , tag_map.sakuhin_tag_code2
                            , tag_map.sakuhin_tag_code3
                            , tag_map.sakuhin_tag_code4
                            , tag_map.sakuhin_tag_code5
                          FROM
                            m_sakuhin_map sakuhin
                            inner JOIN m_manga_title manga
                              ON sakuhin.title_code = manga.manga_title_code
                            LEFT JOIN m_sakuhin_tag_map tag_map
                              ON manga.tag_map_code = tag_map.tag_map_code
                          WHERE
                            sakuhin_code = %s
                            and tag_map.sakuhin_tag_code1 is not null
                            and tag_map.sakuhin_tag_code1 <> ''
                        ) tag1
                      UNION ALL
                      SELECT
                        tag2.sakuhin_code as sakuhin_code
                        , tag2.sakuhin_tag_code2 as tag_code
                        , 1 as count
                      FROM
                        (
                          SELECT
                            sakuhin.sakuhin_code
                            , sakuhin.title_code
                            , manga.manga_title_name
                            , tag_map.sakuhin_tag_code1
                            , tag_map.sakuhin_tag_code2
                            , tag_map.sakuhin_tag_code3
                            , tag_map.sakuhin_tag_code4
                            , tag_map.sakuhin_tag_code5
                          FROM
                            m_sakuhin_map sakuhin
                            inner JOIN m_manga_title manga
                              ON sakuhin.title_code = manga.manga_title_code
                            LEFT JOIN m_sakuhin_tag_map tag_map
                              ON manga.tag_map_code = tag_map.tag_map_code
                          WHERE
                            sakuhin_code = %s
                            and tag_map.sakuhin_tag_code2 is not null
                            and tag_map.sakuhin_tag_code2 <> ''
                        ) tag2
                      UNION ALL
                      SELECT
                        tag3.sakuhin_code as sakuhin_code
                        , tag3.sakuhin_tag_code3 as tag_code
                        , 1 as count
                      FROM
                        (
                          SELECT
                            sakuhin.sakuhin_code
                            , sakuhin.title_code
                            , manga.manga_title_name
                            , tag_map.sakuhin_tag_code1
                            , tag_map.sakuhin_tag_code2
                            , tag_map.sakuhin_tag_code3
                            , tag_map.sakuhin_tag_code4
                            , tag_map.sakuhin_tag_code5
                          FROM
                            m_sakuhin_map sakuhin
                            inner JOIN m_manga_title manga
                              ON sakuhin.title_code = manga.manga_title_code
                            LEFT JOIN m_sakuhin_tag_map tag_map
                              ON manga.tag_map_code = tag_map.tag_map_code
                          WHERE
                            sakuhin_code = %s
                            and tag_map.sakuhin_tag_code3 is not null
                            and tag_map.sakuhin_tag_code3 <> ''
                        ) tag3
                      UNION ALL
                      SELECT
                        tag4.sakuhin_code as sakuhin_code
                        , tag4.sakuhin_tag_code4 as tag_code
                        , 1 as count
                      FROM
                        (
                          SELECT
                            sakuhin.sakuhin_code
                            , sakuhin.title_code
                            , manga.manga_title_name
                            , tag_map.sakuhin_tag_code1
                            , tag_map.sakuhin_tag_code2
                            , tag_map.sakuhin_tag_code3
                            , tag_map.sakuhin_tag_code4
                            , tag_map.sakuhin_tag_code5
                          FROM
                            m_sakuhin_map sakuhin
                            inner JOIN m_manga_title manga
                              ON sakuhin.title_code = manga.manga_title_code
                            LEFT JOIN m_sakuhin_tag_map tag_map
                              ON manga.tag_map_code = tag_map.tag_map_code
                          WHERE
                            sakuhin_code = %s
                            and tag_map.sakuhin_tag_code4 is not null
                            and tag_map.sakuhin_tag_code4 <> ''
                        ) tag4
                      UNION ALL
                      SELECT
                        tag5.sakuhin_code as sakuhin_code
                        , tag5.sakuhin_tag_code4 as tag_code
                        , 1 as count
                      FROM
                        (
                          SELECT
                            sakuhin.sakuhin_code
                            , sakuhin.title_code
                            , manga.manga_title_name
                            , tag_map.sakuhin_tag_code1
                            , tag_map.sakuhin_tag_code2
                            , tag_map.sakuhin_tag_code3
                            , tag_map.sakuhin_tag_code4
                            , tag_map.sakuhin_tag_code5
                          FROM
                            m_sakuhin_map sakuhin
                            inner JOIN m_manga_title manga
                              ON sakuhin.title_code = manga.manga_title_code
                            LEFT JOIN m_sakuhin_tag_map tag_map
                              ON manga.tag_map_code = tag_map.tag_map_code
                          WHERE
                            sakuhin_code = %s
                            and tag_map.sakuhin_tag_code5 is not null
                            and tag_map.sakuhin_tag_code5 <> ''
                        ) tag5
                    ) tag_all
                  GROUP BY
                    sakuhin_code
                    , tag_code
                  ORDER BY
                    count desc
                ) tag_rank
                GROUP BY sakuhin_code
              ) tag
            """
      return self.selectWithParam(sql,[sakuhin_code,sakuhin_code,sakuhin_code,sakuhin_code,sakuhin_code])
