from django.urls import path
from . import views

app_name = 'myfiles'

urlpatterns = [
    # path('', home, name='home'),
    path('/list',views.file_list, name='file_list' ),
    path('/upload',views.upload_file, name='upload_file' ),
]