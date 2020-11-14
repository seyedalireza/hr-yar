from django.contrib.auth.models import User
from django.db import models

# This file contains all models used in this project.
from django.forms import ModelForm

company_size_groups = [
    ("xss", "1-9"), ("xs", "10-99"), ("s", "100-499"),
    ("n", "500-1000"), ("l", "1000-1999"), ("xl", "2000-10000")
]

applyment_status = [
    ("r", "rejected"), ("i", "in progress "), ("h", "hired")
]


class Company(User):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=11)
    website = models.CharField(max_length=100)
    description = models.TextField()
    size = models.CharField(choices=company_size_groups, max_length=20)


class Person(User):
    description = models.TextField()
    resume = models.BinaryField()  # handle pdf files. or use a storage for it.
    phone_number = models.CharField(max_length=11)
    expected_salary = models.CharField(max_length=128)


class Position(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    salary = models.CharField(max_length=128)
    job_description = models.TextField()
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    requirements = models.TextField()
    rewards = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)


class Applyment(models.Model):
    id = models.BigAutoField(primary_key=True)
    status = models.CharField(choices=applyment_status, max_length=20)
    position = models.ForeignKey(Position, on_delete=models.DO_NOTHING)
    applicant = models.ForeignKey(Person, on_delete=models.DO_NOTHING)
    apply_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)


class CompanyModelForm(ModelForm):
    class Meta:
        model = Company
        fields = '__all__'
        exclude = ['is_staff', 'is_active', 'date_joined', 'last_login', 'is_superuser', 'groups', 'user_permissions']


class PersonModelForm(ModelForm):
    class Meta:
        model = Person
        fields = '__all__'
        exclude = ['is_staff', 'is_active', 'date_joined', 'last_login', 'is_superuser', 'groups', 'user_permissions']
