from rest_framework import serializers
from merge_app.models import UploadFile, SharedFile



class UploadFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadFile
        fields = '__all__'



class SharedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedFile
        fields = '__all__'