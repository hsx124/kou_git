from ipdds_app.dao.dao_main import DaoMain
import datetime

class DaoMIp(DaoMain):

    # 検索用SELECT文
    selectSentence =  """
                      SELECT
                      COALESCE(m_ip.key_visual_file_name, '') AS keyvisual_file_name
                      , m_ip.ip_code
                      , m_ip.ip_name
                      , m_ip.ip_kana_name
                      , COALESCE(m_ip.overview, 'no data')
                      , EXISTS ( SELECT * FROM m_wiki WHERE ip_code = m_ip.ip_code and is_invalid = false ) AS anime 
                      , EXISTS ( SELECT * FROM m_manga_db WHERE ip_code = m_ip.ip_code and is_invalid = false ) AS manga
                      , EXISTS ( SELECT * FROM m_mobile_app WHERE ip_code = m_ip.ip_code and is_invalid = false ) AS app
                      , EXISTS ( SELECT * FROM m_pkg_soft WHERE ip_code = m_ip.ip_code and is_invalid = false ) AS game
                      , EXISTS ( SELECT * FROM m_manga_db WHERE ip_code = m_ip.ip_code and m_manga_db.award_history_anime_film = true and is_invalid = false ) AS theater
                      , COALESCE(core_1.core_code, '')
                      , COALESCE(core_1.core_name, '')
                      , COALESCE(core_2.core_code, '')
                      , COALESCE(core_2.core_name, '')
                      , COALESCE(media.media_code, '')
                      , COALESCE(media.media_name, '')
                      , m_manga_db.is_fiction
                      , COALESCE(fact_1.fact_tag_code, '')
                      , COALESCE(fact_1.fact_tag_name, '')
                      , COALESCE(fact_2.fact_tag_code, '')
                      , COALESCE(fact_2.fact_tag_name, '')
                      , COALESCE(fact_3.fact_tag_code, '')
                      , COALESCE(fact_3.fact_tag_name, '')
                      , COALESCE(fact_4.fact_tag_code, '')
                      , COALESCE(fact_4.fact_tag_name, '')
                      , COALESCE(fact_5.fact_tag_code, '')
                      , COALESCE(fact_5.fact_tag_name, '')
                      , to_char(m_ip.release_date, 'YYYY/MM/DD')
                      , to_char(m_ip.update_date, 'YYYY/MM/DD')

                      , c.sum
                      , c.avg
                      {imp}
                      {book_volume}
                      """
    # 検索用FROM文
    fromSentence =  """
                    FROM
                    m_ip 
                    LEFT JOIN m_manga_db 
                      ON m_manga_db.ip_code = m_ip.ip_code 
                         and m_manga_db.is_invalid = false
                    LEFT JOIN m_core AS core_1 
                      ON m_manga_db.core_1 = core_1.core_code 
                         and core_1.is_invalid = false
                    LEFT JOIN m_core AS core_2 
                      ON m_manga_db.core_2 = core_2.core_code 
                         and core_2.is_invalid = false
                    LEFT JOIN m_media AS media 
                      ON m_manga_db.publication_media = media.media_code 
                         and media.is_invalid = false
                    LEFT JOIN m_fact_tag AS fact_1 
                      ON m_manga_db.fact_tag_1 = fact_1.fact_tag_code 
                         and fact_1.is_invalid = false
                    LEFT JOIN m_fact_tag AS fact_2 
                      ON m_manga_db.fact_tag_2 = fact_2.fact_tag_code 
                         and fact_2.is_invalid = false
                    LEFT JOIN m_fact_tag AS fact_3 
                      ON m_manga_db.fact_tag_3 = fact_3.fact_tag_code 
                         and fact_3.is_invalid = false
                    LEFT JOIN m_fact_tag AS fact_4 
                      ON m_manga_db.fact_tag_4 = fact_4.fact_tag_code 
                         and fact_4.is_invalid = false
                    LEFT JOIN m_fact_tag AS fact_5 
                      ON m_manga_db.fact_tag_5 = fact_5.fact_tag_code 
                         and fact_5.is_invalid = false
                    LEFT JOIN
                    (
                      SELECT
                       a.imp_category_code
                       {max_imp}
                      FROM
                      (
                        SELECT
                         imp_category_code
                         , m_imp.imp_code
                         , m_imp.imp_name
                         , row_number() OVER (PARTITION BY imp_category_code ORDER BY m_imp.imp_code ASC) AS seq
                        FROM
                         m_imp_category
                        LEFT JOIN
                         m_imp
                        ON m_imp_category.imp_code = m_imp.imp_code
                           and m_imp.is_invalid = false
                        WHERE
                        imp_flag = true
                        and m_imp_category.is_invalid = false
                      )AS a
                      GROUP BY
                        a.imp_category_code
                    )AS a --印象
                    ON m_manga_db.imp_category_code = a.imp_category_code
                    LEFT JOIN
                    (
                    SELECT
                     a.ip_code
                     , a.sum
                     , a.avg 
                    FROM
                     ( 
                       SELECT
                         m_book.ip_code
                         , to_char(sum(t_book.qty_total_sales_2),'999,999,999,999,999') AS sum
                         , to_char(avg(COALESCE(t_book.qty_total_sales_2,0)),'999,999,999,999,999') AS avg 
                       FROM
                         m_book 
                         INNER JOIN t_book
                           ON m_book.isbn = t_book.isbn 
                           and t_book.result_yyyymm = ( 
                           SELECT
                             max(result_yyyymm) 
                           FROM
                             t_book
                           WHERE
                             m_book.isbn = t_book.isbn
                             and t_book.result_yyyymm < to_char(current_timestamp, 'yyyy/mm')
                         ) 
                       WHERE
                          m_book.is_invalid = false
                       GROUP BY
                         m_book.ip_code
                     ) a
                    ) AS c -- IP毎の書籍データ
                    ON m_manga_db.ip_code = c.ip_code
                    
                    """

    #書籍データ（巻単位）JOIN文
    joinSentenceForBookVolume =  """
                              LEFT JOIN
                              (
					                    SELECT
					                      a.ip_code
					                      {max_book_volume}
					                    FROM
					                    (
                                SELECT
                                 a.ip_code
                                 , a.isbn
                                 , a.book_name
                                 , a.qty_total_sales_2
                                 , seq
                                FROM
                                 (
                                   SELECT
                                     m_book.ip_code
                                     , m_book.isbn
                                     , m_book.book_name
                                     , t_book.qty_total_sales_2::numeric::integer AS qty_total_sales_2
                                     , book_issue_date
                                     , row_number() OVER (PARTITION BY ip_code ORDER BY book_issue_date {asc_or_desc},m_book.isbn {asc_or_desc}) AS seq
                                   FROM
                                     m_book
                                     LEFT JOIN t_book
                                       ON m_book.isbn = t_book.isbn
                                          and t_book.result_yyyymm = (
                                            SELECT
                                              max(result_yyyymm)
                                            FROM
                                              t_book
                                            WHERE
                                              m_book.isbn = t_book.isbn
                                              and t_book.result_yyyymm < to_char(current_timestamp, 'yyyy/mm')
                                          )
                                   WHERE
                                     m_book.is_invalid = false
                                     and to_char(m_book.book_issue_date, 'yyyy/mm') < to_char(current_timestamp, 'yyyy/mm')
                                 ) a
                                ) a
					                    GROUP BY ip_code
					                    ORDER BY ip_code
					                    ) {alias} -- 巻毎の書籍データ
                              ON m_ip.ip_code = {alias}.ip_code
                              """
    
    #IPマスタの有効性確認用WHERE句
    whereValidMIp = "WHERE valid_start_date <= now() and now() <= valid_end_date and m_ip.is_invalid = false and "

    # 詳細用SELECT項目
    selectItemForDetail = """
                          ,COALESCE(m_manga_db.also_boughts_1,'')
                          ,COALESCE(m_manga_db.also_boughts_2,'')
                          ,COALESCE(m_manga_db.also_boughts_3,'')
                          ,COALESCE(m_manga_db.also_boughts_4,'')
                          ,COALESCE(m_manga_db.also_boughts_5,'')
                          ,COALESCE(m_manga_db.also_boughts_6,'')
                          ,COALESCE(m_manga_db.also_boughts_7,'')
                          ,COALESCE(m_manga_db.also_boughts_8,'')
                          ,COALESCE(m_manga_db.also_boughts_9,'')
                          ,COALESCE(m_manga_db.also_boughts_10,'')
                          ,COALESCE(m_manga_db.also_boughts_11,'')
                          ,COALESCE(m_manga_db.also_boughts_12,'')
                          ,COALESCE(m_manga_db.also_boughts_13,'')
                          ,COALESCE(m_manga_db.also_boughts_14,'')
                          ,COALESCE(m_manga_db.also_boughts_15,'')
                          ,COALESCE(m_ip.foreign_window,'－')
                          ,COALESCE(m_ip.domestic_window,'－')
                          ,COALESCE(m_ip.memo,'－')
                          ,COALESCE(m_manga_db.author,'　－　')
                          ,COALESCE(m_manga_db.artist,'　－　')
                          ,COALESCE(m_manga_db.original_author,'　－　')
                          ,COALESCE(m_manga_db.past_series,'－')
                          ,COALESCE(m_manga_db.author_note,'－')
                          ,COALESCE(m_manga_db.publisher,'－')
                          ,COALESCE(m_manga_db.series_start_yyyymm,'－')
                          ,case m_manga_db.series_end_flag when true then '終' else '　' end
                          ,COALESCE(m_manga_db.award_history,'－')
                          ,COALESCE(m_manga_db.original_author_past_art,'－')
                          ,case m_manga_db.past_series_tv_anime when true then '〇' else '' end
                          ,case m_manga_db.past_series_live_action_drama when true then '〇' else '' end
                          ,case m_manga_db.past_series_live_action_film when true then '〇' else '' end
                          ,case m_manga_db.past_series_anime_film when true then '〇' else '' end
                          ,case m_manga_db.past_series_stage when true then '〇' else '' end
                          ,case m_manga_db.past_series_game when true then '〇' else '' end
                          ,case m_manga_db.past_series_novel when true then '〇' else '' end
                          ,case m_manga_db.past_series_other when true then '〇' else '' end
                          ,case m_manga_db.web_app_line_manga when true then '〇' else '' end
                          ,case m_manga_db.web_app_comico when true then '〇' else '' end
                          ,case m_manga_db.web_app_manga_one when true then '〇' else '' end
                          ,case m_manga_db.web_app_manga_one_box when true then '〇' else '' end
                          ,case m_manga_db.web_app_shounen_jump_plus when true then '〇' else '' end
                          ,case m_manga_db.web_app_ganma when true then '〇' else '' end
                          ,case m_manga_db.web_app_gangan_pixiv when true then '〇' else '' end
                          ,case m_manga_db.web_app_other when true then '〇' else '' end
                          ,twitter_latest.twitter_id
                          ,'https://twitter.com/' || COALESCE(twitter_latest.user_name,'')
                          ,twitter_latest.account_name
                          ,to_char(twitter_latest.follower_count,'999,999,999,999,999')
                          ,to_char(twitter_3months_ago.follower_count,'999,999,999,999,999')
                          ,to_char(twitter_1year_ago.follower_count,'999,999,999,999,999')
                          , EXISTS ( SELECT * FROM m_manga_db WHERE ip_code = m_ip.ip_code and is_invalid = false ) as is_exist_manga_db
                          , EXISTS ( SELECT * FROM m_gender_ratio WHERE ip_code = m_ip.ip_code and is_invalid = false ) as is_exist_gender_ratio
                          , EXISTS ( SELECT * FROM m_book WHERE ip_code = m_ip.ip_code and is_invalid = false ) as is_exist_book
                          , EXISTS ( SELECT * FROM m_twitter WHERE ip_code = m_ip.ip_code and is_invalid = false ) as is_exist_twitter 
                      , m_manga_db.published_num
                      , m_gender_ratio.male
                      , m_gender_ratio.female
                      , m_gender_ratio.total
                      , m_gender_ratio.male_lteq10
                      , m_gender_ratio.male_11to15
                      , m_gender_ratio.male_16to20
                      , m_gender_ratio.male_21to25
                      , m_gender_ratio.male_26to30
                      , m_gender_ratio.male_31to35
                      , m_gender_ratio.male_36to40
                      , m_gender_ratio.male_41to45
                      , m_gender_ratio.male_46to50
                      , m_gender_ratio.male_gteq51
                      , m_gender_ratio.female_lteq10
                      , m_gender_ratio.female_11to15
                      , m_gender_ratio.female_16to20
                      , m_gender_ratio.female_21to25
                      , m_gender_ratio.female_26to30
                      , m_gender_ratio.female_31to35
                      , m_gender_ratio.female_36to40
                      , m_gender_ratio.female_41to45
                      , m_gender_ratio.female_46to50
                      , m_gender_ratio.female_gteq51
                          """
    #詳細用JOIN句
    fromSentenceForDetail = """
                            LEFT JOIN
                            (
                              SELECT 
                                m_twitter.twitter_id
                                ,m_twitter.user_name
                                ,m_twitter.ip_code
                                ,m_twitter.account_name
                                ,t_twitter.follower_count
                              FROM t_twitter
                              LEFT JOIN m_twitter
                               ON t_twitter.twitter_id = m_twitter.twitter_id
                              WHERE m_twitter.ip_code = %s
                                    and to_char(t_twitter.create_date,'yyyy/mm') < to_char(current_timestamp,'yyyy/mm')
                                    and m_twitter.is_invalid = false
                              ORDER BY m_twitter.twitter_create_date ,t_twitter.create_date DESC
                              LIMIT 1
                            ) twitter_latest
                            ON m_ip.ip_code = twitter_latest.ip_code
                            LEFT JOIN
                            (
                              SELECT 
                                m_twitter.ip_code
                                ,t_twitter.follower_count
                              FROM t_twitter
                              LEFT JOIN m_twitter
                               ON t_twitter.twitter_id = m_twitter.twitter_id
                              WHERE m_twitter.ip_code = %s
                                    and to_char(t_twitter.create_date,'yyyy/mm') = to_char(current_timestamp - interval '3 months','yyyy/mm')
                                    and m_twitter.is_invalid = false
                              ORDER BY m_twitter.twitter_create_date
                              LIMIT 1
                            ) twitter_3months_ago
                            ON  m_ip.ip_code = twitter_3months_ago.ip_code
                            LEFT JOIN
                            (
                              SELECT 
                                m_twitter.ip_code
                                ,t_twitter.follower_count
                              FROM t_twitter
                              LEFT JOIN m_twitter
                               ON t_twitter.twitter_id = m_twitter.twitter_id
                              WHERE m_twitter.ip_code = %s
                                    and to_char(t_twitter.create_date,'yyyy/mm') = to_char(current_timestamp - interval '1 years','yyyy/mm')
                                    and m_twitter.is_invalid = false
                              ORDER BY m_twitter.twitter_create_date
                              LIMIT 1
                            ) twitter_1year_ago
                            ON m_ip.ip_code = twitter_1year_ago.ip_code
                             LEFT JOIN m_gender_ratio
                              ON m_ip.ip_code = m_gender_ratio.ip_code
                                and m_gender_ratio.is_invalid = false
                            """  

    """キービジュアル領域データの取得"""
    def selectRandomKeyVisual(self):

        sql =   """
                SELECT
                  m_ip.ip_code
                  , m_ip.key_visual_file_name
                  , COALESCE(fact_1.fact_tag_code, '') AS fact_1_code
                  , COALESCE(fact_1.fact_tag_name, '') AS fact_1
                  , COALESCE(fact_2.fact_tag_code, '') AS fact_2_code
                  , COALESCE(fact_2.fact_tag_name, '') AS fact_2
                  , COALESCE(fact_3.fact_tag_code, '') AS fact_3_code
                  , COALESCE(fact_3.fact_tag_name, '') AS fact_3
                  , COALESCE(fact_4.fact_tag_code, '') AS fact_4_code
                  , COALESCE(fact_4.fact_tag_name, '') AS fact_4
                  , COALESCE(fact_5.fact_tag_code, '') AS fact_5_code
                  , COALESCE(fact_5.fact_tag_name, '') AS fact_5 
                FROM
                  m_ip 
                  LEFT JOIN m_manga_db 
                    ON m_manga_db.ip_code = m_ip.ip_code 
                       and m_manga_db.is_invalid = false
                  LEFT JOIN m_fact_tag AS fact_1 
                    ON m_manga_db.fact_tag_1 = fact_1.fact_tag_code 
                       and fact_1.is_invalid = false
                  LEFT JOIN m_fact_tag AS fact_2 
                    ON m_manga_db.fact_tag_2 = fact_2.fact_tag_code 
                       and fact_2.is_invalid = false
                  LEFT JOIN m_fact_tag AS fact_3 
                    ON m_manga_db.fact_tag_3 = fact_3.fact_tag_code 
                       and fact_3.is_invalid = false
                  LEFT JOIN m_fact_tag AS fact_4 
                    ON m_manga_db.fact_tag_4 = fact_4.fact_tag_code 
                       and fact_4.is_invalid = false
                  LEFT JOIN m_fact_tag AS fact_5 
                    ON m_manga_db.fact_tag_5 = fact_5.fact_tag_code 
                       and fact_5.is_invalid = false
                WHERE
                  m_ip.id IN (SELECT id FROM m_ip 
                              WHERE m_ip.is_invalid = false 
                                    and valid_start_date <= now() 
                                    and now() <= valid_end_date
                                    and key_visual_file_name != ''
                                    and key_visual_file_name is not null
                              ORDER BY random() LIMIT 8)
                """

        return self.select(sql)

    """キーワードをもとにIPを検索"""
    def selectByKeyword(self,keyword,imp_cnt,book_volume_num):

        # SELECT句を生成
        formatedSelectSentence = ""
        imp = self.createImpSelectItem(imp_cnt)
        # book_volume = self.createBookVolumeSelectItem(book_volume_num)
        formatedSelectSentence = self.selectSentence.format(imp = imp , book_volume = "")
        # FROM句を生成
        formatedFromSentence = ""
        max_imp = self.createImpSelectItemForSubQuery(imp_cnt)
        formatedFromSentence += self.fromSentence.format(max_imp = max_imp)
        # max_book_volume = self.createBookVolumeSelectItemForSubQuery(book_volume_num)
        # formatedFromSentence += self.joinSentenceForBookVolume.format(max_book_volume = max_book_volume,asc_or_desc = "DESC", alias = "b")
        # WHERE句の生成
        params = []
        whereSentence = self.whereValidMIp
        whereSentence +=  """
                          (
                          m_ip.ip_name LIKE %s
                          or m_ip.ip_kana_name LIKE %s 
                          or m_ip.keyword LIKE %s
                          )
                          """
        for x in range(3):
          params.append("%" + keyword + "%")
          

        sql = formatedSelectSentence + formatedFromSentence + whereSentence + 'ORDER BY m_ip.ip_kana_name COLLATE "ja_JP.utf8" ASC'

        return self.selectWithParam(sql,params)
    
    """
    類似検索条件をもとにIPを検索
    (ユーザ入力が全未入力の場合の全検索もここで行う)
    """
    def selectBySimilarCondition(self,inputContents,imp_cnt,book_volume_num):
      
      #キーワード入力有 且つ 類似入力無の場合、類似検索は行わない
      if self.isOnlyKeyword(inputContents):
        return []
      
      # SELECT句を生成
      formatedSelectSentence = ""
      imp = self.createImpSelectItem(imp_cnt)
      book_volume = self.createBookVolumeSelectItem(book_volume_num)
      formatedSelectSentence = self.selectSentence.format(imp = imp , book_volume = book_volume)
      # FROM句を生成
      formatedFromSentence = ""
      max_imp = self.createImpSelectItemForSubQuery(imp_cnt)
      max_book_volume = self.createBookVolumeSelectItemForSubQuery(book_volume_num)
      formatedFromSentence += self.fromSentence.format(max_imp = max_imp)
      formatedFromSentence += self.joinSentenceForBookVolume.format(max_book_volume = max_book_volume, asc_or_desc = "DESC", alias = "b")
      ## WHERE句生成
      params = []
      whereSentence = self.createWhereSentenceForSimilarCondition(params,inputContents,imp_cnt)
      # where句を調整(IP公開有効期間_開始・終了の条件追加と不要な末尾"and"を削除)
      whereSentence = (self.whereValidMIp + whereSentence)[::-1].replace("dna" , "" , 1)[::-1]
      
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
          and not inputContents.imp
          and not inputContents.fiction
          and not inputContents.fact_tag
          and not (inputContents.start_date and ''.join(inputContents.start_date) != '--------')
          and not (inputContents.end_date and ''.join(inputContents.end_date) != '--------')
          ):
        return True
      else:
        return False

    """
    印象用のSELECT項目生成処理
    @param imp_cnt 印象テーブル件数
    @return SELECT項目
    """
    def createImpSelectItem(self,imp_cnt):
      imp = ""
      for i in range(int(imp_cnt/2)):
        imp +=   ",a.imp_code"+ str(i+1)
        imp +=   ",a.imp_name"+ str(i+1)
      return imp

    """
    書籍用のSELECT項目生成処理
    @param book_volume_num 書籍データ表示数
    @return SELECT項目
    """
    def createBookVolumeSelectItem(self,book_volume_num):
      book_volume = ""
      for i in range(book_volume_num):
        book_volume +=   ",b.book_name"+ str(book_volume_num-i)
        book_volume +=   ",to_char(b.qty_total_sales_2_"+ str(book_volume_num-i) + ",'999,999,999,999,999')"
      return book_volume
    """
    書籍用のSELECT項目生成処理（巻毎の書籍サブクエリ用）
    @param imp_cnt 印象テーブル件数
    @return SELECT項目
    """
    def createImpSelectItemForSubQuery(self,imp_cnt):
      max_imp = ""
      for i in range(int(imp_cnt/2)):
        max_imp +=   ",max(case a.seq when "+ str(i+1) +" then a.imp_code else null end) as imp_code"+ str(i+1)
        max_imp +=   ",max(case a.seq when "+ str(i+1) +" then a.imp_name else null end) as imp_name"+ str(i+1)
      return max_imp
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
        max_book_volume += ",max(case a.seq when "+ str(book_volume_num-i) +" then a.qty_total_sales_2 else null end) as qty_total_sales_2_"+ str(book_volume_num-i)
      return max_book_volume

    """
    類似検索用のWHERE句生成処理
    @param params SQLのパラメータ
    @param inutContents ユーザ入力情報
    @param imp_cnt 印象テーブル件数
    @return WHERE句
    """
    def createWhereSentenceForSimilarCondition(self,params, inputContents,imp_cnt):
      whereSentence = ""
      # 分類
      for i in range(len(inputContents.category)):
        if i == 0 :
          whereSentence += "("
        # アニメ
        if inputContents.category[i] == "0":
          whereSentence += "EXISTS ( SELECT * FROM m_wiki WHERE ip_code = m_ip.ip_code and is_invalid = false ) = true"
        # マンガ
        if inputContents.category[i] == "1":
          whereSentence += "EXISTS ( SELECT * FROM m_manga_db WHERE ip_code = m_ip.ip_code and is_invalid = false ) = true"
        # アプリ
        if inputContents.category[i] == "2":
          whereSentence += "EXISTS ( SELECT * FROM m_mobile_app WHERE ip_code = m_ip.ip_code and is_invalid = false ) = true"
        # ゲーム
        if inputContents.category[i] == "3":
          whereSentence += "EXISTS ( SELECT * FROM m_pkg_soft WHERE ip_code = m_ip.ip_code and is_invalid = false ) = true"
        # 劇場
        if inputContents.category[i] == "4":
          whereSentence += "EXISTS ( SELECT * FROM m_manga_db WHERE ip_code = m_ip.ip_code and m_manga_db.award_history_anime_film = true and is_invalid = false ) = true"
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
      # 印象
      for i in range(len(inputContents.imp)):
        for j in range(int(imp_cnt/2)):
          if j == 0:
            whereSentence += "("
          params.append(inputContents.imp[i])
          whereSentence += "a.imp_code"+ str(j+1) +" = %s"
          if j != int(imp_cnt/2)-1:
            whereSentence += " or "
          else:
            whereSentence += ") and "
      # 現実/非現実フラグ
      for i in range(len(inputContents.fiction)):
        if i == 0 :
          whereSentence += "("
        if inputContents.fiction[i] == "0":
          whereSentence += "m_manga_db.is_fiction = false"
        elif inputContents.fiction[i] == "1":
          whereSentence += "m_manga_db.is_fiction = true"
        if i != len(inputContents.fiction)-1:
          whereSentence += " or "
        else:
          whereSentence += ") and "
      # 事実タグ
      for i in range(len(inputContents.fact_tag)):
        if i == 0 :
          whereSentence += "("
        for x in range(5):
          params.append(inputContents.fact_tag[i])
        whereSentence += "COALESCE(fact_1.fact_tag_code, '') = %s or "
        whereSentence += "COALESCE(fact_2.fact_tag_code, '') = %s or "
        whereSentence += "COALESCE(fact_3.fact_tag_code, '') = %s or "
        whereSentence += "COALESCE(fact_4.fact_tag_code, '') = %s or "
        whereSentence += "COALESCE(fact_5.fact_tag_code, '') = %s "
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
                          %s <= to_char(release_date,'yyyymmdd')
                          and to_char(release_date,'yyyymmdd') <= %s
                          ) and
                          """
      return whereSentence

    """タイトル名を検索"""
    def selectTitleNameAll(self):
      
        sql =   """
                SELECT
                  LEFT (m_ip.ip_kana_name, 1)
                  , m_ip.ip_name
                  , m_ip.ip_code 
                FROM
                  m_ip
                WHERE
                  m_ip.is_invalid = false
                  and valid_start_date <= now() and now() <= valid_end_date 
                ORDER BY
                  m_ip.ip_kana_name;

                """
        return self.select(sql)

    """年代別を検索"""
    def selectAgeNameAll(self):
      
        sql =   """
                SELECT
                  to_char(m_ip.release_date, 'YYYY') AS release_date
                  , m_ip.ip_name
                  , m_ip.ip_code 
                FROM
                  m_ip
                WHERE
                  m_ip.is_invalid = false
                  and valid_start_date <= now() and now() <= valid_end_date  
                ORDER BY
                  m_ip.release_date DESC;
                """
        return self.select(sql)

    """IPコードListよりIP名を取得する"""
    def selectCompareIpName(self,ip_code_list):
      value = tuple(ip_code_list)
      params = {'ip_code_list': value}
      sql = """
          SELECT
            ip_code
            , ip_name
          FROM
            m_ip
          WHERE
            m_ip.ip_code in %(ip_code_list)s
            AND m_ip.is_invalid = false
            AND valid_start_date <= now() AND now() <= valid_end_date 
          ORDER BY
            ip_code
          """
      return self.selectWithParam(sql,params)

    """IPコードよりIPマスタ情報を取得する"""
    def selectDetailByIpCode(self,ip_code,imp_cnt):
        # SELECT句を生成
        formatedSelectSentence = ""
        imp = self.createImpSelectItem(imp_cnt)
        book_volume = """
                      ,b.isbn1
                      ,b.book_name1
                      ,to_char(b.qty_total_sales_2_1::numeric::integer,'999,999,999,999,999')
                      ,d.isbn1
                      ,d.book_name1
                      ,to_char(d.qty_total_sales_2_1::numeric::integer,'999,999,999,999,999')
                      """
        formatedSelectSentence = self.selectSentence.format(imp = imp , book_volume = book_volume)
        formatedSelectSentence += self.selectItemForDetail
        # FROM句を生成
        formatedFromSentence = ""
        max_imp = self.createImpSelectItemForSubQuery(imp_cnt)
        formatedFromSentence += self.fromSentence.format(max_imp = max_imp)
        max_book_volume = self.createBookVolumeSelectItemForSubQuery(1)
        formatedFromSentence += self.joinSentenceForBookVolume.format(max_book_volume = max_book_volume,asc_or_desc = "ASC" , alias = "b")
        formatedFromSentence += self.joinSentenceForBookVolume.format(max_book_volume = max_book_volume,asc_or_desc = "DESC", alias = "d")
        formatedFromSentence += self.fromSentenceForDetail
        # WHERE句の生成
        whereSentence = self.whereValidMIp
        whereSentence += "m_ip.ip_code = %s"

        sql = formatedSelectSentence + formatedFromSentence + whereSentence
        return self.selectWithParam(sql,[ip_code,ip_code,ip_code,ip_code])

    """IPコードが存在するか確認"""
    def selectCountByIpCode(self,ip_code):
        sql = """
              SELECT
                count(ip_code)
              FROM
                m_ip
              {whereValidMIp}
              ip_code = %s
              """

        return self.selectWithParam(sql.format(whereValidMIp=self.whereValidMIp),[ip_code])

    """IPコードListよりTwiter情報を取得する"""
    def selectCompareTwitter(self,ip_code_list):
      value = tuple(ip_code_list)
      params = {'ip_code_list': value}

      sql = """
        WITH month_info AS 
          	(SELECT
          	   t_twitter.twitter_id
          	  ,m_twitter.ip_code
          	  ,m_twitter.user_name
          	  ,max((case when to_char(t_twitter.create_date,'yyyy/mm')  < to_char(current_timestamp,'yyyy/mm') 
                then  to_char(t_twitter.create_date,'yyyy/mm') else '' end)) AS new_month
          	  ,to_char(current_timestamp + '-3 months','yyyy/mm') AS three_month
			        ,to_char(current_timestamp + '-12 months','yyyy/mm') AS one_year
          	FROM
          	  t_twitter 
          	INNER JOIN m_twitter 
          	  ON m_twitter.twitter_id = t_twitter.twitter_id
            WHERE m_twitter.ip_code in %(ip_code_list)s
            AND m_twitter.is_invalid = false
          	GROUP BY t_twitter.twitter_id
			        ,m_twitter.ip_code
			        ,m_twitter.user_name 
			        ,m_twitter.twitter_create_date
			      ORDER BY m_twitter.twitter_create_date)
            
          SELECT 
               m_ip.ip_code
             , m_ip.ip_name
             , now_follower.follower_count::numeric::integer AS follower_count
             , three_month_follower.follower_count::numeric::integer AS followers_3months_ago
             , one_year_follower.follower_count::numeric::integer AS followers_1year_ago
             , month_info.user_name
             , month_info.twitter_id
          FROM m_ip
          LEFT JOIN month_info 
          ON m_ip.ip_code = month_info.ip_code
          LEFT JOIN 
            t_twitter now_follower
            ON now_follower.twitter_id = month_info.twitter_id
            AND to_char(now_follower.create_date,'yyyy/mm') = month_info.new_month
          LEFT JOIN 
            t_twitter three_month_follower
            ON three_month_follower.twitter_id = month_info.twitter_id
            AND to_char(three_month_follower.create_date,'yyyy/mm') = month_info.three_month
          LEFT JOIN 
            t_twitter one_year_follower
            ON one_year_follower.twitter_id = month_info.twitter_id
            AND to_char(one_year_follower.create_date,'yyyy/mm') = month_info.one_year
		      WHERE
          	  m_ip.ip_code in %(ip_code_list)s
              AND m_ip.is_invalid = false
              AND m_ip.valid_start_date <= now()
              AND now() <= m_ip.valid_end_date
          ORDER BY ip_code
        """
      return self.selectWithParam(sql,params)

    """IPコードListよりマンガ情報を取得する"""
    def selectCompareBook(self,ip_code_list):
      value = tuple(ip_code_list)
      params = {'ip_code_list': value}

      sql = """
          select
            ip.ip_code
            , ip.ip_name
            , ts.total_sales::numeric::integer total_sales
            , first_isbn.first_total_sales::numeric::integer first_total_sales
            , latest_isbn.last_total_sales::numeric::integer last_total_sales
            , round(ts.total_sales / book.isbn_cnt, 0)::numeric::integer avg
            , first_isbn.isbn firstisbn
            , latest_isbn.isbn latestisbn
          from
            m_ip ip 
            left join ( 
              select
                m.ip_code
                , sum(t.total_sales) total_sales 
              from m_book m 
                inner join ( 
                  select
                    isbn
                    , max(qty_total_sales_2) total_sales 
                  from t_book 
                  where t_book.result_yyyymm < to_char(current_timestamp, 'yyyy/mm')
                  group by isbn) t 
                  on t.isbn = m.isbn
                  and m.is_invalid = FALSE
              group by ip_code
            ) ts 
              on ts.ip_code = ip.ip_code 
            left join ( 
              select
                ip_code
                , isbn
                , (select max(qty_total_sales_2) from t_book where isbn = m.isbn and result_yyyymm < to_char(current_timestamp, 'yyyy/mm') ) first_total_sales 
              from m_book m 
              where
                (ip_code, isbn) in ( 
                  select
                    ip_code
                    , min(isbn) 
                  from m_book 
                  where
                    (ip_code, book_issue_date) in ( 
                      select
                        ip_code
                        , min(book_issue_date) 
                      from m_book 
					            where  m_book.is_invalid = false
                      group by ip_code
                    )
				          and  m_book.is_invalid = false
				          group by ip_code
						      order by ip_code )
              and m.is_invalid = false
            ) first_isbn 
            on first_isbn.ip_code = ip.ip_code 
            left join ( 
              select
                ip_code
                , isbn
                , ( select max(qty_total_sales_2) from t_book where isbn = m.isbn and result_yyyymm < to_char(current_timestamp, 'yyyy/mm')) last_total_sales 
              from m_book m 
              where
                (ip_code, isbn) in ( 
                   select
                      ip_code
                      , max(isbn) 
                    from m_book 
                    where
                      (ip_code, book_issue_date) in ( 
                        select
                          ip_code
                          , max(book_issue_date) 
                        from m_book
						            where  m_book.is_invalid = false
						            and to_char(book_issue_date,'yyyy/mm') < to_char(current_timestamp, 'yyyy/mm')
                        group by ip_code) 
					            and m_book.is_invalid = false 
                      group by ip_code)
                and m.is_invalid = false
            ) latest_isbn 
            on latest_isbn.ip_code = ip.ip_code 
            left join ( 
              select 
                ip_code
               , count(distinct t_book.isbn) isbn_cnt 
              from t_book
			          inner join m_book 
			          on m_book.isbn = t_book.isbn
			        where t_book.result_yyyymm < to_char(current_timestamp, 'yyyy/mm')
					    and m_book.is_invalid = false
              group by ip_code
			  ) book 
            on book.ip_code = ip.ip_code 
          where
            ip.ip_code in %(ip_code_list)s
            AND ip.is_invalid = false
            AND ip.valid_start_date <= now()
            AND now() <= ip.valid_end_date
          order by
            ip_code
          """
      return self.selectWithParam(sql,params)

    """IPコードListよりゲーム情報を取得する"""
    def selectCompareGame(self,ip_code_list):
      value = tuple(ip_code_list)
      params = {'ip_code_list': value}
      sql = """
   	      SELECT
			      m_ip.ip_code
          	, m_ip.ip_name
            , m_pkg_soft.pkg_soft_name
          	, m_pkg_soft.platform_name
          	, m_pkg_soft.distributor_name
            , to_char(m_pkg_soft.release_date,'yyyy年MM月')
            , t_pkg_soft.qty_total_sales::numeric::integer
            , m_pkg_soft.pkg_soft_code
          FROM
          	m_ip
          LEFT  JOIN
          	m_pkg_soft
          ON
          	m_ip.ip_code = m_pkg_soft.ip_code
			      AND m_pkg_soft.is_invalid = FALSE
          LEFT  JOIN
          	t_pkg_soft
          ON
          	m_pkg_soft.pkg_soft_code = t_pkg_soft.pkg_soft_code
          	AND m_pkg_soft.ip_code = t_pkg_soft.ip_code
          	AND t_pkg_soft.result_yyyymm = ( 
              SELECT
                max(result_yyyymm) 
              FROM
                t_pkg_soft
              WHERE
                m_pkg_soft.pkg_soft_code = t_pkg_soft.pkg_soft_code
                AND result_yyyymm < to_char(current_timestamp, 'yyyymm')
          	    )
          WHERE
          	m_ip.ip_code in %(ip_code_list)s
            AND m_ip.is_invalid = false
            AND m_ip.valid_start_date <= now()
            AND now() <= m_ip.valid_end_date
          ORDER BY
            COALESCE(t_pkg_soft.qty_total_sales,0) desc
            ,m_pkg_soft.release_date
          """
      return self.selectWithParam(sql,params)

    """IPコードListよりアプリ情報を取得する"""
    def selectCompareApp(self,ip_code_list):
      value = tuple(ip_code_list)
      params = {'ip_code_list': value}
      sql = """
      	SELECT
        	m_ip.ip_code
        	, m_ip.ip_name
        	, m_mobile_app.app_name
        	, platform
        	, distributor_name
          , m_mobile_app.release_date
          , total_sales::numeric::integer AS total_sales
          , total_download_count::numeric::integer  AS total_download_count
          , avg_sales::numeric::integer AS avg_sales
          , avg_download_count::numeric::integer AS avg_download_count
          , m_mobile_app.app_id_ios
          , m_mobile_app.app_id_android
          , to_char(m_mobile_app.service_start_date,'YYYYMM')
        FROM
        	m_ip
        LEFT JOIN
        	(
        	SELECT
        	  m_mobile_app.ip_code
            , m_mobile_app.app_id_ios
            , m_mobile_app.app_id_android
            , m_mobile_app.app_name
            , m_mobile_app.service_start_date
            , case when COALESCE(app_id_ios,'') != '' then 'IOS' else '' end
              || case when COALESCE(app_id_ios,'') != '' and COALESCE(app_id_android,'') != '' then '    ' else '' end
              || case when COALESCE(app_id_android,'') != '' then 'Android' else '' end
              || case when COALESCE(app_id_ios,'') = '' and COALESCE(app_id_android,'') = '' then 'ー' else '' end   AS  platform
            , distributor_name
            , to_char(service_start_date,'yyyy年MM月') AS release_date
          FROM m_mobile_app
          WHERE
            m_mobile_app.ip_code in %(ip_code_list)s
			      AND m_mobile_app.is_invalid = FALSE
            ) AS m_mobile_app
        ON	m_ip.ip_code = m_mobile_app.ip_code
        LEFT JOIN
        	(
        	 SELECT
        	    app_name
              , sum(monthly_sales)::numeric::integer AS total_sales
			        , round(sum(monthly_sales) / count(DISTINCT result_yyyymm),0)::numeric::integer AS avg_sales
			        , sum(download_count)::numeric::integer AS total_download_count
		          , round(sum(download_count) / count(DISTINCT result_yyyymm),0)::numeric::integer AS avg_download_count
          FROM 
        	 	  t_mobile_app
          WHERE
            t_mobile_app.result_yyyymm < to_char(current_timestamp, 'yyyymm')
          GROUP BY app_name ) AS t_mobile_app_sales
        ON m_mobile_app.app_name = t_mobile_app_sales.app_name
        WHERE m_ip.ip_code in %(ip_code_list)s
            AND m_ip.is_invalid = false
            AND m_ip.valid_start_date <= now()
            AND now() <= m_ip.valid_end_date
        ORDER BY 
          COALESCE(total_sales,0) desc
          , COALESCE(total_download_count,0) desc
          , COALESCE(avg_sales,0) desc
          , COALESCE(avg_download_count,0) desc
          , service_start_date

        """
      return self.selectWithParam(sql,params)

    # """IPコードが存在するか確認"""
    def selectCompareCountByIpCode(self,ip_code_list):
      value = tuple(ip_code_list)
      params = {'ip_code_list': value}
      sql = """
          SELECT
            count(ip_code)
          FROM
            m_ip
          WHERE 
          m_ip.ip_code in %(ip_code_list)s
          AND m_ip.is_invalid = false
          AND m_ip.valid_start_date <= now()
          AND now() <= m_ip.valid_end_date
        """
      return self.selectWithParam(sql,params)