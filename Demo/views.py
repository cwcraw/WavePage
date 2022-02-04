from django.shortcuts import render
from django.http import HttpResponse
from Demo.library.waveFunctionController import WaveFunctionController as wfc


def home(request):
    return render(request, "index.html")


def aboutMe(request):
    return render(request, "aboutMe.html")


# add in 404 support
def waveFunction(request, potential):
    return wfc.view(request, potential)
