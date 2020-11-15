from django.urls import path

from . import views

urlpatterns = [
    path('company/positions/ListPositions/', views.ListPositions, name='ListPositions'),
    path('company/positions/<int:position_id>/', views.Detail, name='Detail'),
    path('company/positions/CreatePosition/', views.create_position, name='CreatePosition')
]
