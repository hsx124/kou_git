from admin_app.dao.dao_main import DaoMain

class DaoMIpMap(DaoMain):
    """作品紐付け解除・無効フラグを有効にする""" 
    def updateInvalidFlgBy(self, param):
        sql =   """
                UPDATE m_ip_map
                SET invalid_flg = true
                    , update_user = %(full_name)s
                    , update_time = now()
                WHERE ip_map_id = %(map_id)s
                """
        return self.updateWithParam(sql, param)

    """作品リストをもとにIP紐付けマスタデータ追加"""
    def insertBySakuhinList(self,param):
        sql =   """
                INSERT INTO m_ip_map( 
                    ip_map_id
                    , ip_code
                    , sakuhin_code
                    , invalid_flg
                    , create_user
                    , create_time
                    , update_user
                    , update_time
                ) 
                SELECT
                    nextval('m_ip_map_ip_map_id_seq' ::regclass)
                    , %(ip_code)s
                    , sakuhin_code
                    , false
                    , %(full_name)s
                    , now()
                    , %(full_name)s
                    , now()
                FROM
                m_sakuhin sakuhin 
                WHERE
                sakuhin.sakuhin_code in %(sakuhin_code_list)s
                AND sakuhin.invalid_flg = false
                """
        return self.updateWithParam(sql,param)

    """IPリストをもとにIP紐付けマスタデータ追加"""
    def insertByIpList(self,param):
        sql =   """
                INSERT INTO m_ip_map( 
                    ip_map_id
                    , ip_code
                    , sakuhin_code
                    , invalid_flg
                    , create_user
                    , create_time
                    , update_user
                    , update_time
                ) 
                SELECT
                    nextval('m_ip_map_ip_map_id_seq' ::regclass)
                    , ip_code
                    , %(sakuhin_code)s
                    , false
                    , %(full_name)s
                    , now()
                    , %(full_name)s
                    , now()
                FROM
                m_ip ip 
                WHERE
                ip.ip_code in %(ip_code_list)s
                AND ip.invalid_flg = false
                """
        return self.updateWithParam(sql,param)