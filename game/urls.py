from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    # Add other game URLs here as needed
]
