from django.shortcuts import render#, redirect
from django.http import HttpRequest, JsonResponse
import json
from django.views.decorators.csrf import csrf_protect
#from django_ratelimit.decorators import ratelimit
from .utils.functions import generate_response
from .models import TextDataset,VectorDataset

# Create your views here.


def home(request: HttpRequest) -> HttpRequest:
    return render(request, 'home.html',)


@csrf_protect
def get_response(request: HttpRequest) -> HttpRequest:
    if request.method == "POST":
        data = json.loads(request.body)
        message = data['message']
        response_data = generate_response(message=message)
        return JsonResponse(response_data)
    else:
        return JsonResponse({"error": "Method Not Allowed"}, status=405)
    

def dataset(request: HttpRequest) -> HttpRequest:
    if request.method == "GET":
        dataset_objects = TextDataset.objects.all()
        return render(request,"dataset.html",{"dataset_objects":dataset_objects})
    else:
        return JsonResponse({"error": "Method Not Allowed"}, status=405)


def vectordataset(request: HttpRequest) -> HttpRequest:
    if request.method == "GET":
        vectordataset_objects = VectorDataset.objects.all()
        return render(request,"vectordataset.html",{"vectordataset_objects":vectordataset_objects})
    else:
        return JsonResponse({"error": "Method Not Allowed"}, status=405)