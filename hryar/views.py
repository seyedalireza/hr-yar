from django.shortcuts import render


def signup(request):
    return render(request, 'signup.html')

def login(request):
    return render(request, 'login.html')

def apply_job(request):
    return render(request, 'apply_job.html')