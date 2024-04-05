from django.shortcuts import render#, redirect
from django.http import HttpRequest, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django_ratelimit.decorators import ratelimit
from .utils.functions import generate_response
from .models import TextDataset,VectorDataset

# Create your views here.


@ratelimit(key="ip", rate="10/d", method="POST", block=True)
def home(request: HttpRequest) -> HttpRequest:
    if request.method == "POST":
        data = json.loads(request.body)
        #print("headers:",request.headers)
        message = data['message']
        response_data = generate_response(message=message)
        return JsonResponse(response_data)
    else:
        return render(request, 'home.html',)
    

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