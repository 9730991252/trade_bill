from django.urls import path
from . import views
urlpatterns = [
    path('search_item', views.search_item, name='search_item'),
    path('delete_purchase_cart_item', views.delete_purchase_cart_item, name='delete_purchase_cart_item'),
    path('delete_sell_cart_item', views.delete_sell_cart_item, name='delete_sell_cart_item'),
    path('add_to_item_weight_purchase', views.add_to_item_weight_purchase, name='add_to_item_weight_purchase'),
    path('remove_item_weight_purchase', views.remove_item_weight_purchase, name='remove_item_weight_purchase'),
    path('calculete_prise_purchase', views.calculete_prise_purchase, name='calculete_prise_purchase'),
    path('farmer_check', views.farmer_check, name='farmer_check'),
    path('save_farmer', views.save_farmer, name='save_farmer'),
    path('sell_search_item', views.sell_search_item, name='sell_search_item'),
    path('add_to_item_weight_sell', views.add_to_item_weight_sell, name='add_to_item_weight_sell'),
    path('calculete_prise_sell', views.calculete_prise_sell, name='calculete_prise_sell'),
    path('remove_item_weight_sell', views.remove_item_weight_sell, name='remove_item_weight_sell'),
    path('customer_check', views.customer_check, name='customer_check'),
    path('save_sell_customer', views.save_sell_customer, name='save_sell_customer'),
    path('change_purchase_cart_qty', views.change_purchase_cart_qty, name='change_purchase_cart_qty'),
    path('change_sell_cart_qty', views.change_sell_cart_qty, name='change_sell_cart_qty'),
]