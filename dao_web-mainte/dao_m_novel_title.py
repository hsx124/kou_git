from admin_app.dao.dao_main import DaoMain

class DaoMNovelTitle(DaoMain):

    """小説タイトル基本マスタ全件取得"""
    def selectAll(self):
        sql =   """
                SELECT
                    novel_title_code
                    , novel_title_name
                    , rensai_start_yyyymm
                    , media_name
                    , publisher_name
                    , m_novel_title.update_user
                    , m_novel_title.update_time
                FROM
                    m_novel_title
                LEFT JOIN m_media
                        ON m_novel_title.media_code = m_media.media_code
                        AND m_media.invalid_flg = false
                LEFT JOIN m_publisher
                        ON m_novel_title.publisher_code = m_publisher.publisher_code
                        AND m_publisher.invalid_flg = false
                WHERE
                    m_novel_title.invalid_flg = false
                ORDER BY
                    update_time DESC
                    , novel_title_code ASC
                """
        return self.select(sql)

    """削除する前に該当データの無効フラグ確認"""
    def selectInvalidFlg(self, param):
        sql =   """
                SELECT
                    invalid_flg
                FROM m_novel_title
                WHERE novel_title_code = %(novel_title_code)s
                """
        return self.selectWithParam(sql, param)[0][0]

    """小説タイトル基本マスタレコード論理削除・無効フラグを有効にする"""
    def updateInvalidFlgByNovelCode(self, param):
        sql =   """
                UPDATE m_novel_title
                SET invalid_flg = true
                    , update_user = %(full_name)s
                    , update_time = now()
                WHERE novel_title_code = %(novel_title_code)s
                """
        return self.updateWithParam(sql, param)

    """CSV出力用小説情報取得"""
    def selectCsvData(self):
        sql =   """
                SELECT
                    novel_title_code
                    , novel_title_name
                    , rensai_start_yyyymm
                    , media_name
                    , publisher_name
                    , m_novel_title.create_user
                    , m_novel_title.create_time
                    , m_novel_title.update_user
                    , m_novel_title.update_time
                FROM
                    m_novel_title
                LEFT JOIN m_media
                        ON m_novel_title.media_code = m_media.media_code
                        AND m_media.invalid_flg = false
                LEFT JOIN m_publisher
                        ON m_novel_title.publisher_code = m_publisher.publisher_code
                        AND m_publisher.invalid_flg = false
                WHERE
                    m_novel_title.invalid_flg = false
                ORDER BY
                    novel_title_code ASC
                """
        return self.select(sql)

    """小説タイトル基本マスタに存在する最大の小説タイトルコードを取得する"""
    def selectMaxNovelTitleCode(self):
        sql =   """
                SELECT
                    coalesce(max(novel_title_code), 'S000000000')
                FROM
                    m_novel_title
                """
        return self.select(sql)[0][0]

    """小説タイトル基本マスタに同一小説タイトルコードがあるか検索"""
    def selectSameCode(self, novel_title_code):
        param = {'novel_title_code':novel_title_code}

        sql =   """
                SELECT count(*)
                FROM m_novel_title
                WHERE novel_title_code = %(novel_title_code)s
                """
        return self.selectWithParam(sql, param)[0][0]

    """小説タイトル基本マスタに同一小説タイトル名があるか検索"""
    def selectSameName(self, novel_title_code, novel_title_name):
        param = {
            'novel_title_code':novel_title_code,
            'novel_title_name':novel_title_name
        }
        sql =   """
                SELECT count(*)
                FROM m_novel_title
                WHERE novel_title_name = %(novel_title_name)s
                AND novel_title_code <> %(novel_title_code)s
                AND invalid_flg = false
                """
        return self.selectWithParam(sql, param)[0][0]

    """小説タイトル基本マスタ作成"""
    def insertNovel(self,entity):
        # 小説タイトルコード重複チェック
        if 0 < self.selectSameCode(entity['novel_title_code']):
            raise DaoMNovelTitle.DuplicateNovelTitleCodeException

        # 小説タイトル名重複チェック
        if 0 < self.selectSameName(entity['novel_title_code'],entity['novel_title_name']):
            raise DaoMNovelTitle.DuplicateNovelTitleNameException

        sql =   """
                INSERT INTO m_novel_title
                    (
                    novel_title_code
                    , novel_title_name
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
                        %(novel_title_code)s
                        , %(novel_title_name)s
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

    """小説タイトル基本マスタ編集画面表示用"""
    def selectUpdateData(self, param):
        sql =   """
                SELECT
                    novel_title_code
                    , novel_title_name
                    , rensai_start_yyyymm
                    , published_cnt ::numeric ::integer
                    , CASE rensai_end_flg WHEN TRUE THEN 'True' ELSE 'False' END
                    , award_history
                    , m_novel_title.media_code
                    , m_media.media_name
                    , m_novel_title.publisher_code
                    , m_publisher.publisher_name
                    , m_novel_title.staff_map_code
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
                    m_novel_title
                    LEFT JOIN m_media
                        ON m_novel_title.media_code = m_media.media_code
                        AND m_media.invalid_flg = false
                    LEFT JOIN m_publisher
                        ON m_novel_title.publisher_code = m_publisher.publisher_code
                        AND m_publisher.invalid_flg = false
                    LEFT JOIN m_staff_map
                        ON m_novel_title.staff_map_code = m_staff_map.staff_map_code
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
                    m_novel_title.invalid_flg = false
                    AND novel_title_code = %(novel_title_code)s
                """
        return self.selectWithParam(sql, param)

    """小説タイトル基本マスタ更新"""
    def updateNovel(self,entity):
        # 小説タイトル名重複チェック
        if 0 < self.selectSameName(entity['novel_title_code'], entity['novel_title_name']):
            raise DaoMNovelTitle.DuplicateNovelTitleNameException

        sql =   """
                UPDATE m_novel_title
                SET
                    novel_title_name = %(novel_title_name)s
                    , rensai_start_yyyymm = %(rensai_start_yyyymm)s
                    , published_cnt = %(published_cnt)s
                    , rensai_end_flg = %(rensai_end_flg)s
                    , award_history = %(award_history)s
                    , media_code = %(media_code)s
                    , publisher_code = %(publisher_code)s
                    , update_user = %(full_name)s
                    , update_time = now()
                WHERE novel_title_code = %(novel_title_code)s
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

    """小説タイトルコード重複エラー"""
    class DuplicateNovelTitleCodeException(Exception):
        pass

    """小説タイトル名重複エラー"""
    class DuplicateNovelTitleNameException(Exception):
        pass

    """タイトル名・タイトルかな名をもとに小説タイトルデータを取得"""
    def selectTitleByName(self, param):
        sql =   """
			    SELECT
                    novel_title_code
                    , novel_title_name
                    , '小説' AS category_name
                    , '02' AS category_code
                    , update_user
                    , update_time
                FROM m_novel_title
                WHERE invalid_flg = false
                AND novel_title_name LIKE %(title_name)s
                ORDER BY novel_title_code
                """
        return self.selectWithParam(sql, param)