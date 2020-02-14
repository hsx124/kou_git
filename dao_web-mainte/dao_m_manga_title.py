from admin_app.dao.dao_main import DaoMain

class DaoMMangaTitle(DaoMain):

    """マンガタイトル基本マスタ全件取得"""
    def selectAll(self):
        sql =   """
                SELECT
                    manga_title_code
                    , manga_title_name
                    , rensai_start_yyyymm
                    , media_name
                    , publisher_name
                    , m_manga_title.update_user
                    , m_manga_title.update_time
                FROM
                    m_manga_title
                LEFT JOIN m_media
                        ON m_manga_title.media_code = m_media.media_code
                        AND m_media.invalid_flg = false
                LEFT JOIN m_publisher
                        ON m_manga_title.publisher_code = m_publisher.publisher_code
                        AND m_publisher.invalid_flg = false
                WHERE
                    m_manga_title.invalid_flg = false
                ORDER BY
                    update_time DESC
                    , manga_title_code ASC
                """
        return self.select(sql)

    """削除する前に該当データの無効フラグ確認""" 
    def selectInvalidFlg(self, param):
        sql =   """
                SELECT
                    invalid_flg
                FROM m_manga_title
                WHERE manga_title_code = %(manga_title_code)s
                """
        return self.selectWithParam(sql, param)[0][0]

    """マンガタイトル基本マスタレコード論理削除・無効フラグを有効にする""" 
    def updateInvalidFlgByMangaCode(self, param):
        sql =   """
                UPDATE m_manga_title
                SET invalid_flg = true
                    , update_user = %(full_name)s
                    , update_time = now()
                WHERE manga_title_code = %(manga_title_code)s
                """
        return self.updateWithParam(sql, param)

    """CSV出力用マンガ情報取得"""
    def selectCsvData(self):
        sql =   """
                SELECT
                    manga_title_code
                    , manga_title_name
                    , rensai_start_yyyymm
                    , media_name
                    , publisher_name
                    , m_manga_title.create_user
                    , m_manga_title.create_time
                    , m_manga_title.update_user
                    , m_manga_title.update_time
                FROM
                    m_manga_title
                LEFT JOIN m_media
                        ON m_manga_title.media_code = m_media.media_code
                        AND m_media.invalid_flg = false
                LEFT JOIN m_publisher
                        ON m_manga_title.publisher_code = m_publisher.publisher_code
                        AND m_publisher.invalid_flg = false
                WHERE
                    m_manga_title.invalid_flg = false
                ORDER BY
                    manga_title_code ASC
                """
        return self.select(sql)

    """マンガタイトル基本マスタに存在する最大のマンガタイトルコードを取得する"""
    def selectMaxMangaTitleCode(self):
        sql =   """
                SELECT
                    coalesce(max(manga_title_code), 'M000000000')
                FROM
                    m_manga_title
                """
        return self.select(sql)[0][0]

    """マンガタイトル基本マスタに同一マンガタイトルコードがあるか検索"""
    def selectSameCode(self, manga_title_code):
        param = {'manga_title_code':manga_title_code}

        sql =   """
                SELECT count(*)
                FROM m_manga_title
                WHERE manga_title_code = %(manga_title_code)s
                """
        return self.selectWithParam(sql, param)[0][0]

    """マンガタイトル基本マスタに同一マンガタイトル名があるか検索"""
    def selectSameName(self, manga_title_code, manga_title_name):
        param = {
            'manga_title_code':manga_title_code,
            'manga_title_name':manga_title_name
        }
        sql =   """
                SELECT count(*)
                FROM m_manga_title
                WHERE manga_title_name = %(manga_title_name)s
                AND manga_title_code <> %(manga_title_code)s
                AND invalid_flg = false
                """
        return self.selectWithParam(sql, param)[0][0]

    """マンガタイトル基本マスタ作成"""
    def insertManga(self,entity):
        # マンガタイトルコード重複チェック
        if 0 < self.selectSameCode(entity['manga_title_code']):
            raise DaoMMangaTitle.DuplicateMangaTitleCodeException

        # マンガタイトル名重複チェック
        if 0 < self.selectSameName(entity['manga_title_code'],entity['manga_title_name']):
            raise DaoMMangaTitle.DuplicateMangaTitleNameException

        sql =   """
                INSERT INTO m_manga_title
                    (
                    manga_title_code
                    , manga_title_name
                    , rensai_start_yyyymm
                    , published_cnt
                    , rensai_end_flg
                    , award_history
                    , media_code
                    , publisher_code
                    , staff_map_code
                    , invalid_flg
                    , create_user
                    , create_time
                    , update_user
                    , update_time
                    )
                VALUES (
                        %(manga_title_code)s
                        , %(manga_title_name)s
                        , %(rensai_start_yyyymm)s
                        , %(published_cnt)s
                        , %(rensai_end_flg)s
                        , %(award_history)s
                        , %(media_code)s
                        , %(publisher_code)s
                        , %(staff_map_code)s
                        , false
                        , %(full_name)s
                        , now()
                        , %(full_name)s
                        , now()
                        )
                """
        return self.updateWithParam(sql,entity)

    def insertStaffMap(self,entity):
        sql =   """
                INSERT INTO m_staff_map
                (
                    staff_map_code
                    , title_category_code
                    , staff_role_code1
                    , staff_code1
                    , staff_role_code2
                    , staff_code2
                    , staff_role_code3
                    , staff_code3
                    , staff_role_code4
                    , staff_code4
                    , staff_role_code5
                    , staff_code5
                    , invalid_flg
                    , create_user
                    , create_time
                    , update_user
                    , update_time
                )
                VALUES
                (
                    %(staff_map_code)s
                    , %(title_category_code)s
                    , %(staff_role_code1)s
                    , %(staff_code1)s
                    , %(staff_role_code2)s
                    , %(staff_code2)s
                    , %(staff_role_code3)s
                    , %(staff_code3)s
                    , %(staff_role_code4)s
                    , %(staff_code4)s
                    , %(staff_role_code5)s
                    , %(staff_code5)s
                    , false
                    , %(full_name)s
                    , now()
                    , %(full_name)s
                    , now()
                )
                """
        return self.updateWithParam(sql,entity)

    """マンガタイトル基本マスタ編集画面表示用"""
    def selectUpdateData(self, param):
        sql =   """
                SELECT
                    manga_title_code
                    , manga_title_name
                    , rensai_start_yyyymm
                    , published_cnt ::numeric ::integer
                    , CASE rensai_end_flg WHEN TRUE THEN 'True' ELSE 'False' END
                    , award_history
                    , m_manga_title.media_code
                    , m_media.media_name
                    , m_manga_title.publisher_code
                    , m_publisher.publisher_name
                    , m_manga_title.staff_map_code
                    , role1.staff_role_code
                    , role1.staff_role_name
                    , role2.staff_role_code
                    , role2.staff_role_name
                    , role3.staff_role_code
                    , role3.staff_role_name
                    , role4.staff_role_code
                    , role4.staff_role_name
                    , role5.staff_role_code
                    , role5.staff_role_name
                    , staff1.staff_code
                    , staff1.staff_name
                    , staff2.staff_code
                    , staff2.staff_name
                    , staff3.staff_code
                    , staff3.staff_name
                    , staff4.staff_code
                    , staff4.staff_name
                    , staff5.staff_code
                    , staff5.staff_name
                FROM
                    m_manga_title
                    LEFT JOIN m_media
                        ON m_manga_title.media_code = m_media.media_code
                        AND m_media.invalid_flg = false
                    LEFT JOIN m_publisher
                        ON m_manga_title.publisher_code = m_publisher.publisher_code
                        AND m_publisher.invalid_flg = false
                    LEFT JOIN m_staff_map
                        ON m_manga_title.staff_map_code = m_staff_map.staff_map_code
                        AND m_staff_map.invalid_flg = false
                    LEFT JOIN m_staff_role AS role1
                        ON m_staff_map.staff_role_code1 = role1.staff_role_code
                        AND role1.invalid_flg = false
                    LEFT JOIN m_staff_role AS role2
                        ON m_staff_map.staff_role_code2 = role2.staff_role_code
                        AND role2.invalid_flg = false
                    LEFT JOIN m_staff_role AS role3
                        ON m_staff_map.staff_role_code3 = role3.staff_role_code
                        AND role3.invalid_flg = false
                    LEFT JOIN m_staff_role AS role4
                        ON m_staff_map.staff_role_code4 = role4.staff_role_code
                        AND role4.invalid_flg = false
                    LEFT JOIN m_staff_role AS role5
                        ON m_staff_map.staff_role_code5 = role5.staff_role_code
                        AND role5.invalid_flg = false
                    LEFT JOIN m_staff AS staff1
                        ON m_staff_map.staff_code1 = staff1.staff_code
                        AND staff1.invalid_flg = false
                    LEFT JOIN m_staff AS staff2
                        ON m_staff_map.staff_code2 = staff2.staff_code
                        AND staff2.invalid_flg = false
                    LEFT JOIN m_staff AS staff3
                        ON m_staff_map.staff_code3 = staff3.staff_code
                        AND staff3.invalid_flg = false
                    LEFT JOIN m_staff AS staff4
                        ON m_staff_map.staff_code4 = staff4.staff_code
                        AND staff4.invalid_flg = false
                    LEFT JOIN m_staff AS staff5
                        ON m_staff_map.staff_code5 = staff5.staff_code
                        AND staff5.invalid_flg = false
                WHERE
                    m_manga_title.invalid_flg = false
                    AND manga_title_code = %(manga_title_code)s
                """
        return self.selectWithParam(sql, param)

    """マンガタイトル基本マスタ更新"""
    def updateManga(self,entity):
        # マンガタイトル名重複チェック
        if 0 < self.selectSameName(entity['manga_title_code'], entity['manga_title_name']):
            raise DaoMMangaTitle.DuplicateMangaTitleNameException

        sql =   """
                UPDATE m_manga_title
                SET
                    manga_title_name = %(manga_title_name)s
                    , rensai_start_yyyymm = %(rensai_start_yyyymm)s
                    , published_cnt = %(published_cnt)s
                    , rensai_end_flg = %(rensai_end_flg)s
                    , award_history = %(award_history)s
                    , media_code = %(media_code)s
                    , publisher_code = %(publisher_code)s
                    , update_user = %(full_name)s
                    , update_time = now()
                WHERE manga_title_code = %(manga_title_code)s
                """
        return self.updateWithParam(sql,entity)

    def updateStaffMap(self,entity):
        sql =   """
                UPDATE m_staff_map
                SET
                    staff_map_code = %(staff_map_code)s
                    , staff_role_code1 = %(staff_role_code1)s
                    , staff_code1 = %(staff_code1)s
                    , staff_role_code2 = %(staff_role_code2)s
                    , staff_code2 = %(staff_code2)s
                    , staff_role_code3 = %(staff_role_code3)s
                    , staff_code3 = %(staff_code3)s
                    , staff_role_code4 = %(staff_role_code4)s
                    , staff_code4 = %(staff_code4)s
                    , staff_role_code5 = %(staff_role_code5)s
                    , staff_code5 = %(staff_code5)s
                    , update_user = %(full_name)s
                    , update_time = now()
                WHERE staff_map_code = %(staff_map_code)s
                """
        return self.updateWithParam(sql,entity)

    """マンガタイトルコード重複エラー"""
    class DuplicateMangaTitleCodeException(Exception):
        pass

    """マンガタイトル名重複エラー"""
    class DuplicateMangaTitleNameException(Exception):
        pass

    """タイトル名・タイトルかな名をもとにマンガタイトルデータを取得""" 
    def selectTitleByName(self, param):
        sql =   """
			    SELECT
                    manga_title_code
                    , manga_title_name
                    , 'マンガ' AS category_name
                    , '01' AS category_code
                    , update_user
                    , update_time
                FROM m_manga_title
                WHERE invalid_flg = false
                AND manga_title_name LIKE %(title_name)s
                ORDER BY manga_title_code
                """
        return self.selectWithParam(sql, param)
    
    def selectMangaTitle(self,manga_title_code):
        param = {'manga_title_code': manga_title_code}
        sql =   """
                SELECT
                    manga_title_code
                    ,manga_title_name
                FROM m_manga_title
                WHERE manga_title_code = %(manga_title_code)s
                """
        return self.selectWithParam(sql, param)

    """キーワードに一致する"""
    def selectMangaByKeyword(self,keyword):
        param = {'keyword':'%'+ keyword +'%'}
        sql =   """
                SELECT
                    manga_title_code
                    , manga_title_name
                    , rensai_start_yyyymm
                    , media_name
                    , publisher_name
                    , m_manga_title.update_user
                    , m_manga_title.update_time
                FROM
                    m_manga_title
                LEFT JOIN m_media
                        ON m_manga_title.media_code = m_media.media_code
                        AND m_media.invalid_flg = false
                LEFT JOIN m_publisher
                        ON m_manga_title.publisher_code = m_publisher.publisher_code
                        AND m_publisher.invalid_flg = false
                WHERE
                    m_manga_title.invalid_flg = false
                    AND m_manga_title.manga_title_name LIKE %(keyword)s
                ORDER BY
                    update_time DESC
                    , manga_title_code ASC
                """
        return self.selectWithParam(sql,param)