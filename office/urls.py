from django.urls import path
from . import views
urlpatterns = [
    path('office_home/', views.office_home, name='office_home'),
    path('add_employee/', views.add_employee, name='add_employee'),
    path('item_category/', views.item_category, name='item_category'),
    path('stock/', views.stock, name='stock'),
    path('new_bill/', views.new_bill, name='new_bill'),
    path('completed_view_bill/<int:order_filter>', views.completed_view_bill, name='completed_view_bill'),
    path('completed_bills/', views.completed_bills, name='completed_bills'),
    path('report/', views.report, name='report'),
    path('employee_sell_item/', views.employee_sell_item, name='employee_sell_item'),
    path('phonepe/', views.phonepe, name='phonepe'),
]