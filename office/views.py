from django.shortcuts import render, redirect
from owner.models import *
from django.views.decorators.csrf import csrf_exempt
from office.helper import *
from django.db.models import Avg, Sum, Min, Max
import math
from datetime import datetime
from django.contrib import messages

# Create your views here.
def logo(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile).first()
        if 'logo'in request.POST:
            image = request.FILES.get('image')
            Logo(
                shope_id=e.shope.id,
                image=image
            ).save()
            return redirect('logo')
        if 'edit_logo'in request.POST:
            image = request.FILES.get('image')
            if image:
                Logo(
                    id=Logo.objects.filter(shope_id=e.shope.id).first().id,
                    shope_id=e.shope.id,
                    image=image
                ).save()
                return redirect('logo')
        context={
            'e':e,
            'l':Logo.objects.filter(shope_id=e.shope.id).first()
        }
        return render(request, 'office/logo.html', context)
    else:
        return redirect('login')

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
    
def profile(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile, status=1).first()
        shope = e.shope
        if 'edit_profile'in request.POST:
            shope_name = request.POST.get('shope_name')
            owner_name = request.POST.get('owner_name')
            address = request.POST.get('address')
            description = request.POST.get('description')
            contact_details = request.POST.get('contact_details')
            mobile = request.POST.get('mobile')
            pin = request.POST.get('pin')
            shope.shope_name = shope_name
            shope.owner_name = owner_name
            shope.address = address
            shope.description = description
            shope.contact_details = contact_details
            shope.pin = pin
            shope.save()
            messages.success(request,"Profile Edited Successfully")
        context={
            'employee':e,
            'shope':shope
        }
        return render(request, 'office/profile.html', context)
    else:
        return redirect('login')
    
def item_detail(request, id):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile, status=1).first()
        item = Item.objects.filter(id=id).first()
        if 'edit_item_purchase'in request.POST:
            purchase_hamali = request.POST.get('purchase_hamali')
            purchase_tolai = request.POST.get('purchase_tolai')
            purchase_aadat = request.POST.get('purchase_aadat')
            purchase_shears = request.POST.get('purchase_shears')
            purchase_eater = request.POST.get('purchase_eater')
            item.purchase_hamali = purchase_hamali
            item.purchase_tolai = purchase_tolai
            item.purchase_aadat = purchase_aadat
            item.purchase_shears = purchase_shears
            item.purchase_eater = purchase_eater
            item.save()
            return redirect('/office/item_detail/'+str(item.id))
        if 'edit_item_sell'in request.POST:
            sell_hamali = request.POST.get('sell_hamali')
            sell_tolai = request.POST.get('sell_tolai')
            sell_aadat = request.POST.get('sell_aadat')
            sell_shears = request.POST.get('sell_shears')
            sell_eater = request.POST.get('sell_eater')
            item.sell_hamali = sell_hamali
            item.sell_tolai = sell_tolai
            item.sell_aadat = sell_aadat
            item.sell_shears = sell_shears
            item.sell_eater = sell_eater
            item.save()
            return redirect('/office/item_detail/'+str(item.id))
        if 'edit_item_marathi_name' in request.POST:
            name = request.POST.get('marathi_name')
            item.marathi_name = name
            item.save()
            return redirect('item_detail', id=id)
        if 'edit_item_english_name' in request.POST:
            name = request.POST.get('english_name')
            item.english_name = name
            item.save()
            return redirect('item_detail', id=id)
        context={
            'employee':e,
            'item':item,
        }
        return render(request, 'office/item_detail.html', context)
    else:
        return redirect('/')
    
def purchase_farmer(request):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile, status=1).first()

        context={
            'employee':e,
            'farmer':Farmer.objects.filter(shope_id=e.shope.id),

        }
        return render(request, 'office/purchase_farmer.html', context)
    else:
        return redirect('/')
    
    
def genereate_sell_bill_image(request, order_filter):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile, status=1).first()
        om = Sell_order_master.objects.filter(shope_id=e.shope_id, order_filter=order_filter).first()
        context = {
            'employee': e,
            'order_master': om,
            'order_detail': Sell_order_detail.objects.filter(shope_id=e.shope_id, order_filter=order_filter),
            'logo':Logo.objects.filter(shope=e.shope).first()
        }
        return render(request, 'office/genereate_sell_bill_image.html', context)
    else:
        return redirect('/')
    
    
