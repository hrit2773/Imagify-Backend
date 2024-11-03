from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

def ping(_):
    return JsonResponse({"status": "OK"})

def home_view(request):
    return render(request, "home.html")