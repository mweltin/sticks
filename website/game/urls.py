from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('turn', views.turn, name='turn'),
    path('swap', views.swap, name='swap'),
]
