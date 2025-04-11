from django.urls import path
from . import views
urlpatterns = [
    path('office_home/', views.office_home, name='office_home'),
    path('add_employee/', views.add_employee, name='add_employee'),
    path('purchase_bill/', views.purchase_bill, name='purchase_bill'),
    path('purchase_completed_bills/', views.purchase_completed_bills, name='purchase_completed_bills'),
    path('item/', views.item, name='item'),
    path('completed_view_purchase_bill/<int:order_filter>', views.completed_view_purchase_bill, name='completed_view_purchase_bill'),
    path('genereate_purchase_bill_image/<int:order_filter>', views.genereate_purchase_bill_image, name='genereate_purchase_bill_image'),
    path('completed_view_sell_bill/<int:order_filter>', views.completed_view_sell_bill, name='completed_view_sell_bill'),
    path('sell_bill/', views.sell_bill, name='sell_bill'),
    path('sell_completed_bills/', views.sell_completed_bills, name='sell_completed_bills'),
    path('genereate_sell_bill_image/<int:order_filter>', views.genereate_sell_bill_image, name='genereate_sell_bill_image'),
    path('pay_purchase_bill/<int:farmer_id>', views.pay_purchase_bill, name='pay_purchase_bill'),
    path('pay_sell_bill/<int:customer_id>', views.pay_sell_bill, name='pay_sell_bill'),
    path('purchase_farmer/', views.purchase_farmer, name='purchase_farmer'),
    path('profile/', views.profile, name='profile'),
    path('item_detail/<id>', views.item_detail, name='item_detail'),

]