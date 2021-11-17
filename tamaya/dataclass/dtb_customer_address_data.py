from dataclasses import field, dataclass


@dataclass(init=True)
class dtb_customer_address_data:

    # ID
    id: int = field(default=None)
    # 依頼主ID
    customer_id: int = field(default=None)
    # 国ID
    country_id: int = field(default=None)
    # 都道府県ID
    pref_id: int = field(default=None)
    # お名前 姓
    name01: str = field(default=None)
    # お名前 名
    name02: str = field(default=None)
    # お名前 カナ
    kana01: str = field(default=None)
    # お名前 メイ
    kana02: str = field(default=None)
    # 会社名
    company_name: str = field(default=None)
    # 郵便番号
    postal_code: str = field(default=None)
    # 市区町村名
    addr01: str = field(default=None)
    # 丁目番地名
    addr02: str = field(default=None)
    # 電話番号
    phone_number: str = field(default=None)
    # 登録日時
    create_date: str = field(default=None)
    # 更新日時
    update_date: str = field(default=None)
    # 識別用値
    discriminator_type:str = field(default=None)
    # 肩書
    position: str = field(default=None)
    # 敬称
    title: str = field(default=None)
    # 承り票番号
    accept_no: int = field(default=None)
    # ページ番号
    page_no: int = field(default=None)
    # 今シーズンで削除
    delete_end_season: int = field(default=None)

