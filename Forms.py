from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import Appointment

class CustomUserCreationForm(UserCreationForm):


    class Meta(UserCreationForm.Meta):
        model = User
        fields=['username','email','password1','password2','role','phone_no']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = self.cleaned_data["role"]
        user.phone_no = self.cleaned_data["phone_no"]  # Save phone_no
        if commit:
            user.save()
            self.save_m2m()  # Save many-to-many fields
        return user

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'date', 'reason']
