from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404, FileResponse
from .forms import FileUploadForm, FolderForm
from .models import FileUpload, Folder, Recycled
from django.db.models import Q  
import os
# from ..my_cloud.settings import settings
from datetime import datetime, timedelta
from pathlib import Path

def hello(request):
    return HttpResponse("Hello World!")

def upload_file(request, id=None):
    
    if request.method == "POST":
        file_upload_form = FileUploadForm(request.POST, request.FILES)
    
        if file_upload_form.is_valid():
            new_file = file_upload_form.save(commit=False)

            if id is not None:
                new_file.parent_folder = Folder.objects.get(pk=id)
                new_file.parent_id = id

                same_name_file = FileUpload.objects.filter(Q(title=new_file.title) & Q(parent_id = new_file.parent_id))
                if same_name_file:
                    error_message = "该文件已存在"
                    return render(request, "error/printError.html", {'error_message': error_message})


                if not new_file.parent_folder:
                        error_message = "指定的父文件夹不存在!"
                        return render(request, "error/printError.html", {'error_message': error_message})
                
                new_file.save()
                folder = Folder.objects.get(id=id)
                context = { 'folder':folder }
                return redirect("myfiles:folder_detail", id=id)
            
            else:
                same_name_file = FileUpload.objects.filter(Q(title=new_file.title) & Q(parent_folder = None)  & ~Q(parent_id = -1))
                if same_name_file:
                    error_message = "该文件title已存在"
                    return render(request, "error/printError.html", {'error_message': error_message})

                new_file.parent_id = 0
                new_file.parent_folder = None
                new_file.save()
                return redirect("myfiles:file_list")       
        
        else:
            error_message = "表单内容有误，请重新填写!"
            return render(request, "error/printError.html", {'error_message': error_message})
            # return HttpResponse("表单内容有误, 请重新填写")
            # return render(request, "myfiles/upload.html", {'file_upload_form': file_upload_form})
    
    elif request.method == "GET":
        file_upload_form = FileUploadForm()
        context = { 'file_upload_form': file_upload_form }
        return render(request, "myfiles/upload.html", context)
    
    else:
        error_message = "非GET, POST请求!"
        return render(request, "error/printError.html", {'error_message': error_message})
        # return HttpResponse("非GET, POST请求")

