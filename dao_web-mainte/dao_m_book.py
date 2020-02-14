from admin_app.dao.dao_main import DaoMain

class DaoMBook(DaoMain):

    def selectBookMasterByIpCode(self, ip_code):
        '''
        書籍マスタ情報取得（グリッド表示用）
        '''

        param = {'ip_code' : ip_code}
        sql =   """
                SELECT
                  m_book.ip_code
                , m_ip.ip_name
                , m_book.book_issue_date
                , m_book.book_name
                , m_book.isbn
                , m_book.update_user
                , m_book.update_date
                FROM m_book
                INNER JOIN m_ip ON (
                    m_book.ip_code = m_ip.ip_code 
                    AND m_ip.is_invalid = false
                )
                WHERE m_book.is_invalid = false
                AND m_book.ip_code = %(ip_code)s
                ORDER BY m_book.book_issue_date DESC
                """
        return self.selectWithParam(sql, param)

    def selectBookMasterforCSV(self):
        '''
        書籍マスタ情報取得(CSVダウンロード全件用)
        '''
        sql =   """
                SELECT
                  m_book.ip_code
                , m_book.book_name
                , m_book.isbn
                , m_book.book_issue_date
                , m_book.create_user
                , m_book.create_date
                , m_book.update_user
                , m_book.update_date 
                FROM m_book
                INNER JOIN m_ip ON (
                    m_book.ip_code = m_ip.ip_code 
                    AND m_ip.is_invalid = false
                )
                WHERE m_book.is_invalid = false 
                ORDER BY
                  m_book.ip_code ASC
                , m_book.book_issue_date DESC
                """
        return self.select(sql)

    def selectBookMasterforCSVByIpCode(self, ip_code):
        '''
        書籍マスタ情報取得(CSVダウンロードIP毎用)
        '''

        param = {'ip_code' : ip_code}
        sql =   """
                SELECT
                  m_book.ip_code
                , m_book.book_name
                , m_book.isbn
                , m_book.book_issue_date
                , m_book.create_user
                , m_book.create_date
                , m_book.update_user
                , m_book.update_date
                FROM m_book
                INNER JOIN m_ip ON (
                    m_book.ip_code = m_ip.ip_code 
                    AND m_ip.is_invalid = false
                )
                WHERE m_book.is_invalid = false
                AND m_book.ip_code = %(ip_code)s
                ORDER BY 
                  m_book.ip_code ASC
                , m_book.book_issue_date DESC
                """
        return self.selectWithParam(sql, param)

    def updateIsInvalidByIsbn(self, isbn, full_name):
        '''
        書籍マスタレコード論理削除
        無効フラグを有効にする
        ''' 
        param = {
                    'isbn': isbn,
                    'full_name': full_name
                 }
        sql =   """
                UPDATE m_book
                SET is_invalid = true
                , update_user = %(full_name)s
                , update_date = now()
                WHERE m_book.isbn = %(isbn)s
                """

        return self.updateWithParam(sql, param)

    def insertMBook(self, entity):
        '''
        新規書籍マスタ作成
        '''
        # isbnコード重複チェック
        if (0 < self.selectCountISBN(entity['isbn'])):
            raise DaoMBook.DuplicateIsbnException

        sql =   """
                INSERT INTO m_book
                (
                  ip_code
                , book_name
                , isbn
                , book_issue_date
                , is_invalid
                , create_user
                , create_date
                , update_user
                , update_date
                )
                VALUES (
                    %(ip_code)s,
                    %(book_name)s, 
                    %(isbn)s, 
                    %(book_issue_date)s, 
                    false, 
                    %(full_name)s, 
                    now(), 
                    %(full_name)s, 
                    now()
                    )
                """

        return self.updateWithParam(sql,entity)

    def selectCountISBN(self, isbn):
        '''
        ISBN重複チェック
        '''
        param = {'isbn': isbn}
        sql =   """
                SELECT count(*)
                FROM m_book
                WHERE isbn = %(isbn)s
                AND is_invalid = false
                """

        return self.selectWithParam(sql,param)[0][0]


    def selectBookByIpcodeIsbn(self, ip_code, isbn):

        param = {
          'ip_code' : ip_code,
          'isbn' : isbn
        }
        '''
        書籍マスタ編集画面表示
        '''
        sql =   """
                SELECT 
                  m_book.ip_code
                , m_ip.ip_name
                , m_book.book_name
                , m_book.isbn
                , m_book.book_issue_date
                FROM m_book
                INNER JOIN m_ip ON (
                    m_book.ip_code = m_ip.ip_code 
                    AND m_ip.is_invalid = false
                )
                WHERE m_ip.ip_code  = %(ip_code)s
                AND isbn = %(isbn)s
                AND m_book.is_invalid = false
                """

        return self.selectWithParam(sql, param)

    def updateMBook(self, entity):
        '''
        書籍マスタレコード編集
        '''

        # isbnコード重複チェック(編集時のみ)
        if (entity['isbn'] != entity['get_isbn']):
            if (0 < self.selectCountISBN(entity['isbn'])):
                raise DaoMBook.DuplicateIsbnException

        sql =   """
                UPDATE m_book
                SET
                  book_name  = %(book_name)s
                , isbn  = %(isbn)s
                , book_issue_date  = %(book_issue_date)s
                , update_user = %(full_name)s
                , update_date = now()
                WHERE ip_code  = %(get_ipcode)s
                AND isbn = %(get_isbn)s
                AND is_invalid = false
                """

        return self.updateWithParam(sql, entity)


    class DuplicateIsbnException(Exception):
        """
        ISBN重複エラー
        """

        pass