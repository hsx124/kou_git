from ipdds_app.dao.dao_main import DaoMain
import datetime

class DaoMSeinendai(DaoMain):
    
    """年代別男女比マスタデータの取得"""
    def selectCompareAgeAll(self,sakuhin_code_list):
        value = tuple(sakuhin_code_list)
        params = {'sakuhin_code_list': value}
        sql =   """
            SELECT
                sakuhin.sakuhin_code
              	,sakuhin.sakuhin_name
                ,sum(seinendai.male_cnt)::numeric::integer AS male
                ,sum(seinendai.female_cnt)::numeric::integer AS female
                ,sum(seinendai.total_cnt)::numeric::integer AS total
                ,sum(seinendai.male_lteq10_cnt)::numeric::integer AS male_lteq10
                ,sum(seinendai.male_11to15_cnt)::numeric::integer AS male_11to15
                ,sum(seinendai.male_16to20_cnt)::numeric::integer AS male_16to20
                ,sum(seinendai.male_21to25_cnt)::numeric::integer AS male_21to25
                ,sum(seinendai.male_26to30_cnt)::numeric::integer AS male_26to30
                ,sum(seinendai.male_31to35_cnt)::numeric::integer AS male_31to35
                ,sum(seinendai.male_36to40_cnt)::numeric::integer AS male_36to40
                ,sum(seinendai.male_41to45_cnt)::numeric::integer AS male_41to45
                ,sum(seinendai.male_46to50_cnt)::numeric::integer AS male_46to50
                ,sum(seinendai.male_gteq51_cnt)::numeric::integer AS male_gteq51
                ,sum(seinendai.female_lteq10_cnt)::numeric::integer AS female_lteq10
                ,sum(seinendai.female_11to15_cnt)::numeric::integer AS female_11to15
                ,sum(seinendai.female_16to20_cnt)::numeric::integer AS female_16to20
                ,sum(seinendai.female_21to25_cnt)::numeric::integer AS female_21to25
                ,sum(seinendai.female_26to30_cnt)::numeric::integer AS female_26to30
                ,sum(seinendai.female_31to35_cnt)::numeric::integer AS female_31to35
                ,sum(seinendai.female_36to40_cnt)::numeric::integer AS female_36to40
                ,sum(seinendai.female_41to45_cnt)::numeric::integer AS female_41to45
                ,sum(seinendai.female_46to50_cnt)::numeric::integer AS female_46to50
                ,sum(seinendai.female_gteq51_cnt)::numeric::integer AS female_gteq51
            FROM
				m_sakuhin sakuhin
			LEFT JOIN m_sakuhin_map sakuhin_map
			ON sakuhin.sakuhin_code = sakuhin_map.sakuhin_code
				AND sakuhin_map.title_category_code = '01'
                AND sakuhin_map.invalid_flg = false
			LEFT JOIN m_manga_title manga 
			ON sakuhin_map.title_code = manga.manga_title_code
                AND manga.invalid_flg = false
			LEFT JOIN m_seinendai seinendai
			ON  manga.seinendai_code = seinendai.seinendai_code
				AND seinendai.invalid_flg = false
            WHERE
                sakuhin.sakuhin_code in %(sakuhin_code_list)s
				AND sakuhin.invalid_flg = false
	            AND sakuhin.valid_start_yyyymmdd <= to_char(now(),'yyyymm')
	            AND to_char(now(),'yyyymm') <= sakuhin.valid_end_yyyymmdd
			GROUP BY
				sakuhin.sakuhin_code
            ORDER BY
                sakuhin.sakuhin_code
            """
        return self.selectWithParam(sql,params)

    """年代別男女比マスタデータの取得（グラフデータ用）"""
    def selectCompareAgeBySakuhinCode(self,sakuhin_code):
        sql =   """
            			SELECT
                sum(seinendai.male_gteq51_cnt)::numeric::integer AS male_gteq51
                , sum(seinendai.male_46to50_cnt)::numeric::integer AS male_46to50
                , sum(seinendai.male_41to45_cnt)::numeric::integer AS male_41to45
                , sum(seinendai.male_36to40_cnt)::numeric::integer AS male_36to40
                , sum(seinendai.male_31to35_cnt)::numeric::integer AS male_31to35
                , sum(seinendai.male_26to30_cnt)::numeric::integer AS male_26to30
                , sum(seinendai.male_21to25_cnt)::numeric::integer AS male_21to25
                , sum(seinendai.male_16to20_cnt)::numeric::integer AS male_16to20
                , sum(seinendai.male_11to15_cnt)::numeric::integer AS male_11to15
                , sum(seinendai.female_gteq51_cnt)::numeric::integer AS female_gteq51
                , sum(seinendai.female_46to50_cnt)::numeric::integer AS female_46to50
                , sum(seinendai.female_41to45_cnt)::numeric::integer AS female_41to45
                , sum(seinendai.female_36to40_cnt)::numeric::integer AS female_36to40
                , sum(seinendai.female_31to35_cnt)::numeric::integer AS female_31to35
                , sum(seinendai.female_26to30_cnt)::numeric::integer AS female_26to30
                , sum(seinendai.female_21to25_cnt)::numeric::integer AS female_21to25
                , sum(seinendai.female_16to20_cnt)::numeric::integer AS female_16to20
                , sum(seinendai.female_11to15_cnt)::numeric::integer AS female_11to15
            FROM m_sakuhin sakuhin
			LEFT JOIN m_sakuhin_map sakuhin_map
			ON sakuhin.sakuhin_code = sakuhin_map.sakuhin_code
				AND sakuhin_map.title_category_code = '01'
                AND sakuhin_map.invalid_flg = false
			LEFT JOIN m_manga_title manga
			ON sakuhin_map.title_code = manga.manga_title_code
                AND manga.invalid_flg = false
			LEFT JOIN m_seinendai seinendai
			ON  manga.manga_title_code = seinendai.manga_title_code
				AND seinendai.invalid_flg = false
            WHERE
                sakuhin.sakuhin_code = %s
				AND sakuhin.invalid_flg = false
	            AND sakuhin.valid_start_yyyymmdd <= to_char(now(),'yyyymmdd')
	            AND to_char(now(),'yyyymmdd') <= sakuhin.valid_end_yyyymmdd
			GROUP BY
				sakuhin.sakuhin_code
            ORDER BY
                sakuhin.sakuhin_code
            """
        return self.selectWithParam(sql,[sakuhin_code])


    """年代別男女比データの取得"""
    def selectDetailBySakuhinCode(self,sakuhin_code):
        sql = """
              SELECT
                sum(m_seinendai.male_cnt) ::numeric ::integer
                , sum(m_seinendai.female_cnt) ::numeric ::integer
                , sum(m_seinendai.total_cnt) ::numeric ::integer
                , sum(m_seinendai.male_11to15_cnt) ::numeric ::integer
                , sum(m_seinendai.male_16to20_cnt) ::numeric ::integer
                , sum(m_seinendai.male_21to25_cnt) ::numeric ::integer
                , sum(m_seinendai.male_26to30_cnt) ::numeric ::integer
                , sum(m_seinendai.male_31to35_cnt) ::numeric ::integer
                , sum(m_seinendai.male_36to40_cnt) ::numeric ::integer
                , sum(m_seinendai.male_41to45_cnt) ::numeric ::integer
                , sum(m_seinendai.male_46to50_cnt) ::numeric ::integer
                , sum(m_seinendai.male_gteq51_cnt) ::numeric ::integer
                , sum(m_seinendai.female_11to15_cnt) ::numeric ::integer
                , sum(m_seinendai.female_16to20_cnt) ::numeric ::integer
                , sum(m_seinendai.female_21to25_cnt) ::numeric ::integer
                , sum(m_seinendai.female_26to30_cnt) ::numeric ::integer
                , sum(m_seinendai.female_31to35_cnt) ::numeric ::integer
                , sum(m_seinendai.female_36to40_cnt) ::numeric ::integer
                , sum(m_seinendai.female_41to45_cnt) ::numeric ::integer
                , sum(m_seinendai.female_46to50_cnt) ::numeric ::integer
                , sum(m_seinendai.female_gteq51_cnt) ::numeric ::integer
              FROM
                m_sakuhin_map
                INNER JOIN m_manga_title
                  ON m_sakuhin_map.title_code = m_manga_title.manga_title_code
                    AND m_manga_title.invalid_flg = false
                INNER JOIN m_seinendai
                  ON m_manga_title.seinendai_code = m_seinendai.seinendai_code
                    AND m_seinendai.invalid_flg = false
              WHERE
                m_sakuhin_map.sakuhin_code = %s
              """
        return self.selectWithParam(sql,[sakuhin_code])