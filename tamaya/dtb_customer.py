from dataclasses import astuple

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


    # 更新処理の実行
    def exec_update(self):

        print("dtb_customerへの反映")
        # 更新件数
        upd_count = 0
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

