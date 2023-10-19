from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UploadFileForm
# from .views import handle_uploaded_file

def hello(request):
    return HttpResponse("Hello World!")

def upload_file(request):
    if request.method == "POST":
        upload_file_form = UploadFileForm(request.POST, request.FILES)
        if upload_file_form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect("/success/url")
        else:
            return HttpResponse("表单内容有误")
    
    else:
        upload_file_form = UploadFileForm()
        return render(request, "upload.html", {"form": upload_file_form})

def handle_uploaded_file(f):
    with open("", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)