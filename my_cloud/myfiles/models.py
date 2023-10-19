from django.db import models
from .forms import UploadFileForm

class Files(models.Model):
    id = models.CharField(max_length=20, default=None, primary_key=True, verbose_name='文件ID')
    name = models.CharField(max_length=50, default=None, verbose_name='文件名')
    origin_name = models.CharField(max_length=50, default=None, verbose_name='原始文件名')
    format = models.CharField(max_length=8, default=None, verbose_name='文件格式')
    # parent = models.ForeignKey(Catalog, on_delete=models.PROTECT, verbose_name='目录ID')
    path = models.CharField(max_length=30, default=None, verbose_name='文件路径')
    size = models.BigIntegerField(default=None, verbose_name='文件大小')
    md5 = models.CharField(max_length=50, default=None, verbose_name='文件的MD5值')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='Create time')
    update_time = models.DateTimeField(auto_now=True, verbose_name='Update time')
    # objects = models.Manager()
    file = FileField(max_length=255)


    class Meta:
        db_table = 'files'
        indexes = [models.Index(fields=['md5']), models.Index(fields=['create_time']), models.Index(fields=['update_time'])]
        ordering = ('-update_time',)

    def __str__(self):
        return self.title