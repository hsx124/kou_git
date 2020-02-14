from admin_app.dao.dao_main import DaoMain

class DaoMStaff(DaoMain):

    def selectStaffByBook(self):
        sql =   """
                SELECT
                    staff_code
                    ,staff_name
                FROM
                    m_staff
                WHERE
                    invalid_flg = false
                ORDER BY staff_name ASC
                """
        return self.select(sql)

    def selectStaffKeyword(self,keyword):
        param = {'keyword':'%' + keyword + '%'}

        sql =   """
                SELECT
                    staff_code
                    ,staff_name
                FROM
                    m_staff
                WHERE
                    invalid_flg = false
                    AND staff_name LIKE %(keyword)s
                """
        return self.selectWithParam(sql,param)

    def selectStaffList(self):
        sql = """
              SELECT
                  staff_code
                , staff_name
                , past_sakuhin
                , remarks
                , update_user
                , update_time
                FROM m_staff
                WHERE invalid_flg = false
                ORDER BY update_time DESC,staff_code DESC
              """
        return self.select(sql)

    """削除する前に該当データの無効フラグ確認""" 
    def selectInvalidFlg(self, param):
        sql =   """
                SELECT
                    invalid_flg
                FROM m_staff
                WHERE staff_code = %(staff_code)s
                """
        return self.selectWithParam(sql, param)[0][0]

    """スタッフマスタレコード論理削除・無効フラグを有効にする""" 
    def updateInvalidFlgByStaffCode(self, param):
        sql =   """
                UPDATE m_staff
                SET invalid_flg = true
                    , update_user = %(full_name)s
                    , update_time = now()
                WHERE staff_code = %(staff_code)s
                """
        return self.updateWithParam(sql, param)

    """CSV出力用マンガ情報取得"""
    def selectCsvData(self):
        sql =   """
                SELECT
                    staff_code
                  , staff_name
                  , past_sakuhin
                  , remarks
                  , create_user
                  , create_time
                  , update_user
                  , update_time
                FROM
                  m_staff
                WHERE
                  invalid_flg = false
                ORDER BY
                  staff_code ASC
                """
        return self.select(sql)
    
    """スタッフマスタに存在する最大のスタッフコードを取得する"""
    def selectMaxStaffCode(self):
        sql =   """
                SELECT
                    coalesce(max(staff_code), '00000')
                FROM
                    m_staff
                """
        return self.select(sql)[0][0]

    """スタッフマスタに同一スタッフコードがあるか検索"""
    def selectSameCode(self, staff_code):
        param = {'staff_code':staff_code}

        sql =   """
                SELECT count(*)
                FROM m_staff
                WHERE staff_code = %(staff_code)s
                """
        return self.selectWithParam(sql, param)[0][0]

    """スタッフマスタに同一スタッフ名があるか検索"""
    def selectSameName(self, staff_code, staff_name):
        param = {
            'staff_code':staff_code,
            'staff_name':staff_name
        }
        sql =   """
                SELECT count(*)
                FROM m_staff
                WHERE staff_name = %(staff_name)s
                AND staff_code <> %(staff_code)s
                AND invalid_flg = false
                """
        return self.selectWithParam(sql, param)[0][0]

    """スタッフマスタ作成"""
    def insertStaff(self,entity):
        # スタッフコード重複チェック
        if 0 < self.selectSameCode(entity['staff_code']):
            raise DaoMStaff.DuplicateStaffCodeException

        # スタッフ名重複チェック
        if 0 < self.selectSameName(entity['staff_code'],entity['staff_name']):
            raise DaoMStaff.DuplicateStaffNameException

        sql =   """
                INSERT INTO m_staff
                  (
                  staff_code
                  , staff_name
                  , past_sakuhin
                  , remarks
                  , invalid_flg
                  , create_user
                  , create_time
                  , update_user
                  , update_time
                  )
                VALUES (
                        %(staff_code)s
                        , %(staff_name)s
                        , %(past_sakuhin)s
                        , %(remarks)s
                        , false
                        , %(full_name)s
                        , now()
                        , %(full_name)s
                        , now()
                        )
                """
        return self.updateWithParam(sql,entity)

    """スタッフマスタ編集画面表示用"""
    def selectUpdateData(self, param):
        sql =   """
                SELECT
                  staff_code
                  , staff_name
                  , past_sakuhin
                  , remarks
                FROM
                  m_staff
                WHERE
                  invalid_flg = false
                  AND staff_code = %(staff_code)s
                """
        return self.selectWithParam(sql, param)

    """スタッフマスタ更新"""
    def updateStaff(self,entity):
        # スタッフ名重複チェック
        if 0 < self.selectSameName(entity['staff_code'], entity['staff_name']):
            raise DaoMStaff.DuplicateStaffNameException

        sql =   """
                UPDATE m_staff
                SET
                    staff_name = %(staff_name)s
                    , past_sakuhin = %(past_sakuhin)s
                    , remarks = %(remarks)s
                    , update_user = %(full_name)s
                    , update_time = now()
                WHERE staff_code = %(staff_code)s
                """
        return self.updateWithParam(sql,entity)

    """スタッフコード重複エラー"""
    class DuplicateStaffCodeException(Exception):
        pass

    """スタッフ名重複エラー"""
    class DuplicateStaffNameException(Exception):
        pass