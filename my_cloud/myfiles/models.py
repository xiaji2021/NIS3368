from django.db import models
# from .forms import FileUploadForm

class FileUpload(models.Model):
    # id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    # upload_to参数，用来指定上传上来的文件保存到哪里
    file = models.FileField(upload_to="media/%Y%m%d/")   # verbose_name='文件'

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='Create time')   # 后台 admin 不会显示
    update_time = models.DateTimeField(auto_now=True, verbose_name='Update time')

    # id = models.CharField(max_length=20, default=None, primary_key=True, verbose_name='文件ID')
    # name = models.CharField(max_length=50, default=None, verbose_name='文件名')
    # origin_name = models.CharField(max_length=50, default=None, verbose_name='原始文件名')
    # format = models.CharField(max_length=8, default=None, verbose_name='文件格式')
    # # parent = models.ForeignKey(Catalog, on_delete=models.PROTECT, verbose_name='目录ID')
    # path = models.CharField(max_length=30, default=None, verbose_name='文件路径')
    # size = models.BigIntegerField(default=None, verbose_name='文件大小')
    # md5 = models.CharField(max_length=50, default=None, verbose_name='文件的MD5值')
    # objects = models.Manager()



    class Meta:
    #     db_table = 'files'
    #     indexes = [models.Index(fields=['md5']), models.Index(fields=['create_time']), models.Index(fields=['update_time'])]
        ordering = ('-update_time',)

    def __str__(self):
        return self.title