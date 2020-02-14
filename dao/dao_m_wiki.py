from ipdds_app.dao.dao_main import DaoMain
import datetime

class DaoMWiki(DaoMain):

    """IPコードより放送期間、放送局を取得する"""
    def selectBroadCastByIpCode(self,ip_code):
      sql = """
            SELECT
              COALESCE(period,'no data')
              , COALESCE(broadcaster,'no data')
            FROM
              m_wiki
            WHERE
              m_wiki.ip_code = %s
              and m_wiki.is_invalid = false
            """
      return self.selectWithParam(sql,[ip_code])