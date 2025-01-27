from django.http import JsonResponse
from django.shortcuts import render
from owner.models import *
from django.template.loader import *
from django.db.models import Q
from django.db.models import Avg, Sum, Min, Max
# Create your views here.
def item_search_by_category(request):
    if request.method == 'GET':
        cat_id = request.GET['cat_id']
        shope_id = request.GET['shope_id']
        item = Stock_item.objects.filter(shope_id=shope_id, item_category_id=cat_id, stock_status=1, status=1)
        print(item)
        context={
            'item':item
        }
        t = render_to_string('ajax/office/item_search_by_category.html', context)
    return JsonResponse({'t': t})

def search_item(request):
    if request.method == 'GET':
        shope_id = request.GET['shope_id']
        item_name = request.GET['item_name']
        item = []
        if item_name:
            item = Item.objects.filter(Q(english_name__icontains=item_name, shope_id=shope_id))
        
        context={
            'item':item
        }
        t = render_to_string('ajax/office/search_item.html', context)
    return JsonResponse({'t': t})

def delete_purchase_cart_item(request):
    if request.method == 'GET':
        cart_id = request.GET['c_id']
        Purchase_cart.objects.filter(id=cart_id).delete()
    return JsonResponse({'t': 't'})

def add_to_item_weight_purchase(request):
    if request.method == 'GET':
        cart_id = request.GET['cart_id']
        weight = request.GET['weight']
        employee_id = request.GET['employee_id']
        c = Purchase_cart.objects.filter(id=cart_id).first()
        
        c.qty += 1
        c.save()
        Purchase_item_weight_detail(
            cart_id=cart_id,
            weight=weight
        ).save()
    t = render_to_string('ajax/office/purchase_bill_ajax.html', {'cart':Purchase_cart.objects.filter(office_employee_id=employee_id), 'employee':office_employee.objects.filter(id=employee_id).first()})
    return JsonResponse({'t': t})

def remove_item_weight_purchase(request):
    if request.method == 'GET':
        item_weight_detail_id = request.GET['item_weight_detail_id']
        cart_id = request.GET['cart_id']
        cart = Purchase_cart.objects.filter(id=cart_id).first()
        c = Purchase_cart.objects.filter(id=cart_id).first()
        c.qty -= 1
        c.save()
        Purchase_item_weight_detail.objects.get(id=item_weight_detail_id).delete()
    t = render_to_string('ajax/office/purchase_bill_ajax.html', {'cart':Purchase_cart.objects.filter(office_employee_id=cart.office_employee.id), 'employee_id':office_employee.objects.filter(id=cart.office_employee.id).first()})
    return JsonResponse({'t': t})
    
def search_item_by_words(request):
    if request.method == 'GET':
        words = request.GET['words']
        shope_id = request.GET['shope_id']
        if words:
            item = Stock_item.objects.filter(Q(item_name_english__icontains=words, shope_id=shope_id))
        context={
            'item': item
        }
        t = render_to_string('ajax/office/item_search_by_category.html', context)
    return JsonResponse({'t': t})

def customer_check(request):
    if request.method == 'GET':
        c = ''
        name = request.GET['name']
        address = request.GET['address']
        mobile = request.GET['mobile']
        shope_id = request.GET['shope_id']
        if 4 < len(name) :
            c = Customer.objects.filter(Q(name__icontains=name),shope_id=shope_id)
        if 4 < len(address) :
            c = Customer.objects.filter(Q(address__icontains=address),shope_id=shope_id)
        if 4 < len(mobile) :
            c = Customer.objects.filter(Q(mobile__icontains=name),shope_id=shope_id)
        context={
            'c':c[0:3]
        }
        t = render_to_string('ajax/office/customer_check.html', context)
    return JsonResponse({'t': t})

def add_to_item_weight(request):
    if request.method == 'GET':
        cart_id = request.GET['cart_id']
        weight = request.GET['weight']
        employee_id = request.GET['employee_id']
        stock_item_id = request.GET['stock_item_id']
        c = Cart.objects.filter(id=cart_id).first()
        c.qty += 1
        c.save()
        Item_weight_detail(
            cart_id=cart_id,
            weight=weight
        ).save()
        s = Stock_item.objects.filter(id=stock_item_id).first()
        s.stock_weight -= int(weight)
        s.stock_qty -= 1
        s.save()
        if s.stock_weight < 1:
            s.stock_status = 0
            s.save()
        context={
            'cart':Cart.objects.filter(office_employee_id=employee_id),
            'employee_id':employee_id
        }
        t = render_to_string('ajax/office/add_to_item_weight.html', context)
    return JsonResponse({'t': t})

def remove_cart_item(request):
    if request.method == 'GET':
        cart_id = request.GET['cart_id']
        employee_id = request.GET['employee_id']
        Item_weight_detail.objects.filter(cart_id=cart_id).delete()
        Cart.objects.filter(id=cart_id).delete()
        context={
            'cart':Cart.objects.filter(office_employee_id=employee_id),
            'employee_id':employee_id
        }
        t = render_to_string('ajax/office/add_to_item_weight.html', context)
    return JsonResponse({'t': t, 'cart':len(Cart.objects.filter(office_employee_id=employee_id))})

