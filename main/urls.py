from django.urls import path, include

from main.views import main_page, GreetingView

urlpatterns = [path("", main_page), path("get_result", GreetingView.as_view())]
