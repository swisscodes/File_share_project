from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

#Model to upload file
class UploadFile(models.Model):
    STATUS_CHOICES = (
        ('private', 'Private'),
        ('share_all', 'Share publicly'),
        ('share_friends', 'Share with friends')
    )
    user =  models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_upload')
    record_no = models.CharField(max_length=30)
    file_name = models.CharField(max_length=150)
    description = models.CharField(max_length=500)
    document = models.FileField(upload_to='uploads/%Y/%m/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    share_status = models.CharField(max_length=13, choices=STATUS_CHOICES,\
        default='private')

    class Meta:
        ordering = ('-uploaded_at',)

    
    def __str__(self):
        return self.file_name
    

    

class SharedFile(models.Model):
    share_by = models.ForeignKey(User, on_delete=models.CASCADE,\
        related_name='user_shared')
    file_id = models.ForeignKey(UploadFile, on_delete=models.CASCADE,\
        related_name='shared_file')
    

    def __str__(self):
        return self.file_id.file_name
