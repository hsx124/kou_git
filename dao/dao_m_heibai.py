from ipdds_app.dao.dao_main import DaoMain

class DaoMHeibai(DaoMain):

    sentence = """
            SELECT
              heibai_data.heibai || '_' || COALESCE(heibai_data.heibai_name, '')
              , m_manga_title.manga_title_name
              , CASE WHEN (staff_role_1.staff_role_name != '' AND staff_1.staff_name != '') THEN staff_role_1.staff_role_name || ' : ' || staff_1.staff_name
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
            FROM
              (
                SELECT
                  {heibai}
                FROM
                  m_manga_title
                  LEFT JOIN m_heibai
                    ON m_manga_title.heibai_code = m_heibai.heibai_code
                    AND m_heibai.invalid_flg = false
                WHERE
                  m_manga_title.manga_title_code = %s
              ) as heibai_data
              {fromStaff}
            """

    sentenceJoin = """
                  INNER JOIN m_sakuhin_map
                    ON m_sakuhin_map.sakuhin_code = heibai_data.heibai
                    AND m_sakuhin_map.invalid_flg = false
                  INNER JOIN m_manga_title
                    ON m_sakuhin_map.title_code = m_manga_title.manga_title_code
                    AND m_manga_title.invalid_flg = false
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

    def selectHeibaiDataByTitleCode(self,title_code,heibai_cnt):
      heibai = "COALESCE(m_heibai.heibai_name_"+ str(heibai_cnt) +", '') as heibai_name,COALESCE(m_heibai.heibai_"+ str(heibai_cnt) +", '') as heibai"
      sql = self.sentence.format(heibai = heibai,fromStaff=self.sentenceJoin)
      return self.selectWithParam(sql,[title_code])