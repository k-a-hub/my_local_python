from dataclasses import dataclass, field


@dataclass(init=True)
class dtb_customer_data:

    # ID
    id: int = field(default=None)
    # 電話番号
    phone_number: str = field(default=None)
    # 郵便番号
    postal_code: str = field(default=None)
    # 都道府県名
    pref_name: str = field(default=None)
    # 市区町村名
    addr01: str = field(default=None)
    # 丁目番地名
    addr02: str = field(default=None)
    # 会社名
    company_name: str = field(default=None)
    # 肩書
    position: str = field(default=None)
    # お名前 姓
    name01: str = field(default=None)
    # お名前 名
    name02: str = field(default=None)
    # 扱い者コード
    agent_cd: int = field(default=None)
    # 扱い者名
    mem_name: str = field(default=None)
    # 外商口座番号
    sales_account_no: str = field(default=None)

