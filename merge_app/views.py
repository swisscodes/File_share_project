from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from .models import UploadFile, SharedFile
from django.contrib.auth.models import User
from . forms import UploadForm, Shareform, Upload_EditForm
from django.views.generic.edit import DeleteView
from django.core.exceptions import PermissionDenied


# Create your views here.

@login_required
def home_page(request):
    obj = SharedFile.objects.filter(file_id__share_status='share_all').order_by('-file_id__uploaded_at',)
    #to access related field we must use double __   e.g __share_status
    context = {'obj':obj}
    return render(request, 'merge_app/home.html', context)



@login_required
def dashboard(request):
    this_user = User.objects.get(pk=request.user.id)
    if(request.user == this_user):
        try:
            current_user_object = UploadFile.objects.all().filter(user=request.user.id)
        except UploadFile.DoesNotExist:
            current_user_object = "No file uploaded yet"
        context = {'current_user_object': current_user_object, 'this_user': this_user}
        return render(request, 'merge_app/dashboard.html', context)

    raise PermissionDenied()



def register(request):
    if(request.method == 'POST'):
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
        # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
        # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
        # Save the User object
            new_user.save()
            return render(request, 'merge_app/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'merge_app/register.html', {'user_form': user_form})


class DeleteFile(DeleteView):
    model = UploadFile
    
    success_url = "/"




@login_required
def change_status(request, obj_id):
    this_user = User.objects.get(pk=request.user.id)
    if(this_user == request.user):
        if(request.method == 'POST'):
            update_form = Shareform(request.POST)
            if(update_form.is_valid()):
                data = update_form.cleaned_data['share_status']
                UploadFile.objects.filter(pk = obj_id).update(share_status=data)
                obj = SharedFile.objects.filter(file_id__share_status='share_all').order_by('-file_id__uploaded_at',)
                context = {'obj':obj}
                return render(request, 'merge_app/home.html', context)

    update_form = Shareform()
    context = {'update_form':update_form}
    return render(request, 'merge_app/status.html', context)

        



@login_required
def upload(request):
    this_user = User.objects.get(pk=request.user.id)
    if(request.user == this_user):
        new_upload = None
        new_share = None
        if(request.method == 'POST'):
            upload_form = UploadForm(request.POST, request.FILES)
            if(upload_form.is_valid()):
                new_upload = upload_form.save(commit=False)
                new_upload.user = this_user
                new_upload.save()
                new_share = SharedFile.objects.create(share_by=this_user, file_id=new_upload)
                new_share.save()
                messages.success(request, f'Succesfully Uploaded {new_upload.file_name}')
                upload_form = UploadForm()
                current_user_object = UploadFile.objects.all().filter(user=request.user.id)
                context = {'current_user_object':current_user_object}
                return render(request, 'merge_app/dashboard.html', context)
        else:
            upload_form = UploadForm()
        

    context = {'upload_form': upload_form, 'this_user': this_user}
    return render(request, 'merge_app/upload.html', context)


    
@login_required
def editForm(request, obj_id):
    this_user = User.objects.get(pk=request.user.id)
    if(this_user == request.user):
        obj_to_update = UploadFile.objects.get(pk=obj_id)
        if(request.user == this_user):
            if(request.method == 'POST'):
                updated_form = Upload_EditForm(request.POST, instance=obj_to_update)
                if(updated_form.is_valid()):
                    updated_form.user = this_user
                    updated_form.save()
                    messages.success(request, f'Succesfully Updated {obj_to_update.file_name}')
            
            updated_form = Upload_EditForm(instance=obj_to_update)
            context = {'updated_form': updated_form}
            return render(request, 'merge_app/edit.html', context)
    raise PermissionDenied()