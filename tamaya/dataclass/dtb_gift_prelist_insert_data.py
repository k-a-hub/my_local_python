from dataclasses import dataclass, field

from dataclass.dtb_gift_prelist_customer_data import \
    dtb_gift_prelist_customer_data
from dataclass.dtb_gift_prelist_shipping_data import \
    dtb_gift_prelist_shipping_data


@dataclass(init=False)
class dtb_gift_prelist_insert_data:

    # ページ番号
    page_no: int
    # 承り票番号
    accept_no: int
    # 店舗コード
    shop_code: str
    # 依頼主ID
    customer_id: str
    # 依頼主電話番号
    customer_phone_number: str
    # 依頼主固定電話番号、市外局番
    customer_phone_number1: str
    # 依頼主固定電話番号、市内局番
    customer_phone_number2: str
    # 依頼主固定電話番号、加入者番号
    customer_phone_number3: str
    # 依頼主郵便番号、郵便区番号
    customer_postal_code1: str
    # 依頼主郵便番号、町域番号
    customer_postal_code2: str
    # 依頼主住所、都道府県
    customer_address1: str
    # 依頼主住所、市区町村名
    customer_address2: str
    # 依頼主住所、丁目番地名
    customer_address3: str
    # 依頼主会社名
    customer_company_name: str
    # 依頼主肩書
    customer_position: str
    # 依頼主お名前 姓、名
    customer_name: str
    # 依頼主携帯電話番号、携帯番号
    customer_mobile_number1: str
    # 依頼主携帯電話番号、事業者番号
    customer_mobile_number2: str
    # 依頼主携帯電話番号、加入者番号
    customer_mobile_number3: str
    # 依頼主扱い者コード
    agent_code: str
    # 依頼主扱い者名前
    agent_name: str
    # 依頼主外商口座番号
    sales_account_no: str
    # 依頼主?
    customer_char_code: str

    # お届け先1
    # ページ番号
    shipping_pageno: int
    # お届け先電話番号
    shipping_phone_number: str
    # お届け先固定電話番号、市外局番
    shipping_phone_number1: str
    # お届け先固定電話番号、市内局番
    shipping_phone_number2: str
    # お届け先固定電話番号、加入者番号
    shipping_phone_number3: str
    # お届け先郵便番号、郵便区番号
    shipping_postal_code1: str
    # お届け先郵便番号、町域番号
    shipping_postal_code2: str
    # お届け先住所、都道府県
    shipping_address1: str
    # お届け先住所、市区町村名
    shipping_address2: str
    # お届け先住所、丁目番地名
    shipping_address3: str
    # お届け先会社名
    shipping_company_name: str
    # お届け先肩書
    shipping_position: str
    # お届け先お名前
    shipping_name: str
    # お届け先敬称
    shipping_title: str
    # お届け先購入商品1
    shipping_product_name1: str
    # お届け先購入商品数1
    shipping_product_quantity1: int
    # お届け先購入商品金額1
    shipping_product_price1: int
    # お届け先購入商品2
    shipping_product_name2: str
    # お届け先購入商品数2
    shipping_product_quantity2: int
    # お届け先購入商品金額2
    shipping_product_price2: int

    # お届け先2
    # ページ番号
    shipping2_pageno: int
    # お届け先電話番号
    shipping2_phone_number: str
    # お届け先固定電話番号、市外局番
    shipping2_phone_number1: str
    # お届け先固定電話番号、市内局番
    shipping2_phone_number2: str
    # お届け先固定電話番号、加入者番号
    shipping2_phone_number3: str
    # お届け先郵便番号、郵便区番号
    shipping2_postal_code1: str
    # お届け先郵便番号、町域番号
    shipping2_postal_code2: str
    # お届け先住所、都道府県
    shipping2_address1: str
    # お届け先住所、市区町村名
    shipping2_address2: str
    # お届け先住所、丁目番地名
    shipping2_address3: str
    # お届け先会社名
    shipping2_company_name: str
    # お届け先肩書
    shipping2_position: str
    # お届け先お名前
    shipping2_name: str
    # お届け先敬称
    shipping2_title: str
    # お届け先購入商品1
    shipping2_product_name1: str
    # お届け先購入商品数1
    shipping2_product_quantity1: int
    # お届け先購入商品金額1
    shipping2_product_price1: int
    # お届け先購入商品2
    shipping2_product_name2: str
    # お届け先購入商品数2
    shipping2_product_quantity2: int
    # お届け先購入商品金額2
    shipping2_product_price2: int

    # お届け先3
    # ページ番号
    shipping3_pageno: int
    # お届け先電話番号
    shipping3_phone_number: str
    # お届け先固定電話番号、市外局番
    shipping3_phone_number1: str
    # お届け先固定電話番号、市内局番
    shipping3_phone_number2: str
    # お届け先固定電話番号、加入者番号
    shipping3_phone_number3: str
    # お届け先郵便番号、郵便区番号
    shipping3_postal_code1: str
    # お届け先郵便番号、町域番号
    shipping3_postal_code2: str
    # お届け先住所、都道府県
    shipping3_address1: str
    # お届け先住所、市区町村名
    shipping3_address2: str
    # お届け先住所、丁目番地名
    shipping3_address3: str
    # お届け先会社名
    shipping3_company_name: str
    # お届け先肩書
    shipping3_position: str
    # お届け先お名前
    shipping3_name: str
    # お届け先敬称
    shipping3_title: str
    # お届け先購入商品1
    shipping3_product_name1: str
    # お届け先購入商品数1
    shipping3_product_quantity1: int
    # お届け先購入商品金額1
    shipping3_product_price1: int
    # お届け先購入商品2
    shipping3_product_name2: str
    # お届け先購入商品数2
    shipping3_product_quantity2: int
    # お届け先購入商品金額2
    shipping3_product_price2: int

    # お届け先4
    # ページ番号
    shipping4_pageno: int
    # お届け先電話番号
    shipping4_phone_number: str
    # お届け先固定電話番号、市外局番
    shipping4_phone_number1: str
    # お届け先固定電話番号、市内局番
    shipping4_phone_number2: str
    # お届け先固定電話番号、加入者番号
    shipping4_phone_number3: str
    # お届け先郵便番号、郵便区番号
    shipping4_postal_code1: str
    # お届け先郵便番号、町域番号
    shipping4_postal_code2: str
    # お届け先住所、都道府県
    shipping4_address1: str
    # お届け先住所、市区町村名
    shipping4_address2: str
    # お届け先住所、丁目番地名
    shipping4_address3: str
    # お届け先会社名
    shipping4_company_name: str
    # お届け先肩書
    shipping4_position: str
    # お届け先お名前
    shipping4_name: str
    # お届け先敬称
    shipping4_title: str
    # お届け先購入商品1
    shipping4_product_name1: str
    # お届け先購入商品数1
    shipping4_product_quantity1: int
    # お届け先購入商品金額1
    shipping4_product_price1: int
    # お届け先購入商品2
    shipping4_product_name2: str
    # お届け先購入商品数2
    shipping4_product_quantity2: int
    # お届け先購入商品金額2
    shipping4_product_price2: int

    # お届け先5
    # ページ番号
    shipping5_pageno: int
    # お届け先電話番号
    shipping5_phone_number: str
    # お届け先固定電話番号、市外局番
    shipping5_phone_number1: str
    # お届け先固定電話番号、市内局番
    shipping5_phone_number2: str
    # お届け先固定電話番号、加入者番号
    shipping5_phone_number3: str
    # お届け先郵便番号、郵便区番号
    shipping5_postal_code1: str
    # お届け先郵便番号、町域番号
    shipping5_postal_code2: str
    # お届け先住所、都道府県
    shipping5_address1: str
    # お届け先住所、市区町村名
    shipping5_address2: str
    # お届け先住所、丁目番地名
    shipping5_address3: str
    # お届け先会社名
    shipping5_company_name: str
    # お届け先肩書
    shipping5_position: str
    # お届け先お名前
    shipping5_name: str
    # お届け先敬称
    shipping5_title: str
    # お届け先購入商品1
    shipping5_product_name1: str
    # お届け先購入商品数1
    shipping5_product_quantity1: int
    # お届け先購入商品金額1
    shipping5_product_price1: int
    # お届け先購入商品2
    shipping5_product_name2: str
    # お届け先購入商品数2
    shipping5_product_quantity2: int
    # お届け先購入商品金額2
    shipping5_product_price2: int

    # 識別用値
    discriminator_type: str = field(default='giftprelist')


    # コンストラクタ
    def __init__(self, customer_data: dtb_gift_prelist_customer_data, shipping_list: list):

        # 依頼主情報を設定
        self.__dict__.update(customer_data.__dict__)
        # お届け先情報を設定
        for idx in range(0, len(shipping_list), 1):

            # お届け先1の設定
            if idx == 0:
                self.__dict__.update(shipping_list[idx].__dict__)
            else:
                # お届け先2~5の設定
                dlist = list(dtb_gift_prelist_shipping_data.__annotations__.keys())
                # shippingのキーをshipping番号に変換
                dlists = [dd.replace('shipping', f'shipping{idx+1}') for dd in dlist]

                # 今のお届け先を取得
                d: dict = shipping_list[idx].__dict__
                for jdx in range(0, len(dlist), 1):
                    # キー情報の更新
                    d[dlists[jdx]] = d.pop(dlist[jdx])
                self.__dict__.update(d)

