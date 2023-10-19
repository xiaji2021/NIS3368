from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UploadFileForm
# from .views import handle_uploaded_file
from .models import FileUpload

def hello(request):
    return HttpResponse("Hello World!")

def upload_file(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        file = request.FILES.get('file')

        myfile = FileUpload(title=title, content=content, file=file)
        myfile.save()
        # return HttpResponse("SUCCESS")
        return HttpResponseRedirect('myfiles:file_list')
    
    elif request.method == "GET":
        # upload_file_form = UploadFileForm()
        return render(request, "myfiles/upload.html")
    
    else:
        return HttpResponse("非GET, POST请求")

def handle_uploaded_file(f):
    with open("", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def file_list(request):
    files = FileUpload.objects.all()
    context = { 'myfiles': files }
    return render(request, 'myfiles/list.html', context)