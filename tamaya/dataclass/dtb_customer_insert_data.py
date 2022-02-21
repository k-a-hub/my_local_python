from dataclasses import dataclass, field


@dataclass(init=True)
class dtb_customer_insert_data:

    # 性別ID
    sex_id: int
    # 職業ID
    job_id: int
    # 国ID
    country_id: int
    # 都道府県ID
    pref_id: int
    # お名前 姓
    name01: str
    # お名前 名
    name02: str
    # お名前 セイ
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
    # メールアドレス
    email: str
    # 電話番号
    phone_number: str
    # 生年月日
    birth: str
    # 登録日時
    create_date: str
    # 更新日時
    update_date: str
    # 識別値
    discriminator_type: str
    # 担当者コード
    agent_cd: int
    # 外商口座番号
    sales_account_no: str
    # 肩書
    position: str
    # パスワード
    password: str
    # シークレットキー
    secret_key: str = field(default=None)
    # 会員ステータスID
    customer_status_id: int = field(default=1)

