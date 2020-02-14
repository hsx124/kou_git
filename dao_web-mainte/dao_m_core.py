from admin_app.dao.dao_main import DaoMain

class DaoMCore(DaoMain):
    def selectAll(self):
        sql =   '''
                SELECT
                  core_code
                , core_name
                FROM m_core
                ORDER BY core_code
                '''
        return self.select(sql)

    def selectCoreList(self):
        sql = """
              SELECT
                  core_code
                , core_name
                , update_user
                , update_time
                FROM m_core
                WHERE invalid_flg = false
                ORDER BY update_time DESC,core_code DESC
              """
        return self.select(sql)

    """削除する前に該当データの無効フラグ確認""" 
    def selectInvalidFlg(self, param):
        sql =   """
                SELECT
                    invalid_flg
                FROM m_core
                WHERE core_code = %(core_code)s
                """
        return self.selectWithParam(sql, param)[0][0]

    """コアマスタレコード論理削除・無効フラグを有効にする""" 
    def updateInvalidFlgByCoreCode(self, param):
        sql =   """
                UPDATE m_core
                SET invalid_flg = true
                    , update_user = %(full_name)s
                    , update_time = now()
                WHERE core_code = %(core_code)s
                """
        return self.updateWithParam(sql, param)

    """CSV出力用マンガ情報取得"""
    def selectCsvData(self):
        sql =   """
                SELECT
                    core_code
                  , core_name
                  , create_user
                  , create_time
                  , update_user
                  , update_time
                FROM
                  m_core
                WHERE
                  invalid_flg = false
                ORDER BY
                  core_code ASC
                """
        return self.select(sql)

    """コアマスタに存在する最大のコアコードを取得する"""
    def selectMaxCoreCode(self):
        sql =   """
                SELECT
                    coalesce(max(core_code), '000000')
                FROM
                    m_core
                """
        return self.select(sql)[0][0]

    """コアマスタに同一コアコードがあるか検索"""
    def selectSameCode(self, core_code):
        param = {'core_code':core_code}

        sql =   """
                SELECT count(*)
                FROM m_core
                WHERE core_code = %(core_code)s
                """
        return self.selectWithParam(sql, param)[0][0]

    """コアマスタに同一コア名があるか検索"""
    def selectSameName(self, core_code, core_name):
        param = {
            'core_code':core_code,
            'core_name':core_name
        }
        sql =   """
                SELECT count(*)
                FROM m_core
                WHERE core_name = %(core_name)s
                AND core_code <> %(core_code)s
                AND invalid_flg = false
                """
        return self.selectWithParam(sql, param)[0][0]

    """コアマスタ作成"""
    def insertCore(self,entity):
        # コアコード重複チェック
        if 0 < self.selectSameCode(entity['core_code']):
            raise DaoMCore.DuplicateCoreCodeException

        # コア名重複チェック
        if 0 < self.selectSameName(entity['core_code'],entity['core_name']):
            raise DaoMCore.DuplicateCoreNameException

        sql =   """
                INSERT INTO m_core
                  (
                  core_code
                  , core_name
                  , invalid_flg
                  , create_user
                  , create_time
                  , update_user
                  , update_time
                  )
                VALUES (
                        %(core_code)s
                        , %(core_name)s
                        , false
                        , %(full_name)s
                        , now()
                        , %(full_name)s
                        , now()
                        )
                """
        return self.updateWithParam(sql,entity)

    """コアマスタ編集画面表示用"""
    def selectUpdateData(self, param):
        sql =   """
                SELECT
                  core_code
                  , core_name
                FROM
                  m_core
                WHERE
                  invalid_flg = false
                  AND core_code = %(core_code)s
                """
        return self.selectWithParam(sql, param)

    """コアマスタ更新"""
    def updateCore(self,entity):
        # コア名重複チェック
        if 0 < self.selectSameName(entity['core_code'], entity['core_name']):
            raise DaoMCore.DuplicateCoreNameException

        sql =   """
                UPDATE m_core
                SET
                    core_name = %(core_name)s
                    , update_user = %(full_name)s
                    , update_time = now()
                WHERE core_code = %(core_code)s
                """
        return self.updateWithParam(sql,entity)

    """コアコード重複エラー"""
    class DuplicateCoreCodeException(Exception):
        pass

    """コア名重複エラー"""
    class DuplicateCoreNameException(Exception):
        pass