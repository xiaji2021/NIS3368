from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import FileUploadForm
from .models import FileUpload

def hello(request):
    return HttpResponse("Hello World!")

def upload_file(request):
    
    if request.method == "POST":
        file_upload_form = FileUploadForm(request.POST, request.FILES)
    
        if file_upload_form.is_valid():
            # handle_uploaded_file(request.FILES["file"])
    
            # myfile = FileUpload(title=title, content=content, file=file)
            # myfile.save()
            file_upload_form.save()

            return redirect("myfiles:file_list")
        
        else:
            return HttpResponse("表单内容有误, 请重新填写")
            # return render(request, "myfiles/upload.html", {'file_upload_form': file_upload_form})
    
    elif request.method == "GET":
        file_upload_form = FileUploadForm()
        context = { 'file_upload_form': file_upload_form }
        return render(request, "/myfiles/upload.html", context)
    
    else:
        return HttpResponse("非GET, POST请求")

def handle_uploaded_file(f):
    with open("media/%Y%m%d/", "wb+") as destination:
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

def file_delete(request, id):
    if request.method == "POST":
        file = FileUpload.objects.get(id=id)
        file.delete()
        return redirect("myfiles:file_list")
    else:
        return HttpResponse("仅允许post请求")
    
def file_update(request, id):
    file = FileUpload.objects.get(id=id)

    if request.method == "POST":

        file_post_form = FileUploadForm(request.POST, request.FILES)

        if file_post_form.is_valid():

            file.title = request.POST['title']
            file.content = request.POST['content']
            file.file = request.FILES['file']
            file.save()

            return redirect("myfiles:file_detail", id=id)
            # return redirect("file:file_list")

        else:
            return HttpResponse("表单内容有误，请重新填写。")
        
    else:
        file_post_form = FileUploadForm()
        context = {'file': file, 'file_post_form': file_post_form}

        return render(request, 'myfiles/update.html', context)