def handle_uploaded_file(f):
    with open("media/%Y%m%d/", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def file_list(request):
    files = FileUpload.objects.all()
    folders = Folder.objects.all()

    for file in files:
        file.file_extension = '.' + file.file.name.split('.')[-1]

    context = { 'folders': folders, 'files': files }    # 字典
    return render(request, 'myfiles/list.html', context)

def file_detail(request, id):
    file = FileUpload.objects.get(id=id)

    context = { 'file': file }

    file.file_extension = '.' + file.file.name.split('.')[-1]
    
    return render(request, 'myfiles/detail.html', context)

def file_delete_old(request, id):
    if request.method == "POST":
        file = FileUpload.objects.get(id=id)
        parent = file.parent_folder

        BASE_DIR = Path(__file__).resolve().parent.parent

        fname = os.path.join(BASE_DIR, 'media', str(file.file.name))
        # MEDIA_URL = '/media/'

        # fname = os.path.join(settings.MEDIA_ROOT, str(files)[6:])
        if os.path.isfile(fname):
            os.remove(fname)

        # for i in file:
        #     os.remove(dir+'{}'.format(i.name))
        file.delete()

        return redirect("myfiles:recycled_detail")
    else:
        error_message = "仅允许post请求!"
        return render(request, "error/printError.html", {'error_message': error_message})
        # return HttpResponse("仅允许post请求")

def file_delete(request, id):
    if request.method == "POST":
        file = FileUpload.objects.get(id=id)
        parent = file.parent_folder
        file.parent_id = -1
        # file.parent_folder = None
        
        current_time = datetime.now()
        file.delete_time = current_time + timedelta(days=30)

        file.save()

        if parent is not None:
            return redirect("myfiles:folder_detail", id=parent.id)
        else:
            return redirect("myfiles:file_list")
    else:
        error_message = "仅允许post请求!"
        return render(request, "error/printError.html", {'error_message': error_message})
        # return HttpResponse("仅允许post请求")

def file_recover(request, id): 
    if request.method == "POST":
        file = FileUpload.objects.get(id=id)
        parent = file.parent_folder
        
        if file.parent_folder is not None:
            file.parent_id = parent.id
        else:
            file.parent_id = 0
        
        file.delete_time = None

        file.save()

        return redirect("myfiles:recycled_detail")

    else:
        error_message = "仅允许post请求!"
        return render(request, "error/printError.html", {'error_message': error_message})
    
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
            error_message = "表单内容有误，请重新填写!"
            return render(request, "error/printError.html", {'error_message': error_message})
            # return HttpResponse("表单内容有误，请重新填写。")
        
    else:
        file_post_form = FileUploadForm()
        context = {'file': file, 'file_post_form': file_post_form}

        return render(request, 'myfiles/update.html', context)
    
def error(request):
    return render(request, 'error/printError.html')

def create_folder(request, id=None):
    if request.method == "POST":
        folder_form = FolderForm(request.POST)
    
        if folder_form.is_valid():
            new_folder = folder_form.save(commit=False)

            if id is not None:
                new_folder.parent_folder = Folder.objects.get(pk=id)
                new_folder.parent_id = id

                same_name_folder = Folder.objects.filter(Q(name=new_folder.name) & Q(parent_id = new_folder.parent_id))
                if same_name_folder:
                    error_message = "该文件夹已存在"
                    return render(request, "error/printError.html", {'error_message': error_message})

                if not new_folder.parent_folder:
                    error_message = "指定的父文件夹不存在!"
                    return render(request, "error/printError.html", {'error_message': error_message})
                
            else:
                same_name_folder = Folder.objects.filter(Q(name=new_folder.name) & Q(parent_folder = None) & ~Q(parent_id = -1))
                if same_name_folder:
                    error_message = "该文件夹已存在"
                    return render(request, "error/printError.html", {'error_message': error_message})
                                
                new_folder.parent_id = 0
                new_folder.parent_folder = None

            new_folder.save()

            if new_folder.parent_folder is not None:
                return redirect("myfiles:folder_detail", id=id)
            else:
                return redirect("myfiles:file_list")
        
        else:
            error_message = "表单内容有误，请重新填写!"
            return render(request, "error/printError.html", {'error_message': error_message})
    
    elif request.method == "GET":
        folder_form = FolderForm()
        context = { 'folder_form': folder_form }
        return render(request, "myfiles/createFolder.html", context)
    
    else:
        error_message = "非GET, POST请求!"
        return render(request, "error/printError.html", {'error_message': error_message})
    
def folder_detail(request, id):
    folder = Folder.objects.get(id=id)
    children_folder = Folder.objects.filter(parent_folder_id=folder.id)
    children_file = FileUpload.objects.filter(parent_folder_id=folder.id)

    for file in children_file:
        file.file_extension = '.' + file.file.name.split('.')[-1]

    context = { 'folder': folder, 'children_folder':children_folder, 'children_file':children_file }
    return render(request, 'myfiles/folderDetail.html', context)

def folder_delete(request, id):
    if request.method == "POST":
        folder = Folder.objects.get(id=id)
        parent = folder.parent_folder

        # folder.delete()
        folder.parent_id = -1
        # folder.parent_folder = None

        current_time = datetime.now()
        folder.delete_time = current_time + timedelta(days=30)

        folder.save()

        if parent is not None:
            return redirect("myfiles:folder_detail", id=parent.id)
        else:
            return redirect("myfiles:file_list")
            
    else:
        error_message = "仅允许post请求!"
        return render(request, "error/printError.html", {'error_message': error_message})
        
def folder_delete_old(request, id):
    if request.method == "POST":
        folder = Folder.objects.get(id=id)
        parent = folder.parent_folder

        files = FileUpload.objects.filter(parent_id=id)
        for file in files:
            BASE_DIR = Path(__file__).resolve().parent.parent

            fname = os.path.join(BASE_DIR, 'media', str(file.file.name))
            if os.path.isfile(fname):
                os.remove(fname)

            file.delete()

        folder.delete()
        
        return redirect("myfiles:recycled_detail")
            
    else:
        error_message = "仅允许post请求!"
        return render(request, "error/printError.html", {'error_message': error_message})
    
def folder_recover(request, id): 
    if request.method == "POST":
        folder = Folder.objects.get(id=id)
        parent = folder.parent_folder

        if folder.parent_folder is not None:
            folder.parent_id = parent.id
        else:
            folder.parent_id = 0
        
        folder.delete_time = None

        folder.save()

        return redirect("myfiles:recycled_detail")
    else:
        error_message = "仅允许post请求!"
        return render(request, "error/printError.html", {'error_message': error_message})
    
def folder_update(request, id):
    folder = Folder.objects.get(id=id)

    if request.method == "POST":

        folder_post_form = FolderForm(request.POST)

        if folder_post_form.is_valid():

            folder.name = request.POST['name']
            folder.parent_id = request.POST.get('parent_id')

            if folder.parent_id:
                folder.parent_folder = Folder.objects.get(pk=folder.parent_id)
            else:
                folder.parent_folder = None
                folder.parent_id = 0
            folder.save()

            return redirect("myfiles:folder_detail", id=id)

        else:
            error_message = "表单内容有误，请重新填写!"
            return render(request, "error/printError.html", {'error_message': error_message})
        
    else:
        folder_post_form = FolderForm()
        context = {'folder': folder, 'folder_post_form': folder_post_form}

        return render(request, 'myfiles/folderUpdate.html', context)
    
def file_download(request, id):
    file = FileUpload.objects.get(id=id)

    # 检查用户是否有权限下载该文件  
    
    filename = file.file.name
    file = open(os.path.join('', filename), 'rb')

    response = FileResponse(file)
    response['content_type'] = "application/octet-stream"
    # response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
    # response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'%s\'\'' % "{filename}"+'download'
    response['Content-Disposition'] = "attachment; filename*=utf-8''{}".format(filename)
    return response

def recycled_detail(request):
    recycled = Recycled.Recycled
    children_folder = Folder.objects.filter(parent_id=-1)
    children_file = FileUpload.objects.filter(parent_id=-1)

    for file in children_file:
        file.file_extension = '.' + file.file.name.split('.')[-1]

    context = { 'recycled': recycled, 'children_folder':children_folder, 'children_file':children_file }
    return render(request, 'myfiles/recycledDetail.html', context)

def recycled_purge(request):
    if request.method == "POST":

        recycled = Recycled.Recycled
        children_folder = Folder.objects.filter(parent_id=-1)
        children_file = FileUpload.objects.filter(parent_id=-1)

        for folder in children_folder:
            files = FileUpload.objects.filter(parent_id=folder.id)
            for file in files:
                BASE_DIR = Path(__file__).resolve().parent.parent

                fname = os.path.join(BASE_DIR, 'media', str(file.file.name))
                if os.path.isfile(fname):
                    os.remove(fname)

                file.delete()
            folder.delete()
        
        for file in children_file:
            BASE_DIR = Path(__file__).resolve().parent.parent
            fname = os.path.join(BASE_DIR, 'media', str(file.file.name))

            if os.path.isfile(fname):
                os.remove(fname)
            file.delete()

        return redirect("myfiles:recycled_detail")
    
    else:
        error_message = "仅允许post请求!"
        return render(request, "error/printError.html", {'error_message': error_message})
    
def recycled_recover(request):
    if request.method == "POST":

        recycled = Recycled.Recycled
        children_folder = Folder.objects.filter(parent_id=-1)
        children_file = FileUpload.objects.filter(parent_id=-1)

        for folder in children_folder:
            if folder.parent_folder is not None:
                folder.parent_id = folder.parent_folder.id
            else:
                folder.parent_id = 0 

            folder.delete_time = None
            folder.save()

        for file in children_file:
            if file.parent_folder is not None:
                file.parent_id = file.parent_folder.id
            else:
                file.parent_id = 0
            
            file.delete_time = None
            file.save()

        return redirect("myfiles:recycled_detail")
    
    else:
        error_message = "仅允许post请求!"
        return render(request, "error/printError.html", {'error_message': error_message})