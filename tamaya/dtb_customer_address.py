
class dtb_customer_address:

    # コンストラクタ
    def __init__(self):

        # 更新リスト
        self.update_list = []
        # 登録リスト
        self.insert_list = []
    
    # 更新リスト追加
    def add_update_list(self, order, shipping_join_item, customer_address):
        # 更新する受注のお届け先情報を追加
        self.update_list.append([order, shipping_join_item, customer_address])

    # 登録リスト追加
    def add_insert_list(self, order, shipping_join_item):
        # 登録する受注のお届け先情報を追加
        self.insert_list.append([order, shipping_join_item])
