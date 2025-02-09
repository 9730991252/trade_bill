from django import template
from owner.models import *
from datetime import timedelta, date
from django.db.models import Avg, Sum, Min, Max
register = template.Library()
import math


@register.inclusion_tag('inclusion_tag/office/purchase_item_weight_detail.html')
def purchase_item_weight_detail(cart_id):
    i = Purchase_item_weight_detail.objects.filter(cart_id=cart_id)
    return {
        'i':i
        }
    
@register.inclusion_tag('inclusion_tag/office/sell_item_weight_detail.html')
def sell_item_weight_detail(cart_id):
    i = Sell_item_weight_detail.objects.filter(cart_id=cart_id)
    return {
        'i':i
        }
    
@register.simple_tag
def stock_item_weight(item_id):
    i = Purchase_order_detail.objects.filter(stock_status=1 , item_id=item_id).aggregate(Sum('weight'))['weight__sum']
    i = i
    if i:
        return i
    else:
        return 0
    
@register.simple_tag
def order_master_farmer(farmer_id):
    if farmer_id:
        return Purchase_order_master.objects.filter(farmer_id=farmer_id)
    

    
@register.simple_tag
def check_order_detail_farmer(order_detail_id):
    i = Purchase_order_detail.objects.filter(id=order_detail_id).first()
    m = Purchase_order_master.objects.filter(shope_id = i.shope_id, order_filter=i.order_filter).first()
    if m:
        farmer = m.farmer
        if farmer:
            return farmer.name
        else:
            return 'Unknown'
    
@register.simple_tag
def order_detail(order_filter, shope_id):
    if order_filter:
        return Purchase_order_detail.objects.filter(order_filter=order_filter, stock_status=1, shope_id=shope_id)
    
@register.simple_tag
def total_item_amount_purchase(employee_id):
    if employee_id:
        cart = Purchase_cart.objects.filter(office_employee_id=employee_id)
        total=0
        for c in cart:
            i = Purchase_item_weight_detail.objects.filter(cart_id=c.id).aggregate(Sum('weight'))
            i = i['weight__sum']
            if i == None:
                i = 0
            else:
                a = c.prise * i
                total += a
            
        return int(total)
    
@register.simple_tag
def total_item_amount_sell(employee_id):
    if employee_id:
        cart = Sell_cart.objects.filter(office_employee_id=employee_id)
        total=0
        for c in cart:
            i = Sell_item_weight_detail.objects.filter(cart_id=c.id).aggregate(Sum('weight'))
            i = i['weight__sum']
            if i == None:
                i = 0
            else:
                a = c.prise * i
                total += a
            
        return int(total)

@register.simple_tag
def calculate_remaining_order_detail_weight(order_detail_id):
    i = Purchase_order_detail.objects.filter(id=order_detail_id, stock_status=1).first().weight
    weight = 0
    if i:
        weight = i
        
    return weight

@register.simple_tag
def all_sell_customer_total_pending_amount(shope_id):
    pending_amount = Sell_order_master.objects.filter(shope_id=shope_id).aggregate(Sum('total'))['total__sum']
    if pending_amount == None:
        pending_amount = 0
    paid_total_amount = Customer_sell_payment_transaction.objects.filter(shope_id=shope_id).aggregate(Sum('amount'))['amount__sum']
    if paid_total_amount == None:
        paid_total_amount = 0
    return (pending_amount - paid_total_amount)

@register.simple_tag
def all_purchase_farmer_total_pending_amount(shope_id):
    pending_amount = Purchase_order_master.objects.filter(shope_id=shope_id).aggregate(Sum('total'))['total__sum']
    if pending_amount == None:
        pending_amount = 0
    paid_total_amount = Farmer_purchase_payment_transaction.objects.filter(shope_id=shope_id).aggregate(Sum('amount'))['amount__sum']
    if paid_total_amount == None:
        paid_total_amount = 0
    return (pending_amount - paid_total_amount)


@register.simple_tag
def change_purchase_farmer_bill_paid_status(farmer_id):
    opning = Farmer_purchase_opning_balance.objects.filter(farmer_id=farmer_id).first()
    recived_payment = Farmer_purchase_payment_transaction.objects.filter(farmer_id=farmer_id).aggregate(Sum('amount'))['amount__sum']
    final_amount = recived_payment
    if opning.type == 1:
        final_amount += opning.balance
    else:
        final_amount -= opning.balance
    if final_amount == None:
        final_amount = 0      
    bill_amount = Purchase_order_master.objects.filter(farmer_id=farmer_id, paid_status = 1).aggregate(Sum('total'))['total__sum']
    if bill_amount == None:
        bill_amount = 0      
    if int(math.floor(float(bill_amount))) >= int(math.floor(float(final_amount))):
        bill = Purchase_order_master.objects.filter(farmer_id=farmer_id, paid_status = 1).first()
        if bill:
            bill.paid_status = 0
            bill.save()
            print('yes')
    else:
        bill = Purchase_order_master.objects.filter(farmer_id=farmer_id, paid_status = 0).first()
        if bill:
            bill.paid_status = 1
            bill.save()
            print('no')
    
@register.simple_tag
def item_weight_detail_sum_purchase(id):
    i = 0
    if id:
        i = Purchase_item_weight_detail.objects.filter(cart_id=id).aggregate(Sum('weight'))
        if i:
            i = i['weight__sum']
    if i:
        return i
    else:
        return 0

@register.simple_tag
def item_weight_detail_sum_sell(id):
    i = 0
    if id:
        i = Sell_item_weight_detail.objects.filter(cart_id=id).aggregate(Sum('weight'))
        if i:
            i = i['weight__sum']
    if i:
        return i
    else:
        return 0
    





@register.simple_tag
def calculete_item_prise(weight, prise):
    if weight:
        return prise * weight
    else:
        return 0
    

        
 
