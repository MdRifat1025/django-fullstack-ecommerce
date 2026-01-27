from django.shortcuts import render,redirect
from .forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Save the form to create the user instance
            user = form.save()
            
            # Log the user in immediately after successful registration
            login(request, user)
            
            # Add a success message
            messages.success(request, "Registration successful!")
            
            # Redirect to the home page (or a specified success URL)
            return redirect('login')
        else:
            # If the form is not valid, the errors will be rendered on the template
            messages.error(request, "Error in registration. Please check the details.")
    else:
        # For a GET request, create a blank form
        form = RegisterForm()
            
    # Render the registration template, passing the form context
    return render(request, 'accounts/register.html', {'form': form})



def login_view(request):
    if request.method == "POST":
        name=request.POST.get('username')
        password=request.POST.get('password')

        user = authenticate(request, username=name, password=password)
        if user:
            login(request,user)

            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
        
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')