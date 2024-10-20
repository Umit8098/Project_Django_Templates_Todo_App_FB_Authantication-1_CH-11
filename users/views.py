from django.shortcuts import render, redirect
from django.contrib.auth.forms import (
    UserCreationForm, 
    AuthenticationForm,
)
from django.contrib.auth import authenticate, login

from .forms import (
    UserProfileForm, 
    UserForm,
)


## Normal register: default UserCreationForm() ile oluşturduğumuz view (username, password)
# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password1']
#             user = authenticate(username=username, password=password)
#             login(request, user)
#             return redirect('home')
#     else:
#         form = UserCreationForm()
#         return render(request, 'registration/register.html', {'form': form})


## Genişletilmiş User modeli ile register: UserCreationForm()'un genişletilerek email eklenmiş hali ile oluşturduğumuz view (username, email, password)
def register(request):
    form_user = UserForm()
    form_profile = UserProfileForm()
    if request.method == 'POST':
        form_user = UserForm(request.POST)
        form_profile = UserProfileForm(request.POST, request.FILES) # dosyaları almak için
        if form_user.is_valid() and form_profile.is_valid():
            user = form_user.save()
            profile = form_profile.save(commit=False)
            profile.user = user
            profile.save()
            
            login(request, user)
            
            return redirect('home')
    
    context = {
        'form_user': form_user,
        'form_profile': form_profile
    }
    return render(request, 'users/register.html', context)
        

def user_login(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('home')
    return render(request, 'users/login.html', {'form':form})