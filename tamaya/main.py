from datetime import datetime
from math import floor
from sys import argv, exit
from time import perf_counter

from db_accessor import db_accessor
from dtb_customer import dtb_customer
from dtb_customer_address import dtb_customer_address
from dtb_order import dtb_order


# 引数確認
def validation_args(argv: list):

    # エラーメッセージ
    error_message: str = ""

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
        exit()
    else:
        # 戻り値
        return_value: datetime = None
        try:
            # 日付型に変換
            if len(argv[1]) == 10:
                return_value = datetime.strptime(argv[1], '%Y-%m-%d')
            else:
                return_value = datetime.strptime(argv[1], '%Y-%m-%d %H:%M:%S')
        except Exception as e:
            # 日付変換エラー
            print(f"日付変換エラー\n{e}")
            # 以降の処理を実施せずに終了
            exit()

    return return_value.strftime('%Y-%m-%d %H:%M:%S')


# ここから開始
if __name__ == '__main__':

    # 処理開始時間
    start_time: float = perf_counter()

    # 引数の正常性確認
    order_date: str = validation_args(argv)

    # DB接続クラス作成
    # TODO: 最終確認時以外は引数にFalseを設定
    dba: db_accessor = db_accessor(commit_flg=False)

    # dtb_order用リスト保持オブジェクト
    obj_order = dtb_order(dba)
    obj_order.get_order_list(order_date)

    # dtb_customer_address用リスト保持オブジェクト
    obj_customer_address = dtb_customer_address(dba)
    # 依頼主IDと受注IDをキーに更新、登録リストへの追加を行う
    obj_customer_address.add_upsert_list(obj_order.customer_id_order_id_dict)

    # dtb_customer_addressへの反映
    print("dtb_customer_addressへの反映")
    # 更新処理
    print(f"\t更新実行件数: {obj_customer_address.exec_update()}件")
    # 追加処理
    print(f"\t追加実行件数: {obj_customer_address.exec_insert()}件")

    # dtb_customerへの反映
    obj_customer = dtb_customer(dba)
    # 依頼主IDと受注IDをキーに更新リストへの追加を行う
    obj_customer.add_update_list(obj_order.customer_id_order_dict)
    print(f"\t更新実行件数: {obj_customer.exec_update()}件")

    print(f"処理にかかった時間: {floor(perf_counter() - start_time)}秒")
    # 処理終了
    exit()

    # 今シーズンで削除のお届け先情報の削除
    obj_customer_address.get_delete_end_season(db_accessor)
    print(f"削除実行件数: {obj_customer_address.exec_delete(db_accessor)}件")

