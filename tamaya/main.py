import db_accessor as dba

# 受注注文日
order_date = "2021-12-31 00:00:00"


# ここから開始
if __name__ == '__main__':

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
    print(order_shipping_list)

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
    print(customer_address_list)

    # 「dtb_order と dtb_shippingの結合」リスト と dtb_customer_addressリスト の突き合わせ
    
        # 名前と郵便番号 が一致するか？
            # 一致の場合、updateリストに追加
            # 不一致の場合、insertリストに追加

    # dtb_customer_addressへの反映
    # updateリストの更新
    # insertリストの追加

    # 処理終了
    exit
