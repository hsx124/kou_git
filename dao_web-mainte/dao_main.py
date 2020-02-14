from django.db import connection


class DaoMain():
    """Daoの親クラス
        Args:
            query: sqlクエリ
            key_list: keyに設定するlist 
        Returns:
            res_list: selectの結果のタプル
    """
    def select(self,query):
        cursor = connection.cursor()
        #クエリ実行
        cursor.execute(query)
        #タプルを返す
        return cursor.fetchall()

    """Daoの親クラス
        Args:
            query: sqlクエリ
            param_list: sqlパラメータ
            key_list: keyに設定するlist 
        Returns:
            res_list: selectの結果のタプル
    """
    def selectWithParam(self,query,param_list):
        cursor = connection.cursor()
        #クエリ実行
        cursor.execute(query,param_list)
        #タプルを返す
        return cursor.fetchall()


    """Daoの親クラス
        Args:
            query: sqlクエリ
    """
    def update(self,query):
        cursor = connection.cursor()
        #クエリ実行
        cursor.execute(query)

    """Daoの親クラス
        Args:
            query: sqlクエリ
    """
    def updateWithParam(self,query,param_list):
        cursor = connection.cursor()
        #クエリ実行
        cursor.execute(query,param_list)

