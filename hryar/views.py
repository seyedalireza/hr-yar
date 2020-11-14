from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader

from hryar.models import Position, Company
from django.views import generic


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
            archived = True if request.POST.get("archived", 'off') == 'on' else False
            print(archived)
            position = Position(name=name, salary=salary, job_description=job_description,
                                company=Company.objects.get(name=company), requirements=requirements, rewards=rewards, archived=archived)
            position.save()
            return redirect("/")

    return render(request, "hryar/CreatePosition.html", {"positions": positons, "companies": companies})
