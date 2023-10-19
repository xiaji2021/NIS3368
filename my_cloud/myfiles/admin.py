from django.contrib import admin

from .models import FileUpload

# 注册ArticlePost到admin中
admin.site.register(FileUpload)