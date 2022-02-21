from dataclasses import dataclass


@dataclass(init=True)
class dtb_shipping_data:

    # 都道府県名
    pref_name: str
    # お名前 性
    name01: str
    # お名前 名
    name02: str
    # 会社名
    company_name: str
    # 電話番号
    phone_number: str
    # 住所 郵便番号
    postal_code: str
    # 住所 都道府県名
    addr01: str
    # 住所 市区町村名
    addr02: str
    # 肩書
    position: str
    # 敬称
    title: str

