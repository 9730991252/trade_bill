from django.urls import path
from . import views
urlpatterns = [
    path('item_search_by_category', views.item_search_by_category, name='item_search_by_category'),
    path('customer_check', views.customer_check, name='customer_check'),
    path('add_to_item_weight', views.add_to_item_weight, name='add_to_item_weight'),
    path('calculete_prise', views.calculete_prise, name='calculete_prise'),
    path('cart_qty', views.cart_qty, name='cart_qty'),
    path('remove_cart_item', views.remove_cart_item, name='remove_cart_item'),
    path('remove_item_weight', views.remove_item_weight, name='remove_item_weight'),
    path('search_item_by_words', views.search_item_by_words, name='search_item_by_words'),
    path('set_purchase_amount', views.set_purchase_amount, name='set_purchase_amount'),
    path('save_cash_amount', views.save_cash_amount, name='save_cash_amount'),
    path('save_phonepe_amount', views.save_phonepe_amount, name='save_phonepe_amount'),
    path('set_vehicle_charges', views.set_vehicle_charges, name='set_vehicle_charges'),
    path('save_discount_amount', views.save_discount_amount, name='save_discount_amount'),
]