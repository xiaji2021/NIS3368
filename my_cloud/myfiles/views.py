from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import FileUploadForm
from .models import FileUpload

def hello(request):
    return HttpResponse("Hello World!")

def upload_file(request):
    
    if request.method == "POST":
        file_upload_form = FileUploadForm(request.POST, request.FILES)
    
        # if file_upload_form.is_valid():
        file_upload_form.save()
            # new_file = file_upload_form.save(commit=False)

            # new_file.save()
    
            # myfile = FileUpload(title=title, content=content, file=file)
            # myfile.save()

        return HttpResponseRedirect("myfiles:file_list")
        
        # else:
            # title = request.POST.get('title')
            # content = request.POST.get('content')
            # file = request.FILES.get('file')

            # if file:
            #     return HttpResponse("file check")
            # elif content:
            #     return HttpResponse("content check")
            # elif title:
            #     return HttpResponse("title check")
            # else:

            # return HttpResponse("表单内容有误, 请重新填写")
            # return render(request, "myfiles/upload.html", {'file_upload_form': file_upload_form})
    
    elif request.method == "GET":
        file_upload_form = FileUploadForm()
        context = { 'file_upload_form': file_upload_form }
        return render(request, "myfiles/upload.html", context)
    
    else:
        return HttpResponse("非GET, POST请求")

def handle_uploaded_file(f):
    with open("", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def file_list(request):
    files = FileUpload.objects.all()
    context = { 'files': files }    # 字典
    return render(request, 'myfiles/list.html', context)

def file_detail(request, id):
    file = FileUpload.objects.get(id=id)

    context = { 'file': file }
    return render(request, 'myfiles/detail.html', context)