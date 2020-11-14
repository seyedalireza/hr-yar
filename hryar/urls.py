from django.urls import path

from . import views

urlpatterns = [
    path('ListPositions/', views.ListPositions.as_view(), name='ListPositions'),
    path('<int:position_id>/', views.Detail, name='Detail'),
    path('CreatePosition/', views.CreatePosition, name='CreatePosition')
]
