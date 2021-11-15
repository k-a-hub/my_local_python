from dataclasses import dataclass


@dataclass(init=True)
class dtb_customer_address_insert_data:

    # 依頼主ID
    customer_id: int
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
    # 登録日時
    create_date: str
    # 更新日時
    update_date: str
    # 識別用値
    discriminator_type: str
    # 肩書
    position: str
    # 敬称
    title: str
    # 承り票番号
    accept_no: int
    # ページ番号
    page_no: int

