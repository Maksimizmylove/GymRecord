from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from autRecord.models import Contact,MembershipPlan,Trainer,Enrollment,Gallery,Attendance

# Create your views here.
def Home(request):
    return render(request,"index.html")

def gallery(request):
    posts=Gallery.objects.all()
    context={"posts":posts}
    return render(request,"gallery.html",context)

def attendance(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Пожалуйста, авторизуйтесь и попробуйте снова")
        return redirect('/login')
    SelectTrainer=Trainer.objects.all()
    context={"SelectTrainer":SelectTrainer}
    if request.method=="POST":
        phonenumber=request.POST.get('PhoneNumber')
        Login=request.POST.get('logintime')
        Logout=request.POST.get('loginout')
        SelectWorkout=request.POST.get('workout')
        TrainedBy=request.POST.get('trainer')
        query=Attendance(phonenumber=phonenumber,Login=Login,Logout=Logout,SelectWorkout=SelectWorkout,TrainedBy=TrainedBy)
        query.save()
        messages.warning(request,"Посещаемость добавлена!")
        return redirect('/attendance')
    return render(request,"attendance.html",context)

def profile(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Пожалуйста, авторизуйтесь и попробуйте снова")
        return redirect('/login')
    user_phone=request.user
    posts=Enrollment.objects.filter(PhoneNumber=user_phone)
    attendance=Attendance.objects.filter(phonenumber=user_phone)
    print(posts)
    context={"posts":posts,"attendance":attendance}
    return render(request,"profile.html",context)

def signup(request):
    if request.method=="POST":
        username=request.POST.get('usernumber')
        email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        pass2=request.POST.get('pass2')
      
        if len(username)<10:
            messages.info(request,"Номер телефона должен содержать 10 цифр")
            return redirect('/signup')

        if pass1!=pass2:
            messages.info(request,"Пароли не совпадают")
            return redirect('/signup')
       
        try:
            if User.objects.get(username=username):
                messages.warning(request,"Такой номер уже используется")
                return redirect('/signup')
           
        except Exception as identifier:
            pass
            
        try:
            if User.objects.get(email=email):
                messages.warning(request,"Такой Email уже используется")
                return redirect('/signup')
           
        except Exception as identifier:
            pass
              
        myuser=User.objects.create_user(username,email,pass1)
        myuser.save()
        messages.success(request,"Вы зарегестрированы, пожалуйста войдите")
        return redirect('/login')
             
    return render(request,"signup.html")

def handlelogin(request):
    if request.method=="POST":        
        username=request.POST.get('usernumber')
        pass1=request.POST.get('pass1')
        myuser=authenticate(username=username,password=pass1)
        if myuser is not None:
            login(request,myuser)
            messages.success(request,"Успешный вход")
            return redirect('/')
        else:
            messages.error(request,"Неверные данные")
            return redirect('/login')
            
    return render(request,"handlelogin.html")

def handleLogout(request):
    logout(request)
    messages.success(request,"Вы вышли из аккаунта")    
    return redirect('/login')

def contact(request):
    if request.method=="POST":
        name=request.POST.get('fullname')
        email=request.POST.get('email')
        number=request.POST.get('num')
        desc=request.POST.get('desc')
        myquery=Contact(name=name,email=email,phonenumber=number,description=desc)
        myquery.save()       
        messages.info(request,"Спасибо за обратную связь")
        return redirect('/contact')
        
    return render(request,"contact.html")

def enroll(request):
    if not request.user.is_authenticated:
        messages.warning(request,"Пожалуйста, авторизуйтесь и попробуйте снова")
        return redirect('/login')

    Membership=MembershipPlan.objects.all()
    SelectTrainer=Trainer.objects.all()
    context={"Membership":Membership,"SelectTrainer":SelectTrainer}
    if request.method=="POST":
        FullName=request.POST.get('FullName')
        email=request.POST.get('email')
        gender=request.POST.get('gender')
        PhoneNumber=request.POST.get('PhoneNumber')
        DOB=request.POST.get('DOB')
        member=request.POST.get('member')
        trainer=request.POST.get('trainer')
        query=Enrollment(FullName=FullName,Email=email,Gender=gender,PhoneNumber=PhoneNumber,DOB=DOB,SelectMembershipplan=member,SelectTrainer=trainer)
        query.save()
        messages.success(request,"Вы успешно присоеденились к нам")
        return redirect('/join')



    return render(request,"enroll.html",context)