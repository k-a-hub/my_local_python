from dataclasses import astuple

from dataclass.dtb_gift_prelist_customer_data import \
    dtb_gift_prelist_customer_data
from dataclass.dtb_gift_prelist_insert_data import dtb_gift_prelist_insert_data
from dataclass.dtb_gift_prelist_shipping_data import \
    dtb_gift_prelist_shipping_data
from dataclass.dtb_order_data import dtb_order_data
from dataclass.dtb_shipping_data import dtb_shipping_data
from db_accessor import db_accessor
from dtb_customer import dtb_customer


class dtb_gift_prelist:

    # コンストラクタ
    def __init__(self, dba: db_accessor):

        # DBアクセス
        self.dba: db_accessor = dba

        # 登録リスト
        self.insert_list: list = []
        # 登録時の分割件数
        self.split_insert_num = 5000

        # お届け先分割件数
        self.split_shipping_num = 5

        # 固定電話番号名
        self.phone_number_name: str = 'phone'
        # 携帯電話番号名
        self.mobile_number_name: str = 'mobile'
        # 携帯電話番号の携帯番号リスト
        self.mobile_phone_number_list: list = ['090', '080', '070', '050']


    # 登録データ生成
    def make_insert_data(self, order_id_dict: dict):

        # 予測変換を出すために定義
        order: dtb_order_data = None

        for order_id, order in order_id_dict.items():

            # 承り票番号を取得
            accept_no_select_sql: str = f"""
                SELECT
                    IFNULL(accept_no, 0) AS `accept_no`
                FROM
                    dtb_order_item
                WHERE
                    order_id = {order_id}
                LIMIT
                    1
            """
            select_list: list = self.dba.execute_query(accept_no_select_sql)
            accept_no: int = 0
            # 商品が1件も無い場合
            if len(select_list) >= 1:
                accept_no = select_list[0]['accept_no']

            # 非会員の場合、依頼主IDを取得
            if order.customer_id is None:
                customer_id_select_sql: str = f"""
                    SELECT
                        id
                    FROM
                        {dtb_customer.__name__}
                    WHERE
                        name01 = '{order.name01}'
                      AND
                        name02 = '{order.name02}'
                      AND
                        phone_number = '{order.phone_number}'
                """
                order.customer_id = self.dba.execute_query(customer_id_select_sql)[0]['id']

            # 依頼主側のデータ生成
            gift_prelist_customer_data: dtb_gift_prelist_customer_data = self.make_gift_prelist_customer(accept_no, order)

            # お届け先を取得
            shipping_select_sql = f"""
                SELECT
                    pref.name AS `pref_name`
                    ,ship.name01
                    ,ship.name02
                    ,ship.company_name
                    ,ship.phone_number
                    ,ship.postal_code
                    ,ship.addr01
                    ,ship.addr02
                    ,ship.position
                    ,ship.title
                FROM
                    dtb_shipping AS `ship`
                JOIN
                    mtb_pref AS `pref`
                  ON ship.pref_id = pref.id
                WHERE
                    order_id = {order_id}
            """
            shipping_list: list = self.dba.execute_query(shipping_select_sql)
            shipping_data_list: list = [dtb_shipping_data(**s) for s in shipping_list]
            # お届け先側のデータ生成
            gift_prelist_shipping_data_list = self.make_gift_prelist_shipping(shipping_data_list)

            # 登録データを整形して追加
            self.add_insert_list(gift_prelist_customer_data, gift_prelist_shipping_data_list)

        print('------------------------------')
        print(f'dtb_gift_prelistの追加件数: {len(self.insert_list)}件')
        print('------------------------------')


    # 登録データの依頼主側を生成
    def make_gift_prelist_customer(self, accept_no: int, order: dtb_order_data):

        # 登録するデータ
        data: dtb_gift_prelist_customer_data = dtb_gift_prelist_customer_data(
            accept_no=accept_no
            ,shop_code=order.shop_id
            ,customer_id=order.customer_id
            ,customer_phone_number=order.phone_number
            ,customer_postal_code1=order.postal_code[0:3]
            ,customer_postal_code2=order.postal_code[3:7]
            ,customer_address1=f"{order.pref_name}{order.addr01}"
            ,customer_address2=order.addr02
            ,customer_company_name=order.company_name
            ,customer_position=order.position
            ,customer_name=f"{order.name01}　{order.name02}"
            ,agent_code=order.agent_cd
            ,agent_name=order.agent_name
            ,sales_account_no=order.sales_account_no
            ,customer_char_code=order.customer_kbn
        )

        return data


    # 登録データのお届け先側を生成
    def make_gift_prelist_shipping(self, shipping_data_list: list):

        # 戻り値
        gift_prelist_shipping_data_list: list = []
        # ページ番号カウント
        page_no_count: int = 1
        # 予測変換のため定義
        shipping_data: dtb_shipping_data = None

        # お届け先の繰り返し
        for shipping_data in shipping_data_list:

            # 登録するデータ
            data: dtb_gift_prelist_shipping_data = dtb_gift_prelist_shipping_data(
                shipping_pageno=page_no_count
                ,shipping_phone_number=shipping_data.phone_number
                ,shipping_postal_code1=shipping_data.postal_code[0:3]
                ,shipping_postal_code2=shipping_data.postal_code[3:7]
                ,shipping_address1=f"{shipping_data.pref_name}{shipping_data.addr01}"
                ,shipping_address2=shipping_data.addr02
                ,shipping_company_name=shipping_data.company_name
                ,shipping_position=shipping_data.position
                ,shipping_name=f"{shipping_data.name01}　{shipping_data.name02}"
                ,shipping_title=shipping_data.title
            )

            # 戻り値のリストに詰める
            gift_prelist_shipping_data_list.append(data)

            # ページ番号のカウントを増やす
            page_no_count += 1

        return gift_prelist_shipping_data_list


    # 登録データの追加
    def add_insert_list(self, gift_prelist_customer_data: dtb_gift_prelist_customer_data, gift_prelist_shipping_data_list: list):

        # 依頼主のページ番号
        customer_page_no: int = 1
        # お届け先の数
        ship_len: int = len(gift_prelist_shipping_data_list)
        # お届け先カウント
        ship_count: int = 0

        # お届け先情報を5件ごとに分割
        for ship_index in range(0, ship_len, self.split_shipping_num):

            # 依頼主ページ番号セット
            gift_prelist_customer_data.page_no = customer_page_no

            # 5件のお届け先を取得
            shipping_list: list = gift_prelist_shipping_data_list[ship_index:ship_index + self.split_shipping_num]

            # 残りのお届け先件数
            remaining_ship_index = ship_len - (ship_count * self.split_shipping_num)

            # 残りのお届け先件数が5件より少ない場合、ダミーを作成
            if remaining_ship_index < self.split_shipping_num:
                # ダミー作成数
                dummy_index: int = self.split_shipping_num - remaining_ship_index
                [shipping_list.append(dtb_gift_prelist_shipping_data()) for idx in range(0, dummy_index, 1)]

            # 登録するデータ
            data: dtb_gift_prelist_insert_data = dtb_gift_prelist_insert_data(gift_prelist_customer_data, shipping_list)
            # 登録リストに追加
            self.insert_list.append(data)

            # ループカウンター増加
            customer_page_no += 1
            ship_count += 1


    # 追加処理
    def exec_insert(self):

        # 登録件数
        ins_count: int = 0
        # 登録データがある場合に実施
        if len(self.insert_list) > 0:

            # 登録SQL
            insert_sql: str = f"""
                INSERT INTO `{__class__.__name__}` (
                    {",".join([f"`{k}`" for k in dtb_gift_prelist_insert_data.__annotations__.keys()])}
                ) VALUES (
                    {",".join(["%s" for i in range(0, len(dtb_gift_prelist_insert_data.__annotations__.keys()))])}
                )
            """

            # 5000件ごとに分割
            for idx in range(0, len(self.insert_list), self.split_insert_num):

                # 5000件の配列を取り出す
                values_list: list = self.insert_list[idx: idx + self.split_insert_num]
                # タプルに変換してリスト化
                tuples_list: list = [astuple(value) for value in values_list]
                # 登録実施
                ins_count += self.dba.execute_insert(insert_sql, tuples_list)

        print(f"\t追加実行件数: {ins_count}件")


