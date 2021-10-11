
# ここから開始
if __name__ == '__main__':
    
    # dtb_order と dtb_shipping を id と order_id　で結合
    # 絞り込み条件は進物受付 かつ シーズン内の期間のデータ
    # MEMO: 1受注のお届け先情報リスト

    # dtb_customer_addressの一覧を取得
    # 条件なし
    # MEMO: 依頼主のお届け先情報リスト

    # 「dtb_order と dtb_shippingの結合」リスト と dtb_customer_addressリスト の突き合わせ
    
        # 名前と郵便番号 が一致するか？
            # 一致の場合、updateリストに追加
            # 不一致の場合、insertリストに追加

    # dtb_customer_addressへの反映
    # updateリストの更新
    # insertリストの追加

    # 処理終了
    exit
