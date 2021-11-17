from mysql.connector import connect


class db_accessor:

    # mysql接続情報
    # saga_tamaya_mysql_1への接続情報
    config: dict = {
        'host': 'saga_tamaya_mysql_1'
        , 'port': '3306'
        , 'user': 'dbuser'
        , 'password': 'secret'
        , 'database': 'sagatamaya_ec1'
    }


    # コンストラクタ
    def __init__(self, commit_flg = True):

        # コミットを行うかのフラグ
        self.commit_flg = commit_flg

        try:
            # mysqlに接続
            self.conn = connect(**self.config)
            # コネクションが切れた時に再接続してくれるよう設定
            self.conn.ping(reconnect=True)
            # 自動コミット設定をオフ
            self.conn.autocommit = False

            self.conn.is_connected()
            # カーソル情報の作成(辞書型リストとして結果を取得するよう設定)
            self.cur = self.conn.cursor(dictionary=True)
        except Exception as e:
            print(f"connect error: \r\n{e}")


    # デストラクタ
    def __del__(self):

        try:
            self.conn.close()
        except Exception as e:
            print(f"connect close error: \r\n{e}")


    # クエリ実行
    def execute_query(self, sql: str):

        try:
            # クエリ実行
            self.cur.execute(sql)
            result = self.cur.fetchall()
            return result
        except Exception as e:
            print(f"query error: \r\n{e}")


    # UPDATE実行
    def execute_update(self, sql: str, value: list):

        try:
            self.cur.executemany(sql, value)
            if self.commit_flg: self.conn.commit()
            # 更新の必要がない場合、0を返すので、最大値で1を返す
            return max(self.cur.rowcount, 1)
        except Exception as e:
            self.conn.rollback()
            print(f"update error: \r\n{e}")


    # INSERT実行
    def execute_insert(self, sql: str, values: list):

        try:
            self.cur.executemany(sql, values)
            if self.commit_flg: self.conn.commit()
            return self.cur.rowcount
        except Exception as e:
            self.conn.rollback()
            print(f"insert error: \r\n{e}")
            # print(self.cur._executed)


    # DELETE実行
    def execute_delete(self, sql: str, values: list):

        try:
            self.cur.executemany(sql, values)
            if self.commit_flg: self.conn.commit()
            return self.cur.rowcount
        except Exception as e:
            self.conn.rollback()
            print(f"delete error: \r\n{e}")

