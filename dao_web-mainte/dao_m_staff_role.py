from admin_app.dao.dao_main import DaoMain

class DaoMStaffRole(DaoMain):

    def selectStaffRoleByBook(self):
        sql =   """
                SELECT
                    staff_role_code
                    ,staff_role_name
                FROM
                    m_staff_role
                WHERE
                    invalid_flg = false
                """
        return self.select(sql)

    def selectStaffRoleKeyword(self,keyword):
        param = {'keyword':'%' + keyword + '%'}

        sql =   """
                SELECT
                    staff_role_code
                    ,staff_role_name
                FROM
                    m_staff_role
                WHERE
                    invalid_flg = false
                    AND staff_role_name LIKE %(keyword)s
                """
        return self.selectWithParam(sql,param)

    def selectStaffRoleList(self):
        sql = """
              SELECT
                  staff_role_code
                , staff_role_name
                , update_user
                , update_time
                FROM m_staff_role
                WHERE invalid_flg = false
                ORDER BY update_time DESC,staff_role_code DESC
              """
        return self.select(sql)

    """削除する前に該当データの無効フラグ確認"""
    def selectInvalidFlg(self, param):
        sql =   """
                SELECT
                    invalid_flg
                FROM m_staff_role
                WHERE staff_role_code = %(staff_role_code)s
                """
        return self.selectWithParam(sql, param)[0][0]

    """スタッフ役割マスタレコード論理削除・無効フラグを有効にする"""
    def updateInvalidFlgByStaffRoleCode(self, param):
        sql =   """
                UPDATE m_staff_role
                SET invalid_flg = true
                    , update_user = %(full_name)s
                    , update_time = now()
                WHERE staff_role_code = %(staff_role_code)s
                """
        return self.updateWithParam(sql, param)

    """CSV出力用マンガ情報取得"""
    def selectCsvData(self):
        sql =   """
                SELECT
                    staff_role_code
                  , staff_role_name
                  , create_user
                  , create_time
                  , update_user
                  , update_time
                FROM
                  m_staff_role
                WHERE
                  invalid_flg = false
                ORDER BY
                  staff_role_code ASC
                """
        return self.select(sql)

    """スタッフ役割マスタに存在する最大のスタッフ役割コードを取得する"""
    def selectMaxStaffRoleCode(self):
        sql =   """
                SELECT
                    coalesce(max(staff_role_code), '000000')
                FROM
                    m_staff_role
                """
        return self.select(sql)[0][0]

    """スタッフ役割マスタに同一スタッフ役割コードがあるか検索"""
    def selectSameCode(self, staff_role_code):
        param = {'staff_role_code':staff_role_code}

        sql =   """
                SELECT count(*)
                FROM m_staff_role
                WHERE staff_role_code = %(staff_role_code)s
                """
        return self.selectWithParam(sql, param)[0][0]

    """スタッフ役割マスタに同一スタッフ役割名があるか検索"""
    def selectSameName(self, staff_role_code, staff_role_name):
        param = {
            'staff_role_code':staff_role_code,
            'staff_role_name':staff_role_name
        }
        sql =   """
                SELECT count(*)
                FROM m_staff_role
                WHERE staff_role_name = %(staff_role_name)s
                AND staff_role_code <> %(staff_role_code)s
                AND invalid_flg = false
                """
        return self.selectWithParam(sql, param)[0][0]

    """スタッフ役割マスタ作成"""
    def insertStaffRole(self,entity):
        # スタッフ役割コード重複チェック
        if 0 < self.selectSameCode(entity['staff_role_code']):
            raise DaoMStaffRole.DuplicateStaffRoleCodeException

        # スタッフ役割名重複チェック
        if 0 < self.selectSameName(entity['staff_role_code'],entity['staff_role_name']):
            raise DaoMStaffRole.DuplicateStaffRoleNameException

        sql =   """
                INSERT INTO m_staff_role
                  (
                  staff_role_code
                  , staff_role_name
                  , invalid_flg
                  , create_user
                  , create_time
                  , update_user
                  , update_time
                  )
                VALUES (
                        %(staff_role_code)s
                        , %(staff_role_name)s
                        , false
                        , %(full_name)s
                        , now()
                        , %(full_name)s
                        , now()
                        )
                """
        return self.updateWithParam(sql,entity)

    """スタッフ役割マスタ編集画面表示用"""
    def selectUpdateData(self, param):
        sql =   """
                SELECT
                  staff_role_code
                  , staff_role_name
                FROM
                  m_staff_role
                WHERE
                  invalid_flg = false
                  AND staff_role_code = %(staff_role_code)s
                """
        return self.selectWithParam(sql, param)

    """スタッフ役割マスタ更新"""
    def updateStaffRole(self,entity):
        # スタッフ役割名重複チェック
        if 0 < self.selectSameName(entity['staff_role_code'], entity['staff_role_name']):
            raise DaoMStaffRole.DuplicateStaffRoleNameException

        sql =   """
                UPDATE m_staff_role
                SET
                    staff_role_name = %(staff_role_name)s
                    , update_user = %(full_name)s
                    , update_time = now()
                WHERE staff_role_code = %(staff_role_code)s
                """
        return self.updateWithParam(sql,entity)

    """スタッフ役割コード重複エラー"""
    class DuplicateStaffRoleCodeException(Exception):
        pass

    """スタッフ役割名重複エラー"""
    class DuplicateStaffRoleNameException(Exception):
        pass