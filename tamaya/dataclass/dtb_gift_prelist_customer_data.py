from dataclasses import dataclass, field


@dataclass(init=True)
class dtb_gift_prelist_customer_data:

    # ページ番号
    page_no: int = field(default=None)
    # 承り票番号
    accept_no: int = field(default=None)
    # 店舗コード
    shop_code: str = field(default=None)
    # 依頼主ID
    customer_id: str = field(default=None)
    # 依頼主電話番号
    customer_phone_number: str = field(default=None)
    # 依頼主固定電話番号、市外局番
    customer_phone_number1: str = field(default=None)
    # 依頼主固定電話番号、市内局番
    customer_phone_number2: str = field(default=None)
    # 依頼主固定電話番号、加入者番号
    customer_phone_number3: str = field(default=None)
    # 依頼主郵便番号、郵便区番号
    customer_postal_code1: str = field(default=None)
    # 依頼主郵便番号、町域番号
    customer_postal_code2: str = field(default=None)
    # 依頼主住所、都道府県
    customer_address1: str = field(default=None)
    # 依頼主住所、市区町村名
    customer_address2: str = field(default=None)
    # 依頼主住所、丁目番地名
    customer_address3: str = field(default=None)
    # 依頼主会社名
    customer_company_name: str = field(default=None)
    # 依頼主肩書
    customer_position: str = field(default=None)
    # 依頼主お名前 姓、名
    customer_name: str = field(default=None)
    # 依頼主携帯電話番号、携帯番号
    customer_mobile_number1: str = field(default=None)
    # 依頼主携帯電話番号、事業者番号
    customer_mobile_number2: str = field(default=None)
    # 依頼主携帯電話番号、加入者番号
    customer_mobile_number3: str = field(default=None)
    # 依頼主扱い者コード
    agent_code: str = field(default=None)
    # 依頼主扱い者名前
    agent_name: str = field(default=None)
    # 依頼主外商口座番号
    sales_account_no: str = field(default=None)
    # 依頼主?
    customer_char_code: str = field(default=0)

