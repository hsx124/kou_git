from admin_app.dao.dao_main import DaoMain

class DaoMSeinendai(DaoMain):
    
    """マンガタイトル基本マスタ全件取得"""
    def selectAll(self):
        sql =   """
                SELECT
                COALESCE(m_seinendai.seinendai_code, 'no-code') AS seinendai_code
                , m_manga_title.manga_title_code
                , m_manga_title.manga_title_name
                , COALESCE(total_cnt, '-1') ::numeric ::integer AS total_cnt
                , COALESCE(male_cnt, '-1') ::numeric ::integer AS male_cnt
                , COALESCE(female_cnt, '-1') ::numeric ::integer AS female_cnt
                , m_seinendai.update_user
                , m_seinendai.update_time 
                FROM m_manga_title 
                LEFT JOIN m_seinendai 
                    ON m_manga_title.manga_title_code = m_seinendai.manga_title_code 
                    AND m_seinendai.invalid_flg = false 
                WHERE m_manga_title.invalid_flg = false 
                ORDER BY
                m_seinendai.update_time DESC
                , m_manga_title.manga_title_code ASC
                """
        return self.select(sql)

    """削除する前に該当データの無効フラグ確認""" 
    def selectInvalidFlg(self, param):
        sql =   """
                SELECT invalid_flg
                FROM m_seinendai
                WHERE seinendai_code = %(seinendai_code)s
                """
        return self.selectWithParam(sql, param)[0][0]

    """性年代マスタレコード論理削除・無効フラグを有効にする""" 
    def updateInvalidFlgByMangaSeinendaiCode(self, param):
        sql =   """
                UPDATE m_seinendai
                SET invalid_flg = true
                    , update_user = %(full_name)s
                    , update_time = now()
                WHERE seinendai_code = %(seinendai_code)s
                """
        return self.updateWithParam(sql, param)

    """マンガ基本タイトルマスタの性年代コードを削除する""" 
    def updateInvalidFlgByMangaTitleCode(self, param):
        sql =   """
                UPDATE m_manga_title
                SET seinendai_code = NULL
                    , update_user = %(full_name)s
                    , update_time = now()
                WHERE m_manga_title.seinendai_code = %(seinendai_code)s
                """
        return self.updateWithParam(sql, param)

    """CSV出力用マンガ情報取得"""
    def selectCsvData(self):
        sql =   """
                SELECT
                m_manga_title.manga_title_code
                , m_manga_title.manga_title_name
                , COALESCE(total_cnt, '-1') ::numeric ::integer
                , COALESCE(male_cnt, '-1') ::numeric ::integer
                , COALESCE(female_cnt, '-1') ::numeric ::integer
                , m_seinendai.create_user
                , m_seinendai.create_time
                , m_seinendai.update_user
                , m_seinendai.update_time 
                FROM
                m_manga_title 
                LEFT JOIN m_seinendai 
                    ON m_manga_title.manga_title_code = m_seinendai.manga_title_code 
                    AND m_seinendai.invalid_flg = false 
                WHERE
                m_manga_title.invalid_flg = false 
                ORDER BY
                manga_title_code ASC

                """
        return self.select(sql)
