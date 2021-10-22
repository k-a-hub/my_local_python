import sys
import datetime as dt
import db_accessor as dba
import dtb_customer_address as c_address

# 引数確認
def validation_args(argv):
    
    # エラーメッセージ
    error_message = ""

    # 引数が無い場合
    if len(argv) == 1:
        error_message = f"""
    「受注日」か「受注日時」を引数として設定してください。
    受注日のみの場合、時刻は0時0分0秒が設定されます。
    設定例):
            python3 {argv[0]} "2021-04-01 10:00:00"
    もしくは
            python3 {argv[0]} 2021-04-01
        """
    elif len(argv) != 2:
        # 引数が多い場合
        error_message = "引数が多すぎます。"
    
    if error_message != "":
        # エラーメッセージの表示
        print(error_message)
        # 以降の処理を実施せずに終了
        sys.exit()
    else:
        # 戻り値
        return_value = ""
        try:
            # 日付型に変換
            if len(argv[1]) == 10:
                return_value = dt.datetime.strptime(argv[1], '%Y-%m-%d')
            else:                
                return_value = dt.datetime.strptime(argv[1], '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            # 日付変換エラー
            print(f"日付変換エラー\n{e}")
            # 以降の処理を実施せずに終了
            sys.exit()

    return return_value.strftime('%Y-%m-%d %H:%M:%S')


# ここから開始
if __name__ == '__main__':

    # 引数の正常性確認
    order_date = validation_args(sys.argv)

    # DB接続クラス作成
    db_accessor = dba.db_accessor()
    
    # 期間内で依頼主ごとの最新の受注情報のSELECT文
    # dtb_customer_address登録時にdtb_customerに登録されていないcustomer_idも存在するのでJOINして未登録分を弾く
    # dtb_orderのみ
    latest_order_select_sql = f"""
        SELECT
            order.id AS order_id
            ,order.customer_id AS customer_id
            ,order.order_date
        FROM
            (
                SELECT
                    id
                    ,customer_id
                    ,order_date
                FROM
                    dtb_order
                WHERE
                    payment_id IN (7,8,9)
                AND
                    order_date >= '{order_date}'
                AND
                    customer_id IS NOT NULL
                GROUP BY
                    id
                ORDER BY
                    customer_id ASC
                    ,order_date DESC
            ) AS `order`
        JOIN
            `dtb_customer` AS customer ON order.customer_id = customer.id
        GROUP BY
            order.customer_id
    """

    latest_order_list = db_accessor.execute_query(latest_order_select_sql)
    print(f"依頼主ごとの最新受注情報リスト: {len(latest_order_list)}件")

    # upsert用リスト保持オブジェクト
    obj_customer_address = c_address.dtb_customer_address()

    # 依頼主ごとの最新受注情報リストの繰り返し
    for latest_order in latest_order_list:

        # 最新受注情報のIDをキーにお届け先情報のSELECT文
        # dtb_shippingとdtb_order_itemの結合
        order_shipping_join_item_select_sql = f"""
            SELECT
                ship.id AS ship_id
                ,country_id
                ,pref_id
                ,name01
                ,name02
                ,kana01
                ,kana02
                ,company_name
                ,postal_code
                ,addr01
                ,addr02
                ,phone_number
                ,update_date
                ,position
                ,title
                ,item.id AS item_id
                ,accept_no
            FROM
                dtb_shipping AS `ship`
            JOIN
                dtb_order_item AS `item` ON ship.id = item.shipping_id
            WHERE
                item.product_code IS NOT NULL
            AND
                ship.order_id = {latest_order["order_id"]}
        """

        order_shipping_join_item_list = db_accessor.execute_query(order_shipping_join_item_select_sql)
        # print(f"受注ID {latest_order['id']} のお届け先数: {len(order_shipping_join_item_list)}件")

        # お届け先情報リストの繰り返し
        for order_shipping_join_item in order_shipping_join_item_list:

            # 受注の依頼主IDとお届け先の名前をキーに依頼主のお届け先情報のSELECT文
            # dtb_customer_addressのみ
            customer_address_select_sql = f"""
                SELECT
                    *
                FROM
                    dtb_customer_address
                WHERE
                    customer_id = {latest_order["customer_id"]}
                AND
                    name01 = '{order_shipping_join_item["name01"]}'
                AND
                    name02 = '{order_shipping_join_item["name02"]}'
            """

            customer_address_data = db_accessor.execute_query(customer_address_select_sql)
            # print(f"依頼主のお届け先有無: {'追加' if len(customer_address_data) == 0 else '更新'}")

            if len(customer_address_data) > 0:
                # 取得できれば更新
                obj_customer_address.add_update_list(order_shipping_join_item, customer_address_data[0])
            else:
                # 取得できなければ追加
                obj_customer_address.add_insert_list(latest_order, order_shipping_join_item)

    # dtb_customer_addressへの反映
    print(f"dtb_customer_addresの更新件数: {len(obj_customer_address.update_list)}件")
    print(f"dtb_customer_addresの追加件数: {len(obj_customer_address.insert_list)}件")
    # 更新処理
    print(f"更新実行件数: {obj_customer_address.exec_update(db_accessor)}件")
    # 追加処理
    print(f"追加実行件数: {obj_customer_address.exec_insert(db_accessor)}件")

    # 処理終了
    exit
