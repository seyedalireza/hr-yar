from django.contrib.auth import authenticate, login
from django.shortcuts import render

from hryar.models import CompanyModelForm, PersonModelForm


def company_signup(request):
    url = "/company/signup/"
    if request.method == 'GET':
        form = CompanyModelForm()
        return render(request, 'common_form_template.html', {'form': form, 'url': url})
    else:
        form = CompanyModelForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'login.html')
        else:
            return render(request, 'common_form_template.html', {'form': form, 'url': url})


def person_signup(request):
    url = "/user/signup/"
    if request.method == 'GET':
        form = PersonModelForm()
        return render(request, 'common_form_template.html', {'form': form, 'url': url})
    else:
        form = PersonModelForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'login.html')
        else:
            return render(request, 'common_form_template.html', {'form': form, 'url': url})


def login_api(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request=request, user=user)
            return render(request, 'home.html') # TODO redirect to home
        return render(request, 'login.html')


def apply_job(request):
    return render(request, 'apply_job.html')