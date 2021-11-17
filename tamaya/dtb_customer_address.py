from dataclasses import astuple
from datetime import datetime

from dataclass.dtb_customer_address_data import dtb_customer_address_data
from dataclass.dtb_customer_address_delete_data import dtb_customer_delete_data
from dataclass.dtb_customer_address_insert_data import \
    dtb_customer_address_insert_data
from dataclass.dtb_customer_address_update_data import \
    dtb_customer_address_update_data
from dataclass.dtb_shipping_join_order_item_data import \
    dtb_order_shipping_join_order_item_data
from db_accessor import db_accessor


class dtb_customer_address:

    # コンストラクタ
    def __init__(self, dba: db_accessor):

        # DBアクセス
        self.dba: db_accessor = dba

        # 依頼主ごとの重複を削除した最新のお届け先リスト
        self.deduplication_latest_shipping_list: dict = {}

        # 更新リスト
        self.update_list: list = []
        # 登録リスト
        self.insert_list: list = []
        # 削除リスト
        self.delete_list: list = []

        # 登録データの設定値
        # 登録日時
        self.insert_create_date: str = datetime.now().strftime('%Y-%m-%d %H:%M:00')
        # 識別用値
        self.insert_discriminator_type: str = "customeraddress"
        # ページ番号
        self.insert_max_page_no_select_sql: str = """
            SELECT
                IFNULL(MAX(page_no)+1, 1) AS `page_no`
            FROM
                `dtb_customer_address`
            WHERE
                customer_id = {}
        """
        # 分割件数
        self.insert_division_num: int = 5000


    # お届け先の更新、登録リストへの追加
    def add_upsert_list(self, customer_id_order_id_dict: dict):

        # 期間内の依頼主IDと受注IDのデータを繰り返す
        for customer_id, order_id_list in customer_id_order_id_dict.items():

            # お届け先情報の取得
            # dtb_shippingとdtb_order_itemの結合
            order_shipping_join_order_item_select_sql: str = f"""
                SELECT
                    ship.id AS ship_id
                    ,ship.country_id
                    ,ship.pref_id
                    ,ship.name01
                    ,ship.name02
                    ,ship.kana01
                    ,ship.kana02
                    ,ship.company_name
                    ,ship.postal_code
                    ,ship.addr01
                    ,ship.addr02
                    ,ship.phone_number
                    ,ship.update_date
                    ,ship.position
                    ,ship.title
                    ,item.id AS item_id
                    ,accept_no
                FROM (
                    SELECT
                        MAX(ship.id) AS ship_id, name01, name02, MAX(update_date)
                    FROM
                        dtb_shipping AS `ship`
                    WHERE
                        ship.order_id IN (
                            {",".join([str(o) for o in order_id_list])}
                        )
                    GROUP BY
                        name01
                        ,name02
                ) AS `ship1`
                JOIN
                    dtb_shipping AS `ship` ON ship.id = ship1.ship_id
                JOIN
                    dtb_order_item AS `item` ON ship.id = item.shipping_id
                WHERE
                    item.product_code IS NOT NULL
            """
            # 受注IDをキーにお届け先と購入商品を取得
            select_list: list = self.dba.execute_query(order_shipping_join_order_item_select_sql)
            # データクラスに変換してリスト化
            order_shipping_join_order_item_data_list: list = [dtb_order_shipping_join_order_item_data(**s) for s in select_list]
            # 重複を削除した最新のお届け先リストに追加
            self.deduplication_latest_shipping_list[customer_id] = order_shipping_join_order_item_data_list

        # 重複を削除した最新のお届け先の繰り返し
        for customer_id, shipping_list in self.deduplication_latest_shipping_list.items():

            # 登録時のページ番号を取得
            page_no: int = int(self.dba.execute_query(self.insert_max_page_no_select_sql.format(customer_id))[0]['page_no'])

            for shipping in shipping_list:
                # 受注の依頼主IDとお届け先の名前をキーに依頼主のお届け先情報のSELECT文
                # dtb_customer_addressのみ
                customer_address_select_sql: str = f"""
                    SELECT
                        *
                    FROM
                        dtb_customer_address
                    WHERE
                        customer_id = {customer_id}
                      AND
                        name01 = '{shipping.name01}'
                      AND
                        name02 = '{shipping.name02}'
                """
                # 依頼主のお届け先情報を取得
                customer_address_data: list = self.dba.execute_query(customer_address_select_sql)
                # 取得有無の確認
                if len(customer_address_data) > 0:
                    # 取得できれば更新
                    data: dtb_customer_address_data = dtb_customer_address_data(**customer_address_data[0])
                    # 更新リストに追加
                    self.add_update_list(shipping, data)
                else:
                    # 取得できなければ追加
                    self.add_insert_list(customer_id, shipping, page_no)
                    # ページ番号を加算
                    page_no += 1

        print("------------------------------")
        print(f" dtb_customer_addresの更新件数: {len(self.update_list)}件")
        print(f" dtb_customer_addresの追加件数: {len(self.insert_list)}件")
        print("------------------------------")
        print("dtb_customer_addressへの反映")


    # 更新リスト追加
    def add_update_list(self, shipping: dtb_order_shipping_join_order_item_data, customer_address: dtb_customer_address_data):

        # 更新するデータ
        data: dtb_customer_address_update_data = dtb_customer_address_update_data(
            shipping.country_id
            ,shipping.pref_id
            ,shipping.name01
            ,shipping.name02
            ,shipping.kana01
            ,shipping.kana02
            ,shipping.company_name
            ,shipping.postal_code
            ,shipping.addr01
            ,shipping.addr02
            ,shipping.phone_number
            ,shipping.update_date
            ,shipping.position
            ,shipping.title
            ,shipping.accept_no
            ,customer_address.id
        )
        # 更新する受注のお届け先情報を追加
        self.update_list.append(data)


    # 登録リスト追加
    def add_insert_list(self, customer_id: int, shipping: dtb_order_shipping_join_order_item_data, page_no: int):

        # 登録するデータ
        data: dtb_customer_address_insert_data = dtb_customer_address_insert_data(
            customer_id
            ,shipping.country_id
            ,shipping.pref_id
            ,shipping.name01
            ,shipping.name02
            ,shipping.kana01
            ,shipping.kana02
            ,shipping.company_name
            ,shipping.postal_code
            ,shipping.addr01
            ,shipping.addr02
            ,shipping.postal_code
            ,self.insert_create_date
            ,shipping.update_date
            ,self.insert_discriminator_type
            ,shipping.position
            ,shipping.title
            ,shipping.accept_no
            ,page_no
        )
        # 登録する受注のお届け先情報を追加
        self.insert_list.append(data)


    # 今シーズンで削除のお届け先情報の取得
    def get_delete_end_season(self):
        # 今シーズンで削除のお届け先情報のSELECT文
        delete_end_season_select_sql: str = f"""
            SELECT
                id
            FROM
                `{__class__.__name__}`
            WHERE
                delete_end_season = 1
        """

        # 今シーズンで削除のお届け先情報を取得
        delete_end_season_list: list = self.dba.execute_query(delete_end_season_select_sql)
        # データクラスに変換してリスト化
        delete_end_season_data_list: list = [dtb_customer_address_data(**d) for d in delete_end_season_list]

        # 取得して削除リストに詰める
        self.add_delete_list(delete_end_season_data_list)
        print("------------------------------")
        print(f" 今シーズンで削除のお届け先リスト: {len(self.delete_list)}件")
        print("------------------------------")


    # 削除リスト追加
    def add_delete_list(self, customer_address_list: list):

        for customer_address in customer_address_list:

            # 削除するデータ
            data = dtb_customer_delete_data(
                customer_address.id
            )
            # 削除するお届け先を追加
            self.delete_list.append(data)


    # 更新処理
    def exec_update(self):

        # 更新件数
        upd_count: int = 0
        # 更新データがある場合に実施
        if len(self.update_list) > 0:
            for update in self.update_list:
                # 更新SQL
                update_sql: str = f"""
                    UPDATE
                        `{__class__.__name__}`
                    SET
                        country_id = %s
                        ,pref_id = %s
                        ,name01 = %s
                        ,name02 = %s
                        ,kana01 = %s
                        ,kana02 = %s
                        ,company_name = %s
                        ,postal_code = %s
                        ,addr01 = %s
                        ,addr02 = %s
                        ,phone_number = %s
                        ,update_date = %s
                        ,position = %s
                        ,title = %s
                        ,accept_no = %s
                    WHERE
                        id = %s
                """
                # 更新実施
                upd_count += self.dba.execute_update(update_sql, [astuple(update)])

        print(f"\t更新実行件数: {upd_count}件")


    # 追加処理
    def exec_insert(self):

        # 登録件数
        ins_count: int = 0
        # 登録データがある場合に実施
        if len(self.insert_list) > 0:

            # 登録SQL
            insert_sql: str = f"""
                INSERT INTO `{__class__.__name__}` (
                    {",".join([f"`{k}`" for k in dtb_customer_address_insert_data.__annotations__.keys()])}
                ) VALUES (
                    {",".join("%s" for i in range(0, len(dtb_customer_address_insert_data.__annotations__.keys())))}
                )
            """

            # 5000件ごとに分割
            for idx in range(0, len(self.insert_list), self.insert_division_num):

                # 5000件の配列を取り出す
                values_list: list = self.insert_list[idx:idx + self.insert_division_num]
                # タプルに変換してリスト化
                tuples_list: list = [astuple(value) for value in values_list]
                # 登録実施
                ins_count += self.dba.execute_insert(insert_sql, tuples_list)

        print(f"\t追加実行件数: {ins_count}件")


    # 削除処理
    def exec_delete(self):

        print("dtb_customer_addressの今シーズン削除のお届け先削除")
        # 削除件数
        del_count: int = 0
        # 削除データがある場合に実施
        if len(self.delete_list) > 0:

            # 削除SQL
            delete_sql = f"""
                DELETE FROM
                    `{__class__.__name__}`
                WHERE\
                    id IN ({",".join('%s' for i in range(0, len(dtb_customer_delete_data.__annotations__.keys())))})
            """

            # タプルに変換してリスト化
            tuples_list: list = [astuple(d) for d in self.delete_list]
            # 削除実施
            del_count += self.dba.execute_delete(delete_sql, tuples_list)

        print(f"\t削除実行件数: {del_count}件")

