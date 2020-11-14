from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from hryar.models import Position, Company
from django.views import generic


def signup(request):
    return render(request, 'signup.html')


def login(request):
    return render(request, 'login.html')


def apply_job(request):
    return render(request, 'apply_job.html')


def Detail(request, position_id):
    return HttpResponse("You're looking at position %s." % position_id)


class ListPositions(generic.ListView):
    template_name = 'hryar/ListPositions.html'
    context_object_name = 'latest_position_list'

    def get_queryset(self):
        return Position.objects.order_by('create_date')


def CreatePosition(request):
    positons = Position.objects.all()
    companies = Company.objects.all()
    if request.method == "POST":
        if "jobAdd" in request.POST:
            print("requset:", request)
            name = request.POST["name"]
            salary = request.POST["salary"]
            job_description = request.POST["job_description"]
            company = request.POST["company"]
            requirements = request.POST["requirements"]
            rewards = request.POST["rewards"]
            archived = True if request.POST["archived"] == 'on' else False
            position = Position(name=name, salary=salary, job_description=job_description,
                                company=Company.objects.get(name=company), requirements=requirements, rewards=rewards,
                                archived=archived)
            position.save()
            return redirect("/")

    return render(request, "hryar/CreatePosition.html", {"positions": positons, "companies": companies})
