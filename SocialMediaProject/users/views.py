from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import UserRegistrationForm,UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.contrib.auth.models import User

def register(request):
    if request.method=="POST":
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            user=User.objects.get(username=form.cleaned_data.get('username'))
            Profile.objects.create(user=user)
            username=form.cleaned_data.get("username")
            messages.success(request,f'Account is created for {username}!')
            return redirect('login')
        else:
            username=form.cleaned_data.get("username")
            messages.warning(request,f'Account is not created for {username}!')
            return redirect('register')
    else:
        form=UserRegistrationForm()
        return render(request,'users/register.html',{'form':form,'title':'Register'})

@login_required
def profile(request):
    if request.method=="POST":
        u_form=UserUpdateForm(request.POST,instance=request.user)
        p_form=ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile,)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form=UserUpdateForm(instance=request.user)
        p_form=ProfileUpdateForm(instance=request.user.profile)
        context={'u_form':u_form,'p_form':p_form}
    return render(request,'users/profile.html',context)
