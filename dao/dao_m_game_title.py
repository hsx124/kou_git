from ipdds_app.dao.dao_main import DaoMain

class DaoMGame(DaoMain):

    """作品コードに紐づくゲームタイトルコードを取得"""
    def selectGame(self,sakuhin_code):
        sql = """
              SELECT
                game_title_code
              FROM
                m_game_title
              LEFT JOIN
                m_sakuhin_map
                ON m_game_title.game_title_code = m_sakuhin_map.title_code
                AND m_sakuhin_map.invalid_flg = false
              WHERE
                m_game_title.invalid_flg = false
                AND m_sakuhin_map.sakuhin_code = %s
              """
        return  self.selectWithParam(sql,[sakuhin_code])

    """ゲームタイトルコードをもとにゲームデータの取得"""
    def selectGameDataByTitleCode(self,title_code):
        sql = """
              SELECT
                  m_game_title.game_title_code
                , m_game_title.game_title_name
                ,m_game_title.platform_name
                ,m_game_title.hanbai_company_name
                ,TO_CHAR(TO_DATE(m_game_title.release_yyyymmdd,'yyyymmdd'),'yyyy年MM月')
                ,t_game.total_sales_cnt ::numeric::integer
              FROM
                m_game_title
              INNER JOIN
                t_game
              ON  m_game_title.game_title_name = t_game.game_title_name
                AND t_game.result_yyyymm = (
                        SELECT
                          max(result_yyyymm)
                        FROM
                          t_game
                        WHERE
                          m_game_title.game_title_name = t_game.game_title_name
                          AND result_yyyymm < TO_CHAR(current_timestamp, 'yyyymm')
                )
                AND m_game_title.platform_name = t_game.platform_name
                AND m_game_title.release_yyyymmdd = t_game.release_yyyymmdd
              WHERE
                m_game_title.invalid_flg = false
                AND m_game_title.game_title_code = %s
              ORDER BY COALESCE(t_game.total_sales_cnt,0) DESC ,m_game_title.release_yyyymmdd ASC
              """
        return  self.selectWithParam(sql,[title_code])