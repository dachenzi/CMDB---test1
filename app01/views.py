from django.shortcuts import render,HttpResponse,redirect

# Create your views here.




def login(request):

    return render(request,'login.html')


def index(request):

    return render(request, 'nav.html')

def cmdbshow(request):

    return render(request,'cmdbshow.html')