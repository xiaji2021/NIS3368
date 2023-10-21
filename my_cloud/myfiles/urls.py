from django.urls import path
from . import views

app_name = 'myfiles'

urlpatterns = [
    # path('', home, name='home'),
    path('',views.file_list, name='file_list' ),
    path('list/',views.file_list, name='file_list' ),
    path('upload/',views.upload_file, name='upload_file' ),
    path('detail/<int:id>/',views.file_detail, name='file_detail' ),
]