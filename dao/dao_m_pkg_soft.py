from ipdds_app.dao.dao_main import DaoMain

class DaoMPkgSoft(DaoMain):

    """IPコードをもとにゲームデータの取得"""
    def selectGameData(self,ip_code):
        sql = """
              SELECT
                m_pkg_soft.pkg_soft_code
                ,m_pkg_soft.pkg_soft_name
                ,m_pkg_soft.platform_name
                ,m_pkg_soft.distributor_name
                ,to_char(m_pkg_soft.release_date,'yyyy年MM月')
                ,to_char(t_pkg_soft.qty_total_sales,'999,999,999,999,999')
              FROM
                m_pkg_soft
              LEFT JOIN
                t_pkg_soft
              ON  m_pkg_soft.pkg_soft_code = t_pkg_soft.pkg_soft_code
                  and t_pkg_soft.result_yyyymm = ( 
                           SELECT
                             max(result_yyyymm) 
                           FROM
                             t_pkg_soft
                           WHERE
                             m_pkg_soft.pkg_soft_code = t_pkg_soft.pkg_soft_code
                             and result_yyyymm < to_char(current_timestamp, 'yyyymm')
                  ) 
              WHERE
                m_pkg_soft.is_invalid = false
                and m_pkg_soft.ip_code = %s
              ORDER BY COALESCE(t_pkg_soft.qty_total_sales,0) DESC ,m_pkg_soft.release_date ASC
              """
        return  self.selectWithParam(sql,[ip_code])