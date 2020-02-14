from admin_app.dao.dao_main import DaoMain

class DaoMHeibai(DaoMain):

    """併売マスタ全件取得(マンガ)"""
    def selectMangaAll(self):
        sql =   """
                SELECT
                COALESCE(m_heibai.heibai_code, 'no-code') AS heibai_code
                , m_manga_title.manga_title_code
                , m_manga_title.manga_title_name
                , m_heibai.heibai_name_1
                , m_heibai.heibai_name_2
                , m_heibai.heibai_name_3
                , m_heibai.heibai_name_4
                , m_heibai.heibai_name_5
                , m_heibai.update_user
                , m_heibai.update_time
                FROM m_manga_title
                LEFT JOIN m_heibai
                    ON m_manga_title.heibai_code = m_heibai.heibai_code
                    AND m_heibai.invalid_flg = false
                WHERE m_manga_title.invalid_flg = false
                ORDER BY
                m_heibai.update_time DESC
                , m_manga_title.manga_title_code ASC
                """
        return self.select(sql)

    """併売マスタ全件取得(小説)"""
    def selectNovelAll(self):
        sql =   """
                SELECT
                COALESCE(m_heibai.heibai_code, 'no-code') AS heibai_code
                , m_novel_title.novel_title_code
                , m_novel_title.novel_title_name
                , m_heibai.heibai_name_1
                , m_heibai.heibai_name_2
                , m_heibai.heibai_name_3
                , m_heibai.heibai_name_4
                , m_heibai.heibai_name_5
                , m_heibai.update_user
                , m_heibai.update_time
                FROM m_novel_title
                LEFT JOIN m_heibai
                    ON m_novel_title.heibai_code = m_heibai.heibai_code
                    AND m_heibai.invalid_flg = false
                WHERE m_novel_title.invalid_flg = false
                ORDER BY
                m_heibai.update_time DESC
                , m_novel_title.novel_title_code ASC
                """
        return self.select(sql)

    """削除する前に該当データの無効フラグ確認"""
    def selectInvalidFlg(self, param):
        sql =   """
                SELECT invalid_flg
                FROM m_heibai
                WHERE heibai_code = %(heibai_code)s
                """
        return self.selectWithParam(sql, param)[0][0]

    """併売マスタレコード論理削除・無効フラグを有効にする"""
    def updateInvalidFlgByHeibaiCode(self, param):
        sql =   """
                UPDATE m_heibai
                SET invalid_flg = true
                    , update_user = %(full_name)s
                    , update_time = now()
                WHERE heibai_code = %(heibai_code)s
                """
        return self.updateWithParam(sql, param)

    """マンガタイトル基本マスタの併売コードを削除する""" 
    def updateInvalidFlgByMangaTitleCode(self, param):
        sql =   """
                UPDATE m_manga_title
                SET heibai_code = NULL
                    , update_user = %(full_name)s
                    , update_time = now()
                WHERE m_manga_title.heibai_code = %(heibai_code)s
                """
        return self.updateWithParam(sql, param)

    """小説タイトル基本マスタの併売コードを削除する""" 
    def updateInvalidFlgByNovelTitleCode(self, param):
        sql =   """
                UPDATE m_novel_title
                SET heibai_code = NULL
                    , update_user = %(full_name)s
                    , update_time = now()
                WHERE m_novel_title.heibai_code = %(heibai_code)s
                """
        return self.updateWithParam(sql, param)

    """CSV出力用マンガ情報取得"""
    def selectMangaCsvData(self):
        sql =   """
                SELECT
                m_manga_title.manga_title_code
                , m_manga_title.manga_title_name
                , m_heibai.heibai_code
                , m_heibai.heibai_name_1
                , m_heibai.heibai_1
                , m_heibai.heibai_name_2
                , m_heibai.heibai_2
                , m_heibai.heibai_name_3
                , m_heibai.heibai_3
                , m_heibai.heibai_name_4
                , m_heibai.heibai_4
                , m_heibai.heibai_name_5
                , m_heibai.heibai_5
                , m_heibai.create_user
                , m_heibai.create_time
                , m_heibai.update_user
                , m_heibai.update_time
                FROM
                    m_manga_title
                LEFT JOIN m_heibai
                    ON m_manga_title.heibai_code = m_heibai.heibai_code
                    AND m_heibai.invalid_flg = false
                WHERE
                    m_manga_title.invalid_flg = false
                ORDER BY
                    manga_title_code ASC

                """
        return self.select(sql)
    
    """CSV出力用小説情報取得"""
    def selectNovelCsvData(self):
        sql =   """
                SELECT
                m_novel_title.novel_title_code
                , m_novel_title.novel_title_name
                , m_heibai.heibai_code
                , m_heibai.heibai_name_1
                , m_heibai.heibai_1
                , m_heibai.heibai_name_2
                , m_heibai.heibai_2
                , m_heibai.heibai_name_3
                , m_heibai.heibai_3
                , m_heibai.heibai_name_4
                , m_heibai.heibai_4
                , m_heibai.heibai_name_5
                , m_heibai.heibai_5
                , m_heibai.create_user
                , m_heibai.create_time
                , m_heibai.update_user
                , m_heibai.update_time
                FROM
                    m_novel_title
                LEFT JOIN m_heibai
                    ON m_novel_title.heibai_code = m_heibai.heibai_code
                    AND m_heibai.invalid_flg = false
                WHERE
                    m_novel_title.invalid_flg = false
                ORDER BY
                    novel_title_code ASC

                """
        return self.select(sql)
