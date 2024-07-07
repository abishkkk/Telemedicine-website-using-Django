from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, AppointmentForm
from .models import Appointment, Doctor, Patient
from django.contrib.auth import logout

def home(request):
    """Render the home page."""
    return render(request, 'home.html')

def registeration(request):
    """Handle user registration."""
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully. Please log in.")
            return redirect("/login")
        else:
            messages.error(request, "User creation failed. Please try again.")
    return render(request, 'registeration.html', {'form': form})

def user_login(request):
    """Handle user login."""
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if user.role == 'patient':
                return redirect("/appointments")
            elif user.role == 'doctor':
                return redirect("/patients")
            elif user.role == 'admin':
                return redirect("/home")
            else:
                return redirect("/home")  # Redirect to home page for unknown roles
        else:
            messages.error(request, "Username or Password is incorrect!")
    return render(request, "login.html")


@login_required
def appointment_list(request):
    """Render the appointment list."""
    if request.user.role == 'PATIENT':
        appointments = Appointment.objects.filter(patient__user=request.user)
        return render(request, 'appointment_list.html', {'appointments': appointments})
    else:
        return redirect('home')

@login_required
def doctors_list(request):
    """Render the doctor list."""
    if request.user.role == 'DOCTOR':
        doctors = Doctor.objects.all()
        return render(request, 'doctors_list.html', {'doctors': doctors})
    else:
        return redirect('home')

@login_required
def patients_list(request):
    """Render the patient list."""
    if request.user.role == 'ADMIN':
        patients = Patient.objects.all()
        return render(request, 'patients_list.html', {'patients': patients})
    else:
        return redirect('home')
def logout_view(request):
    """Handle user logout."""
    logout(request)
    return redirect('home')
