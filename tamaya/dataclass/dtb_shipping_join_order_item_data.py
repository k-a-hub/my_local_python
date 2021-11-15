from dataclasses import dataclass


@dataclass(init=True)
class dtb_order_shipping_join_order_item_data:

    # お届け先ID
    ship_id: int
    # 国ID
    country_id: int
    # 都道府県ID
    pref_id: int
    # お名前 姓
    name01: str
    # お名前 名
    name02: str
    # お名前 カナ
    kana01: str
    # お名前 メイ
    kana02: str
    # 会社名
    company_name: str
    # 郵便番号
    postal_code: str
    # 市区町村名
    addr01: str
    # 丁目番地名
    addr02: str
    # 電話番号
    phone_number: str
    # 更新日時
    update_date: str
    # 肩書
    position: str
    # 敬称
    title: str
    # 購入商品ID
    item_id: int
    # 承り票番号
    accept_no: int

