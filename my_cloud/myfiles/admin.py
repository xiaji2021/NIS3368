from django.contrib import admin

from .models import FileUpload, Folder

# 注册ArticlePost到admin中
admin.site.register(FileUpload)
admin.site.register(Folder)