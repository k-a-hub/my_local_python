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
    
    # dtb_order と dtb_shipping を id と order_id　で結合
    # 絞り込み条件は進物受付 かつ シーズン内の期間のデータ
    # MEMO: 1受注のお届け先情報リスト
    order_shipping_select_sql = f"""
    select
	    dtb_order.customer_id as "会員ID"
	    ,dtb_order.id as "注文番号"
        ,dtb_order_item.accept_no as "承り票番号"
        ,dtb_shipping.phone_number
        ,dtb_shipping.postal_code
        ,dtb_shipping.addr01
        ,dtb_shipping.addr02
        ,dtb_shipping.company_name
        ,dtb_shipping.name01
        ,dtb_shipping.name02
    from
        dtb_shipping
        ,dtb_order
        ,dtb_order_item
    where
	    dtb_shipping.order_id = dtb_order.id
        and	dtb_shipping.order_id = dtb_order_item.order_id
        and	dtb_order.order_date > '{order_date}'
        and	dtb_order_item.product_code is not null
        and	dtb_order.payment_id IN(7, 8, 9)
    group by
        dtb_order.customer_id
        ,dtb_order.id
        ,dtb_order_item.accept_no
        ,dtb_shipping.phone_number
        ,dtb_shipping.postal_code
        ,dtb_shipping.addr01
        ,dtb_shipping.addr02
        ,dtb_shipping.company_name
        ,dtb_shipping.name01
        ,dtb_shipping.name02
    """

    order_shipping_list = db_accessor.execute_query(order_shipping_select_sql)
    print(f"1受注のお届け先情報リスト: {len(order_shipping_list)}件")

    # dtb_customer_addressの一覧を取得
    # 条件なし
    # MEMO: 依頼主のお届け先情報リスト
    customer_address_sql = f"""
    select
        *
    from
        dtb_customer_address
    """

    customer_address_list = db_accessor.execute_query(customer_address_sql)
    print(f"依頼主のお届け先情報リスト: {len(customer_address_list)}件")

    # upsert用リスト保持オブジェクト
    obj_customer_address = c_address.dtb_customer_address()

    # 「dtb_order と dtb_shippingの結合」リスト と dtb_customer_addressリスト の突き合わせ
    # 1受注のお届け先情報リストの繰り返し
    for order_shipping in order_shipping_list:

        # リスト追加フラグ - 追加時にTrue
        list_add_flg = False

        # 依頼主のお届け情報リストの繰り返し
        for customer_address in customer_address_list:

            # 名前と郵便番号 が一致するか？
            if order_shipping["name01"] == customer_address["name01"] \
                and order_shipping["name02"] == customer_address["name02"] \
                and order_shipping["postal_code"] == customer_address["postal_code"]:

                    # 一致の場合、updateリストに追加
                    obj_customer_address.add_update_list(order_shipping, customer_address)
                    # 追加したのでフラグを変更
                    list_add_flg = not list_add_flg
                    # 以降の依頼主のお届け情報リストの比較は必要ないので次の受注へ
                    break

        # 更新リストへの追加が無い場合
        if not list_add_flg:
            # 不一致の場合、insertリストに追加
            obj_customer_address.add_insert_list(order_shipping)
    
    print(f"\t更新件数: {len(obj_customer_address.update_list)}件")
    print(f"\t登録件数: {len(obj_customer_address.insert_list)}件")

    # dtb_customer_addressへの反映
    # updateリストの更新
    # insertリストの追加

    # 処理終了
    exit
