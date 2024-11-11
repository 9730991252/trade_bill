from django.shortcuts import render, redirect
from owner.models import *
from django.views.decorators.csrf import csrf_exempt
from office.helper import *
from django.db.models import Avg, Sum, Min, Max
# Create your views here.
def office_home(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile, status=1).first()
        context={
            'employee':e,
            'stock':Stock_item.objects.filter(status=1,stock_status=1,shope_id=e.shope.id).order_by('item_category', '-id'),

        }
        return render(request, 'office/office_home.html', context)
    else:
        return redirect('/')

  
  
  
     
def add_employee(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile).first()
        if 'Add_employee'in request.POST:
            name = request.POST.get('name')
            mobile = request.POST.get('mobile')
            pin = request.POST.get('pin')
            if office_employee.objects.filter(mobile=mobile).exists():
                pass
            else:
                office_employee(
                    shope_id=e.shope.id,
                    name=name,
                    mobile=mobile,
                    pin=pin,
                ).save()    
            return redirect('/office/add_employee/')
        if 'Edit_employee'in request.POST:
            id = request.POST.get('id')
            name = request.POST.get('name')
            mobile = request.POST.get('mobile')
            pin = request.POST.get('pin')
            office_employee(
                id=id,
                shope_id=e.shope.id,
                name=name,
                mobile=mobile,
                pin=pin,
            ).save()
            return redirect('/office/add_employee/')
        if 'active'in request.POST:
            id = request.POST.get('id')
            c = office_employee.objects.filter(id=id).first()
            c.status = 0
            c.save()
            return redirect('/office/add_employee/')
        if 'deactive'in request.POST:
            id = request.POST.get('id')
            c = office_employee.objects.filter(id=id).first()
            c.status = 1
            c.save()
            return redirect('/office/add_employee/')
        context={
            'e':e,
            'office_employee':office_employee.objects.filter(shope_id=e.shope.id)
        }
        return render(request, 'office/add_employee.html', context)
    else:
        return redirect('login')
     
     
     
     
     
     
     
     
def item_category(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile, status=1).first()
        if 'Add_item_category'in request.POST:
            name = request.POST.get('name')
            shears = request.POST.get('shears')
            Item_category(
                shope_id=e.shope.id,
                name=name,
                shears=shears,
            ).save()    
            return redirect('/office/item_category/')
        if 'Edit_item_category'in request.POST:
            id = request.POST.get('id')
            name = request.POST.get('name')
            shears = request.POST.get('shears')
            Item_category(
                id=id,
                shope_id=e.shope.id,
                name=name,
                shears=shears,
            ).save()
            return redirect('/office/item_category/')
        if 'active'in request.POST:
            id = request.POST.get('id')
            c = Item_category.objects.filter(id=id).first()
            c.status = 0
            c.save()
            return redirect('/office/item_category/')
        if 'deactive'in request.POST:
            id = request.POST.get('id')
            c = Item_category.objects.filter(id=id).first()
            c.status = 1
            c.save()
            return redirect('/office/item_category/')
        context={
            'employee':e,
            'item_category':Item_category.objects.filter(shope_id=e.shope.id)
        }
        return render(request, 'office/item_category.html', context)
    else:
        return redirect('/') 
    
    
    
    
    
def stock(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile, status=1).first()
        if 'Add_stock'in request.POST:
            item_category_id = request.POST.get('item_category')
            item_name_english = request.POST.get('item_name_english')
            item_name_marathi = request.POST.get('item_name_marathi')
            qty = request.POST.get('qty')
            weight = request.POST.get('weight')
            stock_weight = request.POST.get('weight')
            vehicle_number = request.POST.get('vehicle_number')
            party_name = request.POST.get('party_name')
            purchase_amount = request.POST.get('purchase_amount')
            Stock_item(
                office_employee_id=e.id,
                shope_id=e.shope.id,
                item_category_id=item_category_id,
                item_name_english=item_name_english,
                item_name_marathi=item_name_marathi,
                qty=qty,
                stock_qty=qty,
                weight=weight,
                stock_weight=stock_weight,
                vehicle_number=vehicle_number,
                party_name=party_name,
                purchase_amount=purchase_amount,
            ).save()
        context={
            'employee':e,
            'item_category':Item_category.objects.filter(shope_id=e.shope.id, status=1),
            'stock':Stock_item.objects.filter(status=1,stock_status=1,shope_id=e.shope.id).order_by('item_category', '-id'),
        }
        return render(request, 'office/stock.html', context)
    else:
        return redirect('/')
    
