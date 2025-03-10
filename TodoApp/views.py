from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Todo
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

@login_required(login_url='Login')
def Home(request):
   if request.user.is_authenticated:
      user  = request.user
      TodoList = Todo.objects.filter(user=user,IsDelete=False).all()
      context = {'TodoList':TodoList}
      return render(request,"Todo/Home.html",context)
   else:
        return  redirect('Login')

@login_required(login_url='Login')
def AddTask(request):
   user = request.user
   TID  = request.GET.get('TID')
   Todoobj = None
   if TID is not None and TID != '':
      try:
         obj  = Todo.objects.filter(user=user,id=TID)
         if obj.exists():
            Todoobj  = obj.first()
      except:
         print("Not Found")      




   if request.method == "POST":
      Title =  request.POST.get('Title')
      Description  =  request.POST.get('Description')
      CompletionDate = request.POST.get('CompletionDate')
      Status = request.POST.get('completionStatus')
   
      completionStatus = False
      if Status == 'on':
         completionStatus = True

      if TID:
         Todoobj.Title = Title
         Todoobj.Description = Description
         Todoobj.CompletionDate = CompletionDate
         Todoobj.completionStatus = completionStatus
         Todoobj.save()
      else:
         Todoobj =  Todo.objects.create(
            user=user,
            Title = Title,Description = Description,CompletionDate = CompletionDate,
            completionStatus = completionStatus
         )
      return redirect('Home')   

   context = {'Todoobj':Todoobj}
   return render(request,"Todo/AddTask.html",context)


@login_required(login_url='Login')
def Delete(request):
   user = request.user
   TID  = request.GET.get('TID')
   Todoobj = None
   if TID is not None and TID != '':
      try:
         obj  = Todo.objects.filter(user=user,id=TID)
         if obj.exists():
            Todoobj  = obj.first()
            Todoobj.IsDelete=True
            Todoobj.save()
            return redirect('Home')
      except:
         print("Not Found") 

@login_required(login_url='Login')
def Logout(requset):
     logout(requset)
     return redirect('Login')



def Register(request):
   if request.method ==  "POST":
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
            else:
                user=User.objects.create_user(username=username,email=email,password = password)
                user.save()
             
                user= authenticate(
                    request,username=username ,password=password
                )
                login(request,user)
                return redirect('Home')
        else:
            messages.info(request,"Passwords Don't Match")
        

   return render(request,'Todo/Register.html')

def Login(request):
   
    if request.method == "POST":
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('Home')
        else:
            messages.info(request,'Invalid Creadentails')

           
    return render(request,'Todo/Login.html')