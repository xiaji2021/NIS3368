from django.db import models
# from .forms import FileUploadForm
from django.core.files.storage import default_storage

class Folder(models.Model):
    name = models.CharField(max_length=255)
    parent_folder = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, verbose_name="父文件夹", related_name='child_folders')
    parent_id = models.IntegerField(default=None, null=True, blank=True, verbose_name='父文件夹ID')

    # child_folder = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, verbose_name="子文件夹", related_name='parent_folders')
    # child_id = models.CharField(max_length=20, default=None,null=True, blank=True, verbose_name='子父文件夹ID')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='Create time')
    update_time = models.DateTimeField(auto_now=True, verbose_name='Update time')
    delete_time = models.DateTimeField(null=True, blank=True,  verbose_name='Delete time')


    class Meta:
        ordering = ('-update_time',)

    def __str__(self):
        return self.name
    
class Recycled(models.Model):
    Recycled = Folder(name = 'Recycled')

    def __str__(self):
        return self.Recycled.name
    

class FileUpload(models.Model):
    # id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    # upload_to参数，用来指定上传上来的文件保存到哪里
    file = models.FileField(upload_to="%Y%m%d/")   # verbose_name='文件'

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='Create time')   # 后台 admin 不会显示
    update_time = models.DateTimeField(auto_now=True, verbose_name='Update time')
    delete_time = models.DateTimeField(null=True, blank=True,  verbose_name='Delete time')

    parent_folder = models.ForeignKey(Folder, null=True, blank=True, on_delete=models.CASCADE, verbose_name = '父文件夹')
    parent_id = models.IntegerField(default=None, null=True, blank=True, verbose_name='父文件夹ID')


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
    
    def filesize(self):
        if self.file:
            x = self.file.size
            y = 512000
            if x < y:
                value = round(x / 1024, 2)
                ext = ' KB'
            elif x < y * 1024:
                value = round(x / (1024 * 1024), 2)
                ext = ' MB'
            else:
                value = round(x / (1024 * 1024 * 1024), 2)
                ext = ' GB'
            return str(value) + ext    
        return None
    
    def filename(self):
        if self.title:
            new_name = self.file.name.split('/')[-1]
            return new_name
        return None