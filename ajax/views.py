from django.http import JsonResponse
from django.shortcuts import render
from owner.models import *
from django.template.loader import *
from django.db.models import Q
from django.db.models import Avg, Sum, Min, Max
# Create your views here.

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

def sell_search_item(request):
    if request.method == 'GET':
        shope_id = request.GET['shope_id']
        item_name = request.GET['item_name']
        item = []
        if item_name:
            item = Purchase_order_detail.objects.filter(Q(item__english_name__icontains=item_name, shope_id=shope_id, stock_status=1 ) )
        
        context={
            'item':item
        }
        t = render_to_string('ajax/office/sell_search_item.html', context)
    return JsonResponse({'t': t})

def add_to_item_weight_sell(request):
    if request.method == 'GET':
        cart_id = request.GET['cart_id']
        weight = request.GET['weight']
        employee_id = request.GET['employee_id']
        c = Sell_cart.objects.filter(id=cart_id).first()
        
        c.qty += 1
        c.save()
        Sell_item_weight_detail(
            cart_id=cart_id,
            weight=weight
        ).save()
    t = render_to_string('ajax/office/sell_bill_ajax.html', {'cart':Sell_cart.objects.filter(office_employee_id=employee_id), 'employee':office_employee.objects.filter(id=employee_id).first()})
    return JsonResponse({'t': t})

def delete_purchase_cart_item(request):
    if request.method == 'GET':
        cart_id = request.GET['c_id']
        Purchase_cart.objects.filter(id=cart_id).delete()
    return JsonResponse({'t': 't'})
def delete_sell_cart_item(request):
    if request.method == 'GET':
        cart_id = request.GET['c_id']
        Sell_cart.objects.filter(id=cart_id).delete()
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
    
def remove_item_weight_sell(request):
    if request.method == 'GET':
        item_weight_detail_id = request.GET['item_weight_detail_id']
        cart_id = request.GET['cart_id']
        cart = Sell_cart.objects.filter(id=cart_id).first()
        c = Sell_cart.objects.filter(id=cart_id).first()
        c.qty -= 1
        c.save()
        Sell_item_weight_detail.objects.get(id=item_weight_detail_id).delete()
    t = render_to_string('ajax/office/sell_bill_ajax.html', {'cart':Sell_cart.objects.filter(office_employee_id=cart.office_employee.id), 'employee_id':office_employee.objects.filter(id=cart.office_employee.id).first()})
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

def calculete_prise_sell(request):
    if request.method == 'GET':
        cart_id = request.GET['cart_id']
        prise = request.GET['prise']
        c = Sell_cart.objects.filter(id=cart_id).first()
        c.prise = float(prise)
        c.save()
    cart = Sell_cart.objects.filter(id=cart_id).first()
    context={
        'cart':Sell_cart.objects.filter(office_employee_id=cart.office_employee.id),
        'employee':office_employee.objects.filter(id=cart.office_employee.id).first()
    }
    t = render_to_string('ajax/office/sell_bill_ajax.html', context)
    return JsonResponse({'t': t})


def farmer_check(request):
    if request.method == 'GET':
        c = ''
        name = request.GET['name']
        address = request.GET['address']
        mobile = request.GET['mobile']
        shope_id = request.GET['shope_id']
        add_btn_status = 1
        print(shope_id)
        if 0 < len(name) :
            c = list(Farmer.objects.filter(Q(name__icontains=name),shope_id=shope_id))
        if 0 < len(address) :
            c += Farmer.objects.filter(Q(address__icontains=address),shope_id=shope_id)
        if 0 < len(mobile) :
            c += Farmer.objects.filter(Q(mobile__icontains=mobile),shope_id=shope_id)
            if (c):
                if int(c[0].mobile) == int(mobile):
                    add_btn_status = 0
        context={
            'c':c[0:3]
        }
        t = render_to_string('ajax/office/farmer_check.html', context)
    return JsonResponse({'t': t, 'add_btn_status': add_btn_status})

def customer_check(request):
    if request.method == 'GET':
        c = ''
        name = request.GET['name']
        address = request.GET['address']
        mobile = request.GET['mobile']
        shope_id = request.GET['shope_id']
        add_btn_status = 1
        if 0 < len(name) :
            c = list(Customer.objects.filter(Q(name__icontains=name),shope_id=shope_id))
        if 0 < len(address) :
            c += Customer.objects.filter(Q(address__icontains=address),shope_id=shope_id)
        if 0 < len(mobile) :
            c += Customer.objects.filter(Q(mobile__icontains=mobile),shope_id=shope_id)
            if (c):
                if int(c[0].mobile) == int(mobile):
                    add_btn_status = 0
        context={
            'c':c[0:3]
        }
        t = render_to_string('ajax/office/customer_check.html', context)
    return JsonResponse({'t': t, 'add_btn_status': add_btn_status})

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

def save_sell_customer(request):
    if request.method == 'GET':
        name = request.GET['name']
        address = request.GET['address']
        mobile = request.GET['mobile']
        shope_id = request.GET['shope_id']
        Customer(
            name=name,
            address=address,
            mobile=mobile,
            shope_id=shope_id
        ).save()
        id = Customer.objects.filter(shope_id=shope_id).first().id
    return JsonResponse({'id': id})