from django.contrib import admin

# Register your models here.
from django.contrib import admin

from hryar.models import Company, Person


class PersonAdmin(admin.ModelAdmin):
    pass


class CompanyAdmin(admin.ModelAdmin):
    pass


admin.register(Company, CompanyAdmin)
admin.register(Person, PersonAdmin)
