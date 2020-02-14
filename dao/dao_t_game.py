from ipdds_app.dao.dao_main import DaoMain

class DaoTGame(DaoMain):

    """タイトルコードをもとにゲームデータの取得(グラフ用)"""
    def selectGraphData(self,title_code):

        sql = """
              SELECT
                  m_game_title.game_title_code
                , m_game_title.game_title_name
                , left(t_game.result_yyyymm,4) || '-' || right(t_game.result_yyyymm,2)
                , t_game.total_sales_cnt::numeric::integer
              FROM
                t_game
                INNER JOIN m_game_title
                ON t_game.game_title_name = m_game_title.game_title_name
                AND m_game_title.invalid_flg = false
              WHERE
                TO_CHAR(current_timestamp - interval '1 years','yyyymm') <= t_game.result_yyyymm
                AND t_game.result_yyyymm < TO_CHAR(current_timestamp,'yyyymm')
                AND m_game_title.platform_name = t_game.platform_name
                AND m_game_title.release_yyyymmdd = t_game.release_yyyymmdd
                AND m_game_title.game_title_code = %s
              """
        return self.selectWithParam(sql,[title_code])

    """ゲームの発売日を取得(グラフ用)"""
    def selectGameServiceStartDate(self,game_title_code):
        sql = """
          SELECT
            LEFT(MIN(release_yyyymmdd),6)
          FROM m_game_title
          WHERE
            game_title_code = %s
            AND invalid_flg = FALSE
          LIMIT 1
          """
        return self.selectWithParam(sql,[game_title_code])

    """ゲームタイトルコードをもとに累計売上本数（発売日からNか月）の取得(グラフ用)"""
    def selectFromServiceStartDateGraphData(self,firstDate,game_title_code):
        sql = """
          SELECT 
            left (t.result_yyyymm, 4) || '-' || right (t.result_yyyymm, 2) AS result_yyyymm
            , total_sales_cnt::numeric::integer
          FROM m_game_title game
          LEFT JOIN t_game t
          ON game.game_title_name = t.game_title_name
            AND game.platform_name = t.platform_name
            AND game.release_yyyymmdd = t.release_yyyymmdd
          WHERE
            t.result_yyyymm >= %s
        		AND t.result_yyyymm < to_char((to_date(%s, 'YYYYMMDD') + interval '1 years'),'yyyymm')
            AND t.result_yyyymm < to_char(current_timestamp,'yyyymm')
            AND game.invalid_flg = false
            AND game.game_title_code = %s
          """
        return self.selectWithParam(sql,[firstDate,firstDate,game_title_code])

    """ゲームタイトルコードをもとに累計売上本数の取得(グラフ用)"""
    def selectGameTotleSalesGraphData(self,firstDate,game_title_code):
        sql = """
          SELECT 
            left (t.result_yyyymm, 4) || '-' || right (t.result_yyyymm, 2) AS result_yyyymm
            , total_sales_cnt::numeric::integer
          FROM m_game_title game
          LEFT JOIN t_game t
          ON game.game_title_name = t.game_title_name
            AND game.platform_name = t.platform_name
            AND game.release_yyyymmdd = t.release_yyyymmdd
          WHERE
            t.result_yyyymm >= to_char(current_timestamp - interval '1 years','yyyymm')
            AND t.result_yyyymm < to_char(current_timestamp,'yyyymm')
            AND t.result_yyyymm >= %s
            AND game.invalid_flg = false
            AND game.game_title_code = %s
          """
        return self.selectWithParam(sql,[firstDate,game_title_code])