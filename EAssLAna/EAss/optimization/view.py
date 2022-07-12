from django.http.response import HttpResponse

from django.shortcuts import render

from .. import models


def coloring(request):
    cat = request.GET.get('t', '')

    if request.method == 'POST':
        return HttpResponse("Test")
    else:
        return render(request, 'mapcoloring.html', {
            "karnaugh": {
                "0": {
                    "0": True,
                    "1": False,
                    "2": False,
                    "3": True,
                },
                "1": {
                    "0": True,
                    "1": False,
                    "2": False,
                    "3": True,
                },
                "2": {
                    "0": True,
                    "1": False,
                    "2": False,
                    "3": True,
                },
                "3": {
                    "0": True,
                    "1": False,
                    "2": False,
                    "3": True,
                },
            }
        })

def optimization(request):
    cat = request.GET.get('t', '')

    if request.method == 'POST':
        return HttpResponse("Test")
    else:
        return render(request, 'mapcreation.html', {
            "problem": {
                "function": [{
                    "0": True,
                    "1": False,
                    "2": False,
                    "3": True,
                }],
                "name": "f",
                "variables": {
                    "0": "x1",
                    "1": "x2",
                    "2": "x3",
                    "3": "x4",
                }
            }
        })
