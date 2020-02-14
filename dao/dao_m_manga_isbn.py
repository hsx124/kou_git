from ipdds_app.dao.dao_main import DaoMain

class DaoMMangaIsbn(DaoMain):

    """マンガタイトルコードからマンガ実績を取得"""
    def selectMangaIsbn(self,title_code):
        sql = """
              SELECT
                  m_manga_title.manga_title_code
                , m_manga_title.manga_title_name
                , one_total_sales
                , last_total_sales
                , manga_average_sales
                , manga_total_sales
              FROM
                m_manga_isbn
                INNER JOIN m_manga_title
                  ON m_manga_isbn.manga_title_code = m_manga_title.manga_title_code
                    AND m_manga_title.invalid_flg = false
                INNER JOIN (
                  SELECT
                    m_manga_isbn.manga_title_code
                    , SUM(t_isbn.total_sales_cnt) ::numeric ::integer as one_total_sales
                  FROM
                    m_manga_isbn
                    LEFT JOIN t_isbn
                      ON m_manga_isbn.isbn = t_isbn.isbn
                  WHERE
                    m_manga_isbn.manga_title_code = %s
                    AND m_manga_isbn.invalid_flg = false
                  GROUP BY
                    m_manga_isbn.manga_title_code
                    , m_manga_isbn.isbn
                    , book_issue_yyyymmdd
                  ORDER BY
                    book_issue_yyyymmdd ASC
                  LIMIT
                    1
                ) as one_total -- 1巻の累計売上
                  ON m_manga_isbn.manga_title_code = one_total.manga_title_code
                INNER JOIN (
                  SELECT
                    m_manga_isbn.manga_title_code
                    , SUM(t_isbn.total_sales_cnt) ::numeric ::integer as last_total_sales
                  FROM
                    m_manga_isbn
                    LEFT JOIN t_isbn
                      ON m_manga_isbn.isbn = t_isbn.isbn
                  WHERE
                    m_manga_isbn.manga_title_code = %s
                    AND m_manga_isbn.invalid_flg = false
                  GROUP BY
                    m_manga_isbn.manga_title_code
                    , m_manga_isbn.isbn
                    , book_issue_yyyymmdd
                  ORDER BY
                    book_issue_yyyymmdd DESC
                  LIMIT
                    1
                ) as last_total -- 最新刊の累計売上
                  ON m_manga_isbn.manga_title_code = last_total.manga_title_code
                INNER JOIN (
                  SELECT
                    m_manga_isbn.manga_title_code
                    , AVG(total_avg.total_sales_cnt) ::numeric ::integer as manga_average_sales
                  FROM
                    m_manga_isbn
                    LEFT JOIN (
                      SELECT
                        m_manga_isbn.manga_title_code
                        , m_manga_isbn.isbn
                        , SUM(t_isbn.total_sales_cnt) ::numeric ::integer as total_sales_cnt
                      FROM
                        m_manga_isbn
                        LEFT JOIN t_isbn
                          ON m_manga_isbn.isbn = t_isbn.isbn
                      WHERE
                        m_manga_isbn.manga_title_code = %s
                        AND m_manga_isbn.invalid_flg = false
                      GROUP BY
                        m_manga_isbn.manga_title_code
                        , m_manga_isbn.isbn
                        , book_issue_yyyymmdd
                    ) as total_avg
                      ON m_manga_isbn.manga_title_code = total_avg.manga_title_code
                  GROUP BY
                    m_manga_isbn.manga_title_code
                ) as manga_average -- 作品の平均発行部数
                  ON m_manga_isbn.manga_title_code = manga_average.manga_title_code
                INNER JOIN (
                  SELECT
                    m_manga_isbn.manga_title_code
                    , SUM(total_sum.total_sales_cnt) ::numeric ::integer as manga_total_sales
                  FROM
                    m_manga_isbn
                    LEFT JOIN (
                      SELECT
                        m_manga_isbn.manga_title_code
                        , m_manga_isbn.isbn
                        , SUM(t_isbn.total_sales_cnt) ::numeric ::integer as total_sales_cnt
                      FROM
                        m_manga_isbn
                        LEFT JOIN t_isbn
                          ON m_manga_isbn.isbn = t_isbn.isbn
                      WHERE
                        m_manga_isbn.manga_title_code = %s
                        AND m_manga_isbn.invalid_flg = false
                      GROUP BY
                        m_manga_isbn.manga_title_code
                        , m_manga_isbn.isbn
                        , book_issue_yyyymmdd
                    ) as total_sum
                      ON m_manga_isbn.manga_title_code = total_sum.manga_title_code
                  GROUP BY
                    m_manga_isbn.manga_title_code
                ) as manga_total -- 作品の累計発行部数
                  ON m_manga_isbn.manga_title_code = manga_total.manga_title_code
              GROUP BY
                  m_manga_title.manga_title_code
                , m_manga_title.manga_title_name
                , one_total_sales
                , last_total_sales
                , manga_average_sales
                , manga_total_sales
              """
        return self.selectWithParam(sql,[title_code,title_code,title_code,title_code])


    """タイトルコードをもとに書籍データを取得（グラフ用）"""
    def selectGraphData(self,title_code):
        sql = """
              SELECT
                manga_title_code
                , book_name
                ,left (t_isbn.result_yyyymm, 4) || '-' || right (t_isbn.result_yyyymm, 2)
                , t_isbn.total_sales_cnt ::numeric ::integer
              FROM
                t_isbn
                INNER JOIN (
                  SELECT
                    manga_title_code
                    , m_manga_isbn.isbn
                    , book_name
                  FROM
                    m_manga_isbn
                    LEFT JOIN t_isbn
                      ON m_manga_isbn.isbn = t_isbn.isbn
                  WHERE
                    m_manga_isbn.manga_title_code = %s
                    and m_manga_isbn.invalid_flg = false
                  GROUP BY
                    m_manga_isbn.manga_title_code
                    , m_manga_isbn.isbn
                    , book_name
                    , book_issue_yyyymmdd
                  ORDER BY
                    book_issue_yyyymmdd ASC
                  LIMIT
                    1
                ) as one_isbn
                  ON t_isbn.isbn = one_isbn.isbn
              WHERE
                t_isbn.isbn = one_isbn.isbn
                AND to_char(
                  current_timestamp - interval '1 years'
                  , 'yyyymm'
                ) <= t_isbn.result_yyyymm
                AND t_isbn.result_yyyymm < to_char(current_timestamp, 'yyyymm')
              UNION ALL
              SELECT
                manga_title_code
                , book_name
                , left (t_isbn.result_yyyymm, 4) || '-' || right (t_isbn.result_yyyymm, 2)
                , t_isbn.total_sales_cnt ::numeric ::integer
              FROM
                t_isbn
                INNER JOIN (
                  SELECT
                    manga_title_code
                    , m_manga_isbn.isbn
                    , book_name
                  FROM
                    m_manga_isbn
                    LEFT JOIN t_isbn
                      ON m_manga_isbn.isbn = t_isbn.isbn
                  WHERE
                    m_manga_isbn.manga_title_code = %s
                    and m_manga_isbn.invalid_flg = false
                  GROUP BY
                    m_manga_isbn.manga_title_code
                    , m_manga_isbn.isbn
                    , book_name
                    , book_issue_yyyymmdd
                  ORDER BY
                    book_issue_yyyymmdd DESC
                  LIMIT
                    1
                ) as latest_isbn
                  ON t_isbn.isbn = latest_isbn.isbn
              WHERE
                t_isbn.isbn = latest_isbn.isbn
                AND to_char(
                  current_timestamp - interval '1 years'
                  , 'yyyymm'
                ) <= t_isbn.result_yyyymm
                AND t_isbn.result_yyyymm < to_char(current_timestamp, 'yyyymm')
              """
        return self.selectWithParam(sql,[title_code,title_code])

    def selectGraphDataForTotalSales(self,title_code):
      sql = """
            SELECT
              m_manga_isbn.manga_title_code
              , m_manga_title.manga_title_name
              , total_sum.result_yyyymm
              , SUM(total_sum.total_sales_cnt) ::numeric ::integer as manga_total_sales
            FROM
              m_manga_isbn
              LEFT JOIN (
                SELECT
                  m_manga_isbn.manga_title_code
                  , m_manga_isbn.isbn
                  , left (t_isbn.result_yyyymm, 4) || '-' || right (t_isbn.result_yyyymm, 2) as result_yyyymm
                  , SUM(t_isbn.total_sales_cnt) ::numeric ::integer as total_sales_cnt
                FROM
                  m_manga_isbn
                  LEFT JOIN t_isbn
                    ON m_manga_isbn.isbn = t_isbn.isbn
                WHERE
                  m_manga_isbn.manga_title_code = %s
                  AND m_manga_isbn.invalid_flg = false
                GROUP BY
                  m_manga_isbn.manga_title_code
                  , t_isbn.result_yyyymm
                  , m_manga_isbn.isbn
                  , book_issue_yyyymmdd
              ) as total_sum
                ON m_manga_isbn.manga_title_code = total_sum.manga_title_code
              INNER JOIN m_manga_title
                ON m_manga_isbn.manga_title_code = m_manga_title.manga_title_code
            WHERE
              m_manga_isbn.manga_title_code = %s
            GROUP BY
              m_manga_isbn.manga_title_code
              , m_manga_title.manga_title_name
              , total_sum.result_yyyymm
            """
      return self.selectWithParam(sql,[title_code,title_code])