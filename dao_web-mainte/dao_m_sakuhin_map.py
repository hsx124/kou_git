from admin_app.dao.dao_main import DaoMain

class DaoMSakuhinMap(DaoMain):
    """タイトルデータ取得""" 
    def selectTitleByCode(self, param):
        sql =   """
                SELECT 
                    manga.manga_title_code
                    , manga.manga_title_name
                    , category.title_category_name
                    , category.title_category_code
                    , sakuhin_map.update_user
                    , sakuhin_map.update_time
                    , sakuhin_map.sakuhin_map_id
                FROM
                    m_manga_title manga
                INNER JOIN
                    m_sakuhin_map sakuhin_map
                    ON manga.manga_title_code = sakuhin_map.title_code
                    AND manga.invalid_flg = FALSE
                INNER JOIN m_sakuhin sakuhin
                    ON sakuhin_map.sakuhin_code = sakuhin.sakuhin_code
                    AND sakuhin_map.invalid_flg = FALSE
                    AND sakuhin_map.title_category_code = '01'
                INNER JOIN m_title_category category
                    ON sakuhin_map.title_category_code = category.title_category_code
                    AND category.invalid_flg = FALSE
                WHERE sakuhin.sakuhin_code = %(sakuhin_code)s
                AND sakuhin.invalid_flg = FALSE

				UNION ALL
                SELECT 
                    novel.novel_title_code
                    , novel.novel_title_name
					, category.title_category_name
                    , category.title_category_code
					, sakuhin_map.update_user
					, sakuhin_map.update_time
                    , sakuhin_map.sakuhin_map_id
                FROM
                    m_novel_title novel
                INNER JOIN m_sakuhin_map sakuhin_map
                    ON novel.novel_title_code = sakuhin_map.title_code
                    AND novel.invalid_flg = FALSE
                INNER JOIN m_sakuhin sakuhin
                    ON sakuhin_map.sakuhin_code = sakuhin.sakuhin_code
                    AND sakuhin_map.invalid_flg = FALSE
                    AND sakuhin_map.title_category_code = '02'
				INNER JOIN m_title_category category
					ON sakuhin_map.title_category_code = category.title_category_code
					AND category.invalid_flg = FALSE
                WHERE sakuhin.sakuhin_code = %(sakuhin_code)s
                AND sakuhin.invalid_flg = FALSE
		       
				UNION ALL
                SELECT 
                    anime.anime_title_code
                    , anime.anime_title_name
					, category.title_category_name
                    , category.title_category_code
					, sakuhin_map.update_user
					, sakuhin_map.update_time
                    , sakuhin_map.sakuhin_map_id
                FROM
                    m_anime_title anime
                INNER JOIN m_sakuhin_map sakuhin_map
                    ON anime.anime_title_code = sakuhin_map.title_code
                    AND anime.invalid_flg = FALSE
                INNER JOIN m_sakuhin sakuhin
                    ON sakuhin_map.sakuhin_code = sakuhin.sakuhin_code
                    AND sakuhin_map.invalid_flg = FALSE
                    AND sakuhin_map.title_category_code = '03'
				INNER JOIN m_title_category category
					ON sakuhin_map.title_category_code = category.title_category_code
					AND category.invalid_flg = FALSE
                WHERE sakuhin.sakuhin_code = %(sakuhin_code)s
                AND sakuhin.invalid_flg = FALSE
				
				UNION ALL
                SELECT 
                    app.app_title_code
                    , app.app_title_name
					, category.title_category_name
                    , category.title_category_code
					, sakuhin_map.update_user
					, sakuhin_map.update_time
                    , sakuhin_map.sakuhin_map_id
                FROM
                    m_app_title app
                INNER JOIN m_sakuhin_map sakuhin_map
                    ON app.app_title_code = sakuhin_map.title_code
                    AND app.invalid_flg = FALSE
                INNER JOIN m_sakuhin sakuhin
                    ON sakuhin_map.sakuhin_code = sakuhin.sakuhin_code
                    AND sakuhin_map.invalid_flg = FALSE
                    AND sakuhin_map.title_category_code = '04'
				INNER JOIN m_title_category category
					ON sakuhin_map.title_category_code = category.title_category_code
					AND category.invalid_flg = FALSE
                WHERE sakuhin.sakuhin_code = %(sakuhin_code)s
                AND sakuhin.invalid_flg = FALSE

				UNION ALL
                SELECT 
                    report.media_report_code
                    , report.media_report_name
					, category.title_category_name
                    , category.title_category_code
					, sakuhin_map.update_user
					, sakuhin_map.update_time
                    , sakuhin_map.sakuhin_map_id
                FROM
                    m_media_report report
                INNER JOIN m_sakuhin_map sakuhin_map
                    ON report.media_report_code = sakuhin_map.title_code
                    AND report.invalid_flg = FALSE
                INNER JOIN m_sakuhin sakuhin
                    ON sakuhin_map.sakuhin_code = sakuhin.sakuhin_code
                    AND sakuhin_map.invalid_flg = FALSE
                    AND sakuhin_map.title_category_code = '07'
				INNER JOIN m_title_category category
					ON sakuhin_map.title_category_code = category.title_category_code
					AND category.invalid_flg = FALSE
                WHERE sakuhin.sakuhin_code = %(sakuhin_code)s
                AND sakuhin.invalid_flg = FALSE
                ORDER BY update_time DESC
                """
        return self.selectWithParam(sql, param)

    """タイトル紐付け解除を行い・無効フラグを有効にする""" 
    def updateInvalidFlgBy(self, param):
        sql =   """
                UPDATE m_sakuhin_map
                SET invalid_flg = true
                    , update_user = %(full_name)s
                    , update_time = now()
                WHERE sakuhin_map_id = %(sakuhin_map_id)s
                """
        return self.updateWithParam(sql, param)

    """タイトルリストをもとに作品紐付けマスタデータ追加"""
    def insertByTitleList(self,sakuhin_code,full_name,title_code_list,category_code_list):
        insertsql = """
                    INSERT INTO m_sakuhin_map(
                    sakuhin_map_id
                    , sakuhin_code
                    , title_code
                    , title_category_code
                    , invalid_flg
                    , create_user
                    , create_time
                    , update_user
                    , update_time
                    ) VALUES
                    """
        params = []
        for i in range(len(title_code_list)):
            if i > 0:
                insertsql += ','
            insertsql += "(nextval('m_sakuhin_map_sakuhin_map_id_seq'::regclass)"
            insertsql += ", %s"
            insertsql += ", %s"
            insertsql += ", %s"
            insertsql += ', false'
            insertsql += ", %s"
            insertsql += ", now()"
            insertsql += ", %s"
            insertsql += ", now()"
            insertsql += ")"

            params.append(sakuhin_code)
            params.append(title_code_list[i])
            params.append(category_code_list[i])
            params.append(full_name)
            params.append(full_name)
        
        return self.updateWithParam(insertsql,params)

    """作品コードをもとに、紐付けTwitterのMainFlg=Trueのデータ検索"""
    def selectSakuhinForFlg(self, param):
        sql =   """
                SELECT
                	sakuhin_map.sakuhin_map_id
                    , twitter.account_name
                FROM m_twitter twitter
				INNER JOIN m_sakuhin_map sakuhin_map
                    ON  twitter.twitter_code = sakuhin_map.title_code
                    AND twitter.invalid_flg = FALSE
                    AND twitter.main_account_flg = TRUE
				INNER JOIN m_sakuhin sakuhin
                    ON  sakuhin_map.sakuhin_code = sakuhin.sakuhin_code
                    AND sakuhin_map.invalid_flg = FALSE
                WHERE sakuhin.sakuhin_code = %(sakuhin_code)s
                AND sakuhin.invalid_flg  = FALSE
                """
        return self.selectWithParam(sql,param)

    """作品をもとに作品紐付けマスタデータ追加（作品・Twitter）"""
    def insertBySakuhinCode(self,param):
        sql =   """
                INSERT INTO m_sakuhin_map(
                    sakuhin_map_id
                    , sakuhin_code
                    , title_code
                    , title_category_code
                    , invalid_flg
                    , create_user
                    , create_time
                    , update_user
                    , update_time
                    )
                VALUES (
                    nextval('m_sakuhin_map_sakuhin_map_id_seq'::regclass)
                    , %(sakuhin_code)s
                    , %(twitter_code)s
                    , '06'
                    , false
                    , %(full_name)s
                    , now()
                    , %(full_name)s 
                    , now()
                    )
                """
        return self.updateWithParam(sql,param)

    """作品リストをもとに作品紐付けマスタデータ追加（作品・ゲーム）"""
    def insertBySakuhinList(self,param):
        sql =   """
                INSERT INTO m_sakuhin_map(
                    sakuhin_map_id
                    , sakuhin_code
                    , title_code
                    , title_category_code
                    , invalid_flg
                    , create_user
                    , create_time
                    , update_user
                    , update_time
                ) 
                SELECT
                    nextval('m_sakuhin_map_sakuhin_map_id_seq'::regclass)
                    , sakuhin_code
                    , %(game_code)s
                    , '05'
                    , false
                    , %(full_name)s
                    , now()
                    , %(full_name)s
                    , now()
                FROM
                m_sakuhin sakuhin 
                WHERE
                sakuhin.sakuhin_code in %(sakuhin_code_list)s
                AND sakuhin.invalid_flg = false
                """
        return self.updateWithParam(sql,param)