from admin_app.dao.dao_main import DaoMain

class DaoMSeisakuCompany(DaoMain):

    """制作会社マスタ全件取得"""
    def selectAll(self):
        sql =   """
                SELECT
                    seisaku_company_code
                    , seisaku_company_name
                    , update_user
                    , update_time
                FROM m_seisaku_company
                WHERE invalid_flg = false
                ORDER BY
                    update_time DESC
                    , seisaku_company_code ASC
                """
        return self.select(sql)

    """削除する前に該当データの無効フラグ確認""" 
    def selectInvalidFlg(self, param):
        sql =   """
                SELECT
                    invalid_flg
                FROM m_seisaku_company
                WHERE seisaku_company_code = %(seisaku_company_code)s
                """
        return self.selectWithParam(sql, param)[0][0]

    """制作会社マスタレコード論理削除・無効フラグを有効にする""" 
    def updateInvalidFlg(self, param):
        sql =   """
                UPDATE m_seisaku_company
                SET invalid_flg = true
                    , update_user = %(full_name)s
                    , update_time = now()
                WHERE seisaku_company_code = %(seisaku_company_code)s
                """
        return self.updateWithParam(sql, param)

    """CSV出力用制作会社情報取得"""
    def selectCsvData(self):
        sql =   """
                SELECT
                    seisaku_company_code
                    , seisaku_company_name
                    , create_user
                    , create_time
                    , update_user
                    , update_time
                FROM m_seisaku_company
                WHERE invalid_flg = false
                ORDER BY seisaku_company_code ASC
                """
        return self.select(sql)

    """制作会社に存在する最大の制作会社コードを取得する"""
    def selectMaxCode(self):
        sql =   """
                SELECT coalesce(max(seisaku_company_code),'00000')
                FROM m_seisaku_company 
                """
        return self.select(sql)[0][0]

    """制作会社に同一制作会社コードを検索"""
    def selectSameCode(self, seisaku_company_code):
        param = {'seisaku_company_code':seisaku_company_code}

        sql =   """
                SELECT count(*)
                FROM m_seisaku_company
                WHERE seisaku_company_code = %(seisaku_company_code)s
                """
        return self.selectWithParam(sql, param)[0][0]

    """制作会社に同一制作会社名を検索"""
    def selectSameName(self, seisaku_company_code, seisaku_company_name):
        param = {
            'seisaku_company_code':seisaku_company_code,
            'seisaku_company_name':seisaku_company_name
        }
        sql =   """
                SELECT count(*)
                FROM m_seisaku_company
                WHERE seisaku_company_name = %(seisaku_company_name)s
                AND seisaku_company_code <> %(seisaku_company_code)s
                AND invalid_flg = false
                """
        return self.selectWithParam(sql, param)[0][0]

    """新規制作会社マスタ作成"""
    def insert(self,entity):
        # 制作会社コード重複チェック
        if 0 < self.selectSameCode(entity['seisaku_company_code']):
            raise DaoMSeisakuCompany.DuplicateSeisakuCompanyCodeException

        # 制作会社名重複チェック
        if 0 < self.selectSameName(entity['seisaku_company_code'],entity['seisaku_company_name']):
            raise DaoMSeisakuCompany.DuplicateSeisakuCompanyNameException
        
        sql =   """
                INSERT INTO m_seisaku_company
                    (
                    seisaku_company_code
                    , seisaku_company_name
                    , invalid_flg
                    , create_user
                    , create_time
                    , update_user
                    , update_time
                    )
                VALUES (%(seisaku_company_code)s, %(seisaku_company_name)s, false, %(full_name)s , now(), %(full_name)s , now())
                """
        return self.updateWithParam(sql,entity)

    """制作会社マスタ編集画面表示用"""
    def selectUpdateData(self, param):
        sql =   """
                SELECT
                    seisaku_company_code
                    , seisaku_company_name
                FROM m_seisaku_company
                WHERE invalid_flg = false
                AND seisaku_company_code = %(seisaku_company_code)s
                """
        return self.selectWithParam(sql, param)

    """制作会社マスタ更新"""
    def update(self,entity):
        # 制作会社名重複チェック
        if 0 < self.selectSameName(entity['seisaku_company_code'], entity['seisaku_company_name']):
          raise DaoMSeisakuCompany.DuplicateSeisakuCompanyNameException

        sql =   """
                UPDATE m_seisaku_company
                SET
                    seisaku_company_name = %(seisaku_company_name)s
                    , update_user = %(full_name)s
                    , update_time = now()
                WHERE seisaku_company_code = %(seisaku_company_code)s
                """
        return self.updateWithParam(sql,entity)

    """制作会社コード重複エラー"""
    class DuplicateSeisakuCompanyCodeException(Exception):
        pass

    """制作会社名重複エラー"""
    class DuplicateSeisakuCompanyNameException(Exception):
        pass