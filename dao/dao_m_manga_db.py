from ipdds_app.dao.dao_main import DaoMain

class DaoMMangaDb(DaoMain):

    """マンガDBよりIP名、作者、出版社を取得"""
    def selectAuthorAndPublisherByIpList(self,ip_code):

        params = []
        whereSentence = ""
        for tmp in ip_code:
            if tmp == "":
                continue
            params.append(tmp)
            whereSentence += " or ip_code = %s"

        sql =   """
                SELECT
                  ip_code
                  , ip_name
                  , author
                  , publisher
                FROM
                  m_manga_db 
                WHERE
                  is_invalid = false
                {whereSentence}
                """

        return self.selectWithParam(sql.format(whereSentence = whereSentence),params)
    
    def selectSimilarIpByFactCode(self,fact_tag_code,ip_code):

        if not fact_tag_code:
          return []
        fact_tag_code.sort()
        ## WHERE句の生成
        params_where = []
        whereSentence = ""
        for i in range(len(fact_tag_code)):
            for j in range(5):
              params_where.append(fact_tag_code[i])
              if i == 0 and j == 0:
                whereSentence += "fact_tag_"
              else:
                whereSentence += " or fact_tag_"
              whereSentence += str(j+1)+" = %s"
        
        ## 類似率計算部分の生成
        params_similar = []
        similar_sql = ""
        template = "case when {condition} then 1 else 0 end"
        for i in range(len(fact_tag_code)):
            if i != 0:
              similar_sql += " + "
            tmp_condition = ""
            for j in range(5):
              params_similar.append(fact_tag_code[i])
              if j == 0:
                tmp_condition += "fact_"+str(j+1)+".fact_tag_code = %s"
              else:
                tmp_condition += "or fact_"+str(j+1)+".fact_tag_code = %s"
            similar_sql += template.format(condition = tmp_condition)

        template = "case when {condition} then '1' else '0' end"
        for i in range(len(fact_tag_code)):
            similar_sql += " || "
            tmp_condition = ""
            for j in range(5):
              params_similar.append(fact_tag_code[i])
              if j == 0:
                tmp_condition += "fact_"+str(j+1)+".fact_tag_code = %s"
              else:
                tmp_condition += "or fact_"+str(j+1)+".fact_tag_code = %s"
            similar_sql += template.format(condition = tmp_condition)

        sql =   """
                SELECT
                  m_ip.ip_code
                  , m_ip.ip_name
                  , COALESCE(fact_1.fact_tag_code, '') AS fact_1_code
                  , COALESCE(fact_1.fact_tag_name, '') AS fact_1
                  , COALESCE(fact_2.fact_tag_code, '') AS fact_2_code
                  , COALESCE(fact_2.fact_tag_name, '') AS fact_2
                  , COALESCE(fact_3.fact_tag_code, '') AS fact_3_code
                  , COALESCE(fact_3.fact_tag_name, '') AS fact_3
                  , COALESCE(fact_4.fact_tag_code, '') AS fact_4_code
                  , COALESCE(fact_4.fact_tag_name, '') AS fact_4
                  , COALESCE(fact_5.fact_tag_code, '') AS fact_5_code
                  , COALESCE(fact_5.fact_tag_name, '') AS fact_5
                  ,{similar_rate}
                FROM
                  m_manga_db 
                LEFT JOIN m_ip
                  ON m_manga_db.ip_code = m_ip.ip_code
                LEFT JOIN m_fact_tag AS fact_1 
                  ON m_manga_db.fact_tag_1 = fact_1.fact_tag_code 
                     and fact_1.is_invalid = false
                LEFT JOIN m_fact_tag AS fact_2 
                  ON m_manga_db.fact_tag_2 = fact_2.fact_tag_code 
                     and fact_2.is_invalid = false
                LEFT JOIN m_fact_tag AS fact_3 
                  ON m_manga_db.fact_tag_3 = fact_3.fact_tag_code 
                     and fact_3.is_invalid = false
                LEFT JOIN m_fact_tag AS fact_4 
                  ON m_manga_db.fact_tag_4 = fact_4.fact_tag_code 
                     and fact_4.is_invalid = false
                LEFT JOIN m_fact_tag AS fact_5 
                  ON m_manga_db.fact_tag_5 = fact_5.fact_tag_code 
                     and fact_5.is_invalid = false
                WHERE
                  m_manga_db.is_invalid = false
                  and valid_start_date <= now() and now() <= valid_end_date
                  and m_ip.is_invalid = false
                  and (
                  {whereSentence}
                  )
                  and m_ip.ip_code != %s
                ORDER BY {similar_rate} DESC
                LIMIT 10
                """
        sql = sql.format(whereSentence = whereSentence,similar_rate = similar_sql)

        return self.selectWithParam(sql,params_similar + params_where + [ip_code] + params_similar)