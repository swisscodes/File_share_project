from django.urls import path
from . views import UploadAPIView, SharedAPIView, DetailShare, DetailUpload

urlpatterns = [

path('upload', UploadAPIView.as_view(), name="uploadapi"),
path('upload/<int:pk>/', DetailUpload.as_view(), name="detail_uploadapi"),
path('share', SharedAPIView.as_view(), name="sharedapi"),
path('share/<int:pk>/', DetailShare.as_view(), name="detail_sharedapi"),

]