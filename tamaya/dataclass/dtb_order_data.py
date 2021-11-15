from dataclasses import dataclass


@dataclass(init=True)
class dtb_order_data:

    # 受注ID
    order_id: int
    # 依頼主ID
    customer_id: int
    # 注文日
    order_date: str

