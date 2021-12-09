from dataclasses import dataclass, field


@dataclass(init=True)
class dtb_gift_prelist_shipping_data:

    # ページ番号
    shipping_pageno: int = field(default=0)
    # お届け先電話番号
    shipping_phone_number: str = field(default=None)
    # お届け先固定電話番号、市外局番
    shipping_phone_number1: str = field(default=None)
    # お届け先固定電話番号、市内局番
    shipping_phone_number2: str = field(default=None)
    # お届け先固定電話番号、加入者番号
    shipping_phone_number3: str = field(default=None)
    # お届け先郵便番号、郵便区番号
    shipping_postal_code1: str = field(default=None)
    # お届け先郵便番号、町域番号
    shipping_postal_code2: str = field(default=None)
    # お届け先住所、都道府県
    shipping_address1: str = field(default=None)
    # お届け先住所、市区町村名
    shipping_address2: str = field(default=None)
    # お届け先住所、丁目番地名
    shipping_address3: str = field(default=None)
    # お届け先会社名
    shipping_company_name: str = field(default=None)
    # お届け先肩書
    shipping_position: str = field(default=None)
    # お届け先お名前
    shipping_name: str = field(default=None)
    # お届け先敬称
    shipping_title: str = field(default=None)
    # お届け先購入商品1
    shipping_product_name1: str = field(default=None)
    # お届け先購入商品数1
    shipping_product_quantity1: int = field(default=0)
    # お届け先購入商品金額1
    shipping_product_price1: int = field(default=0)
    # お届け先購入商品2
    shipping_product_name2: str = field(default=None)
    # お届け先購入商品数2
    shipping_product_quantity2: int = field(default=0)
    # お届け先購入商品金額2
    shipping_product_price2: int = field(default=0)


    # 電話番号設定
    def set_phone_number(self, phone_number_name: str, mobile_number_name: str, phone_type: str, split_phone_number_dict: dict):

        # 分割した電話番号の格納を電話番号タイプにより分ける
        if phone_type == phone_number_name:
            # 固定電話の場合
            self.shipping_phone_number1 = split_phone_number_dict['customer_phone_number1']
            self.shipping_phone_number2 = split_phone_number_dict['customer_phone_number2']
            self.shipping_phone_number3 = split_phone_number_dict['customer_phone_number3']
        elif phone_type == mobile_number_name:
            # 携帯電話の場合
            self.shipping_phone_number1 = split_phone_number_dict['customer_mobile_number1']
            self.shipping_phone_number2 = split_phone_number_dict['customer_mobile_number2']
            self.shipping_phone_number3 = split_phone_number_dict['customer_mobile_number3']


    # 購入商品設定
    def set_product(self, order_item_list: list):

        # 購入数
        item_num = len(order_item_list)

        if item_num == 1:
            self.shipping_product_name1 = order_item_list[0]['product_name']
            self.shipping_product_quantity1 = order_item_list[0]['quantity']
            self.shipping_product_price1 = order_item_list[0]['price']
        elif item_num == 2:
            self.shipping_product_name1 = order_item_list[0]['product_name']
            self.shipping_product_quantity1 = order_item_list[0]['quantity']
            self.shipping_product_price1 = order_item_list[0]['price']
            self.shipping_product_name2 = order_item_list[1]['product_name']
            self.shipping_product_quantity2 = order_item_list[1]['quantity']
            self.shipping_product_price2 = order_item_list[1]['price']

