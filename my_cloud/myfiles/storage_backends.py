# from obs import ObsClient
# from django.conf import settings
# from django.core.files.storage import Storage
#
# class HuaweiObsStorage(Storage):
#     def __init__(self, *args, **kwargs):
#         self.obs_client = ObsClient(
#             access_key_id=settings.HUAWEI_ACCESS_KEY,
#             secret_access_key=settings.HUAWEI_SECRET_KEY,
#             server=settings.HUAWEI_OBS_ENDPOINT
#         )
#         super().__init__(*args, **kwargs)
#
#     def _save(self, name, content):
#         self.obs_client.putContent(settings.HUAWEI_BUCKET_NAME, name, content.read())
#         return name
#
#     def url(self, name):
#         # 只生成了URL，可能需要根据实际的权限策略来签名等操作
#         return f"{settings.HUAWEI_OBS_ENDPOINT}/{settings.HUAWEI_BUCKET_NAME}/{name}"
