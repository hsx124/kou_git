from admin_app.dao.dao_main import DaoMain

class DaoMMobileApp(DaoMain):

    def selectAppMasterByIpCode(self, ip_code):
        '''
        アプリマスタ情報取得（グリッド表示用）
        '''

        param = {'ip_code' : ip_code}
        sql =   """
                SELECT
                  m_ip.ip_code
                , m_mobile_app.app_name
                , m_mobile_app.app_id_ios
                , m_mobile_app.app_id_android
                , m_mobile_app.distributor_name
                , m_mobile_app.service_start_date
                , m_mobile_app.service_end_date
                , m_mobile_app.update_user
                , m_mobile_app.update_date
                FROM m_mobile_app
                INNER JOIN m_ip ON (
                    m_mobile_app.ip_code = m_ip.ip_code 
                    AND m_ip.is_invalid = false
                )
                WHERE m_mobile_app.is_invalid = false
                AND m_mobile_app.ip_code = %(ip_code)s
                ORDER BY m_mobile_app.app_name ASC
                """

        return self.selectWithParam(sql, param)

    def selectAppMasterforCSV(self):
        '''
        アプリマスタ情報取得(CSVダウンロード全件用)
        '''

        sql =   """
                SELECT
                  m_mobile_app.ip_code
                , m_mobile_app.app_name
                , m_mobile_app.app_id_ios
                , m_mobile_app.app_id_android
                , m_mobile_app.distributor_name
                , m_mobile_app.service_start_date
                , m_mobile_app.service_end_date
                , m_mobile_app.create_user
                , m_mobile_app.create_date
                , m_mobile_app.update_user
                , m_mobile_app.update_date
                FROM m_mobile_app
                INNER JOIN m_ip ON (
                    m_mobile_app.ip_code = m_ip.ip_code 
                    AND m_ip.is_invalid = false
                )
                WHERE m_mobile_app.is_invalid = false
                ORDER BY
                  m_mobile_app.ip_code ASC
                , m_mobile_app.app_name ASC
                """

        return self.select(sql)

    def selectAppMasterforCSVByIpCode(self,ip_code):
        '''
        アプリマスタ情報取得(CSVダウンロードIP毎用)
        '''

        param = {'ip_code' : ip_code}
        sql =   """
                SELECT
                  m_mobile_app.ip_code
                , m_mobile_app.app_name
                , m_mobile_app.app_id_ios
                , m_mobile_app.app_id_android
                , m_mobile_app.distributor_name
                , m_mobile_app.service_start_date
                , m_mobile_app.service_end_date
                , m_mobile_app.create_user
                , m_mobile_app.create_date
                , m_mobile_app.update_user
                , m_mobile_app.update_date
                FROM m_mobile_app
                INNER JOIN m_ip ON (
                    m_mobile_app.ip_code = m_ip.ip_code 
                    AND m_ip.is_invalid = false
                )
                WHERE m_mobile_app.is_invalid = false
                AND m_mobile_app.ip_code = %(ip_code)s
                ORDER BY
                  m_mobile_app.ip_code ASC
                , m_mobile_app.app_name ASC
                """

        return self.selectWithParam(sql, param)

    def updateIsInvalidByAppName(self, app_name, full_name):
        '''
        アプリマスタレコード論理削除
        無効フラグを有効にする
        ''' 

        param = {'app_name' : app_name,
                 'full_name' : full_name
        }
        sql =   """
                UPDATE m_mobile_app
                SET is_invalid = true
                , update_user = %(full_name)s
                , update_date = now()
                WHERE m_mobile_app.app_name = %(app_name)s
                """

        return self.updateWithParam(sql, param)

    def insertMMobileApp(self, entity):
        '''
        新規アプリマスタレコード作成
        '''

        # アプリ名重複チェック
        if 0 < self.selectCountSameAppName(entity['ip_code'],entity['app_name']):
            raise DaoMMobileApp.DuplicateAppNameException

        # アプリID_iOS重複チェック
        if (entity['app_id_ios']):
            if 0 < self.selectCountSameAppIdIosForCreate(entity['ip_code'], entity['app_id_ios']):
                raise DaoMMobileApp.DuplicateAppIdException

        # アプリID_Android重複チェック
        if (entity['app_id_android']):
            if 0 < self.selectCountSameAppIdAndroidForCreate(entity['ip_code'], entity['app_id_android']):
                raise DaoMMobileApp.DuplicateAppIdException
        
        sql =   """
                INSERT INTO m_mobile_app
                (
                   ip_code
                 , app_name
                 , app_id_ios
                 , app_id_android
                 , distributor_name
                 , is_working
                 , service_start_date
                 , service_end_date
                 , is_invalid
                 , create_user
                 , create_date
                 , update_user
                 , update_date
                )
                VALUES (
                    %(ip_code)s,
                    %(app_name)s,
                    %(app_id_ios)s,
                    %(app_id_android)s,
                    %(distributor_name)s,
                    %(is_working)s,
                    %(service_start_date)s,
                    %(service_end_date)s,
                    false,
                    %(full_name)s ,
                    now(),
                    %(full_name)s ,
                    now())
                """

        return self.updateWithParam(sql,entity)

    def selectAppByIpCodeAppName(self, ip_code, app_name):
        '''
        アプリマスタ編集画面表示用
        '''
        param = {
            'ip_code' : ip_code,
            'app_name':app_name
         }
        sql =   """
                SELECT
                  m_mobile_app.ip_code
                , m_ip.ip_name
                , m_mobile_app.app_name
                , m_mobile_app.app_id_ios
                , m_mobile_app.app_id_android
                , m_mobile_app.distributor_name
                , m_mobile_app.service_start_date
                , m_mobile_app.service_end_date
                FROM m_mobile_app
                INNER JOIN m_ip ON (
                    m_mobile_app.ip_code = m_ip.ip_code 
                    AND m_ip.is_invalid = false
                )
                WHERE m_mobile_app.is_invalid = false
                AND m_mobile_app.ip_code = %(ip_code)s
                AND m_mobile_app.app_name = %(app_name)s
                LIMIT 1
                """
        return self.selectWithParam(sql, param)

    def updateMMobileApp(self, entity):
        '''
        アプリマスタレコード編集
        '''

        # アプリ名重複チェック
        # アプリ名編集時のみチェックを実施
        if entity['get_app_name'] != entity['app_name']:
            if 0 < self.selectCountSameAppName(entity['get_ip_code'], entity['app_name']):
                raise DaoMMobileApp.DuplicateAppNameException

        # アプリID_iOS重複チェック
        if (entity['app_id_ios']):
            if 0 < self.selectCountSameAppIdIosForUpdate(entity['get_ip_code'], entity['app_id_ios'], entity['get_app_name']):
                raise DaoMMobileApp.DuplicateAppIdException

        # アプリID_Android重複チェック
        if (entity['app_id_android']):
            if 0 < self.selectCountSameAppIdAndroidForUpdate(entity['get_ip_code'], entity['app_id_android'], entity['get_app_name']):
                raise DaoMMobileApp.DuplicateAppIdException
        
        sql =   """
                UPDATE m_mobile_app
                SET
                   app_name = %(app_name)s
                 , app_id_ios = %(app_id_ios)s
                 , app_id_android = %(app_id_android)s
                 , distributor_name = %(distributor_name)s
                 , is_working = %(is_working)s
                 , service_start_date = %(service_start_date)s
                 , service_end_date = %(service_end_date)s
                 , update_user = %(full_name)s
                 , update_date= now()
                 WHERE m_mobile_app.ip_code = %(get_ip_code)s
                 AND m_mobile_app.app_name = %(get_app_name)s
                 AND is_invalid = false
                """

        return self.updateWithParam(sql, entity)

    def selectCountSameAppName(self, ip_code, app_name):
        '''
        アプリ名重複チェック
        IPコードとアプリ名が一致する場合、同一アプリと判断
        '''

        param = {
            'app_name' : app_name,
            'ip_code' : ip_code
        }
        sql =   """
                SELECT count(*)
                FROM m_mobile_app
                WHERE app_name = %(app_name)s
                AND ip_code = %(ip_code)s
                AND is_invalid = false
                """

        return self.selectWithParam(sql, param)[0][0]

    def selectCountSameAppIdIosForCreate(self, ip_code, app_id_ios):
        '''
        アプリID_iOS重複チェック（新規登録用）
        同一IPコードに同一アプリIDが紐づいていないかカウントする
        '''
        param = {
            'app_id_ios' : app_id_ios,
            'ip_code' : ip_code
        }
        sql =   """
                SELECT count(*)
                FROM m_mobile_app
                WHERE app_id_ios = %(app_id_ios)s
                AND ip_code = %(ip_code)s
                AND is_invalid = false
                """

        return self.selectWithParam(sql, param)[0][0]
    
    def selectCountSameAppIdAndroidForCreate(self, ip_code, app_id_android):
        '''
        アプリID_Android重複チェック（新規登録用）
        同一IPコードに同一アプリIDが紐づいていないかカウントする
        '''

        param = {
            'app_id_android' : app_id_android,
            'ip_code' : ip_code
        }
        sql =   """
                SELECT count(*)
                FROM m_mobile_app
                WHERE app_id_android = %(app_id_android)s
                AND ip_code = %(ip_code)s
                AND is_invalid = false
                """

        return self.selectWithParam(sql, param)[0][0]

    def selectCountSameAppIdIosForUpdate(self, ip_code, app_id_ios, app_name):
        '''
        アプリID_iOS重複チェック（編集用）
        IPコードとアプリ名が一致する場合はアプリ編集時と判断し、カウントしない
        '''
        param = {
            'app_id_ios' : app_id_ios,
            'app_name' : app_name,
            'ip_code' : ip_code
        }
        sql =   """
                SELECT count(*)
                FROM m_mobile_app
                WHERE app_id_ios = %(app_id_ios)s
                AND ip_code = %(app_name)s
                AND app_name <> %(ip_code)s
                AND is_invalid = false
                """

        return self.selectWithParam(sql, param)[0][0]
    
    def selectCountSameAppIdAndroidForUpdate(self, ip_code, app_id_android, app_name):
        '''
        アプリID_Android重複チェック（編集用）
        IPコードとアプリ名が一致する場合はアプリ編集時と判断し、カウントしない
        '''
        param = {
            'app_id_android' : app_id_android,
            'app_name' : app_name,
            'ip_code' : ip_code
        }
        sql =   """
                SELECT count(*)
                FROM m_mobile_app
                WHERE app_id_android = %(app_id_android)s
                AND ip_code = %(ip_code)s
                AND app_name <> %(app_name)s
                AND is_invalid = false
                """

        return self.selectWithParam(sql, param)[0][0]

    class DuplicateAppIdException(Exception):
        """
        アプリID重複エラー
        """
        pass

    class DuplicateAppNameException(Exception):
        """
        アプリ名重複エラー
        """
        pass
