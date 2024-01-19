from django.urls import path

from .views import process_input

urlpatterns = [
    path('', process_input, name='process_input'),
]
