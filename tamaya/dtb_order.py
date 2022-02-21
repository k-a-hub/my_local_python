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
        # 依頼主IDをキーに受注情報を配列化した変数
        self.customer_id_order_dict: dict = {}
        # 依頼主IDのリスト
        self.customer_id_list: list = []
        # 非会員の名前と電話番号をキーに受注情報を格納した変数
        self.non_customer_dict: dict = {}
        # 非会員の名前と電話番号をキーに受注IDを配列化した変数
        self.non_customer_order_id_dict: dict = {}
        # gift_prelist用の受注IDをキーに受注情報を格納した変数
        self.gift_prelist_order_id_dict: dict = {}


    # 期間内受注一覧取得
    def get_order_list(self, order_date: str):

        # 期間内の受注情報SELECT文
        order_select_sql: str = f"""
            SELECT
                order.id AS order_id
                ,order.customer_id AS customer_id
                ,order.sex_id
                ,order.job_id
                ,order.country_id
                ,order.pref_id
                ,pref.name AS pref_name
                ,order.name01
                ,order.name02
                ,order.kana01
                ,order.kana02
                ,order.company_name
                ,order.postal_code
                ,order.addr01
                ,order.addr02
                ,order.email
                ,order.phone_number
                ,order.birth
                ,order.update_date
                ,order.order_date
                ,order.shop_id
                ,order.agent_cd
                ,member.name AS agent_name
                ,order.sales_account_no
                ,order.position
                ,IFNULL(customer.customer_kbn, 0) AS customer_kbn
            FROM
                dtb_order AS `order`
            LEFT OUTER JOIN
                dtb_customer AS `customer` ON order.customer_id = customer.id
            JOIN
                mtb_pref AS `pref` ON order.pref_id = pref.id
            JOIN
                dtb_member AS `member` ON order.agent_cd = member.id
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

            # gift_prelist用に受注IDをキーに受注情報を格納
            self.gift_prelist_order_id_dict[order_id] = order_data

            # 非会員の受注か確認
            if customer_id is None:
                # 名前と電話番号を結合
                name_phone_join = f"{order_data.name01},{order_data.name02},{order_data.phone_number}"

                # 既に名前と電話番号が存在するか
                if name_phone_join in self.non_customer_dict:
                    # 最新の受注情報か
                    if order_data.order_date >= self.non_customer_dict[name_phone_join].order_date:
                        # 最新の受注情報を格納
                        self.non_customer_dict[name_phone_join] = order_data
                else:
                    # 名前と電話番号をキーに受注情報の配列に追加
                    self.non_customer_dict[name_phone_join] = order_data

                # 既に名前と電話番号が存在するか
                if name_phone_join in self.non_customer_order_id_dict:
                    # 受注ID配列に追加
                    self.non_customer_order_id_dict[name_phone_join].append(order_id)
                else:
                    # 非会員の名前と電話番号をキーに受注IDの配列に追加
                    self.non_customer_order_id_dict[name_phone_join] = [order_id]

                # 非会員なので以降の処理は行わず、次の受注を参照
                continue

            # 既に依頼主IDが存在するか
            if customer_id in self.customer_id_order_id_dict:
                # 受注ID配列に追加
                self.customer_id_order_id_dict[customer_id].append(order_id)
            else:
                # 依頼主IDをキーに受注IDの配列を追加
                self.customer_id_order_id_dict[customer_id] = [order_id]

            # 既に依頼主IDが存在するか
            if customer_id in self.customer_id_order_dict:
                # 最新の受注情報か
                if order_data.order_date >= self.customer_id_order_dict[customer_id].order_date:
                    # 最新の受注方法を格納
                    self.customer_id_order_dict[customer_id] = order_data
            else:
                # 依頼主IDをキーに受注情報の配列に追加
                self.customer_id_order_dict[customer_id] = order_data

        # 差分はないはずだけど、2つのdictのキーを配列に変換して、一意の値化
        customer_id_list: set = set(list(self.customer_id_order_dict.keys()) + list(self.customer_id_order_dict.keys()))
        # 受注の依頼主IDをリストに変換して保持
        self.customer_id_list = list(customer_id_list)
        # gift_prelist用の受注IDを昇順で並び替え
        tuple_list = sorted(self.gift_prelist_order_id_dict.items())
        self.gift_prelist_order_id_dict.clear()
        self.gift_prelist_order_id_dict.update(tuple_list)