@csrf_exempt
def pay_sell_bill(request, customer_id):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile, status=1).first()
        if e:
            remening_amount = change_sell_farmer_bill_paid_status(customer_id)

            if 'cash' in request.POST:
                date = request.POST.get('date')
                amount = request.POST.get('cash_amount')
                Pay_cash_amount_sell(e.shope.id,customer_id,date,amount)
                return redirect('pay_sell_bill', customer_id=customer_id)
            
            if 'phone_pe' in request.POST:
                date = request.POST.get('date')
                amount = request.POST.get('phone_pe_amount')
                phonepe_number = request.POST.get('phone_pe_number')
                Pay_phone_pe_amount_sell(e.shope.id,customer_id,date,amount,phonepe_number)
                return redirect('pay_sell_bill', customer_id=customer_id)
            
            if 'bank' in request.POST:
                date = request.POST.get('date')
                amount = request.POST.get('bank_amount')
                bank_name = request.POST.get('bank_name')
                bank_number = request.POST.get('bank_number')
                Pay_bank_amount_sell(e.shope.id,customer_id,date,amount,bank_number)
                return redirect('pay_sell_bill', customer_id=customer_id)
            if 'add_opning_amount'in request.POST:
                t = request.POST.get('type')
                amount = request.POST.get('amount')
                print(amount)
                if Customer_sell_opning_balance.objects.filter(customer_id=customer_id).exists():
                    pass
                else:
                    Customer_sell_opning_balance(
                        customer_id = customer_id,
                        shope_id = e.shope_id,
                        balance = amount,
                        type = t,
                    ).save()
                return redirect('pay_sell_bill', customer_id=customer_id)
            if 'edit_opning_balance'in request.POST:
                t = request.POST.get('type')
                amount = request.POST.get('amount')
                
                if Customer_sell_opning_balance.objects.filter(customer_id=customer_id).exists():
                    of = Customer_sell_opning_balance.objects.filter(customer_id=customer_id).first()
                    nf = Customer_sell_opning_balance.objects.filter(customer_id=customer_id).first()
                    nf.balance = amount
                    nf.type = t
                    nf.save()    
                    
                if int(t) == 1:
                    ba = int(math.floor(float(of.balance))) - int(math.floor(float(nf.balance)))
                    bill = Sell_order_master.objects.filter(customer_id=customer_id, paid_status=1).order_by('id')
                    for b in bill:
                        if ba <= b.total:
                            b.paid_status = 0
                            b.save()
                            ba -= b.total
                        else:
                            break
                else:
                    ba = int(math.floor(float(of.balance))) - int(math.floor(float(nf.balance)))
                    bill = Sell_order_master.objects.filter(customer_id=customer_id, paid_status=1).order_by('id')
                    for b in bill:
                        if ba <= b.total:
                            b.paid_status = 0
                            b.save()
                            ba -= b.total
                        else:
                            break
                        
                            
                return redirect('pay_sell_bill', customer_id=customer_id)   
            
            pending_amount = Sell_order_master.objects.filter(customer_id=customer_id).aggregate(Sum('total'))['total__sum']
            if pending_amount == None:
                pending_amount = 0
            paid_total_amount = Customer_sell_payment_transaction.objects.filter(customer_id=customer_id).aggregate(Sum('amount'))['amount__sum']
            if paid_total_amount == None:
                paid_total_amount = 0
                
        last_year = datetime.now().year
        last_year -= 1
        b_opn = Customer_sell_opning_balance.objects.filter(customer_id=customer_id).first()
        final_amount = (int(pending_amount) -  int(paid_total_amount))
        check_paid_total_amount = ''
        if b_opn:
            if b_opn.type == 0:
                final_amount += int(b_opn.balance)
                check_paid_total_amount = int(paid_total_amount) - int(b_opn.balance)
            else:
                final_amount -= int(b_opn.balance)
                check_paid_total_amount =int(paid_total_amount) + int(b_opn.balance)
        context = {
            'employee': e,
            'customer':Customer.objects.filter(id=customer_id).first(),
            'bill':Sell_order_master.objects.filter(customer_id=customer_id).order_by('-id'),
            'remening_amount':remening_amount,
            'transaction':Customer_sell_payment_transaction.objects.filter(customer_id=customer_id).order_by('-date'),
            'paid_total_amount':paid_total_amount,
            'final_amount':final_amount,
            'bill_total_amount':pending_amount,
            'last_year':last_year,
            'customer_sell_opning_balance':Customer_sell_opning_balance.objects.filter(customer_id=customer_id).first(),
            'check_paid_total_amount':check_paid_total_amount
        }
        return render(request, 'office/pay_sell_bill.html', context)
    else:
        return redirect('/')
    
def Pay_bank_amount_sell(shope_id, customer_id, date, amount, bank_number):
    Customer_sell_payment_transaction(
        shope_id=shope_id,
        customer_id=customer_id,
        date=date,
        amount=amount,
        bank_number=bank_number,
        payment_type='bank',
    ).save()
    
