from django.forms.fields import DateTimeField
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm
from .models import UploadFile, SharedFile
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from . forms import UploadForm
from django.views.generic.edit import DeleteView


# Create your views here.

@login_required
def dashboard(request):
    this_user = User.objects.get(pk=request.user.id)
    if(request.user == this_user):
        new_upload = None
        if(request.method == 'POST'):
            upload_form = UploadForm(request.POST, request.FILES)
            if(upload_form.is_valid()):
                new_upload = upload_form.save(commit=False)
                new_upload.user = this_user
                new_upload.save()
                upload_form = UploadForm()
        else:
            upload_form = UploadForm()
        try:
            current_user_object = UploadFile.objects.all().filter(user=request.user.id)
        except UploadFile.DoesNotExist:
            current_user_object = "No file uploaded yet"

    context = {'section': 'dashboard', 'current_user_object': current_user_object,\
        'upload_form': upload_form, 'this_user': this_user}
    return render(request, 'merge_app/dashboard.html', context)



def register(request):
    if request.method == 'POST':
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