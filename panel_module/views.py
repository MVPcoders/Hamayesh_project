from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.


def management(request):


    context = {

    }
    return render(request, 'panel_module/management.html',context)
