from admin_app.dao.dao_main import DaoMain

class DaoMSakuhinTag(DaoMain):

    def selectSakuhinTagAll(self):
        """
        タグマスタ全件取得
        """
        sql =   """
                SELECT
                  m_sakuhin_tag.sakuhin_tag_code
                  , m_sakuhin_tag_category.sakuhin_tag_category_name
                  , m_sakuhin_tag.sakuhin_tag_name
                  , m_sakuhin_tag.update_user
                  , to_char(m_sakuhin_tag.update_time, 'yyyy/mm/dd') AS update_time 
                FROM m_sakuhin_tag
                INNER JOIN m_sakuhin_tag_category 
                  ON ( 
                    m_sakuhin_tag.sakuhin_tag_category_code = m_sakuhin_tag_category.sakuhin_tag_category_code
                    AND m_sakuhin_tag_category.invalid_flg = false 
                  )  
                WHERE m_sakuhin_tag.invalid_flg = false 
                ORDER BY 
                  update_time DESC
                  , sakuhin_tag_code DESC

                """
        return self.select(sql)

    def selectInvalidFlg(self, param):
        """
        削除する前に該当データの無効フラグ確認
        """
        sql =   """
                SELECT invalid_flg
                FROM m_sakuhin_tag
                WHERE sakuhin_tag_code = %(tag_code)s
                """
        return self.selectWithParam(sql, param)[0][0]
    
    def selectSakuhinTagCategoryByCategoryCode(self,param):
        """
        カテゴリマスタの取得
        """
        sql =   """
                SELECT
                m_sakuhin_tag.sakuhin_tag_code
                , m_sakuhin_tag_category.sakuhin_tag_category_name
                , m_sakuhin_tag.sakuhin_tag_name
                , m_sakuhin_tag.update_user
                , to_char(m_sakuhin_tag.update_time,'yyyy/mm/dd') AS update_time
                FROM m_sakuhin_tag
                INNER JOIN m_sakuhin_tag_category 
                ON ( 
                  m_sakuhin_tag.sakuhin_tag_category_code = m_sakuhin_tag_category.sakuhin_tag_category_code
                  AND m_sakuhin_tag_category.invalid_flg = false 
                )   
                WHERE 
                  m_sakuhin_tag.invalid_flg = false
                AND m_sakuhin_tag.sakuhin_tag_category_code  = %(category_code)s
                ORDER BY sakuhin_tag_code
                """
        return self.selectWithParam(sql,param)

    def updateInvalidFlgByTagCode(self, param):
        """
        タグマスタレコード論理削除・無効フラグを有効にする
        """
        sql =   """
                UPDATE m_sakuhin_tag
                SET invalid_flg = true
                    , update_user = %(full_name)s
                    , update_time = now()
                WHERE sakuhin_tag_code = %(tag_code)s
                """
        return self.updateWithParam(sql, param)

    def selectTagMasterForCSV(self):
        """
        CSV出力用タグマスタ全件取得
        """
        sql =   """
                SELECT
                  m_sakuhin_tag.sakuhin_tag_code
                  , m_sakuhin_tag_category.sakuhin_tag_category_name
                  , m_sakuhin_tag.sakuhin_tag_name
                  , m_sakuhin_tag.create_user
                  , m_sakuhin_tag.create_time
                  , m_sakuhin_tag.update_user
                  , m_sakuhin_tag.update_time 
                FROM m_sakuhin_tag
                    INNER JOIN m_sakuhin_tag_category 
                    ON ( 
                      m_sakuhin_tag.sakuhin_tag_category_code = m_sakuhin_tag_category.sakuhin_tag_category_code
                      AND m_sakuhin_tag_category.invalid_flg = false 
                    )   
                WHERE m_sakuhin_tag.invalid_flg = false 
                ORDER BY sakuhin_tag_code ASC
                """
        return self.select(sql)

    """タグに存在する最大のタグコードを取得する"""
    def selectMaxTagCode(self):
        sql =   """
                SELECT coalesce(max(sakuhin_tag_code),'0000000000')
                FROM m_sakuhin_tag 
                """
        return self.select(sql)[0][0]

    """タグに同一タグコードを検索"""
    def selectSameCode(self, sakuhin_tag_code):
        param = {'sakuhin_tag_code':sakuhin_tag_code}

        sql =   """
                SELECT count(*)
                FROM m_sakuhin_tag
                WHERE sakuhin_tag_code = %(sakuhin_tag_code)s
                """
        return self.selectWithParam(sql, param)[0][0]

    """タグに同一タグ名を検索"""
    def selectSameName(self, sakuhin_tag_code, sakuhin_tag_name):
        param = {
            'sakuhin_tag_code':sakuhin_tag_code,
            'sakuhin_tag_name':sakuhin_tag_name
        }
        sql =   """
                SELECT count(*)
                FROM m_sakuhin_tag
                WHERE sakuhin_tag_name = %(sakuhin_tag_name)s
                AND sakuhin_tag_code <> %(sakuhin_tag_code)s
                AND invalid_flg = false
                """
        return self.selectWithParam(sql, param)[0][0]

    """新規タグマスタ作成"""
    def insert(self,entity):
        # タグコード重複チェック
        if 0 < self.selectSameCode(entity['tag_code']):
            raise DaoMSakuhinTag.DuplicateTagCodeException

        # タグ名重複チェック
        if 0 < self.selectSameName(entity['tag_code'],entity['tag_name']):
            raise DaoMSakuhinTag.DuplicateTagNameException
        
        sql =   """
                INSERT INTO m_sakuhin_tag
                    (
                    sakuhin_tag_code
                    , sakuhin_tag_name
                    , sakuhin_tag_category_code
                    , invalid_flg
                    , create_user
                    , create_time
                    , update_user
                    , update_time
                    )
                VALUES (%(tag_code)s, %(tag_name)s, %(tag_category_code)s, false, %(full_name)s, now(), %(full_name)s , now())
                """
        return self.updateWithParam(sql,entity)

    """タグマスタ編集画面表示用"""
    def selectUpdateData(self, param):
        sql =   """
                SELECT
                    sakuhin_tag_code
                    , sakuhin_tag_name
                    , sakuhin_tag_category_code
                FROM m_sakuhin_tag
                WHERE invalid_flg = false
                AND sakuhin_tag_code = %(tag_code)s
                """
        return self.selectWithParam(sql, param)

    """タグマスタ更新"""
    def update(self,entity):
        # タグ名重複チェック
        if 0 < self.selectSameName(entity['tag_code'], entity['tag_name']):
          raise DaoMSakuhinTag.DuplicateTagNameException

        sql =   """
                UPDATE m_sakuhin_tag
                SET
                    sakuhin_tag_name = %(tag_name)s
                    , sakuhin_tag_category_code = %(tag_category_code)s
                    , update_user = %(full_name)s
                    , update_time = now()
                WHERE sakuhin_tag_code = %(tag_code)s
                """
        return self.updateWithParam(sql,entity)

    """タグコード重複エラー"""
    class DuplicateTagCodeException(Exception):
        pass

    """タグ名重複エラー"""
    class DuplicateTagNameException(Exception):
      pass