def Pay_phone_pe_amount_sell(shope_id, customer_id, date, amount, phonepe_number):
    Customer_sell_payment_transaction(
        shope_id=shope_id,
        customer_id=customer_id,
        date=date,
        amount=amount,
        phonepe_number=phonepe_number,
        payment_type='phonepe',
    ).save()
    
def Pay_cash_amount_sell(shope_id, customer_id, date, amount):
    Customer_sell_payment_transaction(
        shope_id=shope_id,
        customer_id=customer_id,
        date=date,
        amount=amount,
        payment_type='cash',
    ).save()
    
def change_sell_farmer_bill_paid_status(customer_id):
    b_opn = Customer_sell_opning_balance.objects.filter(customer_id=customer_id).first()
    recived_payment = Customer_sell_payment_transaction.objects.filter(customer_id=customer_id).aggregate(Sum('amount'))['amount__sum']
    if b_opn:
        if b_opn.type == 0:
            recived_payment -= int(b_opn.balance)
        else:
            recived_payment += int(b_opn.balance)
    
    if recived_payment == None:
        recived_payment = 0
    paid_bill_amount = Sell_order_master.objects.filter(customer_id=customer_id, paid_status = 1).aggregate(Sum('total'))['total__sum']
    if paid_bill_amount == None:
        paid_bill_amount = 0
    remening_amount = (int(recived_payment) - int(paid_bill_amount))
    bill = Sell_order_master.objects.filter(customer_id=customer_id, paid_status=0).order_by('date')
    
    bill_id = 0
    for b in bill:
        if remening_amount >= b.total:
            b.paid_status = 1
            b.save()
            remening_amount -= b.total
        else:
            bill_id = b.id
            if int(remening_amount) != 0:
                remening_amount = int(b.total) - int(remening_amount)
            break
    return {'bill_id':bill_id, 'remening_amount':remening_amount}
@csrf_exempt
def pay_purchase_bill(request, farmer_id):
    if request.session.has_key('office_mobile'):
        mobile = request.session['office_mobile']
        e = office_employee.objects.filter(mobile=mobile, status=1).first()
        if e:
            remening_amount = change_purchase_farmer_bill_paid_status(farmer_id)
            if 'cash' in request.POST:
                date = request.POST.get('date')
                amount = request.POST.get('cash_amount')
                Pay_cash_amount_purchase(e.shope.id,farmer_id,date,amount)
                return redirect('pay_purchase_bill', farmer_id=farmer_id)
            if 'phone_pe' in request.POST:
                date = request.POST.get('date')
                amount = request.POST.get('phone_pe_amount')
                phonepe_number = request.POST.get('phone_pe_number')
                Pay_phone_pe_amount_purchase(e.shope.id,farmer_id,date,amount,phonepe_number)
                return redirect('pay_purchase_bill', farmer_id=farmer_id)
            if 'bank' in request.POST:
                date = request.POST.get('date')
                amount = request.POST.get('bank_amount')
                bank_number = request.POST.get('bank_number')
                Pay_bank_amount_purchase(e.shope.id,farmer_id,date,amount,bank_number)
                return redirect('pay_purchase_bill', farmer_id=farmer_id)
            if 'add_opning_amount'in request.POST:
                t = request.POST.get('type')
                amount = request.POST.get('amount')
                if Farmer_purchase_opning_balance.objects.filter(farmer_id=farmer_id).exists():
                    pass
                else:
                    Farmer_purchase_opning_balance(
                        farmer_id = farmer_id,
                        shope_id = e.shope_id,
                        balance = amount,
                        type = t,
                    ).save()
                return redirect('pay_purchase_bill', farmer_id=farmer_id)   
            if 'edit_opning_balance'in request.POST:
                t = request.POST.get('type')
                amount = request.POST.get('amount')
                
                if Farmer_purchase_opning_balance.objects.filter(farmer_id=farmer_id).exists():
                    of = Farmer_purchase_opning_balance.objects.filter(farmer_id=farmer_id).first()
                    nf = Farmer_purchase_opning_balance.objects.filter(farmer_id=farmer_id).first()
                    nf.balance = amount
                    nf.type = t
                    nf.save()    
                    
                if int(t) == 1:
                    ba = int(math.floor(float(of.balance))) - int(math.floor(float(nf.balance)))
                    bill = Purchase_order_master.objects.filter(farmer_id=farmer_id, paid_status=1).order_by('id')
                    for b in bill:
                        if ba <= b.total:
                            b.paid_status = 0
                            b.save()
                            ba -= b.total
                        else:
                            break
                else:
                    ba = int(math.floor(float(of.balance))) - int(math.floor(float(nf.balance)))
                    bill = Purchase_order_master.objects.filter(farmer_id=farmer_id, paid_status=1).order_by('id')
                    for b in bill:
                        if ba <= b.total:
                            b.paid_status = 0
                            b.save()
                            ba -= b.total
                        else:
                            break
                        
                            
                    

                return redirect('pay_purchase_bill', farmer_id=farmer_id)   
            pending_amount = Purchase_order_master.objects.filter(farmer_id=farmer_id).aggregate(Sum('total'))['total__sum']
            if pending_amount == None:
                pending_amount = 0
            paid_total_amount = Farmer_purchase_payment_transaction.objects.filter(farmer_id=farmer_id).aggregate(Sum('amount'))['amount__sum']
            if paid_total_amount == None:
                paid_total_amount = 0
                
        last_year = datetime.now().year
        last_year -= 1
        b_opn = Farmer_purchase_opning_balance.objects.filter(farmer_id=farmer_id).first()
        final_amount = (int(pending_amount) -  int(paid_total_amount))
        check_paid_total_amount = Farmer_purchase_payment_transaction.objects.filter(farmer_id=farmer_id).aggregate(Sum('amount'))['amount__sum']
        if b_opn:
            if b_opn.type == 0:
                final_amount += int(b_opn.balance)
                check_paid_total_amount = int(paid_total_amount) - int(b_opn.balance)
            else:
                final_amount -= int(b_opn.balance)
                check_paid_total_amount =int(paid_total_amount) + int(b_opn.balance)
        context = {
            'employee': e,
            'farmer':Farmer.objects.filter(id=farmer_id).first(),
            'transaction':Farmer_purchase_payment_transaction.objects.filter(farmer_id=farmer_id).order_by('-date'),
            'paid_total_amount':paid_total_amount,
            'bill':Purchase_order_master.objects.filter(farmer_id=farmer_id),
            'remening_amount':remening_amount,
            'final_amount':final_amount,
            'bill_total_amount':pending_amount,
            'last_year':last_year,
            'farmer_purchase_opning_balance':Farmer_purchase_opning_balance.objects.filter(farmer_id=farmer_id).first(),
            'check_paid_total_amount':check_paid_total_amount
        }
        return render(request, 'office/pay_purchase_bill.html', context)
    else:
        return redirect('/')
    
    
