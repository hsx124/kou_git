from admin_app.dao.dao_main import DaoMain

class DaoMSakuhinTagCategory(DaoMain):

    def selectSakuhinTagCategoryAll(self):
        # カテゴリマスタの取得
        sql =   """
                SELECT
                sakuhin_tag_category_code
                , sakuhin_tag_category_name
                FROM m_sakuhin_tag_category
                WHERE invalid_flg = false
                """
        return self.select(sql)

    def selectSakuhinTagCategoryList(self):
        sql = """
              SELECT
                  sakuhin_tag_category_code
                , sakuhin_tag_category_name
                , update_user
                , update_time
                FROM m_sakuhin_tag_category
                WHERE invalid_flg = false
                ORDER BY update_time DESC,sakuhin_tag_category_code DESC
              """
        return self.select(sql)

    """削除する前に該当データの無効フラグ確認""" 
    def selectInvalidFlg(self, param):
        sql =   """
                SELECT
                    invalid_flg
                FROM m_sakuhin_tag_category
                WHERE sakuhin_tag_category_code = %(sakuhin_tag_category_code)s
                """
        return self.selectWithParam(sql, param)[0][0]

    """タグカテゴリマスタレコード論理削除・無効フラグを有効にする""" 
    def updateInvalidFlgBySakuhinTagCategoryCode(self, param):
        sql =   """
                UPDATE m_sakuhin_tag_category
                SET invalid_flg = true
                    , update_user = %(full_name)s
                    , update_time = now()
                WHERE sakuhin_tag_category_code = %(sakuhin_tag_category_code)s
                """
        return self.updateWithParam(sql, param)

    """CSV出力用マンガ情報取得"""
    def selectCsvData(self):
        sql =   """
                SELECT
                    sakuhin_tag_category_code
                  , sakuhin_tag_category_name
                  , create_user
                  , create_time
                  , update_user
                  , update_time
                FROM
                  m_sakuhin_tag_category
                WHERE
                  invalid_flg = false
                ORDER BY
                  sakuhin_tag_category_code ASC
                """
        return self.select(sql)

    """タグカテゴリマスタに存在する最大のタグカテゴリコードを取得する"""
    def selectMaxSakuhinTagCategoryCode(self):
        sql =   """
                SELECT
                    coalesce(max(sakuhin_tag_category_code), '00000')
                FROM
                    m_sakuhin_tag_category
                """
        return self.select(sql)[0][0]

    """タグカテゴリマスタに同一タグカテゴリコードがあるか検索"""
    def selectSameCode(self, sakuhin_tag_category_code):
        param = {'sakuhin_tag_category_code':sakuhin_tag_category_code}

        sql =   """
                SELECT count(*)
                FROM m_sakuhin_tag_category
                WHERE sakuhin_tag_category_code = %(sakuhin_tag_category_code)s
                """
        return self.selectWithParam(sql, param)[0][0]

    """タグカテゴリマスタに同一タグカテゴリ名があるか検索"""
    def selectSameName(self, sakuhin_tag_category_code, sakuhin_tag_category_name):
        param = {
            'sakuhin_tag_category_code':sakuhin_tag_category_code,
            'sakuhin_tag_category_name':sakuhin_tag_category_name
        }
        sql =   """
                SELECT count(*)
                FROM m_sakuhin_tag_category
                WHERE sakuhin_tag_category_name = %(sakuhin_tag_category_name)s
                AND sakuhin_tag_category_code <> %(sakuhin_tag_category_code)s
                AND invalid_flg = false
                """
        return self.selectWithParam(sql, param)[0][0]

    """タグカテゴリマスタ作成"""
    def insertSakuhinTagCategory(self,entity):
        # タグカテゴリコード重複チェック
        if 0 < self.selectSameCode(entity['sakuhin_tag_category_code']):
            raise DaoMSakuhinTagCategory.DuplicateSakuhinTagCategoryCodeException

        # タグカテゴリ名重複チェック
        if 0 < self.selectSameName(entity['sakuhin_tag_category_code'],entity['sakuhin_tag_category_name']):
            raise DaoMSakuhinTagCategory.DuplicateSakuhinTagCategoryNameException

        sql =   """
                INSERT INTO m_sakuhin_tag_category
                  (
                  sakuhin_tag_category_code
                  , sakuhin_tag_category_name
                  , invalid_flg
                  , create_user
                  , create_time
                  , update_user
                  , update_time
                  )
                VALUES (
                        %(sakuhin_tag_category_code)s
                        , %(sakuhin_tag_category_name)s
                        , false
                        , %(full_name)s
                        , now()
                        , %(full_name)s
                        , now()
                        )
                """
        return self.updateWithParam(sql,entity)

    """タグカテゴリマスタ編集画面表示用"""
    def selectUpdateData(self, param):
        sql =   """
                SELECT
                  sakuhin_tag_category_code
                  , sakuhin_tag_category_name
                FROM
                  m_sakuhin_tag_category
                WHERE
                  invalid_flg = false
                  AND sakuhin_tag_category_code = %(sakuhin_tag_category_code)s
                """
        return self.selectWithParam(sql, param)

    """タグカテゴリマスタ更新"""
    def updateSakuhinTagCategory(self,entity):
        # タグカテゴリ名重複チェック
        if 0 < self.selectSameName(entity['sakuhin_tag_category_code'], entity['sakuhin_tag_category_name']):
            raise DaoMSakuhinTagCategory.DuplicateSakuhinTagCategoryNameException

        sql =   """
                UPDATE m_sakuhin_tag_category
                SET
                    sakuhin_tag_category_name = %(sakuhin_tag_category_name)s
                    , update_user = %(full_name)s
                    , update_time = now()
                WHERE sakuhin_tag_category_code = %(sakuhin_tag_category_code)s
                """
        return self.updateWithParam(sql,entity)

    """タグカテゴリコード重複エラー"""
    class DuplicateSakuhinTagCategoryCodeException(Exception):
        pass

    """タグカテゴリ名重複エラー"""
    class DuplicateSakuhinTagCategoryNameException(Exception):
        pass