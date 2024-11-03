from django.shortcuts import redirect, render
from sunil.models import *
from owner.models import *
# Create your views here.
def index(request):

    return render(request, 'home/index.html')

def login(request):
    if request.session.has_key('owner_mobile'):
        return redirect('owner_home')
    if request.session.has_key('office_mobile'):
        return redirect('office_home')
    else:
        if request.method == "POST":
            number=request.POST ['number']
            pin=request.POST ['pin']
            s= Shope.objects.filter(mobile=number,pin=pin,status=1)
            if s:
                request.session['owner_mobile'] = request.POST["number"]
                return redirect('owner_home')
            o= office_employee.objects.filter(mobile=number,pin=pin,status=1)
            if o:
                request.session['office_mobile'] = request.POST["number"]
                return redirect('office_home')
            else:
                return redirect('/login/')
    return render(request, 'home/login.html')


def owner_logout(request):
    del request.session['owner_mobile']
    return redirect('/')
    
def office_logout(request):
    del request.session['office_mobile']
    return redirect('/')