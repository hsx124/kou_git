from admin_app.dao.dao_main import DaoMain

class DaoMStaffMap(DaoMain):

    """スタッフ紐づけマスタに存在する最大のスタッフマップコードを取得する"""
    def selectMaxStaffMapCode(self):
        sql =   """
                SELECT
                    coalesce(max(staff_map_code), '0000000000')
                FROM
                    m_staff_map
                """
        return self.select(sql)[0][0]