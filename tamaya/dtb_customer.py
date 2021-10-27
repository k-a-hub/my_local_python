from dataclasses import astuple, dataclass

class dtb_customer:

    # コンストラクタ
    def __init__(self):

        # 更新リスト
        self.update_list = []

    # 更新リストの追加
    def add_update_list(self, latest_order_list):
        
        for order in latest_order_list:
            data = dtb_customer_data(
                order['customer_id']
                ,order['sex_id']
                ,order['job_id']
                ,order['country_id']
                ,order['pref_id']
                ,order['name01']
                ,order['name02']
                ,order['kana01']
                ,order['kana02']
                ,order['company_name']
                ,order['postal_code']
                ,order['addr01']
                ,order['addr02']
                ,order['email']
                ,order['phone_number']
                ,order['birth']
                ,order['update_date']
                ,order['agent_cd']
                ,order['sales_account_no']
                ,order['position']
            )

            self.update_list.append(astuple(data))

    # 更新処理の実行
    def exec_update(self, instance_db_accessor):
        upd_count = 0
        if len(self.update_list) > 0:
            for update in self.update_list:
                update_sql = " \
                    UPDATE \
                        `dtb_customer` \
                    SET \
                        sex_id = {0[1]} \
                        ,job_id = {0[2]} \
                        ,country_id = {0[3]}\
                        ,pref_id = {0[4]}\
                        ,name01 = {0[5]}\
                        ,name02 = {0[6]}\
                        ,kana01 = {0[7]}\
                        ,kana02 = {0[8]}\
                        ,company_name = {0[9]}\
                        ,postal_code = {0[10]}\
                        ,addr01 = {0[11]}\
                        ,addr02 = {0[12]}\
                        ,email = {0[13]}\
                        ,phone_number = {0[14]}\
                        ,birth = {0[15]}\
                        ,update_date = {0[16]}\
                        ,agent_cd = {0[17]}\
                        ,sales_account_no = {0[18]}\
                        ,position = {0[19]}\
                    WHERE \
                        id = {0[0]} \
                "
                # 更新SQLの実施
                upd_count += instance_db_accessor.excecute_update(update_sql.format(update))
        return upd_count
        

# コンストラクタは省略
@dataclass(init=True)
class dtb_customer_data:
    
    # 依頼主ID
    id: int
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
    # 更新日時
    update_date: str
    # 担当者コードID
    agent_cd: int
    # 外商口座番号
    sales_account_no: str
    # 肩書
    position: str


    # コンストラクタ後に実行
    def __post_init__(self):
        
        # NoneならNullに置き換える
        self.id = 'Null' if self.id is None else self.id
        self.sex_id = 'Null' if self.sex_id is None else self.sex_id
        self.job_id = 'Null' if self.job_id is None else self.job_id
        self.country_id = 'Null' if self.country_id is None else self.country_id
        self.pref_id = 'Null' if self.pref_id is None else self.pref_id
        self.name01 = 'Null' if self.name01 is None else self.name01
        self.name02 = 'Null' if self.name02 is None else self.name02
        self.kana01 = 'Null' if self.kana01 is None else self.kana01
        self.kana02 = 'Null' if self.kana02 is None else self.kana02
        self.company_name = 'Null' if self.company_name is None else self.company_name
        self.postal_code = 'Null' if self.postal_code is None else self.postal_code
        self.addr01 = 'Null' if self.addr01 is None else self.addr01
        self.addr02 = 'Null' if self.addr02 is None else self.addr02
        self.email = 'Null' if self.email is None else self.email
        self.phone_number = 'Null' if self.phone_number is None else self.phone_number
        self.birth = 'Null' if self.birth is None else self.birth
        self.update_date = 'Null' if self.update_date is None else self.update_date
        self.agent_cd = 'Null' if self.agent_cd is None else self.agent_cd
        self.sales_account_no = 'Null' if self.sales_account_no is None else self.sales_account_no
        self.position = 'Null' if self.position is None else self.position

        # 文字列にする
        self.name01 = f"'{self.name01}'" if self.name01 != 'Null' else self.name01
        self.name02 = f"'{self.name02}'" if self.name02 != 'Null' else self.name02
        self.kana01 = f"'{self.kana01}'" if self.kana01 != 'Null' else self.kana01
        self.kana02 = f"'{self.kana02}'" if self.kana02 != 'Null' else self.kana02
        self.company_name = f"'{self.company_name}'" if self.company_name != 'Null' else self.company_name
        self.postal_code = f"'{self.postal_code}'" if self.postal_code != 'Null' else self.postal_code
        self.addr01 = f"'{self.addr01}'" if self.addr01 != 'Null' else self.addr01
        self.addr02 = f"'{self.addr02}'" if self.addr02 != 'Null' else self.addr02
        self.email = f"'{self.email}'" if self.email != 'Null' else self.email
        self.phone_number = f"'{self.phone_number}'" if self.phone_number != 'Null' else self.phone_number
        self.birth = f"'{self.birth}'" if self.birth != 'Null' else self.birth
        self.update_date = f"'{self.update_date}'" if self.update_date != 'Null' else self.update_date
        self.sales_account_no = f"'{self.sales_account_no}'" if self.sales_account_no != 'Null' else self.sales_account_no
        self.position = f"'{self.position}'" if self.position != 'Null' else self.position
    
