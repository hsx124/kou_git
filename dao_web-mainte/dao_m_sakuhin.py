from admin_app.dao.dao_main import DaoMain

class DaoMSakuhin(DaoMain):

    def selectAll(self):
        """
        作品マスタ全件取得
        """
        sql =   """
                SELECT
                  m_sakuhin.sakuhin_code
                , m_sakuhin.sakuhin_name
                , m_sakuhin.overview
                , m_sakuhin.key_visual_file_name
                , m_sakuhin.keyword
                , to_date(m_sakuhin.release_yyyymm,'yyyymmdd')
                , m_sakuhin.update_user
                , m_sakuhin.update_time
                FROM m_sakuhin
                WHERE invalid_flg = false
                ORDER BY 
                m_sakuhin.update_time DESC,
                m_sakuhin.sakuhin_code ASC
                """

        return self.select(sql)
    """削除する前に該当データの無効フラグ確認""" 
    def selectInvalidFlg(self, param):
        sql =   """
                SELECT
                invalid_flg
                FROM m_sakuhin
                WHERE sakuhin_code = %(sakuhin_code)s
                """
        return self.selectWithParam(sql, param)[0][0]

    def selectsakuhinMasterForCSV(self):
        """
        CSV出力用作品情報取得
        @param sakuhincode
        """
        sql =   """
                SELECT
                  sakuhin_code,
                  sakuhin_name,
                  sakuhin_kana_name,
                  key_visual_file_name,
                  release_yyyymm,
                  valid_start_yyyymmdd,
                  valid_end_yyyymmdd,
                  foreign_window,
                  domestic_window,
                  memo,
                  overview,
                  keyword,
                  invalid_flg,
                  create_user,
                  create_time,
                  update_user,
                  update_time
                FROM m_sakuhin
                WHERE invalid_flg = false
                ORDER BY sakuhin_code ASC
                """

        return self.select(sql)

    def selectSakuhinMasterBySakuhinCode(self, sakuhin_code):
        """
        作品コードから作品名を取得
        @param sakuhincode
        """
        param = {'sakuhin_code' : sakuhin_code}
        sql =   """
                SELECT
                  m_sakuhin.sakuhin_code
                , m_sakuhin.sakuhin_name
                FROM m_sakuhin
                WHERE invalid_flg = false
                AND sakuhin_code = %(sakuhin_code)s
                ORDER BY m_sakuhin.sakuhin_code ASC
                """

        return self.selectWithParam(sql, param)

    def selectSakuhinMasterBySakuhinName(self, searchWord):
        """
        作品名、作品名かなを検索
        検索条件:部分一致 作品コード（昇順）
        @param searchWord 検索ワード
        """

        sql =   """
                SELECT
                  m_sakuhin.sakuhin_code
                , m_sakuhin.sakuhin_name
                FROM m_sakuhin
                WHERE invalid_flg = false
                AND (sakuhin_name LIKE %s OR sakuhin_kana_name LIKE %s)
                ORDER BY m_sakuhin.sakuhin_code ASC
                """
        return self.selectWithParam(sql, ('%' + searchWord + '%', '%' + searchWord + '%'))

    def updateInvalidFlgBySakuhinCode(self, sakuhin_code, full_name):
        '''
        作品マスタレコード論理削除
        無効フラグを有効にする
        ''' 

        param = {
                  'sakuhin_code' : sakuhin_code,
                  'full_name' : full_name
                  }
        sql =   """
                UPDATE m_sakuhin
                SET invalid_flg = true
                , update_user = %(full_name)s
                , update_time = now()
                WHERE m_sakuhin.sakuhin_code = %(sakuhin_code)s
                """
        return self.updateWithParam(sql, param)

    def selectMaxSakuhinCode(self):
        '''
        作品コード採番用にm_sakuhinに
        存在する最大の作品コードを取得する
        '''
        sql =   """
                SELECT COALESCE(max(sakuhin_code),'0000000000')
                FROM m_sakuhin 
                """
        # max取得のため必ず一件レコードが取得される
        return self.select(sql)[0][0]

    def selectCountSameSakuhinName(self, sakuhin_code, sakuhin_name):
        '''
        作品名に同一のものがないか検索
        作品コードと作品名が一致する場合は作品編集時と判断しカウントしない
        '''
        param = {
          'sakuhin_code':sakuhin_code,
          'sakuhin_name':sakuhin_name
        }
        sql =   """
                SELECT count(*)
                FROM m_sakuhin
                WHERE sakuhin_name = %(sakuhin_name)s
                AND sakuhin_code <> %(sakuhin_code)s
                AND invalid_flg = false
                """
        return self.selectWithParam(sql, param)[0][0]

    def selectSakuhinUpdateDataBySakuhinCode(self, sakuhin_code):
        '''
        作品マスタ編集画面表示用
        '''
        param = {'sakuhin_code' : sakuhin_code}
        sql =   """
                SELECT
                  sakuhin_code
                , sakuhin_name
                , sakuhin_kana_name
                , key_visual_file_name
                , release_yyyymm
                , valid_start_yyyymmdd
                , valid_end_yyyymmdd
                , domestic_window
                , foreign_window
                , memo
                , overview
                , keyword
                FROM m_sakuhin
                WHERE invalid_flg = false
                AND sakuhin_code = %(sakuhin_code)s
                LIMIT 1
                """
        return self.selectWithParam(sql, param)

    def insertMSakuhin(self,entity):
        '''
        新規作品マスタ作成
        '''
        
        # 作品コード重複チェック
        if entity[0] <= self.selectMaxSakuhinCode():
          raise DaoMSakuhin.DuplicateSakuhinCodeException

        # 作品名重複チェック
        if 0 < self.selectCountSameSakuhinName(entity[0],entity[1]):
          raise DaoMSakuhin.DuplicateSakuhinNameException
        
        sql =   """
                INSERT INTO m_sakuhin
                (
                   sakuhin_code
                 , sakuhin_name
                 , sakuhin_kana_name
                 , key_visual_file_name
                 , release_yyyymm
                 , valid_start_date
                 , valid_end_date
                 , foreign_window
                 , domestic_window
                 , memo
                 , overview
                 , overview_wiki_title
                 , keyword
                 , invalid_flg
                 , create_user
                 , create_time
                 , update_user
                 , update_time
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, false, %s , now(), %s , now())
                """
        # max取得のため必ず一件レコードが取得される
        return self.updateWithParam(sql,entity)

    def updateMSakuhin(self,entity):
        '''
        作品マスタ更新
        '''

        # 作品名重複チェック
        if 0 < self.selectCountSameSakuhinName(entity[13], entity[0]):
          raise DaoMSakuhin.DuplicateSakuhinNameException

        sql =   """
                UPDATE m_sakuhin
                SET
                  sakuhin_name = %s
                , sakuhin_kana_name = %s
                , key_visual_file_name = %s
                , release_yyyymm = %s
                , valid_start_date = %s
                , valid_end_date = %s
                , foreign_window = %s
                , domestic_window = %s
                , memo = %s
                , overview = %s
                , overview_wiki_title = %s
                , keyword = %s
                , update_user = %s 
                , update_time = now()
                WHERE m_sakuhin.sakuhin_code = %s
                """
        # max取得のため必ず一件レコードが取得される
        return self.updateWithParam(sql,entity)

    class DuplicateSakuhinCodeException(Exception):
        """
        作品コード重複エラー
        """
        pass

    class DuplicateSakuhinNameException(Exception):
        """
        作品名重複エラー
        """
        pass

    """作品名、作品かなを作品データ検索"""
    def selectBySakuhinName(self, param):
        sql =   """
                SELECT
                sakuhin_code
                , sakuhin_name
                , sakuhin_kana_name
                , update_user
                , update_time
                FROM m_sakuhin
                WHERE invalid_flg = false
                AND (sakuhin_name LIKE %(sakuhin_name)s OR sakuhin_kana_name LIKE %(sakuhin_name)s)
                ORDER BY sakuhin_code ASC
                """
        return self.selectWithParam(sql, param)

    """Gameに紐付け作品データ取得""" 
    def selectSakuhinByGameCode(self, param):
        sql =   """
                SELECT
                    sakuhin.sakuhin_code
                    , sakuhin.sakuhin_name
                    , sakuhin.sakuhin_kana_name
                    , sakuhin_map.update_user
                    , sakuhin_map.update_time
                    , sakuhin_map.sakuhin_map_id
                FROM
                m_sakuhin sakuhin 
                INNER JOIN m_sakuhin_map sakuhin_map 
                    ON sakuhin.sakuhin_code = sakuhin_map.sakuhin_code
                    AND sakuhin.invalid_flg = FALSE 
                INNER JOIN m_game_title game 
                    ON sakuhin_map.title_code = game.game_title_code
                    AND sakuhin_map.invalid_flg = FALSE 
                WHERE
                game.game_title_code = %(game_code)s
                AND game.invalid_flg = FALSE
                ORDER BY sakuhin_map.update_time DESC
                """
        return self.selectWithParam(sql, param)
