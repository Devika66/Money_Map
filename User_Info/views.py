from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from django.contrib.auth import authenticate ,logout
from django.contrib.auth import login as dj_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseServerError
from .models import Expenses,UserProfile
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import JsonResponse
import datetime






# Create your views here.
def home(request):
    if request.user.is_authenticated:
        return redirect('index')
    return render(request,'login.html')
   # return HttpResponse('This is home')

@login_required(login_url='/handleLogin')   
def index(request):
    user=request.user
    addmoney_category = Expenses.objects.filter(user=user).order_by('-Date')
    paginator = Paginator(addmoney_category , 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
            
           'page_obj' : page_obj
        }
    
    return render(request,'index.html',context)
    
    
def register(request):
    return render(request,'register.html')
    



@login_required(login_url='/handleLogin')
def search(request):
    user=request.user
    fromdate = request.GET['fromdate']
    todate = request.GET['todate']
    addmoney = Expenses.objects.filter(user=user, Date__range=[fromdate,todate]).order_by('-Date')

    return render(request,'tables.html',{'addmoney':addmoney})
                                                  

def tables(request):
        user=request.user
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')
        addmoney = Expenses.objects.filter(user=user).order_by('-Date')

        return render(request,'tables.html',{'addmoney':addmoney})
    
def addmoney(request):
    return render(request,'addmoney.html')


def profile(request):
    return render(request,'profile.html')

@login_required(login_url='/handleLogin')
def profile_edit(request,id):
     user=User.objects.get(id=id)
     return render(request,'profile_edit.html',{'add':user})
    
@login_required(login_url='/handleLogin')
def profile_update(request,id):
    if request.method == "POST":
            user = User.objects.get(id=id)
            user.first_name = request.POST["fname"]
            user.last_name = request.POST["lname"]
            user.email = request.POST["email"]
            user.userprofile.Savings = request.POST["Savings"]
            user.userprofile.income = request.POST["income"]
            user.userprofile.save()
            user.save()
            return redirect('/index')
    
       

def handleSignup(request):
    if request.method =='POST':
            # get the post parameters
            uname = request.POST["uname"]
            fname=request.POST["fname"]
            lname=request.POST["lname"]
            email = request.POST["email"]
            Savings = request.POST['Savings']
            income = request.POST['income']
            pass1 = request.POST["pass1"]
            pass2 = request.POST["pass2"]

            if User.objects.filter(username=uname).exists():
                messages.error(request, "Username already taken,Try something else!")
                return redirect('/register')
            if len(uname)>15:
                messages.error(request, "Username must be max 15 characters")
                return redirect("/register")
            if not uname.isalnum():
                messages.error(request, "Username should only contain letters and numbers")
                return redirect("/register")
            if pass1 != pass2:
                messages.error(request, "Passwords do not match,Try again!")
                return redirect("/register")
            
            user = User.objects.create_user(uname, email, pass1)
            user.first_name = fname
            user.last_name = lname
            user.save()

            profile = UserProfile(user=user, Savings=Savings, income=income)
            profile.save()

            messages.success(request, "Account created successfully")
            return redirect("/")
    return HttpResponse('404 - NOT FOUND')
    
  
def handleLogin(request):
    if request.method =='POST':
        # get the post parameters
        loginuname = request.POST["loginuname"]
        loginpassword1=request.POST["loginpassword1"]

        print("Username:", loginuname)
        print("Password:", loginpassword1)
        
        user = authenticate(username=loginuname, password=loginpassword1)
        print("Authenticated User",user)

        
        if user is not None:
            dj_login(request, user)
            messages.success(request, " Successfully logged in")
            return redirect('/index')
        else:
            messages.error(request," Invalid Credentials, Please try again")  
            return redirect("/")  
    return render(request,'login.html')

@login_required(login_url='/handleLogin')
def handleLogout(request):
         logout(request)
         return redirect('/handleLogin')
    

#add money form
@login_required(login_url='/handleLogin')
def addmoney_submission(request):
    if request.method == "POST":
        try:
            user = request.user
            addmoney_category = request.POST["add_money"]
            expense_category = request.POST.get("expense_category") if addmoney_category=="Expense" else None
            amount = request.POST["amount"]
            Date = request.POST["Date"]

            add = Expenses(
                user=user,
                addmoney_category=addmoney_category,
                expense_category=expense_category,
                amount=amount,
                Date=Date
            )
            add.save()

            return redirect('/index')
        except Exception as e:
            return HttpResponseServerError(f"Error: {e}")
    return redirect('/index')

            
    

