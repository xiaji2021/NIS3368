from django.contrib import admin

from .models import Files

# 注册ArticlePost到admin中
admin.site.register(Files)