from django.contrib import admin
from .models import Company, Person, Position, Applyment

admin.site.register(Company)
admin.site.register(Person)
admin.site.register(Position)
admin.site.register(Applyment)

# Register your models here.
