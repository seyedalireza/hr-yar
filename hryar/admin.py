from django.contrib import admin
from .models import Company, Person, Position, Applyment

admin.site.register(Company)
admin.site.register(Person)
admin.site.register(Position)
admin.site.register(Applyment)

# Register your models here.
from django.contrib import admin

from hryar.models import Company, Person, Position, Applyment


class PersonAdmin(admin.ModelAdmin):
    pass


class CompanyAdmin(admin.ModelAdmin):
    pass

class PositionAdmin(admin.ModelAdmin):
    pass


class ApplymentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Position, PositionAdmin)
admin.site.register(Applyment, ApplymentAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Person, PersonAdmin)
