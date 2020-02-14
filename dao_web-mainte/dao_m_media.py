from admin_app.dao.dao_main import DaoMain

class DaoMMedia(DaoMain):

    """掲載媒体マスタ全件取得"""
    def selectAll(self):
        sql =   """
                SELECT
                    media_code
                    , media_name
                    , show_flg
                    , priority
                    , update_user
                    , update_time
                FROM m_media
                WHERE invalid_flg = false
                ORDER BY 
                    update_time DESC
                    , media_code ASC
                """
        return self.select(sql)

    """削除する前に該当データの無効フラグ確認""" 
    def selectInvalidFlg(self, param):
        sql =   """
                SELECT
                    invalid_flg
                FROM m_media
                WHERE media_code = %(media_code)s
                """
        return self.selectWithParam(sql, param)[0][0]

    """掲載媒体マスタレコード論理削除・無効フラグを有効にする""" 
    def updateInvalidFlgByMediaCode(self, param):
        sql =   """
                UPDATE m_media
                SET invalid_flg = true
                    , update_user = %(full_name)s
                    , update_time = now()
                WHERE media_code = %(media_code)s
                """
        return self.updateWithParam(sql, param)

    """CSV出力用掲載媒体情報取得"""
    def selectCsvData(self):
        sql =   """
                SELECT
                    media_code
                    , media_name
                    , show_flg
                    , priority
                    , create_user
                    , create_time
                    , update_user
                    , update_time
                FROM m_media
                WHERE invalid_flg = false
                ORDER BY media_code ASC
                """
        return self.select(sql)

    """掲載媒体に存在する最大の掲載媒体コードを取得する"""
    def selectMaxMediaCode(self):
        sql =   """
                SELECT coalesce(max(media_code),'00000')
                FROM m_media 
                """
        return self.select(sql)[0][0]

    """掲載媒体に同一掲載媒体コードを検索"""
    def selectSameCode(self, media_code):
        param = {'media_code':media_code}

        sql =   """
                SELECT count(*)
                FROM m_media
                WHERE media_code = %(media_code)s
                """
        return self.selectWithParam(sql, param)[0][0]

    """掲載媒体に同一掲載媒体名を検索"""
    def selectSameName(self, media_code, media_name):
        param = {
            'media_code':media_code,
            'media_name':media_name
        }
        sql =   """
                SELECT count(*)
                FROM m_media
                WHERE media_name = %(media_name)s
                AND media_code <> %(media_code)s
                AND invalid_flg = false
                """
        return self.selectWithParam(sql, param)[0][0]

    """新規掲載媒体マスタ作成"""
    def insert(self,entity):
        # 掲載媒体コード重複チェック
        if 0 < self.selectSameCode(entity['media_code']):
            raise DaoMMedia.DuplicateMediaCodeException

        # 掲載媒体名重複チェック
        if 0 < self.selectSameName(entity['media_code'],entity['media_name']):
            raise DaoMMedia.DuplicateMediaNameException
        
        sql =   """
                INSERT INTO m_media
                    (
                    media_code
                    , media_name
                    , show_flg
                    , priority
                    , invalid_flg
                    , create_user
                    , create_time
                    , update_user
                    , update_time
                    )
                VALUES (%(media_code)s, %(media_name)s, %(show_flg)s, %(priority)s, false, %(full_name)s, now(), %(full_name)s , now())
                """
        return self.updateWithParam(sql,entity)

    """掲載媒体マスタ編集画面表示用"""
    def selectUpdateData(self, param):
        sql =   """
                SELECT
                    media_code
                    , media_name
                    , show_flg
                    , priority
                FROM m_media
                WHERE invalid_flg = false
                AND media_code = %(media_code)s
                """
        return self.selectWithParam(sql, param)

    """掲載媒体マスタ更新"""
    def update(self,entity):
        # 掲載媒体名重複チェック
        if 0 < self.selectSameName(entity['media_code'], entity['media_name']):
          raise DaoMMedia.DuplicateMediaNameException

        sql =   """
                UPDATE m_media
                SET
                    media_name = %(media_name)s
                    , show_flg = %(show_flg)s
                    , priority = %(priority)s
                    , update_user = %(full_name)s
                    , update_time = now()
                WHERE media_code = %(media_code)s
                """
        return self.updateWithParam(sql,entity)

    """掲載媒体コード重複エラー"""
    class DuplicateMediaCodeException(Exception):
        pass

    """掲載媒体名重複エラー"""
    class DuplicateMediaNameException(Exception):
        pass

    def selectMediaByBook(self):
        sql =   """
                SELECT
                    media_code
                    ,media_name
                FROM
                    m_media
                WHERE
                    invalid_flg = false
                """
        return self.select(sql)

    def selectMediaKeyword(self,keyword):
        param = {'keyword':'%' + keyword + '%'}

        sql =   """
                SELECT
                    media_code
                    ,media_name
                FROM
                    m_media
                WHERE
                    invalid_flg = false
                    AND media_name LIKE %(keyword)s
                """
        return self.selectWithParam(sql,param)