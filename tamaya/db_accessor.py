import mysql.connector as mysql


class db_accessor:

    # mysql接続情報
    # Dockerで作成した別コンテナのmysql環境に接続する情報
    config = {
        'host': 'tamaya_db'
        , 'port': '3306'
        , 'user': 'test'
        , 'password': 'password'
        , 'database': 'tamaya'
        , 'auth_plugin': 'mysql_native_password'
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

