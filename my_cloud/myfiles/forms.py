from django import forms
from .models import FileUpload, Folder

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = FileUpload

        fields = ('title', 'content', 'file')

class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ('name',)