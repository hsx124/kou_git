from ipdds_app.dao.dao_main import DaoMain

class DaoTBook(DaoMain):

    """マンガランキングデータの取得"""
    def selectRankingManga(self):

        sql =   """
                SELECT
                  rank() OVER (ORDER BY sum(COALESCE(t_book.qty_sales,0)) DESC) AS rank
                  , COALESCE(m_ip.key_visual_file_name, '')
                  , m_book.ip_code
                  , m_book.book_name
                  , t_book.isbn
                  , to_char(sum(COALESCE(t_book.qty_sales,0)), '999,999,999') AS qty_sqles 
                FROM
                  t_book 
                  INNER JOIN m_book 
                    ON t_book.isbn = m_book.isbn 
                       and m_book.is_invalid = false
                  INNER JOIN m_ip 
                    ON m_book.ip_code = m_ip.ip_code 
                       and m_ip.is_invalid = false
                       and valid_start_date <= now() and now() <= valid_end_date
                WHERE
                  t_book.result_yyyymm >= to_char(current_timestamp + '-3 months', 'yyyy/mm') 
                  and t_book.result_yyyymm < to_char(current_timestamp, 'yyyy/mm') 
                  and m_ip.ip_code IS NOT NULL
                GROUP BY
                  m_book.ip_code
                  , m_book.book_name
                  , t_book.isbn
                  , m_ip.key_visual_file_name 
                ORDER BY
                  sum(COALESCE(t_book.qty_sales,0)) DESC 
                LIMIT
                  5
                """

        return self.select(sql)

    """ISBNをもとに書籍データを取得（グラフ用）"""
    def selectGraphData(self,isbn):

        sql = """
              SELECT
                replace(t_book.result_yyyymm,'/','-')
                , t_book.qty_total_sales_2::numeric::integer
              FROM
                t_book
              WHERE
                t_book.isbn = %s
                AND to_char(current_timestamp - interval '1 years','yyyy/mm') <= t_book.result_yyyymm
                AND t_book.result_yyyymm < to_char(current_timestamp,'yyyy/mm')
              """
        return self.selectWithParam(sql,[isbn])

    """ip_codeをもとに累計発行部数(発売日からN月）/平均発行部数（単巻あたり）（発売日からNか月）を取得（グラフ用）"""
    def selectBookTotalAndAvgFirstDayGraphData(self,ip_code,fromdate):

        sql = """
            SELECT
              replace(SUB1.result_yyyymm,'/','-') AS result_yyyymm
              , round(SUM(SUB1.qty_total_sales_2)::numeric::integer,0)::numeric::integer AS total_sales
              , round(SUM(SUB1.qty_total_sales_2)::numeric::integer/count(isbn),0)::numeric::integer AS avg_sales
            FROM
              (
                SELECT
                  m_book.ip_code
                  , m_book.book_name
                  , m_book.isbn
                  , t_book.result_yyyymm
                  , t_book.qty_total_sales_2
                FROM
                  t_book
                  INNER JOIN m_book
                    ON t_book.isbn = m_book.isbn
                    AND m_book.is_invalid = FALSE
                WHERE
                  t_book.result_yyyymm >= %s
                  AND t_book.result_yyyymm < to_char(current_timestamp,'yyyy/mm')
                  AND t_book.result_yyyymm < to_char((TO_DATE(%s, 'YYYY/MM/DD') + interval '1 years'),'yyyy/mm')
                  AND t_book.isbn in (
                    SELECT
                      m_book.isbn
                    FROM
                      m_book
                    WHERE
                      m_book.ip_code = %s
                  )
              ) SUB1
            GROUP BY
              SUB1.ip_code
              , SUB1.result_yyyymm
            ORDER BY
              SUB1.result_yyyymm 
              """
        return self.selectWithParam(sql,[fromdate,fromdate,ip_code])

    """ip_codeをもとに累計発行部数/平均発行部数（単巻あたり）（直近一年）を取得（グラフ用）"""
    def selectBookTotalAndAvgNowDayGraphData(self,ip_code,book_issue_date):

        sql = """
            SELECT
              replace(SUB1.result_yyyymm,'/','-') AS result_yyyymm
              , SUM(SUB1.qty_total_sales_2)::numeric::integer AS total_sales
              , round(SUM(SUB1.qty_total_sales_2)/count(isbn),0)::numeric::integer AS avg_sales
            FROM
              (
                SELECT
                  m_book.ip_code
                  , m_book.book_name
                  , m_book.isbn
                  , t_book.result_yyyymm
                  , t_book.qty_total_sales_2
                FROM
                  t_book
                  INNER JOIN m_book
                    ON t_book.isbn = m_book.isbn
                    AND m_book.is_invalid = FALSE
                WHERE
                  to_char(current_timestamp - interval '1 years','yyyy/mm') <= t_book.result_yyyymm
                  AND t_book.result_yyyymm < to_char(current_timestamp,'yyyy/mm')
                  AND %s <= t_book.result_yyyymm
                  AND t_book.isbn in (
                    SELECT
                      m_book.isbn
                    FROM
                      m_book
                    WHERE
                      m_book.ip_code = %s
                  )
              ) SUB1
            GROUP BY
              SUB1.ip_code
              , SUB1.result_yyyymm
            ORDER BY
              SUB1.result_yyyymm 
              """
        return self.selectWithParam(sql,[book_issue_date,ip_code])

    """発売日を取得（グラフ用）"""
    def selectFirstDayData(self,ip_code):

        sql = """
            SELECT
              to_char(MIN(book_issue_date),'yyyy/mm')
            FROM
              m_book
            WHERE
              ip_code = %s
              AND m_book.is_invalid = FALSE
            LIMIT 1
            """
        return self.selectWithParam(sql,[ip_code])

    """1巻のISBNを取得（グラフ用）"""
    def selectFirstIsbnData(self,ip_code):

        sql = """
            SELECT
              min(isbn) firstisbn
              , to_char(book_issue_date,'yyyy/mm')
            FROM
              m_book 
            WHERE
              (ip_code, book_issue_date) in ( 
                SELECT
                  ip_code
                  , min(book_issue_date) 
                FROM
                  m_book 
                WHERE
                  m_book.is_invalid = false 
                GROUP BY
                  ip_code
              ) 
              AND m_book.is_invalid = false
              AND m_book.ip_code = %s
            GROUP BY
              ip_code
      			  ,book_issue_date
            """
        return self.selectWithParam(sql,[ip_code])

    """最新刊巻のISBNを取得（グラフ用）"""
    def selectLatestIsbnData(self,ip_code):

        sql = """
            SELECT
              max(isbn) latestisbn
              , to_char(book_issue_date,'yyyy/mm')
            FROM
              m_book 
            WHERE
              (ip_code, book_issue_date) in ( 
                SELECT
                  ip_code
                  , max(book_issue_date) 
                FROM
                  m_book 
                WHERE
                  m_book.is_invalid = false 
                  AND to_char(book_issue_date, 'yyyy/mm') < to_char(current_timestamp, 'yyyy/mm') 
                group by
                  ip_code
              ) 
              AND m_book.is_invalid = false 
              AND m_book.ip_code = %s
            GROUP BY
              ip_code
              ,book_issue_date
            """
        return self.selectWithParam(sql,[ip_code])

    """ISBNをもとに最新巻/1巻の書籍データを取得（グラフ用）"""
    def selectCompareGraphData(self,isbn,book_issue_date):

        sql = """
              SELECT
                replace(t_book.result_yyyymm,'/','-')
                , t_book.qty_total_sales_2::numeric::integer
              FROM
                t_book
              WHERE
                t_book.isbn = %s
                AND %s <= t_book.result_yyyymm
                AND to_char(current_timestamp - interval '1 years','yyyy/mm') <= t_book.result_yyyymm
                AND t_book.result_yyyymm < to_char(current_timestamp,'yyyy/mm')
              """
        return self.selectWithParam(sql,[isbn,book_issue_date])

