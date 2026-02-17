#
#
# def extract_irrep_order(order_as_it_is: str, reference_order: str) -> list[str]:
#     ordering = {i: reference_order.find(i) for i in order_as_it_is}
#     ordering = sorted(ordering.items(), key=lambda item: item[1])
#     positions = list(ordering.keys())