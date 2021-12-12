from dataclasses import dataclass


@dataclass(init=True)
class dtb_customer_data:

    # ID
    id: int
    # 電話番号
    phone_number: str
    # 郵便番号
    postal_code: str
    # 都道府県名
    pref_name: str
    # 市区町村名
    addr01: str
    # 丁目番地名
    addr02: str
    # 会社名
    company_name: str
    # 肩書
    position: str
    # お名前 姓
    name01: str
    # お名前 名
    name02: str
    # 扱い者コード
    agent_cd: int
    # 扱い者名
    mem_name: str
    # 外商口座番号
    sales_account_no: str

