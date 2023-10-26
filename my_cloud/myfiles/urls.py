from django.urls import path
from . import views

app_name = 'myfiles'

urlpatterns = [
    # path('', home, name='home'),
    path('',views.file_list, name='file_list' ),
    path('list/',views.file_list, name='file_list' ),
    path('upload/',views.upload_file, name='upload_file' ),
    path('upload/<int:id>/',views.upload_file, name='upload_child_file' ),
    path('detail/<int:id>/',views.file_detail, name='file_detail' ),
    path('delete/<int:id>/',views.file_delete, name='file_delete' ),
    path('update/<int:id>/',views.file_update, name='file_update' ),

    path('error/',views.error, name='error' ),
    path('create-folder/',views.create_folder, name='create_folder' ),
    path('create-folder/<int:id>/',views.create_folder, name='create_child_folder' ),
    path('folder-detail/<int:id>/',views.folder_detail, name='folder_detail' ),
    path('folder-delete/<int:id>/',views.folder_delete, name='folder_delete' ),
    path('folder-update/<int:id>/',views.folder_update, name='folder_update' ),

    path('download/<int:id>/', views.file_download, name='file_download'), 
]