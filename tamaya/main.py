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
    # dtb_orderのみ
    latest_order_select_sql = f"""
        SELECT
            *
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
        GROUP BY
            order.customer_id
    """

    latest_order_list = db_accessor.execute_query(latest_order_select_sql)
    print(f"依頼主ごとの最新受注情報リスト: {len(latest_order_list)}件")

    # upsert用リスト保持オブジェクト
    obj_customer_address = c_address.dtb_customer_address()

    # 依頼主ごとの最新受注情報リストの繰り返し

        # 最新受注情報のIDをキーにお届け先情報の取得
        # お届け先情報リストの繰り返し
            # dtb_customer_addressから取得
                # 取得できれば更新
                # 取得できなければ追加

    # dtb_customer_addressへの反映
    # updateリストの更新
    # insertリストの追加

    # 処理終了
    exit