def Pay_bank_amount_purchase(shop_id, farm_id, date, amount, number):
    Farmer_purchase_payment_transaction(
        shope_id=shop_id,
        farmer_id=farm_id,
        date=date,
        amount=amount,
        payment_type='Bank',
        bank_number=number,
    ).save()
    
def Pay_phone_pe_amount_purchase(shope_id, farmer_id, date, amount, number):
    Farmer_purchase_payment_transaction(
        shope_id=shope_id,
        farmer_id=farmer_id,
        date=date,
        amount=amount,
        payment_type='PhonePe',
        phonepe_number=number,
    ).save()
    
def change_purchase_farmer_bill_paid_status(farmer_id):
    b_opn = Farmer_purchase_opning_balance.objects.filter(farmer_id=farmer_id).first()
    recived_payment = Farmer_purchase_payment_transaction.objects.filter(farmer_id=farmer_id).aggregate(Sum('amount'))['amount__sum']
    if b_opn:
        if b_opn.type == 0:
            recived_payment -= int(b_opn.balance)
        else:
            recived_payment += int(b_opn.balance)
            
    if recived_payment == None:
        recived_payment = 0
    paid_bill_amount = Purchase_order_master.objects.filter(farmer_id=farmer_id, paid_status = 1).aggregate(Sum('total'))['total__sum']
    if paid_bill_amount == None:
        paid_bill_amount = 0
    remening_amount = (int(recived_payment) - int(paid_bill_amount))
    bill = Purchase_order_master.objects.filter(farmer_id=farmer_id, paid_status=0).order_by('-id')
    bill_id = 0
    for b in bill:
        if remening_amount >= b.total:
            b.paid_status = 1
            b.save()
            remening_amount -= b.total
        else:
            bill_id = b.id
            if int(remening_amount) != 0:
                remening_amount = int(b.total) - int(remening_amount)
            break
    bt = Purchase_order_master.objects.filter(farmer_id=farmer_id, paid_status=0).aggregate(Sum('total'))['total__sum']
    if bt == None:
        bt = 0
    if int(remening_amount) >= int(bt): 
        remening_amount = 0
    return {'bill_id':bill_id, 'remening_amount':remening_amount}

def Pay_cash_amount_purchase(shope_id, farmer_id, date, amount):
    Farmer_purchase_payment_transaction(
        shope_id=shope_id,
        farmer_id=farmer_id,
        date=date,
        amount=amount,
        payment_type='cash',
    ).save()
    
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
                print('id', id)
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
                            item_name = c.item.english_name,
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
                            item_name = c.item.english_name,
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
