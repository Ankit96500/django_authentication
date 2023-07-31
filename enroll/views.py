from django.shortcuts import render,HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout,update_session_auth_hash
from enroll.forms import signupform,usereditprofileform,admineditprofileform
from django.contrib.auth.forms import AuthenticationForm,PasswordChangeForm,SetPasswordForm,UserChangeForm
from django.contrib.auth.models import User


# Create your vixews here.
# make sure U AND C in capital letters in UserCreationForm.... AND MUST USE THESE COMMAND BEFORE START SERVER.. ( MAKEMIGRATIONS..MIGRATE )

# home page..
def home(request):
    return render(request,'enroll/home.html')


# SIGNUP FUNCTION
def sign_up(request):
    if request.method=='POST':
        fm=signupform(request.POST)
        if fm.is_valid():
            unm = fm.cleaned_data['username']
            em = fm.cleaned_data['email']
            fm.save()
            messages.success(request,'YOU SIGNEDUP SUCCESSFULLY !!!')
    else:
        fm=signupform()    
    return render(request,'enroll/signup.html',{'form':fm})

# LOGIN FUNCTION
def log_in(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/profile/')
    if request.method == 'POST':
        fm=AuthenticationForm(request=request,data=request.POST)
        if fm.is_valid():
            uname=fm.cleaned_data['username']
            upass=fm.cleaned_data['password']
            user=authenticate(username=uname,password=upass)
            if user is not None:
                login(request, user)
                # here the message is work when w logged out why!, bcos we redirect this page in {profile.html},jaha par message hamee define nahi kiya hai
                messages.info(request,'you login successfully!!!')        
                return HttpResponseRedirect('/profile/')
    else:
        # this is for get request
        fm=AuthenticationForm()
    return render(request,'enroll/login.html',{'form':fm})                
            

# profile function:
# if we want to show the all users in the [profile page] so we have to import [ from django.contrib.auth.models import users]

def user_profile(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    if request.method == 'POST':
        if request.user.is_superuser == True:
            fm=admineditprofileform(request.POST,instance=request.user)
            pi=User.objects.all()

        else:
            fm=usereditprofileform(request.POST,instance=request.user)
            pi=None
        if fm.is_valid():
            fm.save()
            messages.success(request,'-------------your profile has been updated---------')
            return HttpResponseRedirect('/profile/')        
    else:    
        if request.user.is_superuser == True:
            fm=admineditprofileform(instance=request.user)
            pi=User.objects.all()

        else:    
            fm=usereditprofileform(instance=request.user)
            pi=None 
        return render(request,'enroll/profile.html',{'name':request.user,'form':fm,'users':pi})    


# this function will show user panel in web page

def user_detail(request,id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')
    if request.method == 'POST':
        pi=User.objects.get(pk=id)
        fm=admineditprofileform(request.POST,instance=pi)

        if fm.is_valid():
            fm.save()
            messages.success(request,'------------data update ho gaya hai!!!')
    else:
        pi=User.objects.get(pk=id)        
        fm=admineditprofileform(instance=pi)
    return render(request,'enroll/userdetail.html',{'form':fm})    
    

# change password with old password:

def changepass(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    if request.method == 'POST':
        fm=PasswordChangeForm(user=request.user,data=request.POST)
        if fm.is_valid():
            fm.save()
            update_session_auth_hash(request,fm.user)
            messages.success(request,'your password has been changed!!')  
            return HttpResponseRedirect('/profile/')
    else:
        fm=PasswordChangeForm(user=request.user)
    return render(request,'enroll/changepassword.html',{'form':fm})

# change password with the password:

def changepass1(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login/')
    if request.method == 'POST':
        fm=SetPasswordForm(user=request.user,data=request.POST)
        if fm.is_valid():
            fm.save()
            update_session_auth_hash(request,fm.user)
            messages.success(request,'your password has been changed!!')
            return HttpResponseRedirect('/profile/')  
    else:
        fm=SetPasswordForm(user=request.user)
    return render(request,'enroll/changepassword.html',{'form':fm})



# logout function:

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/login/')
