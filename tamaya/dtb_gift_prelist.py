from dataclasses import astuple

from dataclass.dtb_customer_address_data import dtb_customer_address_data
from dataclass.dtb_customer_data import dtb_customer_data
from dataclass.dtb_gift_prelist_customer_data import \
    dtb_gift_prelist_customer_data
from dataclass.dtb_gift_prelist_insert_data import dtb_gift_prelist_insert_data
from dataclass.dtb_gift_prelist_shipping_data import \
    dtb_gift_prelist_shipping_data
from db_accessor import db_accessor
from dtb_customer import dtb_customer
from dtb_customer_address import dtb_customer_address


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
    def make_insert_data(self, customer_id_list: list):

        for customer_id in customer_id_list:

            # 依頼主の最新受注の承り票番号を取得
            latest_order_sql = f"""
                SELECT
                    order.id
                    ,order.order_date
                    -- TODO: 承り票番号がない場合は0を仮代入
                    ,IFNULL(item.accept_no, 0) AS `accept_no`
                    ,shop_id
                FROM
                    dtb_order AS `order`
                LEFT OUTER JOIN
                    dtb_order_item AS `item`
                  ON order.id = item.order_id
                WHERE
                    order.customer_id = {customer_id}
                ORDER BY
                    order.order_date DESC
                    ,order.id DESC
                LIMIT
                    1
            """
            # 最新の受注情報1件を取得
            latest_order = self.dba.execute_query(latest_order_sql)[0]

            # 登録更新を行った受注の依頼主情報を取得
            customer_select_sql = f"""
                SELECT
                    customer.id
                    ,customer.phone_number
                    ,customer.postal_code
                    ,pref.name AS `pref_name`
                    ,customer.addr01
                    ,customer.addr02
                    ,customer.company_name
                    ,customer.position
                    ,customer.name01
                    ,customer.name02
                    ,customer.agent_cd
                    ,mem.name AS `mem_name`
                    ,customer.sales_account_no
                FROM
                    `{dtb_customer.__name__}` AS `customer`
                JOIN
                    `mtb_pref` AS `pref`
                  ON customer.pref_id = pref.id
                LEFT OUTER JOIN
                    `dtb_member` AS `mem`
                  ON customer.agent_cd = mem.id
                WHERE
                    customer.id = {customer_id}
            """
            # 会員情報を取得
            customer = self.dba.execute_query(customer_select_sql)[0]
            # データクラスに変換
            customer_data = dtb_customer_data(**customer)

            # 依頼主側のデータ生成
            gift_prelist_customer_data: dtb_gift_prelist_customer_data = self.make_gift_prelist_customer(latest_order, customer_data)

            # 登録更新を行った受注の依頼主のお届け先情報を取得
            customer_address_select_sql = f"""
                SELECT
                    c_addr.*
                    ,pref.name AS `pref_name`
                FROM
                    `{dtb_customer_address.__name__}` AS `c_addr`
                JOIN
                    `mtb_pref` AS `pref`
                  ON c_addr.pref_id = pref.id
                WHERE
                    c_addr.customer_id = {customer_id}
            """
            customer_address_list = self.dba.execute_query(customer_address_select_sql)
            customer_address_data_list = [dtb_customer_address_data(**ca) for ca in customer_address_list]
            # お届け先側のデータ生成
            gift_prelist_shipping_data_list: list = self.make_gift_prelist_shipping(customer_address_data_list)

            # 登録データを整形して追加
            self.add_insert_list(gift_prelist_customer_data, gift_prelist_shipping_data_list)

        print('------------------------------')
        print(f'dtb_gift_prelistの追加件数: {len(self.insert_list)}件')
        print('------------------------------')


    # 登録データの依頼主側を生成
    def make_gift_prelist_customer(self, latest_order: dict, customer_data: dtb_customer_data):

        # 電話番号の判別
        phone_type = self.type_phone_number(customer_data.phone_number)
        # 電話番号の分割
        split_phone_number_dict: dict = self.split_phone_number(phone_type, customer_data.phone_number)

        # 登録するデータ
        data: dtb_gift_prelist_customer_data = dtb_gift_prelist_customer_data(
            accept_no=latest_order['accept_no']
            ,shop_code=latest_order['shop_id']
            ,customer_id=customer_data.id
            ,customer_phone_number=customer_data.phone_number
            ,customer_phone_number1=split_phone_number_dict['customer_phone_number1']
            ,customer_phone_number2=split_phone_number_dict['customer_phone_number2']
            ,customer_phone_number3=split_phone_number_dict['customer_phone_number3']
            ,customer_postal_code1=customer_data.postal_code[0:3]
            ,customer_postal_code2=customer_data.postal_code[3:7]
            ,customer_address1=customer_data.pref_name
            ,customer_address2=customer_data.addr01
            ,customer_address3=customer_data.addr02
            ,customer_company_name=customer_data.company_name
            ,customer_name=customer_data.name01 + '　' + customer_data.name02
            ,customer_mobile_number1=split_phone_number_dict['customer_mobile_number1']
            ,customer_mobile_number2=split_phone_number_dict['customer_mobile_number2']
            ,customer_mobile_number3=split_phone_number_dict['customer_mobile_number3']
            ,agent_code=customer_data.agent_cd
            ,agent_name=customer_data.mem_name
            ,sales_account_no=customer_data.sales_account_no
        )

        return data


    # 登録データのお届け先側を生成
    def make_gift_prelist_shipping(self, customer_address_data_list: list):

        # 戻り値
        gift_prelist_shipping_data_list: list = []
        # ページ番号カウント
        page_no_count: int = 1

        # お届け先の繰り返し
        for customer_address_data in customer_address_data_list:

            # お届け先の購入商品を取得
            order_item_select_sql: str = f"""
                SELECT
                    item.product_name
                    ,item.quantity
                    ,item.price
                FROM
                    dtb_order_item AS `item`
                JOIN (
                    SELECT
                        MAX(item.order_id) AS `order_id`
                    FROM
                        dtb_customer_address AS `ca`
                    LEFT OUTER JOIN
                        dtb_shipping AS `ship` ON ca.name01 = ship.name01
                      AND ca.name02 = ship.name02
                    LEFT OUTER JOIN
                        dtb_order_item AS `item` ON ship.id = item.shipping_id
                    LEFT OUTER JOIN
                        dtb_order AS `o` ON ship.order_id = o.id
                    WHERE
                        ca.customer_id = {customer_address_data.customer_id}
                      AND ca.name01 = '{customer_address_data.name01}'
                      AND ca.name02 = '{customer_address_data.name02}'
                ) AS `temp1` ON item.order_id = temp1.order_id
                JOIN
                    dtb_shipping AS `ship` ON item.shipping_id = ship.id
                WHERE
                    item.product_code IS NOT NULL
                  AND ship.name01 = '{customer_address_data.name01}'
                  AND ship.name02 = '{customer_address_data.name02}'
            """
            # お届け先の購入商品一覧を取得
            order_item_list: list = self.dba.execute_query(order_item_select_sql)

            # 電話番号の判別
            phone_type: str = self.type_phone_number(customer_address_data.phone_number)
            # 電話番号の分割
            split_phone_number_dict: dict = self.split_phone_number(phone_type, customer_address_data.phone_number)

            # 登録するデータ
            data: dtb_gift_prelist_shipping_data = dtb_gift_prelist_shipping_data(
                shipping_pageno=page_no_count
                ,shipping_phone_number=customer_address_data.phone_number
                ,shipping_postal_code1=customer_address_data.postal_code[0:3]
                ,shipping_postal_code2=customer_address_data.postal_code[3:7]
                ,shipping_address1=customer_address_data.pref_name
                ,shipping_address2=customer_address_data.addr01
                ,shipping_address3=customer_address_data.addr02
                ,shipping_company_name=customer_address_data.company_name
                ,shipping_position=customer_address_data.position
                ,shipping_name=f'{customer_address_data.name01}　{customer_address_data.name02}'
                ,shipping_title=customer_address_data.title
            )

            # 電話番号の設定
            data.set_phone_number(self.phone_number_name, self.mobile_number_name, phone_type, split_phone_number_dict)

            # 購入商品の設定
            data.set_product(order_item_list)

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


    # 電話番号の判別
    def type_phone_number(self, phone_number: str):

        phone_type: str = ''

        if phone_number[0:3] in self.mobile_phone_number_list:
            # 携帯電話番号
            phone_type = self.mobile_number_name
        else:
            # 固定電話番号
            phone_type = self.phone_number_name

        self.split_phone_number(phone_type, phone_number)

        return phone_type


    # 電話番号の分割
    def split_phone_number(self, phone_type: str, phone_number: str):

        split_dict: dict = {
            'customer_phone_number1': None
            ,'customer_phone_number2': None
            ,'customer_phone_number3': None
            ,'customer_mobile_number1': None
            ,'customer_mobile_number2': None
            ,'customer_mobile_number3': None
        }

        if phone_type == self.phone_number_name:
            # 固定電話番号の場合
            # TODO: 分割方法未定
            pass
        elif phone_type == self.mobile_number_name:
            # 携帯電話番号の場合
            # 3桁, 4桁, 4桁で分割
            split_dict['customer_mobile_number1'] = phone_number[0:3]
            split_dict['customer_mobile_number2'] = phone_number[3:7]
            split_dict['customer_mobile_number3'] = phone_number[7:11]

        return split_dict