def calculete_prise(request):
    if request.method == 'GET':
        cart_id = request.GET['cart_id']
        prise = request.GET['prise']
        c = Cart.objects.filter(id=cart_id).first()
        c.prise = float(prise)
        c.save()
    cart = Cart.objects.filter(id=cart_id).first()
    context={
        'cart':Cart.objects.filter(office_employee_id=cart.office_employee.id),
        'employee_id':cart.office_employee.id
    }
    t = render_to_string('ajax/office/add_to_item_weight.html', context)
    return JsonResponse({'t': t})

def calculete_prise_purchase(request):
    if request.method == 'GET':
        cart_id = request.GET['cart_id']
        prise = request.GET['prise']
        c = Purchase_cart.objects.filter(id=cart_id).first()
        c.prise = float(prise)
        c.save()
    cart = Purchase_cart.objects.filter(id=cart_id).first()
    context={
        'cart':Purchase_cart.objects.filter(office_employee_id=cart.office_employee.id),
        'employee':office_employee.objects.filter(id=cart.office_employee.id).first()
    }
    t = render_to_string('ajax/office/purchase_bill_ajax.html', context)
    return JsonResponse({'t': t})

def farmer_check(request):
    if request.method == 'GET':
        c = ''
        name = request.GET['name']
        address = request.GET['address']
        mobile = request.GET['mobile']
        shope_id = request.GET['shope_id']
        if 1 < len(name) :
            c = Farmer.objects.filter(Q(name__icontains=name),shope_id=shope_id)
        if 1 < len(address) :
            c = Farmer.objects.filter(Q(address__icontains=address),shope_id=shope_id)
        if 1 < len(mobile) :
            c = Farmer.objects.filter(Q(mobile__icontains=name),shope_id=shope_id)
        context={
            'c':c[0:3]
        }
        t = render_to_string('ajax/office/farmer_check.html', context)
    return JsonResponse({'t': t})

def save_farmer(request):
    if request.method == 'GET':
        name = request.GET['name']
        address = request.GET['address']
        mobile = request.GET['mobile']
        shope_id = request.GET['shope_id']
        Farmer(
            name=name,
            address=address,
            mobile=mobile,
            shope_id=shope_id
        ).save()
        id = Farmer.objects.filter(shope_id=shope_id).first().id
    return JsonResponse({'id': id})

def cart_qty(request):
    if request.method == 'GET':
        cart_id = request.GET['cart_id']
        cart_qty_input = request.GET['cart_qty_input']
        if cart_qty_input == '':
            cart_qty_input = str(0)
        cart = Cart.objects.filter(id=cart_id).first()
        cart_qty = cart.qty
        if cart_qty == '':
            cart_qty = 0
        if cart_qty_input > str(cart_qty):
            q = (cart_qty - int(cart_qty_input))
            s = Stock_item.objects.filter(id=cart.stock_item.id).first()
            s.stock_qty += q
            s.save()
        if cart_qty_input < str(cart_qty):
            print('hi')
            new_qty = (cart_qty - int(cart_qty_input))
            s = Stock_item.objects.filter(id=cart.stock_item.id).first()
            s.stock_qty += new_qty
            s.save()
        cart.qty = int(cart_qty_input)
        cart.save()
    context={
        'cart':Cart.objects.filter(office_employee_id=cart.office_employee.id),
        'employee_id':cart.office_employee.id
    }
    t = render_to_string('ajax/office/add_to_item_weight.html', context)
    return JsonResponse({'t': t})

def remove_item_weight(request):
    if request.method == 'GET':
        item_weight_detail_id = request.GET['item_weight_detail_id']
        weight = request.GET['weight']
        cart_id = request.GET['cart_id']
        cart = Cart.objects.filter(id=cart_id).first()
        s = Stock_item.objects.filter(id=cart.stock_item_id).first()
        s.stock_weight += int(weight)
        s.stock_qty += 1
        s.save()
        c = Cart.objects.filter(id=cart_id).first()
        c.qty -= 1
        c.save()
        Item_weight_detail.objects.get(id=item_weight_detail_id).delete()
        context={
            'cart':Cart.objects.filter(office_employee_id=cart.office_employee.id),
            'employee_id':cart.office_employee.id
        }
        t = render_to_string('ajax/office/add_to_item_weight.html', context)
    return JsonResponse({'t': t})

def set_purchase_amount(request):
    if request.method == 'GET':
        s_id = request.GET['s_id']
        purchase_amount = request.GET['purchase_amount']
        s = Stock_item.objects.filter(id=s_id).first()
        s.purchase_amount =purchase_amount
        s.save()
    return JsonResponse({'t': 't'})

def set_vehicle_charges(request):
    if request.method == 'GET':
        s_id = request.GET['s_id']
        set_vehicle_charges = request.GET['set_vehicle_charges']
        s = Stock_item.objects.filter(id=s_id).first()
        s.vehicle_charges =set_vehicle_charges
        s.save()
    return JsonResponse({'t': 't'})

