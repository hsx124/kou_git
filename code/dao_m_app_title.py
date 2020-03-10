from admin_app.dao.dao_main import DaoMain

class DaoMAppTitle(DaoMain):
    """アプリタイトル基本マスタを取得""" 
    def selectAll(self):
        sql =   """
                SELECT
                app_title_code
                , app_title_name
                , app_id_ios
                , app_id_android
                , hanbai_company_name
                , service_start_yyyymmdd
                , service_end_yyyymmdd
                , update_user
                , update_time 
                FROM m_app_title 
                WHERE invalid_flg = false 
                ORDER BY update_time DESC
                , app_title_code
                """
        return self.select(sql)

    """削除する前に該当データの無効フラグ確認""" 
    def selectInvalidFlg(self, param):
        sql =   """
                SELECT
                invalid_flg
                FROM m_app_title
                WHERE app_title_code = %(app_code)s
                """
        return self.selectWithParam(sql, param)[0][0]

    """アプリタイトル基本マスタレコード論理削除・無効フラグを有効にする""" 
    def updateInvalidFlgByAppCode(self, param):
        sql =   """
                UPDATE m_app_title
                SET invalid_flg = true
                    , update_user = %(full_name)s
                    , update_time = now()
                WHERE app_title_code = %(title_code)s
                """
        return self.updateWithParam(sql, param)
    
    """CSV出力用情報取得"""
    def selectCsvData(self):
        sql =   """
                SELECT
                  app_title_code
                  , app_title_name
                  , app_id_android
                  , app_id_ios
                  , hanbai_company_name
                  , service_start_yyyymmdd
                  , service_end_yyyymmdd
                  , create_user
                  , create_time
                  , update_user
                  , update_time 
                FROM m_app_title 
                WHERE invalid_flg = false 
                ORDER BY app_title_code ASC
                """
        return self.select(sql)

    """アプリタイトルコード重複エラー"""
    class DuplicateAppCodeException(Exception):
        pass

    """アプリタイトル名重複エラー"""
    class DuplicateAppNameException(Exception):
        pass
    
    """アプリID_iOS重複エラー"""
    class DuplicateAppIosIdException(Exception):
        pass

    """アプリID_android重複エラー"""
    class DuplicateAppAndroidIdException(Exception):
        pass

    """アプリタイトル基本マスタに存在する最大のアプリタイトルコードを取得する"""
    def selectMaxAppCode(self):
        sql =   """
                SELECT coalesce(max(app_title_code),'00000000')
                FROM m_app_title
                """
        return self.select(sql)[0][0]

    """アプリタイトル基本マスタに同一アプリタイトルコードを検索"""
    def selectSameCode(self, app_code):
        param = {'app_code':app_code}

        sql =   """
                SELECT count(*)
                FROM m_app_title
                WHERE app_title_code = %(app_code)s
                """
        return self.selectWithParam(sql, param)[0][0]

    """アプリタイトル基本マスタに同一アプリタイトル名を検索"""
    def selectSameName(self, app_code, app_name):
        param = {
            'app_code':app_code,
            'app_name':app_name
        }
        sql =   """
                SELECT count(*)
                FROM m_app_title
                WHERE app_title_name = %(app_name)s
                AND app_title_code <> %(app_code)s
                AND invalid_flg = false
                """
        return self.selectWithParam(sql, param)[0][0]

    """アプリタイトル基本マスタに同一アプリID_iOS名を検索"""
    def selectSameIosId(self, app_code, app_id_ios):
        param = {
            'app_code':app_code,
            'app_id_ios':app_id_ios
        }
        sql =   """
                SELECT count(*)
                FROM m_app_title
                WHERE app_id_ios = %(app_id_ios)s
                AND app_title_code <> %(app_code)s
                AND invalid_flg = false
                """
        return self.selectWithParam(sql, param)[0][0]

    """アプリタイトル基本マスタに同一アプリID_android名を検索"""
    def selectSameAndroidId(self, app_code, app_id_android):
        param = {
            'app_code':app_code,
            'app_id_android':app_id_android
        }
        sql =   """
                SELECT count(*)
                FROM m_app_title
                WHERE app_id_android = %(app_id_android)s
                AND app_title_code <> %(app_code)s
                AND invalid_flg = false
                """
        return self.selectWithParam(sql, param)[0][0]

    """新規アプリタイトル基本マスタ作成"""
    def insert(self,entity):
        # アプリタイトルコード重複チェック
        if 0 < self.selectSameCode(entity['app_code']):
            raise DaoMAppTitle.DuplicateAppCodeException

        # アプリタイトル名重複チェック
        if 0 < self.selectSameName(entity['app_code'],entity['app_name']):
            raise DaoMAppTitle.DuplicateAppNameException
        if entity['app_id_ios'] !="":
            # アプリID_iOS重複チェック
            if 0 < self.selectSameIosId(entity['app_code'],entity['app_id_ios']):
                raise DaoMAppTitle.DuplicateAppIosIdException
        if entity['app_id_android'] !="":
            # アプリID_android重複チェック
            if 0 < self.selectSameAndroidId(entity['app_code'],entity['app_id_android']):
                
                raise DaoMAppTitle.DuplicateAppAndroidIdException

        sql =   """
                INSERT INTO m_app_title
                    (
                    app_title_code
                    , app_title_name
                    , app_id_ios
                    , app_id_android
                    , hanbai_company_name
                    , service_start_yyyymmdd
                    , service_end_yyyymmdd
                    , auto_collect_flg
                    , invalid_flg
                    , create_user
                    , create_time
                    , update_user
                    , update_time
                    )
                VALUES (
                    %(app_code)s
                    , %(app_name)s
                    , %(app_id_ios)s
                    , %(app_id_android)s
                    , %(hanbai_company_name)s
                    , %(service_start_yyyymmdd)s
                    , %(service_end_yyyymmdd)s
                    , true
                    , false
                    , %(full_name)s
                    , now()
                    , %(full_name)s 
                    , now())
                """
        return self.updateWithParam(sql,entity)
    
    """アプリタイトル基本マスタ編集画面表示用"""
    def selectUpdateData(self, param):
        sql =   """
                SELECT
                    app_title_code
                    , app_title_name
                    , app_id_ios
                    , app_id_android
                    , hanbai_company_name
                    , service_start_yyyymmdd
                    , service_end_yyyymmdd
                FROM
                    m_app_title
                WHERE
                    invalid_flg = false 
                    AND app_title_code = %(app_code)s

                """
        return self.selectWithParam(sql, param)

    """アプリタイトル基本マスタ更新"""
    def update(self,entity):
        # アプリタイトル名重複チェック
        if 0 < self.selectSameName(entity['app_code'],entity['app_name']):
          raise DaoMAppTitle.DuplicateAppNameException

        if entity['app_id_ios'] !="":
            # アプリID_iOS重複チェック
            if 0 < self.selectSameIosId(entity['app_code'],entity['app_id_ios']):
                raise DaoMAppTitle.DuplicateAppIosIdException
        if entity['app_id_android'] !="":
            # アプリID_android重複チェック
            if 0 < self.selectSameAndroidId(entity['app_code'],entity['app_id_android']):
                raise DaoMAppTitle.DuplicateAppAndroidIdException
                
        sql =   """
                UPDATE m_app_title 
                SET
                    app_title_name = %(app_name)s
                    , app_id_ios = %(app_id_ios)s
                    , app_id_android = %(app_id_android)s
                    , hanbai_company_name = %(hanbai_company_name)s
                    , service_start_yyyymmdd = %(service_start_yyyymmdd)s
                    , service_end_yyyymmdd = %(service_end_yyyymmdd)s
                    , update_user = %(full_name)s
                    , update_time = now() 
                WHERE
                    app_title_code = %(app_code)s

                """
        return self.updateWithParam(sql,entity)