import psycopg2
import sqlalchemy.pool as pool
from django.conf import settings

# コネクションプール
db_conf = settings.DATABASES['default']
def getconn():
    con = psycopg2.connect( host=db_conf['HOST'],
                            port=db_conf['PORT'],
                            dbname=db_conf['NAME'],
                            user=db_conf['USER'],
                            password=db_conf['PASSWORD'],
                            options=db_conf['OPTIONS']['options'])
    return con
mypool = pool.QueuePool(getconn, max_overflow=10, pool_size=5, timeout=10000 )

class DaoMain():
    """Daoの親クラス
        Args:
            query: sqlクエリ
            key_list: keyに設定するlist 
        Returns:
            res_list: selectの結果のタプル
    """

    def select(self,query):
        #コネクションプールよりコネクションを取得
        connection = mypool.connect()
        cursor = connection.cursor()
        #クエリ実行
        cursor.execute(query)
        #タプルを返す
        ret = cursor.fetchall()
        #コネクションプールに戻す
        connection.close()
        return ret

    """Daoの親クラス
        Args:
            query: sqlクエリ
            param_list: sqlパラメータ
            key_list: keyに設定するlist 
        Returns:
            res_list: selectの結果のタプル
    """
    def selectWithParam(self,query,param_list):
        #コネクションプールよりコネクションを取得
        connection = mypool.connect()
        cursor = connection.cursor()
        #クエリ実行
        cursor.execute(query,param_list)
        #タプルを返す
        ret = cursor.fetchall()
        #コネクションプールに戻す
        connection.close()
        return ret