def save_cash_amount(request):
    if request.method == 'GET':
        shope_id = request.GET['shope_id']
        office_employee_id = request.GET['office_employee_id']
        order_master_id = request.GET['order_master_id']
        amount = request.GET['cash_amount']
        Cash_transition(
            shope_id=shope_id,
            office_employee_id=office_employee_id,
            amount=amount,
            order_master_id=order_master_id
        ).save()
        om = order_master.objects.filter(shope_id=shope_id,id=order_master_id).first()
        total_pending_amount = om.total
        total_pending_amount -= om.discount
        if Cash_transition.objects.filter(order_master_id=om.id).exists() or Phonepe_transition.objects.filter(order_master_id=om.id).exists():
            c = Cash_transition.objects.filter(order_master_id=om.id).aggregate(Sum('amount'))
            cash = c['amount__sum']
            if cash == None:
                cash = 0
            if cash:
                total_pending_amount -= cash  
            p = Phonepe_transition.objects.filter(order_master_id=om.id).aggregate(Sum('amount'))
            phonepe = p['amount__sum']
            if phonepe == None:
                phonepe = 0
            if phonepe:
                total_pending_amount -= phonepe
        total_credit = cash + phonepe  
    context={
        'cash_transition':Cash_transition.objects.filter(shope_id=shope_id,order_master_id=order_master_id),
        'phonepe_transition':Phonepe_transition.objects.filter(shope_id=shope_id,order_master_id=order_master_id),
        'total_credit':total_credit
    }
    t = render_to_string('ajax/office/transition_histry.html', context)
    return JsonResponse({'t': t, 'total_pending_amount':total_pending_amount})

def save_phonepe_amount(request):
    if request.method == 'GET':
        shope_id = request.GET['shope_id']
        office_employee_id = request.GET['office_employee_id']
        order_master_id = request.GET['order_master_id']
        amount = request.GET['cash_amount']
        phonepe_number_id = request.GET['phonepe_number_id']
        Phonepe_transition(
            shope_id=shope_id,
            office_employee_id=office_employee_id,
            phonepe_number_id=phonepe_number_id,
            amount=amount,
            order_master_id=order_master_id
        ).save()
        om = order_master.objects.filter(shope_id=shope_id,id=order_master_id).first()
        total_pending_amount = om.total
        total_pending_amount -= om.discount
        if Cash_transition.objects.filter(order_master_id=om.id).exists() or Phonepe_transition.objects.filter(order_master_id=om.id).exists():
            c = Cash_transition.objects.filter(order_master_id=om.id).aggregate(Sum('amount'))
            cash = c['amount__sum']
            if cash == None:
                cash = 0
            if cash:
                total_pending_amount -= cash  
            p = Phonepe_transition.objects.filter(order_master_id=om.id).aggregate(Sum('amount'))
            phonepe = p['amount__sum']
            if phonepe == None:
                phonepe = 0
            if phonepe:
                total_pending_amount -= phonepe  
        total_credit = cash + phonepe
    context={
        'cash_transition':Cash_transition.objects.filter(shope_id=shope_id,order_master_id=order_master_id),
        'phonepe_transition':Phonepe_transition.objects.filter(shope_id=shope_id,order_master_id=order_master_id),
        'total_credit':total_credit
    }
    t = render_to_string('ajax/office/transition_histry.html', context)
    return JsonResponse({'t': t, 'total_pending_amount':total_pending_amount})

def save_discount_amount(request):
    if request.method == 'GET':
        shope_id = request.GET['shope_id']
        office_employee_id = request.GET['office_employee_id']
        order_master_id = request.GET['order_master_id']
        amount = request.GET['discount_amount']
        om = order_master.objects.filter(shope_id=shope_id,id=order_master_id).first()
        total_pending_amount = om.total
        om.discount = amount
        om.save()
        cash = ''
        phonepe = ''
        total_pending_amount -= float(amount)
        if Cash_transition.objects.filter(order_master_id=om.id).exists() or Phonepe_transition.objects.filter(order_master_id=om.id).exists():
            c = Cash_transition.objects.filter(order_master_id=om.id).aggregate(Sum('amount'))
            cash = c['amount__sum']
            if cash == None:
                cash = 0
            if cash:
                total_pending_amount -= cash  
            p = Phonepe_transition.objects.filter(order_master_id=om.id).aggregate(Sum('amount'))
            phonepe = p['amount__sum']
            if phonepe == None:
                phonepe = 0
            if phonepe:
                total_pending_amount -= phonepe  
            
        total_credit = cash + phonepe
    context={
        'cash_transition':Cash_transition.objects.filter(shope_id=shope_id,order_master_id=order_master_id),
        'phonepe_transition':Phonepe_transition.objects.filter(shope_id=shope_id,order_master_id=order_master_id),
        'total_credit':total_credit
    }
    t = render_to_string('ajax/office/transition_histry.html', context)
    return JsonResponse({'t': t, 'total_pending_amount':total_pending_amount})