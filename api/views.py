from django.shortcuts import render
from rest_framework import generics
from merge_app.models import UploadFile, SharedFile
from .serializers import UploadFileSerializer, SharedFileSerializer

# Create your views here.
class UploadAPIView(generics.ListAPIView):
    queryset = UploadFile.objects.all()
    serializer_class = UploadFileSerializer


class DetailUpload(generics.RetrieveAPIView):
    queryset = UploadFile.objects.all()
    serializer_class = UploadFileSerializer



class SharedAPIView(generics.ListAPIView):
    queryset = SharedFile.objects.all()
    serializer_class = SharedFileSerializer



class DetailShare(generics.RetrieveAPIView):
    queryset = SharedFile.objects.all()
    serializer_class = SharedFileSerializer


