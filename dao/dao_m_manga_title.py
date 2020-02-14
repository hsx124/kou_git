from ipdds_app.dao.dao_main import DaoMain

class DaoMMangaTitle(DaoMain):

    """マンガDBより作品名、作者、出版社を取得"""
    def selectAuthorAndPublisherBySakuhinList(self,sakuhin_code):

        params = []
        whereSentence = ""
        for tmp in sakuhin_code:
            if tmp == "":
                continue
            params.append(tmp)
            whereSentence += " or m_sakuhin.sakuhin_code = %s"

        case_sentence = ""
        for i in range(1, 31, 1):
          case_sentence += "WHEN staff_role_code" + str(i) +" = '00001' THEN staff_code" + str(i) +"\n"


        sql =   """
                SELECT
                  m_sakuhin.sakuhin_code
                  , m_sakuhin.sakuhin_name
                  , m_staff.staff_name
                  , m_publisher.publisher_name
                FROM
                  m_manga_title
                LEFT JOIN m_sakuhin_map
                  ON m_manga_title.manga_title_code = m_sakuhin_map.title_code
                LEFT JOIN m_sakuhin
                  ON m_sakuhin_map.sakuhin_code = m_sakuhin.sakuhin_code
                LEFT JOIN m_publisher
                  ON m_manga_title.publisher_code = m_publisher.publisher_code
                LEFT JOIN m_staff_map
                  ON m_manga_title.staff_map_code = m_staff_map.staff_map_code
                LEFT JOIN m_staff
                  ON (CASE
                  {case_sentence}
                  END) = m_staff.staff_code
                WHERE
                  m_manga_title.invalid_flg = false

                {whereSentence}
                """

        return self.selectWithParam(sql.format(case_sentence = case_sentence , whereSentence = whereSentence),params)

    def selectSimilarSakuhinByFactCode(self,sakuhin_tag_code,sakuhin_code):

        if not sakuhin_tag_code:
          return []
        ## WHERE句の生成
        params_where = []
        whereSentence = ""
        for i in range(len(sakuhin_tag_code)):
            for j in range(5):
              params_where.append(sakuhin_tag_code[i])
              if i == 0 and j == 0:
                whereSentence += "tag_code"
              else:
                whereSentence += " or tag_code"
              whereSentence += str(j+1)+" = %s"

        ## 類似率計算部分の生成
        params_similar = []
        similar_sql = ""
        template = "case when {condition} then 1 else 0 end"
        for i in range(len(sakuhin_tag_code)):
            if i != 0:
              similar_sql += " + "
            tmp_condition = ""
            for j in range(5):
              params_similar.append(sakuhin_tag_code[i])
              if j == 0:
                tmp_condition += "tag_all.tag_code"+ str(j+1)+"= %s"
              else:
                tmp_condition += "or tag_all.tag_code"+ str(j+1)+"= %s"
            similar_sql += template.format(condition = tmp_condition)

        template = "case when {condition} then '1' else '0' end"
        for i in range(len(sakuhin_tag_code)):
            similar_sql += " || "
            tmp_condition = ""
            for j in range(5):
              params_similar.append(sakuhin_tag_code[i])
              if j == 0:
                tmp_condition += "tag_all.tag_code"+ str(j+1)+"= %s"
              else:
                tmp_condition += "or tag_all.tag_code"+ str(j+1)+"= %s"
            similar_sql += template.format(condition = tmp_condition)

        sql =   """
                SELECT
                  tag_all.sakuhin_code
                  , tag_all.sakuhin_name
                  , COALESCE(tag_all.tag_code1, '')
                  , COALESCE(tag_all.tag_name1, '')
                  , COALESCE(tag_all.tag_code2, '')
                  , COALESCE(tag_all.tag_name2, '')
                  , COALESCE(tag_all.tag_code3, '')
                  , COALESCE(tag_all.tag_name3, '')
                  , COALESCE(tag_all.tag_code4, '')
                  , COALESCE(tag_all.tag_name4, '')
                  , COALESCE(tag_all.tag_code5, '')
                  , COALESCE(tag_all.tag_name5, '')
                  ,{similar_rate}
                FROM
                  ( SELECT
                      sakuhin_code
                      , sakuhin_name
                      , ( SELECT sakuhin_tag_name AS tag_name1 FROM m_sakuhin_tag WHERE sakuhin_tag_code = tag1 )
                      , tag1 AS tag_code1
                      , ( SELECT sakuhin_tag_name AS tag_name2 FROM m_sakuhin_tag WHERE sakuhin_tag_code = tag2 )
                      , tag2 AS tag_code2
                      , ( SELECT sakuhin_tag_name AS tag_name3 FROM m_sakuhin_tag WHERE sakuhin_tag_code = tag3 )
                      , tag3 AS tag_code3
                      , ( SELECT sakuhin_tag_name AS tag_name4 FROM m_sakuhin_tag WHERE sakuhin_tag_code = tag4 )
                      , tag4 AS tag_code4
                      , ( SELECT sakuhin_tag_name AS tag_name5 FROM m_sakuhin_tag WHERE sakuhin_tag_code = tag5 )
                      , tag5 AS tag_code5
                    FROM
                      (
                        SELECT
                          sakuhin_code
                          , sakuhin_name
                          , max(CASE when rank = 1 then tag_code end) AS tag1
                          , max(CASE when rank = 2 then tag_code end) AS tag2
                          , max(CASE when rank = 3 then tag_code end) AS tag3
                          , max(CASE when rank = 4 then tag_code end) AS tag4
                          , max(CASE when rank = 5 then tag_code end) AS tag5
                        FROM
                          (
                            SELECT
                              sakuhin_code
                              , sakuhin_name
                              , tag_code
                              , COUNT(tag_code)
                              , ROW_NUMBER() OVER (
                                PARTITION BY
                                  sakuhin_code
                                ORDER BY
                                  COUNT(tag_code) DESC
                              ) AS rank
                            FROM
                              (
                                SELECT
                                  tag1.sakuhin_code AS sakuhin_code
                                  , tag1.sakuhin_name AS sakuhin_name
                                  , tag1.sakuhin_tag_code1 AS tag_code
                                  , 1 AS count
                                FROM
                                  (
                                    SELECT
                                      sakuhin.sakuhin_code
                                      , m_sakuhin.sakuhin_name
                                      , sakuhin.title_code
                                      , manga.manga_title_name
                                      , tag_map.sakuhin_tag_code1
                                      , tag_map.sakuhin_tag_code2
                                      , tag_map.sakuhin_tag_code3
                                      , tag_map.sakuhin_tag_code4
                                      , tag_map.sakuhin_tag_code5
                                    FROM
                                      m_sakuhin_map sakuhin
                                      INNER JOIN m_manga_title manga
                                        ON sakuhin.title_code = manga.manga_title_code
                                      LEFT JOIN m_sakuhin_tag_map tag_map
                                        ON manga.tag_map_code = tag_map.tag_map_code
                                      INNER JOIN m_sakuhin
                                        ON sakuhin.sakuhin_code = m_sakuhin.sakuhin_code
                                    WHERE
                                      tag_map.sakuhin_tag_code1 IS NOT NULL
                                      AND tag_map.sakuhin_tag_code1 <> ''
                                  ) tag1
                                UNION ALL
                                SELECT
                                  tag2.sakuhin_code AS sakuhin_code
                                  , tag2.sakuhin_name AS sakuhin_name
                                  , tag2.sakuhin_tag_code2 AS tag_code
                                  , 1 AS count
                                FROM
                                  (
                                    SELECT
                                      sakuhin.sakuhin_code
                                      , m_sakuhin.sakuhin_name
                                      , sakuhin.title_code
                                      , manga.manga_title_name
                                      , tag_map.sakuhin_tag_code1
                                      , tag_map.sakuhin_tag_code2
                                      , tag_map.sakuhin_tag_code3
                                      , tag_map.sakuhin_tag_code4
                                      , tag_map.sakuhin_tag_code5
                                    FROM
                                      m_sakuhin_map sakuhin
                                      INNER JOIN m_manga_title manga
                                        ON sakuhin.title_code = manga.manga_title_code
                                      LEFT JOIN m_sakuhin_tag_map tag_map
                                        ON manga.tag_map_code = tag_map.tag_map_code
                                      INNER JOIN m_sakuhin
                                        ON sakuhin.sakuhin_code = m_sakuhin.sakuhin_code
                                    WHERE
                                      tag_map.sakuhin_tag_code2 IS NOT NULL
                                      AND tag_map.sakuhin_tag_code2 <> ''
                                  ) tag2
                                UNION ALL
                                SELECT
                                  tag3.sakuhin_code AS sakuhin_code
                                  , tag3.sakuhin_name AS sakuhin_name
                                  , tag3.sakuhin_tag_code3 AS tag_code
                                  , 1 AS count
                                FROM
                                  (
                                    SELECT
                                      sakuhin.sakuhin_code
                                      , m_sakuhin.sakuhin_name
                                      , sakuhin.title_code
                                      , manga.manga_title_name
                                      , tag_map.sakuhin_tag_code1
                                      , tag_map.sakuhin_tag_code2
                                      , tag_map.sakuhin_tag_code3
                                      , tag_map.sakuhin_tag_code4
                                      , tag_map.sakuhin_tag_code5
                                    FROM
                                      m_sakuhin_map sakuhin
                                      INNER JOIN m_manga_title manga
                                        ON sakuhin.title_code = manga.manga_title_code
                                      LEFT JOIN m_sakuhin_tag_map tag_map
                                        ON manga.tag_map_code = tag_map.tag_map_code
                                      INNER JOIN m_sakuhin
                                        ON sakuhin.sakuhin_code = m_sakuhin.sakuhin_code
                                    WHERE
                                      tag_map.sakuhin_tag_code3 IS NOT NULL
                                      AND tag_map.sakuhin_tag_code3 <> ''
                                  ) tag3
                                UNION ALL
                                SELECT
                                  tag4.sakuhin_code AS sakuhin_code
                                  , tag4.sakuhin_name AS sakuhin_name
                                  , tag4.sakuhin_tag_code4 AS tag_code
                                  , 1 AS count
                                FROM
                                  (
                                    SELECT
                                      sakuhin.sakuhin_code
                                      , m_sakuhin.sakuhin_name
                                      , sakuhin.title_code
                                      , manga.manga_title_name
                                      , tag_map.sakuhin_tag_code1
                                      , tag_map.sakuhin_tag_code2
                                      , tag_map.sakuhin_tag_code3
                                      , tag_map.sakuhin_tag_code4
                                      , tag_map.sakuhin_tag_code5
                                    FROM
                                      m_sakuhin_map sakuhin
                                      INNER JOIN m_manga_title manga
                                        ON sakuhin.title_code = manga.manga_title_code
                                      LEFT JOIN m_sakuhin_tag_map tag_map
                                        ON manga.tag_map_code = tag_map.tag_map_code
                                      INNER JOIN m_sakuhin
                                        ON sakuhin.sakuhin_code = m_sakuhin.sakuhin_code
                                    WHERE
                                      tag_map.sakuhin_tag_code4 IS NOT NULL
                                      AND tag_map.sakuhin_tag_code4 <> ''
                                  ) tag4
                                UNION ALL
                                SELECT
                                  tag5.sakuhin_code AS sakuhin_code
                                  , tag5.sakuhin_name AS sakuhin_name
                                  , tag5.sakuhin_tag_code5 AS tag_code
                                  , 1 AS count
                                FROM
                                  (
                                    SELECT
                                      sakuhin.sakuhin_code
                                      , m_sakuhin.sakuhin_name
                                      , sakuhin.title_code
                                      , manga.manga_title_name
                                      , tag_map.sakuhin_tag_code1
                                      , tag_map.sakuhin_tag_code2
                                      , tag_map.sakuhin_tag_code3
                                      , tag_map.sakuhin_tag_code4
                                      , tag_map.sakuhin_tag_code5
                                    FROM
                                      m_sakuhin_map sakuhin
                                      INNER JOIN m_manga_title manga
                                        ON sakuhin.title_code = manga.manga_title_code
                                      LEFT JOIN m_sakuhin_tag_map tag_map
                                        ON manga.tag_map_code = tag_map.tag_map_code
                                      INNER JOIN m_sakuhin
                                        ON sakuhin.sakuhin_code = m_sakuhin.sakuhin_code
                                    WHERE
                                      tag_map.sakuhin_tag_code5 IS NOT NULL
                                      AND tag_map.sakuhin_tag_code5 <> ''
                                  ) tag5
                              ) tag_all
                            GROUP BY
                              sakuhin_code
                              , sakuhin_name
                              , tag_code
                            ORDER BY
                              sakuhin_code
                              , rank
                          ) tag_rank
                        GROUP BY
                          sakuhin_code
                          , sakuhin_name
                      ) tag
                  ) AS tag_all
                INNER JOIN m_sakuhin
                ON tag_all.sakuhin_code = m_sakuhin.sakuhin_code
                WHERE
                  TO_DATE(valid_start_yyyymmdd, 'YYYYMMDD') <= now()
                    AND now() <= TO_DATE(valid_end_yyyymmdd, 'YYYYMMDD')
                    AND m_sakuhin.invalid_flg = FALSE
                    AND (
                      {whereSentence}
                      )
                      and tag_all.sakuhin_code != %s
                ORDER BY {similar_rate} DESC
                LIMIT 10
                """
        sql = sql.format(whereSentence = whereSentence,similar_rate = similar_sql)

        return self.selectWithParam(sql,params_similar + params_where + [sakuhin_code] + params_similar)

    """作品コードをもとに連載開始順にマンガコードを取得"""
    def selectMangaCode(self,sakuhin_code):
      sql = """
              SELECT
                m_manga_title.manga_title_code
              FROM
                m_sakuhin_map
                LEFT JOIN m_manga_title
                  ON m_sakuhin_map.title_code = m_manga_title.manga_title_code
                  and m_manga_title.invalid_flg = false
              WHERE
                m_sakuhin_map.sakuhin_code = %s
              ORDER BY rensai_start_yyyymm ASC
              """
      return  self.selectWithParam(sql,[sakuhin_code])

    """タイトルコードをもとにマンガ基本情報を取得"""
    def selectMangaData(self,title_code):
      sql = self.sentence.format(fromStaff=self.sentenceJoin)
      return self.selectWithParam(sql,[title_code])

    sentence = """
            SELECT
              m_manga_title.manga_title_name
              ,CASE WHEN (staff_role_1.staff_role_name != '' AND staff_1.staff_name != '') THEN staff_role_1.staff_role_name || ' : ' || staff_1.staff_name
                WHEN staff_role_1.staff_role_name != '' THEN staff_role_1.staff_role_name
                WHEN staff_1.staff_name != '' THEN staff_1.staff_name
                ELSE '' END
              , CASE WHEN (staff_role_2.staff_role_name != '' AND staff_2.staff_name != '') THEN staff_role_2.staff_role_name || ' : ' || staff_2.staff_name
                WHEN staff_role_2.staff_role_name != '' THEN staff_role_2.staff_role_name
                WHEN staff_2.staff_name != '' THEN staff_2.staff_name
                ELSE '' END
              , CASE WHEN (staff_role_3.staff_role_name != '' AND staff_3.staff_name != '') THEN staff_role_3.staff_role_name || ' : ' || staff_3.staff_name
                WHEN staff_role_3.staff_role_name != '' THEN staff_role_3.staff_role_name
                WHEN staff_3.staff_name != '' THEN staff_3.staff_name
                ELSE '' END
              , COALESCE(m_publisher.publisher_name, '')
              , TO_CHAR(TO_DATE(m_manga_title.rensai_start_yyyymm,'yyyymm'),'yyyy年MM月')
              , m_manga_title.published_cnt ::numeric ::integer
              , case m_manga_title.rensai_end_flg when true then '終' else '' end
              , COALESCE(m_manga_title.award_history, '')
            FROM
              m_manga_title
              {fromStaff}
            WHERE
              m_manga_title.manga_title_code = %s
            """

    sentenceJoin = """
                  LEFT JOIN m_staff_map
                    ON m_manga_title.staff_map_code = m_staff_map.staff_map_code
                    AND m_staff_map.invalid_flg = false
                  LEFT JOIN m_staff_role AS staff_role_1
                    ON m_staff_map.staff_role_code1 = staff_role_1.staff_role_code
                    AND staff_role_1.invalid_flg = false
                  LEFT JOIN m_staff AS staff_1
                    ON m_staff_map.staff_code1 = staff_1.staff_code
                    AND staff_1.invalid_flg = false
                  LEFT JOIN m_staff_role AS staff_role_2
                    ON m_staff_map.staff_role_code2 = staff_role_2.staff_role_code
                    AND staff_role_2.invalid_flg = false
                  LEFT JOIN m_staff AS staff_2
                    ON m_staff_map.staff_code2 = staff_2.staff_code
                    AND staff_2.invalid_flg = false
                  LEFT JOIN m_staff_role AS staff_role_3
                    ON m_staff_map.staff_role_code3 = staff_role_3.staff_role_code
                    AND staff_role_3.invalid_flg = false
                  LEFT JOIN m_staff AS staff_3
                    ON m_staff_map.staff_code3 = staff_3.staff_code
                    AND staff_3.invalid_flg = false
                  LEFT JOIN m_publisher
                    ON m_manga_title.publisher_code = m_publisher.publisher_code
                    AND m_publisher.invalid_flg = false
                  """