@csrf_exempt
def new_bill(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile, status=1).first()
        c = ''
        selected_customer_status = 0
        if 'add_customer'in request.POST:
            name = request.POST.get('name')
            address = request.POST.get('address')
            c_mobile = request.POST.get('mobile')
            if Customer.objects.filter(name=name).exists() and Customer.objects.filter(mobile=c_mobile).exists() and Customer.objects.filter(address=address).exists() and Customer.objects.filter(office_employee_id=e.id).exists():
                pass
            else:
                Customer(
                    office_employee_id=e.id,
                    shope_id=e.shope.id,
                    name=name,
                    address=address,
                    mobile=c_mobile
                ).save()
            c = Customer.objects.filter(office_employee_id=e.id).last()
        if 'Select_Customer'in request.POST:
            id = request.POST.get('customer_id')
            c = Customer.objects.filter(id=id).last()
            selected_customer_status = 1
        if 'select_item'in request.POST:
            id = request.POST.get('id')
            check_cart_item(id,e.id,e.shope.id)
            return redirect('new_bill')
        if 'complete_bill'in request.POST:
            hamali = request.POST.get('hamali')
            tolai = request.POST.get('tolai')
            aadat = request.POST.get('aadat')
            shears = request.POST.get('shears')
            eater = request.POST.get('eater')
            total = request.POST.get('total')
            customer_id = request.POST.get('customer_id')
            order_filter = order_master.objects.filter(shope_id=e.shope.id).count()
            order_filter += 1
            order_master(
                shope_id=e.shope.id,
                office_employee_id = e.id,
                customer_id=customer_id,
                hamali= float(hamali),
                tolai= float(tolai),
                aadat= float(aadat),
                shears= float(shears),
                eater= float(eater),
                total= float(total),
                order_filter=order_filter,
            ).save()
            cart = Cart.objects.filter(shope_id=e.shope.id, office_employee_id=e.id)
            if cart:
                for c in cart:
                    i = Item_weight_detail.objects.filter(cart_id=c.id).aggregate(Sum('weight'))
                    weight = i['weight__sum']
                    Order_detail(
                        shope_id=c.office_employee.shope.id,
                        office_employee_id = c.office_employee.id,
                        customer_id=customer_id,
                        stock_item_id = c.stock_item.id,
                        prise=c.prise,
                        qty=c.qty,
                        order_filter=order_filter,
                        weight=weight
                    ).save()
                    o = Order_detail.objects.filter(order_filter=order_filter, stock_item_id = c.stock_item.id,).first()
                    i = Item_weight_detail.objects.filter(cart_id = c.id)
                    if i:
                        for i in i:
                            it = Item_weight_detail.objects.filter(id = i.id).first()
                            it.cart_id = ''
                            it.order_detail_id = o.id
                            it.save()
            Cart.objects.filter(shope_id=e.shope.id, office_employee_id=e.id).delete()
            return redirect(f'/office/completed_view_bill/{order_filter}')
        context={
            'employee':e,
            'item_category':Item_category.objects.filter(shope_id=e.shope.id, status=1),
            'customer':c,
            'selected_customer_status':selected_customer_status,
            'cart':Cart.objects.filter(shope_id=e.shope.id, office_employee_id=e.id),
            
        }
        return render(request, 'office/new_bill.html', context)
    else:
        return redirect('/')
    
def completed_view_bill(request, order_filter):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile, status=1).first()
        print(order_filter)
        context={
            'employee':e,
            'order_master':order_master.objects.filter(shope_id=e.shope_id,order_filter=order_filter).first(),
            'order_detail':Order_detail.objects.filter(shope_id=e.shope_id,order_filter=order_filter),
        }
        return render(request, 'office/completed_view_bill.html', context)
    else:
        return redirect('/')
    
def completed_bills(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile, status=1).first()
        context={
            'employee':e,
            'order_master':order_master.objects.filter(shope_id=e.shope.id).order_by('-id'),
        }
        return render(request, 'office/completed_bills.html', context)
    else:
        return redirect('/')
    
    
    
    
@csrf_exempt
def report(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile, status=1).first()
        context={
            'employee':e,
            'stock':Stock_item.objects.filter(shope_id=e.shope.id).order_by('item_category', '-id'),

        }
        return render(request, 'office/report.html', context)
    else:
        return redirect('/')
    
@csrf_exempt
def employee_sell_item(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile, status=1).first()
        from_date = ''
        to_date = ''
        order_detail = ''
        selected_employee = ''
        if 'employee_detail'in request.POST:
            from_date = request.POST.get('from_date')
            to_date = request.POST.get('to_date')
            employee_id = request.POST.get('employee_id')
            order_detail = []
            if employee_id == '0':
                print('hi')
                selected_employee = ''
                stock_item = Stock_item.objects.filter(shope_id=e.shope_id)
                if stock_item:
                    for s in stock_item:
                        o = Order_detail.objects.filter(date__gte=from_date,date__lte=to_date,stock_item_id=s.id).first()
                        if o:
                            order_detail.append(o)
            else:
                selected_employee = office_employee.objects.filter(status=1, id=employee_id).first()
                stock_item = Stock_item.objects.filter(shope_id=e.shope_id)
                if stock_item:
                    for s in stock_item:
                        o = Order_detail.objects.filter(date__gte=from_date,date__lte=to_date,office_employee_id=employee_id, stock_item_id=s.id).first()
                        if o:
                            order_detail.append(o)
        context={
            'employee':e,
            'all_employee':office_employee.objects.filter(status = 1, shope_id=e.shope_id),
            'from_date':from_date,
            'to_date':to_date,
            'selected_employee':selected_employee,
            'order_detail':order_detail
        }
        return render(request, 'office/employee_sell_item.html', context)
    else:
        return redirect('/')
    
    
    
    