@login_required(login_url='/handleLogin')
def addmoney_update(request,id):
    if request.method == "POST":
            user=request.user
            add  = Expenses.objects.get(id=id)
            add.addmoney_category = request.POST["addmoney_category"]
            add .expense_category=request.POST.get("expense_category") if add.addmoney_category=="Expense" else None
            add.amount = request.POST["amount"]
            add.Date = request.POST["Date"]
            add .save()
            return redirect("/index")
    return redirect("/home")
        

def expense_edit(request,id):
    addmoney = Expenses.objects.get(id=id)
    user=request.user
    return render(request,'expense_edit.html',{'addmoney':addmoney})
    

def expense_delete(request,id):
    addmoney = Expenses.objects.get(id=id)
    user=request.user
    addmoney.delete()
    return redirect('/index')
    
@login_required(login_url='/handleLogin')
def expense_month(request):
    todays_date = datetime.date.today()
    one_month_ago = todays_date-datetime.timedelta(days=30)
    user=request.user
    addmoney= Expenses.objects.filter(user = user,addmoney_category="Expense",Date__range=(one_month_ago,todays_date))

    finalrep ={}
    for category in addmoney.values_list('expense_category', flat=True).distinct():
        total = addmoney.filter(expense_category=category).aggregate(total=Sum('amount'))['total'] or 0
        finalrep[category] = total
    return JsonResponse({'expense_category_data': finalrep}, safe=False)

    
@login_required(login_url='/handleLogin')
def stats(request):
    todays_date = datetime.date.today()
    one_month_ago = todays_date-datetime.timedelta(days=30)
    user=request.user
    addmoney_info= Expenses.objects.filter(user=user,Date__range=(one_month_ago,todays_date))

    total_expense = addmoney_info.filter(addmoney_category='Expense').aggregate(Sum('amount'))['amount__sum'] or 0
    total_income =addmoney_info.filter(addmoney_category='Income').aggregate(Sum('amount'))['amount__sum'] or 0
    remaining =  user.userprofile.Savings + total_income - total_expense

    if remaining < 0:
        messages.warning(request, 'Your expenses exceeded your savings')
    
    context = {
        'addmoney': addmoney_info,
        'expense': total_expense,
        'budget': total_income,
        'remaining': abs(remaining),
        'overspent': abs(min(0, remaining))
    }
    return render(request, 'stats.html', context)


   
@login_required(login_url='/handleLogin')        
def expense_week(request):
    todays_date = datetime.date.today()
    one_week_ago = todays_date-datetime.timedelta(days=7)
    user=request.user
    addmoney = Expenses.objects.filter(user = user,addmoney_category="Expense",Date__range=(one_week_ago,todays_date))
    
    finalrep ={}
    for category in addmoney.values_list('expense_category', flat=True).distinct():
        total = addmoney.filter(expense_category=category).aggregate(total=Sum('amount'))['total'] or 0
        finalrep[category] = total
    return JsonResponse({'expense_category_data': finalrep}, safe=False)

@login_required(login_url='/handleLogin')       
def weekly(request):
        todays_date = datetime.date.today()
        one_week_ago = todays_date - datetime.timedelta(days=7)
        user=request.user
        addmoney_info= Expenses.objects.filter(user=user, Date__range=(one_week_ago, todays_date))

        total_expense = addmoney_info.filter(addmoney_category='Expense').aggregate(total=Sum('amount'))['total'] or 0
        total_income = addmoney_info.filter(addmoney_category='Income').aggregate(total=Sum('amount'))['total'] or 0
        remaining =  user.userprofile.Savings+ total_income - total_expense

        if remaining < 0:
             messages.warning(request,'Your expenses exceeded your savings')
             


        context = {
        'addmoney_info': addmoney_info,
        'expense': total_expense,
        'budget': total_income,
        'remaining': abs(remaining),
        'overspent': abs(min(0, remaining))
        }
        return render(request, 'weekly.html', context)


def check(request):
    if request.method == 'POST':
        if not User.objects.filter(email=request.POST['email']).exists():
            messages.error(request, "Email not registered")
            return redirect("/reset_password")
        
        messages.success(request, "Email found. Follow instructions sent to email.")
        return redirect("/reset_password")

        






