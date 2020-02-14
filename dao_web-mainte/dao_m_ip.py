from admin_app.dao.dao_main import DaoMain

class DaoMIp(DaoMain):
    
    """IPマスタ全件取得"""
    def selectAll(self):
        sql =   """
                SELECT
                m_ip.ip_code
                , m_ip.ip_name
                , m_ip.ip_kana_name
                , m_ip.ip_control_flg
                , m_ip.update_user
                , m_ip.update_time
                FROM m_ip
                WHERE invalid_flg = false
                ORDER BY 
                m_ip.update_time DESC
                , m_ip.ip_code ASC
                """

        return self.select(sql)
        
    """削除する前に該当データの無効フラグ確認""" 
    def selectInvalidFlg(self, param):
        sql =   """
                SELECT
                invalid_flg
                FROM m_ip
                WHERE ip_code = %(ip_code)s
                """
        return self.selectWithParam(sql, param)[0][0]

    """IPマスタレコード論理削除・無効フラグを有効にする""" 
    def updateInvalidFlgByIpCode(self, param):
        sql =   """
                UPDATE m_ip
                SET invalid_flg = true
                    , update_user = %(full_name)s
                    , update_time = now()
                WHERE ip_code = %(ip_code)s
                """
        return self.updateWithParam(sql, param)

    """CSV出力用IP情報取得"""
    def selectCsvData(self):
        sql =   """
                SELECT
                  ip_code
                  , ip_name
                  , ip_kana_name
                  , ip_control_flg
                  , create_user
                  , create_time
                  , update_user
                  , update_time 
                FROM m_ip 
                WHERE invalid_flg = false 
                ORDER BY ip_code ASC

                """
        return self.select(sql)

        """IPマスタに存在する最大のIPコードを取得する"""
    def selectMaxIpCode(self):
        sql =   """
                SELECT coalesce(max(ip_code),'00000000')
                FROM m_ip
                """
        return self.select(sql)[0][0]

    """IPマスタに同一IPコードを検索"""
    def selectSameCode(self, ip_code):
        param = {'ip_code':ip_code}

        sql =   """
                SELECT count(*)
                FROM m_ip
                WHERE ip_code = %(ip_code)s
                """
        return self.selectWithParam(sql, param)[0][0]

    """IPマスタに同一IP名を検索"""
    def selectSameName(self, ip_code, ip_name):
        param = {
            'ip_code':ip_code,
            'ip_name':ip_name
        }
        sql =   """
                SELECT count(*)
                FROM m_ip
                WHERE ip_name = %(ip_name)s
                AND ip_code <> %(ip_code)s
                AND invalid_flg = false
                """
        return self.selectWithParam(sql, param)[0][0]

    """新規IPマスタ作成"""
    def insert(self,entity):
        # IPコード重複チェック
        if 0 < self.selectSameCode(entity['ip_code']):
            raise DaoMIp.DuplicateIpCodeException

        # IP名重複チェック
        if 0 < self.selectSameName(entity['ip_code'],entity['ip_name']):
            raise DaoMIp.DuplicateIpNameException
        
        sql =   """
                INSERT INTO m_ip
                    (
                    ip_code
                    , ip_name
                    , ip_kana_name
                    , ip_control_flg
                    , invalid_flg
                    , create_user
                    , create_time
                    , update_user
                    , update_time
                    )
                VALUES (%(ip_code)s, %(ip_name)s, %(ip_kana_name)s, %(ip_control_flg)s, false, %(full_name)s, now(), %(full_name)s , now())
                """
        return self.updateWithParam(sql,entity)

    """IPマスタ編集画面表示用"""
    def selectUpdateData(self, param):
        sql =   """
                SELECT
                    ip_code
                    , ip_name
                    , ip_kana_name
                    , ip_control_flg
                FROM m_ip
                WHERE invalid_flg = false
                AND ip_code = %(ip_code)s
                """
        return self.selectWithParam(sql, param)

    """IPマスタ更新"""
    def update(self,entity):
        # IP名重複チェック
        if 0 < self.selectSameName(entity['ip_code'], entity['ip_name']):
          raise DaoMIp.DuplicateIpNameException

        sql =   """
                UPDATE m_ip
                SET
                    ip_name = %(ip_name)s
                    , ip_kana_name = %(ip_kana_name)s
                    , ip_control_flg = %(ip_control_flg)s
                    , update_user = %(full_name)s
                    , update_time = now()
                WHERE ip_code = %(ip_code)s
                """
        return self.updateWithParam(sql,entity)


    """IP名、IP名かなをIPデータ検索"""
    def selectByIpName(self, param):
        sql =   """
                SELECT
                    ip_code
                    , ip_name
                    , ip_kana_name
                    , update_user
                    , update_time
                FROM m_ip
                WHERE invalid_flg = false
                AND (ip_name LIKE %(ip_name)s OR ip_kana_name LIKE %(ip_name)s)
                ORDER BY ip_code ASC
                """
        return self.selectWithParam(sql,param)

    """IPコードを関連作品検索""" 
    def selectByIpCode(self, param):
        sql =   """
                SELECT
                    sakuhin.sakuhin_code
                    , sakuhin.sakuhin_name
                    , sakuhin.sakuhin_kana_name
                    , ip_map.update_user
                    , ip_map.update_time
                    , ip_map.ip_map_id
                FROM
                m_ip ip 
                INNER JOIN m_ip_map ip_map 
                    ON ip.ip_code = ip_map.ip_code 
                    AND ip_map.invalid_flg = FALSE 
                INNER JOIN m_sakuhin sakuhin 
                    ON ip_map.sakuhin_code = sakuhin.sakuhin_code 
                    AND sakuhin.invalid_flg = FALSE 
                WHERE
                ip.ip_code = %(ip_code)s
                AND ip.invalid_flg = FALSE
                ORDER BY 
                    ip_map.update_time DESC
                    , sakuhin.sakuhin_code
                """
        return self.selectWithParam(sql, param)

    """作品コードを関連作品検索""" 
    def selectBySakuhinCode(self, param):
        sql =   """
                SELECT
                    ip.ip_code
                    , ip.ip_name
                    , ip.ip_kana_name
                    , ip_map.update_user
                    , ip_map.update_time
                    , ip_map.ip_map_id
                FROM
                m_ip ip 
                INNER JOIN m_ip_map ip_map 
                    ON ip.ip_code = ip_map.ip_code 
                    AND ip.invalid_flg = FALSE
                INNER JOIN m_sakuhin sakuhin 
                    ON ip_map.sakuhin_code = sakuhin.sakuhin_code 
                    AND ip_map.invalid_flg = FALSE 
                WHERE
                sakuhin.sakuhin_code = %(sakuhin_code)s
                AND sakuhin.invalid_flg = FALSE
                ORDER BY
                    ip_map.update_time DESC
                    , ip.ip_code
                """
        return self.selectWithParam(sql, param)

    """IPコード重複エラー"""
    class DuplicateIpCodeException(Exception):
        pass

    """IP名重複エラー"""
    class DuplicateIpNameException(Exception):
        pass