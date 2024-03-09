from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import SignUpForm
from .models import UserProfile
import uuid

# Create your views here.
# send mail
def send_mail_after_registration(email, token):
    subject = "Verify Email"
    message = f'Click on the link to verify your account http://127.0.0.1:8000/verify/{token}'
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])




def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            uid = uuid.uuid4()
            profile = UserProfile.objects.create(user=new_user, token=uid)
            send_mail_after_registration(new_user.email, uid)
            messages.success(request, 'Account created successfully. Check your email to verify.')
            return redirect('user/signup')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

# Account Verification
def verify(request,token):
    profile = UserProfile.objects.filter(token=token).first()
    # profile = get_object_or_404(UserProfile, token=token)
    profile.verify = True
    profile.save()
    messages.success(request,"Your account is verified please login in your account")
    return redirect('/login')




def login_view(request):
  if not request.user.is_authenticated:
    if request.method == "POST":
            form = AuthenticationForm(request=request, data = request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username = uname , password=password)
                if user is not None:
                    login(request,user)
                    return redirect ('home')
    else:
        form = AuthenticationForm()    
    return render(request,'login.html',{'form':form})
  else:
       return redirect('home')

def home(request):
    return render (request,'home.html')

# Logout
def signout(request):
    request.session.clear()
    return redirect(home)

# change Password
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)   
            messages.success(request, 'Your password was successfully updated!')
            return redirect(home)
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'changepass.html', {'form': form})



# change password 2
@login_required
def change_password2(request):
    if request.method == 'POST':
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)   
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = SetPasswordForm(request.user)
    return render(request, 'changepass2.html', {'form': form})














 
