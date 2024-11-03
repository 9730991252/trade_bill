from django import template
from owner.models import *
from datetime import timedelta, date
from django.db.models import Avg, Sum, Min, Max
register = template.Library()

@register.inclusion_tag('inclusion_tag/office/item_weight.html')
def item_weight_detail(cart_id):
    i = Item_weight_detail.objects.filter(cart_id=cart_id)
    return {
        'i':i
        }


@register.simple_tag
def item_weight_detail_count(id):
    i = Item_weight_detail.objects.filter(cart_id=id).count()
    return i


@register.simple_tag
def item_weight_detail_sum(id):
    i = 0
    if id:
        i = Item_weight_detail.objects.filter(cart_id=id).aggregate(Sum('weight'))
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
    
@register.simple_tag
def total_item_amount(e_id):
    cart = Cart.objects.filter(office_employee_id=e_id)
    total=0

    for c in cart:
        i = Item_weight_detail.objects.filter(cart_id=c.id).aggregate(Sum('weight'))
        i = i['weight__sum']
        if i == None:
            i = 0
        else:
            a = c.prise * i
            total += a
         
    return int(total)
        
 
@register.simple_tag
def sell_weight(weight, stock_weight):
    if weight and stock_weight:
        sell_weight = weight - stock_weight
        return sell_weight
    
@register.simple_tag
def sell_qty(qty, stock_qty):
    if qty and stock_qty:
        sell_qty = qty - stock_qty
        return sell_qty
    
@register.simple_tag
def total_hamali(stock_id):
    order_detail = Order_detail.objects.filter(stock_item_id=stock_id)
    master = 0
    for o in order_detail:
        order_filter = o.order_filter
        m = order_master.objects.filter(order_filter=order_filter).first()
        if m:
            master += m.hamali
    return(master)

@register.simple_tag
def sell_amount(purchase_amount,stock_id):
    p = 0
    if purchase_amount != None:
        o = Order_detail.objects.filter(stock_item_id=stock_id)
        if o :
            for o in o:
                amount = (o.prise * o.weight)
                p += amount
        return p
    
from django.utils.safestring import mark_safe
@register.simple_tag
def profit_loss(purchase_amount, sell_amount):
    if purchase_amount != None:
        if int(sell_amount) > int(purchase_amount):
            t = ('<div class="text-success"><i class="fa-regular fa-face-smile"></i>&nbsp;&nbsp; <b>'+ str((int(sell_amount) - int(purchase_amount))) +'</b></div>')
        if int(sell_amount) < int(purchase_amount):
            t = ('<div class="text-danger"><i class="fa-regular fa-face-sad-tear"></i>&nbsp;&nbsp; <b>'+ str((int(sell_amount) - int(purchase_amount))) +'</b></div>')

        return mark_safe(t)
