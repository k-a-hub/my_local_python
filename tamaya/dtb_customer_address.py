import datetime
import sys


class dtb_customer_address:

    # コンストラクタ
    def __init__(self):

        # 更新リスト
        self.update_list = []
        # 登録リスト
        self.insert_list = []
    
    # 更新リスト追加
    def add_update_list(self, shipping_join_item, customer_address):

        # 更新するデータ
        update = []
        # dtb_customer_addressのid
        update.append(f"{customer_address['id']}")
        # 国ID
        update.append(f"{shipping_join_item['country_id']}")
        # 都道府県ID
        update.append(f"{shipping_join_item['pref_id']}")
        # お名前 姓
        update.append(f"'{shipping_join_item['name01']}'")
        # お名前 名
        update.append(f"'{shipping_join_item['name02']}'")
        # お名前 セイ
        update.append(f"'{shipping_join_item['kana01']}'")
        # お名前 メイ
        update.append(f"'{shipping_join_item['kana02']}'")
        # 会社名
        update.append(f"'{shipping_join_item['company_name']}'")
        # 郵便番号
        update.append(f"'{shipping_join_item['postal_code']}'")
        # 市区町村名
        update.append(f"'{shipping_join_item['addr01']}'")
        # 丁目番地名
        update.append(f"'{shipping_join_item['addr02']}'")
        # 電話番号
        update.append(f"'{shipping_join_item['phone_number']}'")
        # 更新日時
        update.append(f"'{shipping_join_item['update_date']}'")
        # 肩書
        update.append(f"'{shipping_join_item['position']}'")
        # 敬称
        update.append(f"'{shipping_join_item['title']}'")
        # 承り票番号
        update.append(f"'{shipping_join_item['accept_no']}'")

        # 更新する受注のお届け先情報を追加
        self.update_list.append(tuple(update))

    # 登録リスト追加
    def add_insert_list(self, order, shipping_join_item):

        # 登録するデータ
        insert = []
        # 依頼主ID
        insert.append(f"{order['customer_id']}")
        # 国ID
        insert.append(f"{shipping_join_item['country_id']}")
        # 都道府県ID
        insert.append(f"{shipping_join_item['pref_id']}")
        # お名前 姓
        insert.append(f"'{shipping_join_item['name01']}'")
        # お名前 名
        insert.append(f"'{shipping_join_item['name02']}'")
        # お名前 セイ
        insert.append(f"'{shipping_join_item['kana01']}'")
        # お名前 メイ
        insert.append(f"'{shipping_join_item['kana02']}'")
        # 会社名
        insert.append(f"'{shipping_join_item['company_name']}'")
        # 郵便番号
        insert.append(f"'{shipping_join_item['postal_code']}'")
        # 市区町村名
        insert.append(f"'{shipping_join_item['addr01']}'")
        # 丁目番地名
        insert.append(f"'{shipping_join_item['addr02']}'")
        # 電話番号
        insert.append(f"'{shipping_join_item['phone_number']}'")
        # 登録日時
        insert.append(f"'{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:00')}'")
        # 更新日時
        insert.append(f"'{shipping_join_item['update_date']}'")
        # discriminator_type
        insert.append(f"'customeraddress'")
        # 肩書
        insert.append(f"'{shipping_join_item['position']}'")
        # 敬称
        insert.append(f"'{shipping_join_item['title']}'")
        # 承り票番号
        insert.append(f"'{shipping_join_item['accept_no']}'")
        # ページ番号
        insert.append(f"""(
            SELECT IFNULL(MAX(max_page_no)+1, 1)
            FROM (SELECT MAX(page_no) AS `max_page_no` FROM dtb_customer_address WHERE customer_id = {order['customer_id']}) AS `temp1`
        )""")
        

        # 登録する受注のお届け先情報を追加
        self.insert_list.append(tuple(insert))

    # 更新処理
    def exec_update(self, instance_db_accessor):
        upd_count = 0
        if len(self.update_list) > 0:
            for update in self.update_list:
                update_sql = "\
                    UPDATE \
                        `dtb_customer_address` \
                    SET \
                        country_id = {0[1]} \
                        ,pref_id = {0[2]} \
                        ,name01 = {0[3]} \
                        ,name02 = {0[4]} \
                        ,kana01 = {0[5]} \
                        ,kana02 = {0[6]} \
                        ,company_name = {0[7]}\
                        ,postal_code = {0[8]} \
                        ,addr01 = {0[9]} \
                        ,addr02 = {0[10]} \
                        ,phone_number = {0[11]} \
                        ,update_date = {0[12]} \
                        ,position = {0[13]} \
                        ,title = {0[14]} \
                        ,accept_no = {0[15]} \
                    WHERE \
                        id = {0[0]} \
                    "
                upd_count += instance_db_accessor.excecute_update(update_sql.format([u if u != 'None' and u != "'None'" else 'Null' for u in update]))
        return upd_count

    # 追加処理
    def exec_insert(self, instance_db_accessor):   
        ins_count = 0
        if len(self.insert_list) > 0:
            insert_sql = "\
                INSERT INTO `dtb_customer_address` ( \
                    `customer_id` \
                    ,`country_id` \
                    ,`pref_id` \
                    ,`name01` \
                    ,`name02` \
                    ,`kana01` \
                    ,`kana02` \
                    ,`company_name` \
                    ,`postal_code` \
                    ,`addr01` \
                    ,`addr02` \
                    ,`phone_number` \
                    ,`create_date` \
                    ,`update_date` \
                    ,`discriminator_type` \
                    ,`position` \
                    ,`title` \
                    ,`accept_no` \
                    ,`page_no` \
                ) VALUES (\
                   {} \
                ); \
                "

            # 5000件ごとに分割
            for idx in range(0, len(self.insert_list), 5000):
                
                # 5000件の配列を取り出す
                values_list = self.insert_list[idx:idx + 5000]
                values_str = ""
                for i, value in enumerate(values_list):
                    values_str += "),(" if i != 0 else ""
                    for j, v in enumerate(value):
                        values_str += "," if j != 0 else ""
                        values_str += v if v != 'None' and v != "'None'" else 'Null'
                ins_count += instance_db_accessor.execute_insert(insert_sql.format(values_str))
        return ins_count
