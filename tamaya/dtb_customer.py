import random
import string
from dataclasses import astuple
from datetime import datetime

from dataclass.dtb_customer_data import dtb_customer_data
from dataclass.dtb_customer_insert_data import dtb_customer_insert_data
from dataclass.dtb_customer_update_data import dtb_customer_update_data
from dataclass.dtb_order_data import dtb_order_data
from db_accessor import db_accessor


class dtb_customer:

    # コンストラクタ
    def __init__(self, dba: db_accessor):

        # DBアクセス
        self.dba: db_accessor = dba

        # 更新リスト
        self.update_list: list = []
        # 登録リスト
        self.insert_list: list = []

        # 非会員用の依頼主IDをキーに受注IDを配列化した変数
        self.non_customer_id_order_id_dict: dict = {}

        # 登録データの設定値
        # 登録日時
        self.insert_create_date: str = datetime.now().strftime('%Y-%m-%d %H:%M:00')
        # 更新日時
        self.insert_update_date: str = datetime.now().strftime('%Y-%m-%d %H:%M:00')
        # 識別用値
        self.insert_discriminator_type: str = "customer"
        # 分割件数
        self.insert_division_num: int = 5000



    # 更新リストの追加
    def add_update_list(self, customer_id_order_dict: dict):

        # 予測変換を出すため型指定
        order: dtb_order_data = None

        for customer_id, order in customer_id_order_dict.items():

            # 更新するデータ
            data = dtb_customer_update_data(
                order.sex_id
                ,order.job_id
                ,order.country_id
                ,order.pref_id
                ,order.name01
                ,order.name02
                ,order.kana01
                ,order.kana02
                ,order.company_name
                ,order.postal_code
                ,order.addr01
                ,order.addr02
                ,order.email
                ,order.phone_number
                ,order.birth
                ,order.update_date
                ,order.agent_cd
                ,order.sales_account_no
                ,order.position
                ,customer_id
            )
            # 更新する依頼主情報を追加
            self.update_list.append(data)

        print("------------------------------")
        print(f" dtb_customerの更新件数: {len(self.update_list)}件")
        print("------------------------------")


    # 登録リストの追加
    def add_insert_list(self, non_customer_dict: dict):

        # 予測変換を出すため型指定
        non_customer: dtb_order_data = None

        # 生成したシークレットキー用の配列
        created_secret_key_list: list = []

        # キーは不要なので、値のみを取得
        for non_customer in non_customer_dict.values():

            # 登録するデータ
            data = dtb_customer_insert_data(
                sex_id=non_customer.sex_id
                , job_id=non_customer.job_id
                , country_id=non_customer.country_id
                , pref_id=non_customer.pref_id
                , name01=non_customer.name01
                , name02=non_customer.name02
                , kana01=non_customer.kana01
                , kana02=non_customer.kana02
                , company_name=non_customer.company_name
                , postal_code=non_customer.postal_code
                , addr01=non_customer.addr01
                , addr02=non_customer.addr02
                , email=non_customer.email
                , phone_number=non_customer.phone_number
                , birth=non_customer.birth
                , create_date=self.insert_create_date
                , update_date=self.insert_update_date
                , discriminator_type=self.insert_discriminator_type
                , agent_cd=non_customer.agent_cd
                , sales_account_no=non_customer.sales_account_no
                , position=non_customer.position
                , password=f"{''.join(random.choices(string.ascii_letters+string.digits, k=8))}"
            )

            # シークレットキーの設定
            while True:
                # シークレットキーの生成
                create_secret_key = "".join(random.choices(((string.digits + string.ascii_letters) * 16), k=16))
                # シークレットキーをキーに会員ID取得SQL
                select_sql = f"""
                    SELECT
                        id
                    FROM
                        `{__class__.__name__}`
                    WHERE
                        secret_key = '{create_secret_key}'
                """
                # 取得
                exist_customer = self.dba.execute_query(select_sql)
                # 同じシークレットキーが登録されてないか確認
                if len(exist_customer) == 0 and create_secret_key not in created_secret_key_list:
                    # シークレットキーを設定
                    data.secret_key = create_secret_key
                    # 作成済みのシークレットキーリストに追加
                    created_secret_key_list.append(create_secret_key)
                    break

            # 追加する依頼主情報を追加
            self.insert_list.append(data)

        print("------------------------------")
        print("非会員ユーザの登録")
        print(f" dtb_customerの追加件数: {len(self.insert_list)}件")
        print("------------------------------")


    # 非会員ユーザのお届け先情報生成
    def make_non_customer_list(self, non_customer_order_id_dict: dict):

        for name_phone_join, order_id_list in non_customer_order_id_dict.items():

            split_array: list = name_phone_join.split(",")
            name01: str = split_array[0]
            name02: str = split_array[1]
            phone_number: str = split_array[2]

            # 登録した非会員のIDを取得
            non_customer_id_select_sql: str = f"""
                SELECT
                    id
                FROM
                    `{__class__.__name__}`
                WHERE
                    name01 = '{name01}'
                  AND
                    name02 = '{name02}'
                  AND
                    phone_number = '{phone_number}'
            """

            select_list: list = self.dba.execute_query(non_customer_id_select_sql)
            # データクラスに変換
            customer_data: dtb_customer_data = dtb_customer_data(**select_list[0])
            # 非会員の依頼主IDをキーに受注IUDの配列を追加
            self.non_customer_id_order_id_dict[customer_data.id] = order_id_list


    # 更新処理の実行
    def exec_update(self):

        print("dtb_customerへの反映")
        # 更新件数
        upd_count: int = 0
        # 更新データがある場合に実施
        if len(self.update_list) > 0:
            for update in self.update_list:
                # 更新SQL
                update_sql: str = f"""
                    UPDATE
                        `{__class__.__name__}`
                    SET
                        sex_id = %s
                        ,job_id = %s
                        ,country_id = %s
                        ,pref_id = %s
                        ,name01 = %s
                        ,name02 = %s
                        ,kana01 = %s
                        ,kana02 = %s
                        ,company_name = %s
                        ,postal_code = %s
                        ,addr01 = %s
                        ,addr02 = %s
                        ,email = %s
                        ,phone_number = %s
                        ,birth = %s
                        ,update_date = %s
                        ,agent_cd = %s
                        ,sales_account_no = %s
                        ,position = %s
                    WHERE
                        id = %s
                """
                # 更新実施
                upd_count += self.dba.execute_update(update_sql, [astuple(update)])

        print(f"\t更新実行件数: {upd_count}件")


    # 追加処理の実行
    def exec_insert(self):

        print("dtb_customerへの反映")
        # 登録件数
        ins_count: int = 0
        # 登録データがある場合に実施
        if len(self.insert_list) > 0:

            # 登録SQL
            insert_sql: str = f"""
                INSERT INTO `{__class__.__name__}` (
                    {",".join([f"`{k}`" for k in dtb_customer_insert_data.__annotations__.keys()])}
                ) VALUES (
                    {",".join(["%s" for i in range(0, len(dtb_customer_insert_data.__annotations__.keys()))])}
                )
            """

            # 5000件ごとに分割
            for idx in range(0, len(self.insert_list), self.insert_division_num):

                # 5000件の配列を取り出す
                values_list: list = self.insert_list[idx:idx + self.insert_division_num]
                # タプルに変換してリスト化
                tuples_list: list = [astuple(value) for value in values_list]
                # 登録実施
                ins_count += self.dba.execute_insert(insert_sql, tuples_list)

        print(f"\t追加実行件数: {ins_count}件")

