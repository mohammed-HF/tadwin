from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import FileUploadForm
from django.contrib.auth import authenticate, login
from .forms import LoginForm



class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')  # Redirect to login page after successful registration
    template_name = 'registration/signup.html'



@login_required
def dashboard(request):
    return render(request, 'tadwinapp/dashboard.html')



@login_required
def file_upload(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            new_file = UploadedFile(file=request.FILES['file'], user=request.user)
            new_file.save()
            return redirect('dashboard')
    else:
        form = FileUploadForm()
    return render(request, 'tadwinapp/file_upload.html', {'form': form})



def custom_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirect to dashboard if login is successful
            else:
                # Stay on login page and show error if credentials are incorrect
                return render(request, 'login.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})
