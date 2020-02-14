from admin_app.dao.dao_main import DaoMain

class DaoMPublisher(DaoMain):

    """出版社マスタ全件取得"""
    def selectAll(self):
        sql =   """
                SELECT
                    publisher_code
                    , publisher_name
                    , update_user
                    , update_time
                FROM m_publisher
                WHERE invalid_flg = false
                ORDER BY
                    update_time DESC
                    , publisher_code ASC
                """
        return self.select(sql)

    """削除する前に該当データの無効フラグ確認""" 
    def selectInvalidFlg(self, param):
        sql =   """
                SELECT
                    invalid_flg
                FROM m_publisher
                WHERE publisher_code = %(publisher_code)s
                """
        return self.selectWithParam(sql, param)[0][0]

    """出版社マスタレコード論理削除・無効フラグを有効にする""" 
    def updateInvalidFlgByPublisherCode(self, param):
        sql =   """
                UPDATE m_publisher
                SET invalid_flg = true
                    , update_user = %(full_name)s
                    , update_time = now()
                WHERE publisher_code = %(publisher_code)s
                """
        return self.updateWithParam(sql, param)

    """CSV出力用出版社情報取得"""
    def selectCsvData(self):
        sql =   """
                SELECT
                    publisher_code
                    , publisher_name
                    , create_user
                    , create_time
                    , update_user
                    , update_time
                FROM m_publisher
                WHERE invalid_flg = false
                ORDER BY publisher_code ASC
                """
        return self.select(sql)

    """出版社に存在する最大の出版社コードを取得する"""
    def selectMaxPublisherCode(self):
        sql =   """
                SELECT coalesce(max(publisher_code),'00000')
                FROM m_publisher 
                """
        return self.select(sql)[0][0]

    """出版社に同一出版社コードを検索"""
    def selectSameCode(self, publisher_code):
        param = {'publisher_code':publisher_code}

        sql =   """
                SELECT count(*)
                FROM m_publisher
                WHERE publisher_code = %(publisher_code)s
                """
        return self.selectWithParam(sql, param)[0][0]

    """出版社に同一出版社名を検索"""
    def selectSameName(self, publisher_code, publisher_name):
        param = {
            'publisher_code':publisher_code,
            'publisher_name':publisher_name
        }
        sql =   """
                SELECT count(*)
                FROM m_publisher
                WHERE publisher_name = %(publisher_name)s
                AND publisher_code <> %(publisher_code)s
                AND invalid_flg = false
                """
        return self.selectWithParam(sql, param)[0][0]

    """新規出版社マスタ作成"""
    def insert(self,entity):
        # 出版社コード重複チェック
        if 0 < self.selectSameCode(entity['publisher_code']):
            raise DaoMPublisher.DuplicatePublisherCodeException

        # 出版社名重複チェック
        if 0 < self.selectSameName(entity['publisher_code'],entity['publisher_name']):
            raise DaoMPublisher.DuplicatePublisherNameException
        
        sql =   """
                INSERT INTO m_publisher
                    (
                    publisher_code
                    , publisher_name
                    , invalid_flg
                    , create_user
                    , create_time
                    , update_user
                    , update_time
                    )
                VALUES (%(publisher_code)s, %(publisher_name)s, false, %(full_name)s , now(), %(full_name)s , now())
                """
        return self.updateWithParam(sql,entity)

    """出版社マスタ編集画面表示用"""
    def selectUpdateData(self, param):
        sql =   """
                SELECT
                    publisher_code
                    , publisher_name
                FROM m_publisher
                WHERE invalid_flg = false
                AND publisher_code = %(publisher_code)s
                """
        return self.selectWithParam(sql, param)

    """出版社マスタ更新"""
    def update(self,entity):
        # 出版社名重複チェック
        if 0 < self.selectSameName(entity['publisher_code'], entity['publisher_name']):
          raise DaoMPublisher.DuplicatePublisherNameException

        sql =   """
                UPDATE m_publisher
                SET
                    publisher_name = %(publisher_name)s
                    , update_user = %(full_name)s
                    , update_time = now()
                WHERE publisher_code = %(publisher_code)s
                """
        return self.updateWithParam(sql,entity)

    """出版社コード重複エラー"""
    class DuplicatePublisherCodeException(Exception):
        pass

    """出版社名重複エラー"""
    class DuplicatePublisherNameException(Exception):
        pass

    def selectPublisherByBook(self):
        sql =   """
                SELECT
                    publisher_code
                    ,publisher_name
                FROM
                    m_publisher
                WHERE
                    invalid_flg = false
                """
        return self.select(sql)

    def selectPublisherKeyword(self,keyword):
        param = {'keyword':'%' + keyword + '%'}

        sql =   """
                SELECT
                    publisher_code
                    ,publisher_name
                FROM
                    m_publisher
                WHERE
                    invalid_flg = false
                    AND publisher_name LIKE %(keyword)s
                """
        return self.selectWithParam(sql,param)