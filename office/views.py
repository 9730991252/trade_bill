from django.shortcuts import render, redirect
from owner.models import *
from django.views.decorators.csrf import csrf_exempt
from office.helper import *
from django.db.models import Avg, Sum, Min, Max
import math


# Create your views here.
def office_home(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile, status=1).first()
        context={
            'employee':e,
            'item':Item.objects.filter(shope_id=e.shope.id),
            'farmer':Farmer.objects.filter(shope_id=e.shope.id),

        }
        return render(request, 'office/office_home.html', context)
    else:
        return redirect('/')
    
@csrf_exempt
def sell_bill(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile, status=1).first()
        if e:
            if 'add_to_cart'in request.POST:
                item_id = request.POST.get('item_id')
                if Sell_cart.objects.filter(office_employee_id=e.id, item_id=item_id).exists():
                    pass
                else:
                    Sell_cart(
                        shope_id=e.shope.id,
                        office_employee_id=e.id,
                        item_id=item_id,
                    ).save()
                return redirect('/office/sell_bill/')
            if 'remove_cart_item'in request.GET:
                id = request.GET.get('id')
                Sell_cart.objects.filter(id=id).delete()
                return redirect('/office/sell_bill/')

            if 'complete_bill'in request.POST:
                hamali = request.POST.get('hamali')
                tolai = request.POST.get('tolai')
                aadat = request.POST.get('aadat')
                shears = request.POST.get('shears')
                eater = request.POST.get('eater')
                total = request.POST.get('total')
                customer_id = request.POST.get('customer_id')
                order_filter = (int(Sell_order_master.objects.filter(shope_id=e.shope.id).count()) + 1)
                Sell_order_master(
                    shope_id=e.shope.id,
                    office_employee_id = e.id,
                    customer_id=customer_id,
                    hamali= float(hamali),
                    tolai= float(tolai),
                    aadat= float(aadat),
                    shears= float(shears),
                    eater= float(eater),
                    total= float(math.floor(float(total))),
                    order_filter=order_filter,
                ).save()
                om = Sell_order_master.objects.filter(shope_id=e.shope_id,order_filter=order_filter).first()
                c = Sell_cart.objects.filter(office_employee_id=e.id)
                if c:
                    for c in c:
                        i = Sell_item_weight_detail.objects.filter(cart_id=c.id).aggregate(Sum('weight'))
                        weight = i['weight__sum']
                        Sell_order_detail(
                            shope_id=c.office_employee.shope.id,
                            office_employee_id = c.office_employee.id,
                            item_id = c.item.id,
                            order_master_id = om.id,
                            prise=c.prise,
                            qty=c.qty,
                            weight=weight,
                            order_filter=order_filter,
                        ).save()
                        o = Sell_order_detail.objects.filter(item_id = c.item.id,).first()
                        i = Sell_item_weight_detail.objects.filter(cart_id = c.id)
                        if i:
                            for i in i:
                                it = Sell_item_weight_detail.objects.filter(id = i.id).first()
                                it.cart_id = ''
                                it.order_detail_id = o.id
                                it.save()
                Sell_cart.objects.filter(office_employee_id=e.id).delete()
                return redirect('completed_view_sell_bill', order_filter=order_filter)
        context={
            'employee':e,
            'cart':Sell_cart.objects.filter(office_employee_id=e.id),
        }
        return render(request, 'office/sell_bill.html', context)
    
def completed_view_sell_bill(request, order_filter):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile, status=1).first()
        om = Sell_order_master.objects.filter(shope_id=e.shope_id, order_filter=order_filter).first()
        context = {
            'employee': e,
            'order_master': om,
            'order_detail': Sell_order_detail.objects.filter(shope_id=e.shope_id, order_filter=order_filter),
        }
        return render(request, 'office/completed_view_sell_bill.html', context)
    else:
        return redirect('/')
    
def sell_completed_bills(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile, status=1).first()
        context = {
            'employee': e,
            'order_master': Sell_order_master.objects.filter(shope_id=e.shope_id).order_by('-id'),
        }
        return render(request, 'office/sell_completed_bills.html', context)
    else:
        return redirect('/')
    
