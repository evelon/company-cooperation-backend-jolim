from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from accounts.forms import RegisterForm


def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('common:home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/signup.html', {'form': form})
