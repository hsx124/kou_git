from admin_app.dao.dao_main import DaoMain

class DaoMTagBind(DaoMain):


    def selectMangaTagByTitleName(self, param):
        sql = """
               select
                    manga.manga_title_code
                    , manga.manga_title_name
                    , 'マンガ' AS category_name
                    , '01' AS category_code
                    , mp.update_user
                    , mp.update_time
                    , mp.core_code1
                    , mp.core_code2
                    , mp.sakuhin_tag_code1
                    , mp.sakuhin_tag_code2
                    , mp.sakuhin_tag_code3
                    , mp.sakuhin_tag_code4
                    , mp.sakuhin_tag_code5
                    , mp.sakuhin_tag_code6
                    , mp.sakuhin_tag_code7
                    , mp.sakuhin_tag_code8
                    , mp.sakuhin_tag_code9
                    , mp.sakuhin_tag_code10
                    , mp.sakuhin_tag_code11
                    , mp.sakuhin_tag_code12
                    , mp.sakuhin_tag_code13
                    , mp.sakuhin_tag_code14
                    , mp.sakuhin_tag_code15
                    , mp.sakuhin_tag_code16
                    , mp.sakuhin_tag_code17
                    , mp.sakuhin_tag_code18
                    , mp.sakuhin_tag_code19
                    , mp.sakuhin_tag_code20
                    , manga.tag_map_code 
                    from
                        m_manga_title manga 
                    left join m_sakuhin_tag_map mp 
                        on mp.tag_map_code = manga.tag_map_code 
                        and mp.invalid_flg = false
                    left join m_sakuhin_map sm 
                        on sm.title_code = manga.manga_title_code 
                        and sm.invalid_flg = false
                where
                    manga_title_name LIKE %(title_name)s
                    and manga.invalid_flg = false 
                order by mp.update_time DESC
                , manga.manga_title_code ASC
        """
        return self.selectWithParam(sql, param)

    def getTagNameByCode(self,param):
        sql = """
            select
                sakuhin_tag_code,
                sakuhin_tag_name 
            from
                m_sakuhin_tag 
            where
                sakuhin_tag_code in %(tag_code_list)s

            """
        
        return self.selectWithParam(sql, param)

    def selectNovelTagByTitleName(self, param):
        sql = """
                select
                    novel.novel_title_code
                    , novel.novel_title_name
                    , '小説' AS category_name
                    , '02' AS category_code
                    , mp.update_user
                    , mp.update_time
                    , mp.core_code1
                    , mp.core_code2
                    , mp.sakuhin_tag_code1
                    , mp.sakuhin_tag_code2
                    , mp.sakuhin_tag_code3
                    , mp.sakuhin_tag_code4
                    , mp.sakuhin_tag_code5
                    , mp.sakuhin_tag_code6
                    , mp.sakuhin_tag_code7
                    , mp.sakuhin_tag_code8
                    , mp.sakuhin_tag_code9
                    , mp.sakuhin_tag_code10
                    , mp.sakuhin_tag_code11
                    , mp.sakuhin_tag_code12
                    , mp.sakuhin_tag_code13
                    , mp.sakuhin_tag_code14
                    , mp.sakuhin_tag_code15
                    , mp.sakuhin_tag_code16
                    , mp.sakuhin_tag_code17
                    , mp.sakuhin_tag_code18
                    , mp.sakuhin_tag_code19
                    , mp.sakuhin_tag_code20
                    , novel.tag_map_code 
                from
                    m_novel_title novel 
                left join m_sakuhin_tag_map mp 
                    on mp.tag_map_code = novel.tag_map_code 
                    and mp.invalid_flg = false
                left join m_sakuhin_map sm 
                    on sm.title_code = novel.novel_title_code 
                    and sm.invalid_flg = false
                left join m_title_category category 
                    on sm.title_category_code = category.title_category_code 
                    and category.invalid_flg = false
                where
                    novel_title_name LIKE %(title_name)s
                    and novel.invalid_flg = false 
                ORDER BY 
                    mp.update_time DESC
                    , novel.novel_title_code ASC
        """
        return self.selectWithParam(sql, param)

    def selectAnimeTagByTitleName(self, param):
        sql = """
                select
                    anime.anime_title_code
                    , anime.anime_title_name
                    , 'アニメ' AS category_name
                    , '03' AS category_code
                    , mp.update_user
                    , mp.update_time
                    , mp.core_code1
                    , mp.core_code2
                    , mp.sakuhin_tag_code1
                    , mp.sakuhin_tag_code2
                    , mp.sakuhin_tag_code3
                    , mp.sakuhin_tag_code4
                    , mp.sakuhin_tag_code5
                    , mp.sakuhin_tag_code6
                    , mp.sakuhin_tag_code7
                    , mp.sakuhin_tag_code8
                    , mp.sakuhin_tag_code9
                    , mp.sakuhin_tag_code10
                    , mp.sakuhin_tag_code11
                    , mp.sakuhin_tag_code12
                    , mp.sakuhin_tag_code13
                    , mp.sakuhin_tag_code14
                    , mp.sakuhin_tag_code15
                    , mp.sakuhin_tag_code16
                    , mp.sakuhin_tag_code17
                    , mp.sakuhin_tag_code18
                    , mp.sakuhin_tag_code19
                    , mp.sakuhin_tag_code20
                    , anime.tag_map_code 
                from
                    m_anime_title anime 
                left join m_sakuhin_tag_map mp 
                    on mp.tag_map_code = anime.tag_map_code 
                    and mp.invalid_flg = false
                left join m_sakuhin_map sm 
                    on sm.title_code = anime.anime_title_code 
                    and sm.invalid_flg = false
                left join m_title_category category 
                    on sm.title_category_code = category.title_category_code 
                    and category.invalid_flg = false
                where
                    anime_title_name LIKE %(title_name)s
                    and anime.invalid_flg = false 
                ORDER BY 
                    mp.update_time DESC
                    , anime.anime_title_code ASC
            """
        return self.selectWithParam(sql, param)
    def insert(self,param):
        sql =   """
                insert 
                    into m_sakuhin_tag_map( 
                        tag_map_code
                        ,title_category_code
                        , core_code1
                        , core_code2
                        , sakuhin_tag_code1
                        , sakuhin_tag_code2
                        , sakuhin_tag_code3
                        , sakuhin_tag_code4
                        , sakuhin_tag_code5
                        , sakuhin_tag_code6
                        , sakuhin_tag_code7
                        , sakuhin_tag_code8
                        , sakuhin_tag_code9
                        , sakuhin_tag_code10
                        , sakuhin_tag_code11
                        , sakuhin_tag_code12
                        , sakuhin_tag_code13
                        , sakuhin_tag_code14
                        , sakuhin_tag_code15
                        , sakuhin_tag_code16
                        , sakuhin_tag_code17
                        , sakuhin_tag_code18
                        , sakuhin_tag_code19
                        , sakuhin_tag_code20
                        , invalid_flg
                        , create_user
                        , create_time
                        , update_user
                        , update_time
                    ) 
                    values 
                    (
                        %(tag_map_code)s
                        ,%(title_category_code)s
                        , %(core_code1)s
                        , %(core_code2)s
                        , %(tag_1)s
                        , %(tag_2)s
                        , %(tag_3)s
                        , %(tag_4)s
                        , %(tag_5)s
                        , %(tag_6)s
                        , %(tag_7)s
                        , %(tag_8)s
                        , %(tag_9)s
                        , %(tag_10)s
                        , %(tag_11)s
                        , %(tag_12)s
                        , %(tag_13)s
                        , %(tag_14)s
                        , %(tag_15)s
                        , %(tag_16)s
                        , %(tag_17)s
                        , %(tag_18)s
                        , %(tag_19)s
                        , %(tag_20)s
                        , false
                        , %(full_name)s
                        , now()
                        , %(full_name)s
                        , now()
                    )

            
                """
        return self.updateWithParam(sql,param)

    def update(self,param):
        sql =   """
            update m_sakuhin_tag_map
                set
                title_category_code = %(title_category_code)s,
                core_code1 = %(core_code1)s,
                core_code2 = %(core_code2)s,
                sakuhin_tag_code1 = %(tag_1)s,
                sakuhin_tag_code2 = %(tag_2)s,
                sakuhin_tag_code3 = %(tag_3)s,
                sakuhin_tag_code4 = %(tag_4)s,
                sakuhin_tag_code5 = %(tag_5)s,
                sakuhin_tag_code6 = %(tag_6)s,
                sakuhin_tag_code7 = %(tag_7)s,
                sakuhin_tag_code8 = %(tag_8)s,
                sakuhin_tag_code9 = %(tag_9)s,
                sakuhin_tag_code10 = %(tag_10)s,
                sakuhin_tag_code11 = %(tag_11)s,
                sakuhin_tag_code12 = %(tag_12)s,
                sakuhin_tag_code13 = %(tag_13)s,
                sakuhin_tag_code14 = %(tag_14)s,
                sakuhin_tag_code15 = %(tag_15)s,
                sakuhin_tag_code16 = %(tag_16)s,
                sakuhin_tag_code17 = %(tag_17)s,
                sakuhin_tag_code18 = %(tag_18)s,
                sakuhin_tag_code19 = %(tag_19)s,
                sakuhin_tag_code20 = %(tag_20)s,
                update_user = %(full_name)s,
                update_time = now()
            where 
                tag_map_code = %(tag_map_code)s
                """
        return self.updateWithParam(sql,param)

    def selectMaxTagMapCode(self):
        sql =   """
                SELECT coalesce(max(tag_map_code),'00000000')
                FROM m_sakuhin_tag_map
                """

        return self.select(sql)[0][0]

    def updateTagCodeByTitleCode(self,param_list):
        tb_name = '01'
        title_code = 'manga_title_code'
        if param_list['title_category_code'] == '01':
            tb_name = 'm_manga_title'
            title_code = 'manga_title_code'
        elif param_list['title_category_code'] == '02':
            tb_name = 'm_novel_title'
            title_code = 'novel_title_code'
        else:
            tb_name = 'm_anime_title'
            title_code = 'anime_title_code'
        param = {
            'title_code': param_list['title_code'],
            'tap_map_code': param_list['tag_map_code'],
            'full_name':param_list['full_name']
        }

        sql =   """
                update {}
                set
                    tag_map_code = %(tap_map_code)s
                    ,update_user = %(full_name)s
                    ,update_time = now()
                where
                    {} = %(title_code)s

                """
        sql = sql.format(tb_name,title_code)
        return self.updateWithParam(sql,param)

    def selectSakuhinTagByName(self,param):
        sql =   """
                select
                    sakuhin_tag_code
                    , sakuhin_tag_name 
                from
                    m_sakuhin_tag 
                where
                    sakuhin_tag_name like %(tag_name)s 
                    and invalid_flg = false
                """
        return self.selectWithParam(sql, param)
