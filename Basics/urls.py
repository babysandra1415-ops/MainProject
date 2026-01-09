
from django.urls import path,include
from . import views

urlpatterns = [

path('Sum/',views.Sum),
path('Calculator/',views.Calculator),
path('Largest/',views.Largest),
]