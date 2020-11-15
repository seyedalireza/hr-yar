from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.http import HttpResponseForbidden, HttpResponseNotFound, HttpResponse
from django.shortcuts import render, redirect
# from samba.dcerpc.nbt import name
from django.template import loader
from django.views import generic

from djangoProject.settings import USER_GROUP, COMPANY_GROUP
from hryar.models import CompanyModelForm, PersonModelForm, PositionForm, Company, Position


def company_signup(request):
    url = "/company/signup/"
    if request.method == 'GET':
        form = CompanyModelForm()
        return render(request, 'common_form_template.html', {'form': form, 'url': url})
    else:
        form = CompanyModelForm(request.POST)
        if form.is_valid():
            company_group, _ = Group.objects.get_or_create(name=COMPANY_GROUP)
            company_group.save()
            user = form.save(commit=False)
            user.save()
            user.groups.add(company_group)
            user.save()
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
            user_group, _ = Group.objects.get_or_create(name=USER_GROUP)
            user_group.save()
            user = form.save(commit=False)
            user.save()
            user.groups.add(user_group)
            user.save()
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
            return render(request, 'home.html')  # TODO redirect to home
        return render(request, 'login.html')


def apply_job(request):
    return render(request, 'apply_job.html')


def create_position(request):
    # url = "/company/position/"
    if request.method == 'GET':
        position_form = PositionForm()
        return render(request, 'hryar/CreatePosition.html', {'form': position_form})
    elif request.method == 'POST':
        if request.user.is_authenticated and request.user.groups.filter(name=COMPANY_GROUP).exists():
            position_form = PositionForm(request.POST)
            position = position_form.save(commit=False)
            position.company = Company.objects.get(username=request.user.username)
            position.save()
            return redirect("/")
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseNotFound()


def ListPositions(request):
    latest_position_list = Position.objects.order_by('-create_date')
    template = loader.get_template('hryar/ListPositions.html')
    context = {
        'latest_position_list': latest_position_list,
    }
    return HttpResponse(template.render(context, request))


def Detail(request, position_id):
    return HttpResponse("You're looking at position %s." % position_id)
