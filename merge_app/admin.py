from django.contrib import admin
from . models import *

# Register your models here.
admin.site.register(UploadFile),


#admin.site.register(SharedFile),

@admin.register(SharedFile)
class SharedFileAdmin(admin.ModelAdmin):
    list_display = ('share_by', 'file_id')
