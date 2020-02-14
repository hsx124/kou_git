from ipdds_app.dao.dao_main import DaoMain

class DaoTPkgSoft(DaoMain):

    """パッケージソフトコードをもとにゲームデータの取得(グラフ用)"""
    def selectGraphData(self,pkg_soft_code):

        sql = """
              SELECT
                left(t_pkg_soft.result_yyyymm,4) || '-' || right(t_pkg_soft.result_yyyymm,2)
                , t_pkg_soft.qty_total_sales::numeric::integer
              FROM
                t_pkg_soft
              WHERE
                to_char(current_timestamp - interval '1 years','yyyymm') <= t_pkg_soft.result_yyyymm
                and t_pkg_soft.result_yyyymm < to_char(current_timestamp,'yyyymm')
                and t_pkg_soft.pkg_soft_code = %s

              """
        return self.selectWithParam(sql,[pkg_soft_code])

    """パッケージソフトコードをもとに累計売上本数（発売日からNか月）の取得(グラフ用)"""
    def selectFromFirstDayGraphData(self,pkg_soft_code):

        sql = """
          SELECT
            left (t_pkg_soft.result_yyyymm, 4) || '-' || right (t_pkg_soft.result_yyyymm, 2)
            , t_pkg_soft.qty_total_sales::numeric::integer
          FROM
            t_pkg_soft 
          WHERE
            to_char(
              ( 
                SELECT
                  MIN(release_date) 
                FROM
                  m_pkg_soft 
                WHERE
                  pkg_soft_code = %s 
                  AND m_pkg_soft.is_invalid = FALSE) , 'yyyymm') <= t_pkg_soft.result_yyyymm 
            AND t_pkg_soft.result_yyyymm < to_char( 
              ( 
                SELECT
                  MIN(release_date) 
                FROM
                  m_pkg_soft 
                WHERE
                  pkg_soft_code = %s
                  AND m_pkg_soft.is_invalid = FALSE) + interval '1 years' , 'yyyymm') 
            AND t_pkg_soft.pkg_soft_code = %s
            
            """
        return self.selectWithParam(sql,[pkg_soft_code,pkg_soft_code,pkg_soft_code])

    