@csrf_exempt
def purchase_bill(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile, status=1).first()
        if e:
            if 'add_to_cart'in request.POST:
                item_id = request.POST.get('item_id')
                if Purchase_cart.objects.filter(office_employee_id=e.id, item_id=item_id).exists():
                    pass
                else:
                    Purchase_cart(
                        shope_id=e.shope.id,
                        office_employee_id=e.id,
                        item_id=item_id,
                    ).save()
                return redirect('/office/purchase_bill/')
            if 'remove_cart_item'in request.GET:
                id = request.GET.get('id')
                Purchase_cart.objects.filter(id=id).delete()
                return redirect('/office/purchase_bill/')

            # Purchase_order_master.objects.all().delete()
            # Purchase_order_detail.objects.all().delete()
            if 'complete_bill'in request.POST:
                hamali = request.POST.get('hamali')
                tolai = request.POST.get('tolai')
                aadat = request.POST.get('aadat')
                shears = request.POST.get('shears')
                eater = request.POST.get('eater')
                total = request.POST.get('total')
                farmer_id = request.POST.get('farmer_id')
                order_filter = (int(Purchase_order_master.objects.filter(shope_id=e.shope.id).count()) + 1)
                Purchase_order_master(
                    shope_id=e.shope.id,
                    office_employee_id = e.id,
                    farmer_id=farmer_id,
                    hamali= float(hamali),
                    tolai= float(tolai),
                    aadat= float(aadat),
                    shears= float(shears),
                    eater= float(eater),
                    total= float(math.floor(float(total))),
                    order_filter=order_filter,
                ).save()
                c = Purchase_cart.objects.filter(office_employee_id=e.id)
                if c:
                    for c in c:
                        i = Purchase_item_weight_detail.objects.filter(cart_id=c.id).aggregate(Sum('weight'))
                        weight = i['weight__sum']
                        Purchase_order_detail(
                            shope_id=c.office_employee.shope.id,
                            office_employee_id = c.office_employee.id,
                            item_id = c.item.id,
                            prise=c.prise,
                            qty=c.qty,
                            weight=weight,
                            order_filter=order_filter,
                        ).save()
                        o = Purchase_order_detail.objects.filter(item_id = c.item.id,).first()
                        i = Purchase_item_weight_detail.objects.filter(cart_id = c.id)
                        if i:
                            for i in i:
                                it = Purchase_item_weight_detail.objects.filter(id = i.id).first()
                                it.cart_id = ''
                                it.order_detail_id = o.id
                                it.save()
                Purchase_cart.objects.filter(office_employee_id=e.id).delete()
                return redirect('completed_view_purchase_bill', order_filter=order_filter)
        context={
            'employee':e,
            'cart':Purchase_cart.objects.filter(office_employee_id=e.id),
        }
        return render(request, 'office/purchase_bill.html', context)
    else:
        return redirect('/')
    
def completed_view_purchase_bill(request, order_filter):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile, status=1).first()
        om = Purchase_order_master.objects.filter(shope_id=e.shope_id,order_filter=order_filter).first()
        context={
            'employee':e,
            'order_master':om,
            'order_detail':Purchase_order_detail.objects.filter(shope_id=e.shope_id,order_filter=order_filter),
        }
        return render(request, 'office/completed_view_purchase_bill.html', context)
    else:
        return redirect('/')

def genereate_purchase_bill_image(request, order_filter):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile, status=1).first()
        om = Purchase_order_master.objects.filter(shope_id=e.shope_id,order_filter=order_filter).first()
        context={
            'employee':e,
            'order_master':om,
            'order_detail':Purchase_order_detail.objects.filter(shope_id=e.shope_id,order_filter=order_filter),
        }
        return render(request, 'office/genereate_purchase_bill_image.html', context)
    else:
        return redirect('/')

@csrf_exempt
def item(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile, status=1).first()
        if 'add_item'in request.POST:
            marathi_name = request.POST.get('marathi_name')
            english_name = request.POST.get('english_name')
            Item(
                shope_id=e.shope.id,
                marathi_name=marathi_name,
                english_name=english_name,
            ).save()            
            return redirect('/office/item/')
        if 'Edit_item'in request.POST:
            id = request.POST.get('id')
            marathi_name = request.POST.get('marathi_name')
            english_name = request.POST.get('english_name')
            i = Item.objects.filter(id=id).first()
            i.marathi_name = marathi_name
            i.english_name = english_name
            i.save()
            return redirect('/office/item/')
        if 'active'in request.POST:
            id = request.POST.get('id')
            c = Item.objects.filter(id=id).first()
            c.status = 0
            c.save()
            return redirect('/office/item/')
        if 'deactive'in request.POST:
            id = request.POST.get('id')
            c = Item.objects.filter(id=id).first()
            c.status = 1
            c.save()
            return redirect('/office/item/')
        context={
            'employee':e,
            'item':Item.objects.filter(shope_id=e.shope.id)
        }
        return render(request, 'office/item.html', context)
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
    
def purchase_completed_bills(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile, status=1).first()
        context={
            'employee':e,
            'order_master':Purchase_order_master.objects.filter(shope_id=e.shope_id).order_by('-id'),
        }
        return render(request, 'office/purchase_completed_bills.html', context)
    else:
        return redirect('/')
