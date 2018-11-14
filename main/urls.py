from django.urls import path, include

from main.views import main_page

urlpatterns = [
  path('', main_page)
]
