from sys import exit

from dataclass.dtb_order_data import dtb_order_data
from db_accessor import db_accessor


class dtb_order:

    # コンストラクタ
    def __init__(self, dba: db_accessor):

        # DBアクセス
        self.db_accessor: db_accessor = dba
        # 依頼主IDをキーに受注IDを配列化した変数
        self.customer_id_order_id_dict: dict = {}


    # 期間内受注一覧取得
    def get_order_list(self, order_date: str):

        # 期間内の受注情報SELECT文
        order_select_sql: str = f"""
            SELECT
                order.id AS order_id
                ,order.customer_id AS customer_id
                ,order.order_date
            FROM
                dtb_order AS `order`
            JOIN
                dtb_customer AS `customer` ON order.customer_id = customer.id
            WHERE
                order.payment_id IN (7, 8, 9)
              AND
                order.order_date >= '{order_date}'
            GROUP BY
                order.customer_id
                ,order.id
            ORDER BY
                order.customer_id
        """
        # 受注情報の取得
        order_list: list = self.db_accessor.execute_query(order_select_sql)
        # データクラスに変換してリスト化
        order_data_list: list = [dtb_order_data(**o) for o in order_list]
        print(f"期間内の受注件数: {len(order_data_list)}件")

        # 期間内で受注情報が存在しない場合
        if len(order_data_list) == 0:
            print("処理データ無しで終了しました。")
            exit()

        # 受注情報の繰り返し
        for order_data in order_data_list:

            # 受注ID
            order_id: int = order_data.order_id
            # 依頼主ID
            customer_id: int = order_data.customer_id

            # 既に依頼主IDが存在するか
            if customer_id in self.customer_id_order_id_dict:
                # 受注ID配列に追加
                self.customer_id_order_id_dict[customer_id].append(order_id)
            else:
                # 依頼主IDをキーに受注IDの配列を追加
                self.customer_id_order_id_dict[customer_id] = [order_id]

