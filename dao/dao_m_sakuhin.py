from ipdds_app.dao.dao_main import DaoMain
import datetime

class DaoMSakuhin(DaoMain):

    # 検索用SELECT文
    selectSentence =  """
                      SELECT
                      COALESCE(m_sakuhin.key_visual_file_name, '') AS keyvisual_file_name
                      , m_sakuhin.sakuhin_code
                      , m_sakuhin.sakuhin_name
                      , m_sakuhin.sakuhin_kana_name
                      , COALESCE(m_sakuhin.overview, 'no data')
                       , EXISTS ( SELECT * FROM m_anime_title LEFT JOIN m_sakuhin_map ON m_anime_title.anime_title_code = m_sakuhin_map.title_code WHERE m_sakuhin_map.sakuhin_code = m_sakuhin.sakuhin_code and m_anime_title.invalid_flg = false ) AS anime
                      , EXISTS ( SELECT * FROM m_manga_title LEFT JOIN m_sakuhin_map ON m_manga_title.manga_title_code = m_sakuhin_map.title_code WHERE m_sakuhin_map.sakuhin_code = m_sakuhin.sakuhin_code and m_manga_title.invalid_flg = false ) AS manga
                      , EXISTS ( SELECT * FROM m_app_title LEFT JOIN m_sakuhin_map ON m_app_title.app_title_code = m_sakuhin_map.title_code WHERE m_sakuhin_map.sakuhin_code = m_sakuhin.sakuhin_code and m_app_title.invalid_flg = false ) AS app
                      , EXISTS ( SELECT * FROM m_game_title LEFT JOIN m_sakuhin_map ON m_game_title.game_title_code = m_sakuhin_map.title_code WHERE m_sakuhin_map.sakuhin_code = m_sakuhin.sakuhin_code and m_game_title.invalid_flg = false ) AS game
                      , COALESCE(core_1.core_code, '')
                      , COALESCE(core_1.core_name, '')
                      , COALESCE(core_2.core_code, '')
                      , COALESCE(core_2.core_name, '')
                      , COALESCE(media.media_code, '')
                      , COALESCE(media.media_name, '')
                      , COALESCE(fact_1.sakuhin_tag_code, '')
                      , COALESCE(fact_1.sakuhin_tag_name, '')
                      , COALESCE(fact_2.sakuhin_tag_code, '')
                      , COALESCE(fact_2.sakuhin_tag_name, '')
                      , COALESCE(fact_3.sakuhin_tag_code, '')
                      , COALESCE(fact_3.sakuhin_tag_name, '')
                      , COALESCE(fact_4.sakuhin_tag_code, '')
                      , COALESCE(fact_4.sakuhin_tag_name, '')
                      , COALESCE(fact_5.sakuhin_tag_code, '')
                      , COALESCE(fact_5.sakuhin_tag_name, '')
                      , m_sakuhin.release_yyyymm
                      , to_char(m_sakuhin.update_time, 'YYYY/MM/DD')
                      , c.sum
                      , c.avg
                      {book_volume}
                      """
    # 検索用FROM文
    fromSentence =  """
                    FROM
                    m_sakuhin
                    LEFT JOIN m_sakuhin_map
                      ON m_sakuhin.sakuhin_code = m_sakuhin_map.sakuhin_code
                        and m_sakuhin_map.invalid_flg = false
                    LEFT JOIN m_manga_title
                      ON m_manga_title.manga_title_code = m_sakuhin_map.title_code
                        and m_manga_title.invalid_flg = false
                    LEFT JOIN m_sakuhin_tag_map
                      ON m_manga_title.tag_map_code = m_sakuhin_tag_map.tag_map_code
                        and m_sakuhin_tag_map.invalid_flg = false
                    LEFT JOIN m_core AS core_1
                      ON m_sakuhin_tag_map.core_code1 = core_1.core_code
                        and core_1.invalid_flg = false
                    LEFT JOIN m_core AS core_2
                      ON m_sakuhin_tag_map.core_code2 = core_2.core_code
                        and core_2.invalid_flg = false
                    LEFT JOIN m_media AS media
                      ON m_manga_title.media_code = media.media_code
                        and media.invalid_flg = false
                    LEFT JOIN m_sakuhin_tag AS fact_1
                      ON m_sakuhin_tag_map.sakuhin_tag_code1 = fact_1.sakuhin_tag_code
                        and fact_1.invalid_flg = false
                    LEFT JOIN m_sakuhin_tag AS fact_2
                      ON m_sakuhin_tag_map.sakuhin_tag_code2 = fact_2.sakuhin_tag_code
                        and fact_2.invalid_flg = false
                    LEFT JOIN m_sakuhin_tag AS fact_3
                      ON m_sakuhin_tag_map.sakuhin_tag_code3 = fact_3.sakuhin_tag_code
                        and fact_3.invalid_flg = false
                    LEFT JOIN m_sakuhin_tag AS fact_4
                      ON m_sakuhin_tag_map.sakuhin_tag_code4 = fact_4.sakuhin_tag_code
                        and fact_4.invalid_flg = false
                    LEFT JOIN m_sakuhin_tag AS fact_5
                      ON m_sakuhin_tag_map.sakuhin_tag_code5 = fact_5.sakuhin_tag_code
                        and fact_5.invalid_flg = false
                    LEFT JOIN
                    (
                    SELECT
                    a.manga_title_code
                    , a.sum
                    , a.avg
                    FROM
                    (
                      SELECT
                        m_manga_isbn.manga_title_code
                        , to_char(sum(t_isbn.total_sales_cnt),'999,999,999,999,999') AS sum
                        , to_char(avg(COALESCE(t_isbn.total_sales_cnt,0)),'999,999,999,999,999') AS avg 
                      FROM
                        m_manga_isbn
                        INNER JOIN t_isbn
                          ON m_manga_isbn.isbn = t_isbn.isbn
                          and t_isbn.result_yyyymm = (
                          SELECT
                            max(result_yyyymm)
                          FROM
                            t_isbn
                          WHERE
                            m_manga_isbn.isbn = t_isbn.isbn
                            and t_isbn.result_yyyymm < to_char(current_timestamp, 'yyyy/mm')
                        )
                      WHERE
                          m_manga_isbn.invalid_flg = false
                      GROUP BY
                        m_manga_isbn.manga_title_code
                    ) a
                    ) AS c -- 作品毎の書籍データ
                    ON m_manga_title.manga_title_code = c.manga_title_code
                    """

    #書籍データ（巻単位）JOIN文
    joinSentenceForBookVolume =  """
                              LEFT JOIN
                              (
					                    SELECT
					                      a.manga_title_code
					                      {max_book_volume}
					                    FROM
					                    (
                                SELECT
                                a.manga_title_code
                                , a.isbn
                                , a.book_name
                                , a.total_sales_cnt
                                , seq
                                FROM
                                (
                                  SELECT
                                    m_manga_isbn.manga_title_code
                                    , m_manga_isbn.isbn
                                    , m_manga_isbn.book_name
                                    , t_isbn.total_sales_cnt::numeric::integer AS total_sales_cnt
                                    , book_issue_yyyymmdd
                                    , row_number() OVER (PARTITION BY manga_title_code ORDER BY book_issue_yyyymmdd {asc_or_desc},m_manga_isbn.isbn {asc_or_desc}) AS seq
                                  FROM
                                    m_manga_isbn
                                    LEFT JOIN t_isbn
                                      ON m_manga_isbn.isbn = t_isbn.isbn
                                          and t_isbn.result_yyyymm = (
                                            SELECT
                                              max(result_yyyymm)
                                            FROM
                                              t_isbn
                                            WHERE
                                              m_manga_isbn.isbn = t_isbn.isbn
                                              and t_isbn.result_yyyymm < to_char(current_timestamp, 'yyyy/mm')
                                          )
                                  WHERE
                                    m_manga_isbn.invalid_flg = false
                                    and m_manga_isbn.book_issue_yyyymmdd < to_char(current_timestamp, 'yyyy/mm')
                                ) a
                                ) a
					                    GROUP BY manga_title_code
					                    ORDER BY manga_title_code
					                    ) {alias} -- 巻毎の書籍データ
                              ON m_sakuhin_map.title_code = {alias}.manga_title_code
                              """

    # 詳細用SELECT文
    selectSentenceForDetail =  """
                      SELECT
                        COALESCE(m_sakuhin.key_visual_file_name, '') AS keyvisual_file_name
                        , m_sakuhin.sakuhin_code
                        , m_sakuhin.sakuhin_name
                        , m_sakuhin.sakuhin_kana_name
                        , COALESCE(m_sakuhin.overview, 'no data')
                        , m_sakuhin.release_yyyymm
                        , to_char(m_sakuhin.update_time, 'YYYY/MM/DD')
                        , COALESCE(m_sakuhin.foreign_window,'－')
                        , COALESCE(m_sakuhin.domestic_window,'－')
                        , COALESCE(m_sakuhin.memo,'－')
                      FROM
                        m_sakuhin
                      """

    #Sakuhinマスタの有効性確認用WHERE句
    whereValidMSakuhin = "WHERE TO_DATE(valid_start_yyyymmdd, 'YYYYMMDD') <= now() and now() <= TO_DATE(valid_end_yyyymmdd, 'YYYYMMDD') and m_sakuhin.invalid_flg = false and "

    """キービジュアル領域データの取得"""
    def selectRandomKeyVisual(self):

        sql =   """
                SELECT
                  m_sakuhin.sakuhin_code
                  , m_sakuhin.key_visual_file_name
                  , COALESCE(fact_1.sakuhin_tag_code, '') AS fact_1_code
                  , COALESCE(fact_1.sakuhin_tag_name, '') AS fact_1
                  , COALESCE(fact_2.sakuhin_tag_code, '') AS fact_2_code
                  , COALESCE(fact_2.sakuhin_tag_name, '') AS fact_2
                  , COALESCE(fact_3.sakuhin_tag_code, '') AS fact_3_code
                  , COALESCE(fact_3.sakuhin_tag_name, '') AS fact_3
                  , COALESCE(fact_4.sakuhin_tag_code, '') AS fact_4_code
                  , COALESCE(fact_4.sakuhin_tag_name, '') AS fact_4
                  , COALESCE(fact_5.sakuhin_tag_code, '') AS fact_5_code
                  , COALESCE(fact_5.sakuhin_tag_name, '') AS fact_5 
                FROM
                    m_sakuhin
                    LEFT JOIN m_sakuhin_map
                      ON m_sakuhin.sakuhin_code = m_sakuhin_map.sakuhin_code
                        and m_sakuhin_map.invalid_flg = false
                    LEFT JOIN m_manga_title
                      ON m_manga_title.manga_title_code = m_sakuhin_map.title_code
                        and m_manga_title.invalid_flg = false
                    LEFT JOIN m_media AS media
                      ON m_manga_title.media_code = media.media_code
                        and media.invalid_flg = false
                    LEFT JOIN m_sakuhin_tag_map
                      ON m_manga_title.tag_map_code = m_sakuhin_tag_map.tag_map_code
                        and m_sakuhin_tag_map.invalid_flg = false
                    LEFT JOIN m_core AS core_1
                      ON m_sakuhin_tag_map.core_code1 = core_1.core_code
                        and core_1.invalid_flg = false
                    LEFT JOIN m_core AS core_2
                      ON m_sakuhin_tag_map.core_code2 = core_2.core_code
                        and core_2.invalid_flg = false
                    LEFT JOIN m_sakuhin_tag AS fact_1
                      ON m_sakuhin_tag_map.sakuhin_tag_code1 = fact_1.sakuhin_tag_code
                        and fact_1.invalid_flg = false
                    LEFT JOIN m_sakuhin_tag AS fact_2
                      ON m_sakuhin_tag_map.sakuhin_tag_code2 = fact_2.sakuhin_tag_code
                        and fact_2.invalid_flg = false
                    LEFT JOIN m_sakuhin_tag AS fact_3
                      ON m_sakuhin_tag_map.sakuhin_tag_code3 = fact_3.sakuhin_tag_code
                        and fact_3.invalid_flg = false
                    LEFT JOIN m_sakuhin_tag AS fact_4
                      ON m_sakuhin_tag_map.sakuhin_tag_code4 = fact_4.sakuhin_tag_code
                        and fact_4.invalid_flg = false
                    LEFT JOIN m_sakuhin_tag AS fact_5
                      ON m_sakuhin_tag_map.sakuhin_tag_code5 = fact_5.sakuhin_tag_code
                        and fact_5.invalid_flg = false
                WHERE
                  m_sakuhin.sakuhin_code IN (SELECT sakuhin_code FROM m_sakuhin 
                              WHERE m_sakuhin.invalid_flg = false 
                                    and TO_DATE(valid_start_yyyymmdd, 'YYYYMMDD') <= now() 
                                    and now() <= TO_DATE(valid_end_yyyymmdd, 'YYYYMMDD')
                                    and key_visual_file_name != ''
                                    and key_visual_file_name is not null
                              ORDER BY random() LIMIT 8)
                """
        return self.select(sql)

    """タイトル名を検索"""
    def selectTitleNameAll(self):
      
        sql =   """
                SELECT
                  LEFT (m_sakuhin.sakuhin_kana_name, 1)
                  , m_sakuhin.sakuhin_name
                  , m_sakuhin.sakuhin_code 
                FROM
                  m_sakuhin
                WHERE
                  m_sakuhin.invalid_flg = false
                  and TO_DATE(valid_start_yyyymmdd, 'YYYYMMDD') <= now() and now() <= TO_DATE(valid_end_yyyymmdd, 'YYYYMMDD')
                ORDER BY
                  m_sakuhin.sakuhin_kana_name;

                """
        return self.select(sql)

    """年代別を検索"""
    def selectAgeNameAll(self):
      
        sql =   """
                SELECT
                  SUBSTRING(m_sakuhin.release_yyyymm,1,4) AS release_yyyymm
                  , m_sakuhin.sakuhin_name
                  , m_sakuhin.sakuhin_code 
                FROM
                  m_sakuhin
                WHERE
                  m_sakuhin.invalid_flg = false
                  and TO_DATE(m_sakuhin.valid_start_yyyymmdd, 'YYYYMMDD') <= now() and now() <= TO_DATE(m_sakuhin.valid_end_yyyymmdd, 'YYYYMMDD') 
                ORDER BY
                  m_sakuhin.release_yyyymm DESC;
                """
        return self.select(sql)

    """作品コードが存在するか確認"""
    def selectCountBySakuhinCode(self,sakuhin_code):
        sql = """
              SELECT
                count(sakuhin_code)
              FROM
                m_sakuhin
              {whereValidMSakuhin}
              sakuhin_code = %s
              """
        return self.selectWithParam(sql.format(whereValidMSakuhin=self.whereValidMSakuhin),[sakuhin_code])


    """作品コードよりSakuhinマスタ情報を取得する"""
    def selectDetailBySakuhinCode(self,sakuhin_code):
        # sqlを生成
        formatedSelectSentence = self.selectSentenceForDetail
        # WHERE句の生成
        whereSentence = self.whereValidMSakuhin
        whereSentence += "m_sakuhin.sakuhin_code = %s"

        sql = formatedSelectSentence + whereSentence
        return self.selectWithParam(sql,[sakuhin_code])

    """作品コードより分類タグが存在可否を取得する"""
    def selectBunruiTag(self,sakuhin_code):
      sql = """
            SELECT
              EXISTS ( SELECT * FROM m_anime_title LEFT JOIN m_sakuhin_map ON m_anime_title.anime_title_code = m_sakuhin_map.title_code WHERE m_sakuhin_map.sakuhin_code = m_sakuhin.sakuhin_code and m_anime_title.invalid_flg = false ) AS anime
              , EXISTS ( SELECT * FROM m_manga_title LEFT JOIN m_sakuhin_map ON m_manga_title.manga_title_code = m_sakuhin_map.title_code WHERE m_sakuhin_map.sakuhin_code = m_sakuhin.sakuhin_code and m_manga_title.invalid_flg = false ) AS manga
              , EXISTS ( SELECT * FROM m_app_title LEFT JOIN m_sakuhin_map ON m_app_title.app_title_code = m_sakuhin_map.title_code WHERE m_sakuhin_map.sakuhin_code = m_sakuhin.sakuhin_code and m_app_title.invalid_flg = false ) AS app
              , EXISTS ( SELECT * FROM m_game_title LEFT JOIN m_sakuhin_map ON m_game_title.game_title_code = m_sakuhin_map.title_code WHERE m_sakuhin_map.sakuhin_code = m_sakuhin.sakuhin_code and m_game_title.invalid_flg = false ) AS game
            FROM m_sakuhin
            """
      whereSentence = self.whereValidMSakuhin
      whereSentence += "m_sakuhin.sakuhin_code = %s"
      sql += whereSentence
      return self.selectWithParam(sql,[sakuhin_code])

    """
    書籍用のSELECT項目生成処理
    @param book_volume_num 書籍データ表示数
    @return SELECT項目
    """
    def createBookVolumeSelectItem(self,book_volume_num):
      book_volume = ""
      for i in range(book_volume_num):
        book_volume +=   ",b.book_name"+ str(book_volume_num-i)
        book_volume +=   ",to_char(b.total_sales_cnt_"+ str(book_volume_num-i) + ",'999,999,999,999,999')"
      return book_volume

    """
    書籍用のSELECT項目生成処理（巻毎の書籍サブクエリ用）
    @param book_volume_num 書籍データ表示数
    @return SELECT項目
    """
    def createBookVolumeSelectItemForSubQuery(self,book_volume_num):
      max_book_volume = ""
      for i in range(book_volume_num):
        max_book_volume += ",max(case a.seq when "+ str(book_volume_num-i) +" then a.isbn else null end) as isbn"+ str(book_volume_num-i)
        max_book_volume += ",max(case a.seq when "+ str(book_volume_num-i) +" then a.book_name else null end) as book_name"+ str(book_volume_num-i)
        max_book_volume += ",max(case a.seq when "+ str(book_volume_num-i) +" then a.total_sales_cnt else null end) as total_sales_cnt_"+ str(book_volume_num-i)
      return max_book_volume


    """キーワードをもとに作品を検索"""
    def selectByKeyword(self,keyword,book_volume_num):
        # SELECT句を生成
        formatedSelectSentence = ""
        formatedSelectSentence = self.selectSentence.format(book_volume = "")
        # FROM句を生成
        formatedFromSentence = ""
        formatedFromSentence += self.fromSentence
        # WHERE句の生成
        params = []
        whereSentence = self.whereValidMSakuhin
        whereSentence +=  """
                          (
                          m_sakuhin.sakuhin_name LIKE %s
                          or m_sakuhin.sakuhin_kana_name LIKE %s 
                          or m_sakuhin.keyword LIKE %s
                          )
                          """
        for x in range(3):
          params.append("%" + keyword + "%")

        sql = formatedSelectSentence + formatedFromSentence + whereSentence + 'ORDER BY m_sakuhin.sakuhin_kana_name COLLATE "ja_JP.utf8" ASC'
        return self.selectWithParam(sql,params)

    """
    類似検索条件をもとに作品を検索
    (ユーザ入力が全未入力の場合の全検索もここで行う)
    """
    def selectBySimilarCondition(self,inputContents,book_volume_num):

      #キーワード入力有 且つ 類似入力無の場合、類似検索は行わない
      if self.isOnlyKeyword(inputContents):
        return []

      # SELECT句を生成
      formatedSelectSentence = ""
      book_volume = self.createBookVolumeSelectItem(book_volume_num)
      formatedSelectSentence = self.selectSentence.format(book_volume = book_volume)
      # FROM句を生成
      formatedFromSentence = ""
      max_book_volume = self.createBookVolumeSelectItemForSubQuery(book_volume_num)
      formatedFromSentence += self.fromSentence
      formatedFromSentence += self.joinSentenceForBookVolume.format(max_book_volume = max_book_volume, asc_or_desc = "DESC", alias = "b")
      ## WHERE句生成
      params = []
      whereSentence = self.createWhereSentenceForSimilarCondition(params,inputContents)
      # where句を調整(作品公開有効期間_開始・終了の条件追加と不要な末尾"and"を削除)
      whereSentence = (self.whereValidMSakuhin + whereSentence)[::-1].replace("dna" , "" , 1)[::-1]

      sql = formatedSelectSentence + formatedFromSentence + whereSentence
      return self.selectWithParam(sql,params)

    """
    ユーザ入力がキーワード入力のみか判定
    @param inputContents ユーザ入力情報
    @return true:キーワード入力のみ、false:キーワード入力なし
    """
    def isOnlyKeyword(self,inputContents):
      if (''.join(inputContents.keyword) != ''
          and not inputContents.category
          and not inputContents.core
          and not inputContents.media
          and not inputContents.fact_tag
          and not (inputContents.start_date and ''.join(inputContents.start_date) != '--------')
          and not (inputContents.end_date and ''.join(inputContents.end_date) != '--------')
          ):
        return True
      else:
        return False

    """
    類似検索用のWHERE句生成処理
    @param params SQLのパラメータ
    @param inputContents ユーザ入力情報
    @return WHERE句
    """
    def createWhereSentenceForSimilarCondition(self,params, inputContents):
      whereSentence = ""
      # 分類
      for i in range(len(inputContents.category)):
        if i == 0 :
          whereSentence += "("
        # アニメ
        if inputContents.category[i] == "0":
          whereSentence += "EXISTS ( SELECT * FROM m_anime_title WHERE anime_title_code = m_sakuhin_map.title_code and invalid_flg = false ) = true"
        # マンガ
        if inputContents.category[i] == "1":
          whereSentence += "EXISTS ( SELECT * FROM m_manga_title WHERE manga_title_code = m_sakuhin_map.title_code and invalid_flg = false ) = true"
        # アプリ
        if inputContents.category[i] == "2":
          whereSentence += "EXISTS ( SELECT * FROM m_app_title WHERE app_title_code = m_sakuhin_map.title_code and invalid_flg = false ) = true"
        # ゲーム
        if inputContents.category[i] == "3":
          whereSentence += "EXISTS ( SELECT * FROM m_game_title WHERE game_title_code = m_sakuhin_map.title_code and invalid_flg = false ) = true"
        if i != len(inputContents.category)-1:
          whereSentence += " or "
        else:
          whereSentence += ") and "
      # コア
      for i in range(len(inputContents.core)):
        if i == 0 :
          whereSentence += "("
        for x in range(2):
          params.append(inputContents.core[i])
        whereSentence += "core_1.core_code = %s or "
        whereSentence += "core_2.core_code = %s"
        if i != len(inputContents.core)-1:
          whereSentence += " or "
        else:
          whereSentence += ") and "
      # 掲載媒体
      for i in range(len(inputContents.media)):
        if i == 0 :
          whereSentence += "("
        params.append(inputContents.media[i])
        whereSentence += "media.media_code = %s"
        if i != len(inputContents.media)-1:
          whereSentence += " or "
        else:
          whereSentence += ") and "
      # 事実タグ
      for i in range(len(inputContents.fact_tag)):
        if i == 0 :
          whereSentence += "("
        for x in range(5):
          params.append(inputContents.fact_tag[i])
        whereSentence += "COALESCE(fact_1.sakuhin_tag_code, '') = %s or "
        whereSentence += "COALESCE(fact_2.sakuhin_tag_code, '') = %s or "
        whereSentence += "COALESCE(fact_3.sakuhin_tag_code, '') = %s or "
        whereSentence += "COALESCE(fact_4.sakuhin_tag_code, '') = %s or "
        whereSentence += "COALESCE(fact_5.sakuhin_tag_code, '') = %s "
        if i != len(inputContents.fact_tag)-1:
          whereSentence += " or "
        else:
          whereSentence += ") and "
      # 展開時期
      start_date = ''.join(inputContents.start_date)
      end_date = ''.join(inputContents.end_date)
      
      # 展開時期のユーザ入力がない場合、展開時期のWHERE句を追加しない
      if (not (start_date == "--------" and end_date == "--------")
          and not (start_date == "" and end_date == "")):

        # 「-」を補完(FROM：19500101)
        if start_date[0:4] == "----" :
            start_date = "1950" + start_date[4:8]
        if start_date[4:6] == "--":
            start_date = start_date[0:4] + "01" + start_date[6:8]
        if start_date[6:8] == "--":
            start_date = start_date[0:6] + "01"

        # 「-」を補完(TO：2099)
        if end_date[0:4] == "----" :
            end_date = "2099" + end_date[4:8]
        if end_date[4:6] == "--":
            end_date = end_date[0:4] + "12" + end_date[6:8]
        if end_date[6:8] == "--":
            end_date = end_date[0:6] + "31"

        params.append(start_date)
        params.append(end_date)
        whereSentence  += """
                          (
                          %s <= TO_DATE(release_yyyymm,'yyyymmdd')
                          and TO_DATE(release_yyyymm,'yyyymmdd') <= %s
                          ) and
                          """
      return whereSentence

    """作品コードが存在するか確認"""
    def selectCompareCountBySakuhinCode(self,sakuhin_code_list):
        value = tuple(sakuhin_code_list)
        params = {'sakuhin_code_list': value}
        sql = """
          SELECT
            count(sakuhin_code)
          FROM m_sakuhin
          WHERE 
              m_sakuhin.sakuhin_code in %(sakuhin_code_list)s
          AND m_sakuhin.invalid_flg = false
          AND m_sakuhin.valid_start_yyyymmdd <= to_char(now(),'yyyymmdd')
          AND to_char(now(),'yyyymmdd') <= m_sakuhin.valid_end_yyyymmdd
          """
        return self.selectWithParam(sql,params)

    """作品コードListより作品名を取得する"""
    def selectCompareSakuhinName(self,sakuhin_code_list):
      value = tuple(sakuhin_code_list)
      params = {'sakuhin_code_list': value}
      sql = """
		      SELECT
            sakuhin_code
            , sakuhin_name
          FROM m_sakuhin
          WHERE
            m_sakuhin.sakuhin_code in %(sakuhin_code_list)s
            AND m_sakuhin.invalid_flg = false
            AND m_sakuhin.valid_start_yyyymmdd <= to_char(now(),'yyyymmdd')
            AND to_char(now(),'yyyymmdd') <= m_sakuhin.valid_end_yyyymmdd
          ORDER BY
            sakuhin_code
          """
      return self.selectWithParam(sql,params)

    """作品コードListよりTwiter情報を取得する"""
    def selectCompareTwitter(self,sakuhin_code_list):
      value = tuple(sakuhin_code_list)
      params = {'sakuhin_code_list': value} 
      sql = """
        	  WITH month_info AS 
          	(SELECT
          	   twitterInfo.twitter_id
          	  , twitterInfo.twitter_code
          	  , twitterInfo.user_name
              , twitterInfo.sakuhin_code
          	  , max((case when twitterInfo.result_yyyymm  < to_char(current_timestamp,'yyyymm') 
                then twitterInfo.result_yyyymm else '' end)) AS new_month
          	  , to_char(current_timestamp + '-3 months','yyyymm') AS three_month
              , to_char(current_timestamp + '-12 months','yyyymm') AS one_year
            FROM m_sakuhin sakuhin
            LEFT JOIN (
              SELECT 
                t_twitter.twitter_id
                , t_twitter.result_yyyymm
                , m_twitter.twitter_code
                , m_twitter.user_name
                , sakuhin_map.sakuhin_code
              FROM m_sakuhin_map sakuhin_map
              INNER JOIN m_twitter
              ON sakuhin_map.title_code = m_twitter.twitter_code
                AND m_twitter.invalid_flg = false
                AND m_twitter.main_account_flg = true
              INNER JOIN t_twitter
              ON m_twitter.twitter_id = t_twitter.twitter_id
              WHERE
                sakuhin_map.title_category_code = '06'
                AND sakuhin_map.invalid_flg = false
              )twitterInfo
            ON sakuhin.sakuhin_code = twitterInfo.sakuhin_code
              AND sakuhin.invalid_flg = false
            GROUP BY twitterInfo.twitter_id
              , twitterInfo.twitter_code
              , twitterInfo.user_name
              , twitterInfo.sakuhin_code
            ORDER BY
              twitterInfo.twitter_code)
		
            SELECT 
              sakuhin.sakuhin_code
              , sakuhin.sakuhin_name
              , now_follower.follower_cnt::numeric::integer AS followers_latest
              , three_month_follower.follower_cnt::numeric::integer AS followers_3months_ago
              , one_year_follower.follower_cnt::numeric::integer AS followers_1year_ago
              , month_info.user_name
              , month_info.twitter_id
            FROM m_sakuhin sakuhin
            LEFT JOIN month_info
            ON sakuhin.sakuhin_code = month_info.sakuhin_code
            LEFT JOIN 
              t_twitter now_follower
            ON now_follower.twitter_id = month_info.twitter_id
              AND now_follower.result_yyyymm = month_info.new_month
            LEFT JOIN 
              t_twitter three_month_follower
            ON three_month_follower.twitter_id = month_info.twitter_id
              AND three_month_follower.result_yyyymm = month_info.three_month
            LEFT JOIN 
              t_twitter one_year_follower
            ON one_year_follower.twitter_id = month_info.twitter_id
              AND one_year_follower.result_yyyymm = month_info.one_year
		        WHERE
          	  sakuhin.sakuhin_code in %(sakuhin_code_list)s
              AND sakuhin.invalid_flg = false
              AND sakuhin.valid_start_yyyymmdd <= to_char(now(),'yyyymmdd')
              AND to_char(now(),'yyyymmdd') <= sakuhin.valid_end_yyyymmdd
            ORDER BY sakuhin_code
          """
      return self.selectWithParam(sql,params)

    """作品コードListよりマンガ情報を取得する"""
    def selectCompareManga(self,sakuhin_code_list):
      value = tuple(sakuhin_code_list)
      params = {'sakuhin_code_list': value}

      sql = """
          SELECT
            sakuhin.sakuhin_code
            , sakuhin.sakuhin_name
            , ts.total_sales::numeric::integer total_sales
            , first_isbn.first_total_sales::numeric::integer first_total_sales
            , latest_isbn.last_total_sales::numeric::integer last_total_sales
            , round(ts.total_sales / isbn_cnt.isbn_cnt, 0)::numeric::integer avg
            , first_isbn.isbn firstisbn
            , latest_isbn.isbn latestisbn
            , manga.manga_title_name manga_name
            , manga.manga_title_code manga_code
          FROM m_sakuhin sakuhin
		      LEFT JOIN m_sakuhin_map sakuhin_map
		      ON sakuhin.sakuhin_code = sakuhin_map.sakuhin_code
		        AND sakuhin_map.title_category_code = '01'
			      AND sakuhin_map.invalid_flg = false
		      LEFT JOIN m_manga_title manga
		      ON sakuhin_map.title_code = manga.manga_title_code
            AND manga.invalid_flg = false
          LEFT JOIN ( 
              SELECT
                m.manga_title_code
                , sum(t.total_sales) total_sales 
              FROM m_manga_isbn m
              INNER JOIN ( 
                SELECT
                  isbn
                  , max(total_sales_cnt) total_sales 
                FROM t_isbn 
                WHERE t_isbn.result_yyyymm < to_char(current_timestamp, 'yyyymm')
                GROUP BY isbn) t 
              ON t.isbn = m.isbn
                AND m.invalid_flg = FALSE
              GROUP BY manga_title_code
            ) ts
          ON ts.manga_title_code = manga.manga_title_code
          LEFT JOIN ( 
 			        SELECT
                m.manga_title_code
                , m.isbn
                , (SELECT max(total_sales_cnt) FROM t_isbn t WHERE t.isbn = m.isbn AND result_yyyymm < to_char(current_timestamp, 'yyyymm') ) first_total_sales
              FROM m_manga_isbn m
              WHERE
                (manga_title_code, isbn) IN ( 
                  SELECT
                    manga_title_code
                    , min(isbn) 
                  FROM m_manga_isbn m
                  WHERE
         	           (manga_title_code, book_issue_yyyymmdd) IN ( 
	                      SELECT
	                        manga_title_code
	                        , min(book_issue_yyyymmdd) 
	                      FROM  m_manga_isbn m
						            WHERE m.invalid_flg = false
						              AND book_issue_yyyymmdd < to_char(current_timestamp, 'yyyymmdd')
	                      GROUP BY m.manga_title_code
	                      )
				          AND m.invalid_flg = false
				          GROUP BY m.manga_title_code
				          ORDER BY m.manga_title_code)
              AND m.invalid_flg = false
              ) first_isbn 
            ON first_isbn.manga_title_code = manga.manga_title_code
            LEFT JOIN ( 
          	  SELECT
                m.manga_title_code
                , m.isbn
                , (SELECT max(total_sales_cnt) FROM t_isbn WHERE isbn = m.isbn AND result_yyyymm < to_char(current_timestamp, 'yyyymm')) last_total_sales 
              FROM m_manga_isbn m 
              WHERE
                (manga_title_code, isbn) IN ( 
                    SELECT
                      manga_title_code
                      , max(isbn) 
                    FROM m_manga_isbn m
                    WHERE
                      (manga_title_code, book_issue_yyyymmdd) IN ( 
                        SELECT
	                        manga_title_code
	                        , max(book_issue_yyyymmdd) 
              	        FROM m_manga_isbn m
						            WHERE  m.invalid_flg = false
						              AND book_issue_yyyymmdd < to_char(current_timestamp, 'yyyymmdd')
	                      GROUP BY manga_title_code) 
					          AND m.invalid_flg = false 
                    GROUP BY manga_title_code)
              AND m.invalid_flg = false
              )latest_isbn 
            ON latest_isbn.manga_title_code = manga.manga_title_code
            LEFT JOIN ( 
			        SELECT 
                m.manga_title_code
               , count(DISTINCT t.isbn) isbn_cnt 
              FROM t_isbn t
			          INNER JOIN  m_manga_isbn m
			          ON m.isbn = t.isbn
			        WHERE t.result_yyyymm < to_char(current_timestamp, 'yyyymm')
					    AND m.invalid_flg = false
              GROUP BY manga_title_code
			        ) isbn_cnt
            ON isbn_cnt.manga_title_code = manga.manga_title_code
          WHERE
            sakuhin.sakuhin_code in %(sakuhin_code_list)s
            AND sakuhin.invalid_flg = false
            AND sakuhin.valid_start_yyyymmdd <= to_char(now(),'yyyymmdd')
            AND to_char(now(),'yyyymmdd') <= sakuhin.valid_end_yyyymmdd
          ORDER BY
            COALESCE(total_sales,0) DESC 
            , COALESCE(first_total_sales,0) DESC
            , COALESCE(last_total_sales,0) DESC
          """
      return self.selectWithParam(sql,params)

    """作品コードListよりゲーム情報を取得する"""
    def selectCompareGame(self,sakuhin_code_list):
      value = tuple(sakuhin_code_list)
      params = {'sakuhin_code_list': value}
      sql = """
   	      SELECT
			      sakuhin.sakuhin_code
          	, sakuhin.sakuhin_name
            , game.game_title_name
          	, game.platform_name
          	, game.hanbai_company_name
            , game.release_yyyymmdd
            , t.total_sales_cnt::numeric::integer
            , game.game_title_code
          FROM m_sakuhin sakuhin
          LEFT JOIN m_sakuhin_map sakuhin_map
          ON sakuhin.sakuhin_code = sakuhin_map.sakuhin_code
		        AND sakuhin_map.title_category_code = '05'
			      AND sakuhin_map.invalid_flg = FALSE
          LEFT JOIN m_game_title game
          ON sakuhin_map.title_code = game.game_title_code
		  	    AND game.invalid_flg = FALSE
		      LEFT JOIN t_game t
		      ON game.game_title_name = t.game_title_name
		  	    AND game.platform_name = t.platform_name
			      AND game.release_yyyymmdd = t.release_yyyymmdd
          	AND t.result_yyyymm = ( 
              SELECT
                max(result_yyyymm) 
              FROM t_game t
              WHERE
			  	      game.game_title_name = t.game_title_name
			  	      AND game.platform_name = t.platform_name
				        AND game.release_yyyymmdd = t.release_yyyymmdd
                AND t.result_yyyymm < to_char(current_timestamp, 'yyyymm')
          	    )
            WHERE
          	  sakuhin.sakuhin_code in %(sakuhin_code_list)s
              AND sakuhin.invalid_flg = false
              AND sakuhin.valid_start_yyyymmdd <= to_char(now(),'yyyymmdd')
              AND to_char(now(),'yyyymmdd') <= sakuhin.valid_end_yyyymmdd
            ORDER BY
              COALESCE(t.total_sales_cnt,0) desc
              , game.game_title_code
            """
      return self.selectWithParam(sql,params)

    """作品コードListよりアプリ情報を取得する"""
    def selectCompareApp(self,sakuhin_code_list):
      value = tuple(sakuhin_code_list)
      params = {'sakuhin_code_list': value}
      sql = """
		    SELECT
        	sakuhin.sakuhin_code
        	, sakuhin.sakuhin_name
        	, app.app_title_name
		      , app.app_id_ios
			    , app.app_id_android
        	, app.hanbai_company_name
	        , app.service_start_yyyymmdd
	        , t_app.total_sales::numeric::integer AS total_sales
	        , t_app.total_download_cnt::numeric::integer  AS total_download_cnt
	        , t_app.avg_sales::numeric::integer AS avg_sales
	        , t_app.avg_download_cnt::numeric::integer AS avg_download_cnt
          , app.app_title_code
        FROM m_sakuhin sakuhin
		    LEFT JOIN m_sakuhin_map sakuhin_map
		    ON sakuhin.sakuhin_code = sakuhin_map.sakuhin_code
		    	AND sakuhin_map.title_category_code = '04'
		    	AND sakuhin_map.invalid_flg = FALSE
		    LEFT JOIN m_app_title app
		    ON sakuhin_map.title_code = app.app_title_code
		    	AND app.invalid_flg = FALSE
		    LEFT JOIN
          (
		    	  SELECT
        	    app_title_name
              , sum(monthly_sales_gaku)::numeric::integer AS total_sales
			        , round(sum(monthly_sales_gaku) / count(DISTINCT result_yyyymm),0)::numeric::integer AS avg_sales
			        , sum(download_cnt)::numeric::integer AS total_download_cnt
		          , round(sum(download_cnt) / count(DISTINCT result_yyyymm),0)::numeric::integer AS avg_download_cnt
          	FROM t_app
       		  WHERE result_yyyymm < to_char(current_timestamp, 'yyyymm')
		        GROUP BY
			 	      app_title_name 
			      ) AS t_app
		    ON app.app_title_name = t_app.app_title_name
		    WHERE sakuhin.sakuhin_code in %(sakuhin_code_list)s
        AND sakuhin.invalid_flg = FALSE
        AND sakuhin.valid_start_yyyymmdd <= to_char(now(),'yyyymmdd')
        AND to_char(now(),'yyyymmdd') <= sakuhin.valid_end_yyyymmdd
        ORDER BY 
          COALESCE(total_sales,0) desc
          , COALESCE(total_download_cnt,0) desc
          , COALESCE(avg_sales,0) desc
          , COALESCE(avg_download_cnt,0) desc
          , service_start_yyyymmdd
      """
      return self.selectWithParam(sql,params)