from owner.models import *
def check_cart_item(stock_item_id, office_employee_id, shope_id):
    if Cart.objects.filter(stock_item_id=stock_item_id, office_employee_id=office_employee_id, shope_id=shope_id).exists():
        pass
    else:
        Cart(
            stock_item_id=stock_item_id,
            office_employee_id=office_employee_id,
            shope_id=shope_id
        ).save()
