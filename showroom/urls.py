from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add-car/', views.add_car, name='add_car'),
     path("edit-car/<int:id>/", views.edit_car, name="edit_car"),
]