from admin_app.dao.dao_main import DaoMain

class DaoTUpdateHistory(DaoMain):

    # 更新履歴取得（最新5件）
    def selectChangeByTableName(self, table_name):

        param = {'table_name' : table_name}
        sql =   """
                SELECT
                  t_update_history.update_time
                , t_update_history.update_user
                , t_update_history.update_table
                , t_update_history.target_name
                , t_update_history.operation
                , t_update_history.remarks
                FROM t_update_history
                WHERE update_table = %(table_name)s
                ORDER BY t_update_history.update_time DESC
                LIMIT 5;
                """

        return self.selectWithParam(sql, param)

    def selectChangeRecordByTableName(self, table_name):
        '''
        更新履歴全件取得
        '''
        param = {'table_name' : table_name}
        sql =   """
                SELECT
                  t_update_history.update_time
                , t_update_history.update_user
                , t_update_history.update_table
                , t_update_history.target_name
                , t_update_history.operation
                , t_update_history.remarks
                FROM t_update_history
                WHERE update_table = %(table_name)s
                ORDER BY t_update_history.update_time DESC
                """

        return self.selectWithParam(sql, param)

    def selectChangeRecordByDate(self, table_name, datefrom='1900/01/01', dateto='2099/12/31'):
        '''
        更新履歴期間指定取得
        '''
        param = {
            'table_name' : table_name,
            'datefrom' : str(datefrom) + ' 00:00:00.000',
            'dateto' : str(dateto) + ' 23:59:59.999'
        }
        sql =   """
                SELECT
                  t_update_history.update_time
                , t_update_history.update_user
                , t_update_history.update_table
                , t_update_history.target_name
                , t_update_history.operation
                , t_update_history.remarks 
                FROM t_update_history
                WHERE update_table = %(table_name)s
                AND update_time >= %(datefrom)s
                AND update_time <= %(dateto)s
                ORDER BY t_update_history.update_time DESC
                """
        return self.selectWithParam(sql, param)

    def insert(self,entity):
        '''
        更新履歴の登録
        '''
        sql =   """
                INSERT INTO t_update_history
                (
                   update_id
                   , update_table
                   , operation
                   , target_name
                   , remarks
                   , update_user
                   , update_time
                )
                VALUES (nextval('t_update_history_update_id_seq'::regclass), %s, %s, %s, %s, %s, now())
                """

        return self.updateWithParam(sql,entity)

    def selectChangeForHomeListByTableName(self, table_name, table_name2):
        '''
        更新履歴取得（最新5件）お知らせ編集画面用
        '''
        param = {
            'table_name' : table_name,
            'table_name2' : table_name2,
        }
        sql =   """
                SELECT
                t_update_history.update_time
                , t_update_history.update_user
                , t_update_history.operation
                , t_update_history.target_name
                , t_update_history.remarks
                , t_update_history.update_table
                FROM t_update_history
                WHERE (update_table = %(table_name)s OR update_table = %(table_name2)s)
                ORDER BY t_update_history.update_time DESC
                LIMIT 5;
                """
        return self.selectWithParam(sql, param)
                
    def selectChangeRecordForHomeListByTableName(self, table_name, table_name2):
        '''
        更新履歴全件取得お知らせ編集画面用
        '''
        param = {
            'table_name' : table_name,
            'table_name2' : table_name2,
        }
        sql =   """
                SELECT
                t_update_history.update_time
                , t_update_history.update_user
                , t_update_history.update_table
                , t_update_history.target_name
                , t_update_history.operation
                , t_update_history.remarks
                FROM t_update_history
                WHERE (update_table = %(table_name)s OR update_table = %(table_name2)s)
                ORDER BY t_update_history.update_time DESC
                """
                
        return self.selectWithParams(sql, param)
                
    def selectChangeRecordForHomeListByDate(self, table_name, table_name2, datefrom='1900/01/01', dateto='2099/12/31'):
        '''
        更新履歴期間指定取得お知らせ編集画面用
        '''
        param = {
            'table_name' : table_name,
            'table_name2' : table_name2,
            'datefrom' : str(datefrom) + ' 00:00:00.000',
            'dateto' : str(dateto) + ' 23:59:59.999'
        }
        sql =   """
                SELECT
                t_update_history.update_time
                , t_update_history.update_user
                , t_update_history.update_table
                , t_update_history.target_name
                , t_update_history.operation
                , t_update_history.remarks 
                FROM t_update_history
                WHERE (update_table = %(table_name)s OR update_table = %(table_name2)s)
                AND update_time >= %(datefrom)s
                AND update_time <= %(dateto)s
                ORDER BY t_update_history.update_time DESC
                """
                
        return self.selectWithParam(sql, param)

    def insertBySakuhinlist(self,entity):
        '''
        作品リストをもとに更新履歴の登録
        '''
        sql =   """
                INSERT 
                INTO t_update_history( 
                    update_id
                    , update_table
                    , operation
                    , target_name
                    , remarks
                    , update_user
                    , update_time
                    ) 
                select
                    nextval('t_update_history_update_id_seq' ::regclass)
                    , %(update_table)s
                    , %(operation)s
                    , %(target_name)s
                    , sakuhin_name
                    , %(full_name)s
                    , now() 
                from
                m_sakuhin
                where
                sakuhin_code in %(sakuhin_code_list)s
                AND invalid_flg = false
                """
        return self.updateWithParam(sql,entity)

    def insertByIplist(self,entity):
        '''
        IPリストをもとに更新履歴の登録
        '''
        sql =   """
                INSERT 
                INTO t_update_history( 
                    update_id
                    , update_table
                    , operation
                    , target_name
                    , remarks
                    , update_user
                    , update_time
                ) 
                select
                    nextval('t_update_history_update_id_seq' ::regclass)
                    , %(update_table)s
                    , %(operation)s
                    , ip_name
                    , %(remarks)s
                    , %(full_name)s
                    , now()
                from
                m_ip 
                where
                ip_code in %(ip_code_list)s
                AND invalid_flg = false
                """
        return self.updateWithParam(sql,entity)

    def insertByTitleList(self,sakuhin_name,title_name_list,category_name_list,full_name):
        '''タイトルリストをもとに更新履歴の登録'''
        sql =   """
                INSERT 
                INTO t_update_history(
                    update_id
                    , update_table
                    , operation
                    , target_name
                    , remarks
                    , update_user
                    , update_time
                ) VALUES
                """
        params = []
        for i in range(len(title_name_list)):
            if i > 0:
                sql += ','
            sql += "(nextval('t_update_history_update_id_seq'::regclass)"
            sql += ", 'm_sakuhin_map'"
            sql += ", '追加'"
            sql += ", %s"
            sql += ", %s"
            sql += ", %s"
            sql += ", now()"
            sql += ")"

            params.append(sakuhin_name)
            params.append(category_name_list[i] + title_name_list[i])
            params.append(full_name)

        return self.updateWithParam(sql,params)

    def insertSakuhinMapBylist(self,entity):
        '''
        作品リストをもとに更新履歴の登録
        '''
        sql =   """
                INSERT 
                INTO t_update_history( 
                    update_id
                    , update_table
                    , operation
                    , target_name
                    , remarks
                    , update_user
                    , update_time
                    ) 
                select
                    nextval('t_update_history_update_id_seq' ::regclass)
                    , %(update_table)s
                    , %(operation)s
                    , sakuhin_name
                    , %(remarks)s
                    , %(full_name)s
                    , now() 
                from
                m_sakuhin
                where
                sakuhin_code in %(sakuhin_code_list)s
                AND invalid_flg = false
                """
        return self.updateWithParam(sql,entity)