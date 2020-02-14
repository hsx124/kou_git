from ipdds_app.dao.dao_main import DaoMain

class DaoTIsbn(DaoMain):
    """マンガランキングデータの取得"""
    def selectRankingManga(self):

        sql =   """
                SELECT  rank() OVER (
                    ORDER BY
                      sum(COALESCE(t_isbn.sales_cnt, 0)) DESC
                  ) AS rank
                  , COALESCE(m_sakuhin.key_visual_file_name, '')
                  , m_sakuhin_map.sakuhin_code
                  , m_manga_isbn.book_name
                  , t_isbn.isbn
                  , to_char(
                    sum(COALESCE(t_isbn.sales_cnt, 0))
                    , '999,999,999'
                  ) AS qty_sqles
                FROM
                  t_isbn
                  INNER JOIN m_manga_isbn
                    ON t_isbn.isbn = m_manga_isbn.isbn
                    and m_manga_isbn.invalid_flg = false
                  INNER JOIN m_manga_title
                    ON m_manga_isbn.manga_title_code = m_manga_title.manga_title_code
                    and m_manga_title.invalid_flg = false
                  INNER JOIN m_sakuhin_map
                    ON m_manga_title.manga_title_code = m_sakuhin_map.title_code
                    and m_sakuhin_map.invalid_flg = false
                  INNER JOIN m_sakuhin
                    ON m_sakuhin_map.sakuhin_code = m_sakuhin.sakuhin_code
                    and m_sakuhin.invalid_flg = false
                    and TO_DATE(valid_start_yyyymmdd, 'YYYYMMDD') <= now()
                    and now() <= TO_DATE(valid_end_yyyymmdd, 'YYYYMMDD')
                WHERE
                  t_isbn.result_yyyymm >= to_char(current_timestamp + '-3 months', 'yyyymm')
                  and t_isbn.result_yyyymm < to_char(current_timestamp, 'yyyymm')
                  and m_sakuhin.sakuhin_code IS NOT NULL
                GROUP BY
                  m_sakuhin_map.sakuhin_code
                  , m_manga_isbn.book_name
                  , t_isbn.isbn
                  , m_sakuhin.key_visual_file_name
                ORDER BY
                  sum(COALESCE(t_isbn.sales_cnt, 0)) DESC
                LIMIT
                  5
                """

        return self.select(sql)

    """ISBNをもとに書籍データを取得（グラフ用）"""
    def selectGraphData(self,isbn):
        sql = """
              SELECT
                replace(t_isbn.result_yyyymm,'/','-')
                , t_isbn.total_sales_cnt::numeric::integer
              FROM
                t_isbn
              WHERE
                t_isbn.isbn = %s
                AND to_char(current_timestamp - interval '1 years','yyyymm') <= t_isbn.result_yyyymm
                AND t_isbn.result_yyyymm < to_char(current_timestamp,'yyyymm')
              """
        return self.selectWithParam(sql,[isbn])

    """発売日を取得（グラフ用）"""
    def selectMangaServiceStartDate(self,manga_code):
        sql = """
          SELECT
            LEFT(MIN(book_issue_yyyymmdd),6)
          FROM m_manga_title manga
          LEFT JOIN  m_manga_isbn m
          ON manga.manga_title_code = m.manga_title_code
		  	    AND m.invalid_flg = FALSE
          WHERE
            manga.manga_title_code = %s
            AND manga.invalid_flg = FALSE
          LIMIT 1
          """
        return self.selectWithParam(sql,[manga_code])

    """sakuhin_codeをもとに累計発行部数(発売日からN月）/平均発行部数（単巻あたり）（発売日からNか月）を取得（グラフ用）"""
    def selectMangaTotalAndAvgServiceStartDateGraphData(self,manga_code,firstDate):
        sql = """
            SELECT
              left(SUB1.result_yyyymm,4)||'-'||right(SUB1.result_yyyymm,2) AS result_yyyymm
              , round(SUM(SUB1.total_sales_cnt)::numeric::integer,0)::numeric::integer AS total_sales
              , round(SUM(SUB1.total_sales_cnt)::numeric::integer/count(isbn),0)::numeric::integer AS avg_sales
            FROM
              (
                SELECT
                  m.manga_title_code
                  , m.isbn
                  , t.result_yyyymm
                  , t.total_sales_cnt
                FROM t_isbn t
                INNER JOIN m_manga_isbn m
                  ON t.isbn = m.isbn
                  AND m.invalid_flg = FALSE
                WHERE
                  t.result_yyyymm >= %s
                  AND t.result_yyyymm < to_char(current_timestamp,'yyyymm')
                  AND t.result_yyyymm < to_char((to_date(%s, 'YYYYMMDD') + interval '1 years'),'yyyymm')
                  AND t.isbn in (
                    SELECT
                      isbn
                    FROM m_manga_isbn
                    WHERE
                      manga_title_code = %s
                  )
              ) SUB1
            GROUP BY
              SUB1.manga_title_code
              , SUB1.result_yyyymm
            ORDER BY
              SUB1.result_yyyymm 
            """
        return self.selectWithParam(sql,[firstDate,firstDate,manga_code])

    """マンガコードをもとに累計発行部数/平均発行部数（単巻あたり）（直近一年）を取得（グラフ用）"""
    def selectMangaTotalAndAvgNowDayGraphData(self,manga_code,firstDate):
        sql = """
		        SELECT
              left(SUB1.result_yyyymm,4)||'-'||right(SUB1.result_yyyymm,2) AS result_yyyymm
              , round(SUM(SUB1.total_sales_cnt)::numeric::integer,0)::numeric::integer AS total_sales
              , round(SUM(SUB1.total_sales_cnt)::numeric::integer/count(isbn),0)::numeric::integer AS avg_sales
            FROM
              (
                SELECT
                  m.manga_title_code
                  , m.isbn
                  , t.result_yyyymm
                  , t.total_sales_cnt
                FROM t_isbn t
                INNER JOIN m_manga_isbn m
                  ON t.isbn = m.isbn
                  AND m.invalid_flg = FALSE
                WHERE
                  t.result_yyyymm >= to_char(current_timestamp - interval '1 years','yyyymm')
                  AND t.result_yyyymm < to_char(current_timestamp,'yyyymm')
                  AND t.result_yyyymm >= %s
                  AND t.isbn in (
                    SELECT
                      isbn
                    FROM m_manga_isbn
                    WHERE
                      manga_title_code = %s
                  )
              ) SUB1
            GROUP BY
              SUB1.manga_title_code
              , SUB1.result_yyyymm
            ORDER BY
              SUB1.result_yyyymm 
            """
        return self.selectWithParam(sql,[firstDate,manga_code])

    """1巻のISBNを取得（グラフ用）"""
    def selectServiceStartDateIsbnData(self,manga_code):
        sql = """
            SELECT
              min(isbn) firstisbn
              , LEFT(book_issue_yyyymmdd,6)
            FROM m_manga_isbn
            WHERE
              (manga_title_code, book_issue_yyyymmdd) in ( 
                SELECT
                  manga_title_code
                  , min(book_issue_yyyymmdd) 
                FROM m_manga_isbn m
                WHERE
                  m.invalid_flg = false 
                GROUP BY
                  manga_title_code
              ) 
              AND invalid_flg = false
              AND manga_title_code = %s
            GROUP BY
              manga_title_code
      		    , book_issue_yyyymmdd
            """
        return self.selectWithParam(sql,[manga_code])

    """ISBNをもとに最新巻を取得（グラフ用）"""
    def selectCompareGraphData(self,isbn,manga_issue_date):
        sql = """
              SELECT
                left(result_yyyymm,4)||'-'||right(result_yyyymm,2)
                , total_sales_cnt::numeric::integer AS total_sales
              FROM t_isbn
              WHERE
                isbn = %s
                AND result_yyyymm >= %s
                AND result_yyyymm >= to_char(current_timestamp - interval '1 years','yyyymm')
                AND result_yyyymm < to_char(current_timestamp,'yyyymm')
              """
        return self.selectWithParam(sql,[isbn,manga_issue_date])

    """最新刊巻のISBNを取得（グラフ用）"""
    def selectLatestIsbnData(self,manga_code):
        sql = """
           SELECT
              max(isbn) latestisbn
              ,LEFT(book_issue_yyyymmdd,6)
            FROM m_manga_isbn
            WHERE
              (manga_title_code, book_issue_yyyymmdd) in ( 
                SELECT
                  manga_title_code
                  , max(book_issue_yyyymmdd) 
                FROM m_manga_isbn m
                WHERE
                  m.invalid_flg = false 
                  AND book_issue_yyyymmdd < to_char(current_timestamp, 'yyyymmdd') 
                group by
                  manga_title_code
              ) 
              AND invalid_flg = false 
              AND manga_title_code = %s
            GROUP BY
              manga_title_code
              , book_issue_yyyymmdd
            """
        return self.selectWithParam(sql,[manga_code])