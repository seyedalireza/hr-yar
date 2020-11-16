from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group, User
from django.http import HttpResponseForbidden, HttpResponseNotFound, HttpResponse
from django.shortcuts import render, redirect
from django.template import loader

from djangoProject.settings import USER_GROUP, COMPANY_GROUP
from hryar.models import CompanyModelForm, PersonModelForm, PositionForm, Company, Position, Person, Applyment


def company_signup(request):
    url = "/company/signup/"
    title = 'Signup (Company)'
    hl_text = "already have an account? login"
    hl_link = "http://localhost:8000/login"
    if request.method == 'GET':
        form = CompanyModelForm()
        return render(request, 'common_form_template.html', {'form': form, 'url': url, 'title': title,
                                                             'hl_link': hl_link, 'hl_text': hl_text})
    else:
        form = CompanyModelForm(request.POST)
        if form.is_valid():
            company_group, _ = Group.objects.get_or_create(name=COMPANY_GROUP)
            company_group.save()
            username = form.data["username"]
            password = form.data["password"]
            email = form.data["email"]
            user = User(username=username, email=email)
            user.set_password(password)
            user.save()
            user.groups.add(company_group)
            user.save()
            company = form.save(commit=False)
            company.user = user
            company.save()
            return render(request, 'login.html')
        else:
            return render(request, 'common_form_template.html', {'form': form, 'url': url, 'title': title,
                                                                 'hl_link': hl_link, 'hl_text': hl_text})


def person_signup(request):
    url = "/user/signup/"
    title = "Signup (User)"
    hl_text = "already have an account? login"
    hl_link = "http://localhost:8000/login"
    if request.method == 'GET':
        form = PersonModelForm()
        return render(request, 'common_form_template.html', {'form': form, 'url': url, 'title': title,
                                                             'hl_text': hl_text, 'hl_link': hl_link})
    else:
        form = PersonModelForm(request.POST)
        if form.is_valid():
            user_group, _ = Group.objects.get_or_create(name=USER_GROUP)
            user_group.save()
            username = form.data["username"]
            password = form.data["password"]
            email = form.data["email"]
            user = User(username=username, email=email)
            user.set_password(password)
            user.save()
            user.groups.add(user_group)
            user.save()
            person = form.save(commit=False)
            person.user = user
            person.save()
            return render(request, 'login.html')
        else:
            return render(request, 'common_form_template.html', {'form': form, 'url': url,
                                                                 'hl_link': hl_link, 'hl_text': hl_text})

def home(request):
    return render(request, 'home.html')

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


def create_position(request):
    # url = "/company/position/"
    if request.method == 'GET':
        positons = Position.objects.all()
        companies = Company.objects.all()
        return render(request, 'hryar/CreatePosition.html', {"positions": positons, "companies": companies})
    elif request.method == 'POST':
        if request.user.is_authenticated and request.user.groups.filter(name=COMPANY_GROUP).exists():
            position_form = PositionForm(request.POST)
            position = position_form.save(commit=False)
            position.company = Company.objects.get(user__username=request.user.username)
            position.save()
            return render(request, 'hryar/ListPositions.html')
        else:
            return HttpResponseForbidden()
    else:
        return HttpResponseNotFound()


def ListPositions(request):
    if request.method == 'GET':
        positons = Position.objects.order_by('create_date')
        print(positons)
        return render(request, 'hryar/ListPositions.html', {"positions": positons})


def Detail(request, position_id):
    # TODO if user was company show requests
    user_group = ''
    position = Position.objects.get(id=position_id)
    return render(request, 'hryar/PositionDetail.html', {"position": position, "user_group": user_group})


# TODO: in home page if user was company show his open positions

def apply(request, position_id):
    if request.user.is_authenticated and request.user.groups.filter(name=USER_GROUP).exists():
        try:
            position = Position.objects.get(id=position_id)
            person = Person.objects.get(user__username=request.user.username)
            req = Applyment(status="i", applicant=person, position=position)
            req.save()
            return HttpResponse("request sent successfully.")
        except:
            return HttpResponseNotFound("Job not found.")
    else:
        return HttpResponseForbidden()
