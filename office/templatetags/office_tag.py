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
    if e_id:
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
    t = ('')
    if purchase_amount != None:
        if int(sell_amount) > int(purchase_amount):
            t = ('<div class="text-success"><i class="fa-regular fa-face-smile"></i>&nbsp;&nbsp; <b>'+ str((int(sell_amount) - int(purchase_amount))) +'</b></div>')
        if int(sell_amount) < int(purchase_amount):
            t = ('<div class="text-danger"><i class="fa-regular fa-face-sad-tear"></i>&nbsp;&nbsp; <b>'+ str((int(sell_amount) - int(purchase_amount))) +'</b></div>')

    return mark_safe(t)
        

@register.inclusion_tag('inclusion_tag/office/item_stock_summary.html')
def item_stock_summary(shope_id,item_stock_id):
    order_detail = []
    if item_stock_id:
        employee = office_employee.objects.filter(shope_id=shope_id)
        if employee:
            for e in employee:
                o = Order_detail.objects.filter(office_employee_id=e.id,stock_item_id=item_stock_id).first()
                if o:
                    order_detail.append(o)
        return{
            'order_detail':order_detail
        }

from django.utils.safestring import mark_safe
@register.simple_tag
def employee_weight(stock_id, e_id):
    weight = 0
    qty = 0
    if stock_id:
        if e_id:
            order_datail = Order_detail.objects.filter(stock_item_id=stock_id, office_employee_id=e_id)
            for o in order_datail:
                weight += o.weight
                qty += o.qty
    t = ('Weight '+ str(weight) +'- Qty '+ str(qty) +'')
    return mark_safe(t)

@register.simple_tag
def employee_weight_report(stock_id, e_id):
    weight = 0
    qty = 0
    if stock_id:
        if e_id:
            order_datail = Order_detail.objects.filter(stock_item_id=stock_id, office_employee_id=e_id)
            for o in order_datail:
                weight += o.weight
        else:
            order_datail = Order_detail.objects.filter(stock_item_id=stock_id)
            for o in order_datail:
                weight += o.weight
    return weight

@register.simple_tag
def employee_qty_report(stock_id, e_id):
    qty = 0
    if stock_id:
        if e_id:
            order_datail = Order_detail.objects.filter(stock_item_id=stock_id, office_employee_id=e_id)
            for o in order_datail:
                qty += o.qty
        else:
            order_datail = Order_detail.objects.filter(stock_item_id=stock_id)
            for o in order_datail:
                qty += o.qty
            
    return qty


@register.simple_tag
def total_amount_report(e_id, stock_item_id, from_date, to_date):
    if e_id and stock_item_id and from_date:
        total_amount = 0
        o = Order_detail.objects.filter(date__gte=from_date,date__lte=to_date,office_employee_id=e_id, stock_item_id=stock_item_id)
        for o in o:
            amount = o.weight * o.prise
            total_amount += amount
        return total_amount
    else:
        total_amount = 0
        o = Order_detail.objects.filter(date__gte=from_date,date__lte=to_date, stock_item_id=stock_item_id)
        for o in o:
            amount = o.weight * o.prise
            total_amount += amount
        return total_amount
    
@register.simple_tag
def total_item_amount_report(e_id, from_date, to_date):
    total_amount = 0
    if e_id:
        o = Order_detail.objects.filter(date__gte=from_date,date__lte=to_date,office_employee_id=e_id)
        for o in o:
            amount = o.weight * o.prise
            total_amount += amount
        return total_amount
    else:
        o = Order_detail.objects.filter(date__gte=from_date,date__lte=to_date)
        for o in o:
            amount = o.weight * o.prise
            total_amount += amount
        return total_amount