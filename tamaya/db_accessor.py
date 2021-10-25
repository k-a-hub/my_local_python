from datetime import date
import mysql.connector as mysql


class db_accessor:

    # mysql接続情報
    # saga_tamaya_mysql_1への接続情報
    config = {
        'host': 'saga_tamaya_mysql_1'
        , 'port': '3306'
        , 'user': 'dbuser'
        , 'password': 'secret'
        , 'database': 'sagatamaya_ec1'
    }

    # コンストラクタ
    def __init__(self):

        try:
            # mysqlに接続
            self.conn = mysql.connect(**self.config)
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
    def execute_query(self, sql):
        try:
            # クエリ実行
            self.cur.execute(sql)
            result = self.cur.fetchall()
            return result
        except Exception as e:
            print(f"query error: \r\n{e}")

    # UPDATE実行
    def excecute_update(self, sql):

        try:
            self.cur.execute(sql)
            # self.conn.commit()
            return max(self.cur.rowcount, 1)
        except Exception as e:
            self.conn.rollback()
            print(f"update error: \r\n{e}")
            print(f"query: {sql}")

    # INSERT実行
    def execute_insert(self, sql):
        
        try:
            self.cur.execute(sql)
            # self.conn.commit()
            return self.cur.rowcount
        except Exception as e:
            self.conn.rollback()
            print(f"insert error: \r\n{e}")
            # print(f"query: {sql}")

