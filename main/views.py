import json

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.http import HttpResponse
from main.scripts.primbon import get_result


def main_page(request):
    return render(request, "main.html")


class GreetingView(View):
    greeting = "Good Day"

    def post(self, request):
        request_body = json.loads(request.body)
        return HttpResponse(json.dumps(get_result(request_body["duration"])))
