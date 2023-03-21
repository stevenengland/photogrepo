from django.urls import path

from app.main.views import index

app_name = 'main'

urlpatterns = [
    path('hello/', index, name='hello'),
]
