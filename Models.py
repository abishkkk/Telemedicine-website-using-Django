from django.db import models
from django.contrib.auth.models import User,AbstractUser, BaseUserManager
from django.db.models import TimeField
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
# from django.utils import datetime



class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN="ADMIN","Admin"
        PATIENT = "PATIENT", "patient"
        DOCTOR = "DOCTOR", "doctor"

    base_role=Role.ADMIN

    role = models.CharField(max_length=50, choices=Role.choices)
    phone_no = models.BigIntegerField(null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            if not self.role:
                self.role = self.base_role
        return super().save(*args, **kwargs)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        related_name='custom_users',
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        related_name='custom_users',
        related_query_name='custom_user',
    )

    def __str__(self):
        return self.username
class DoctorManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.DOCTOR)


class Doctor(User):

    base_role = User.Role.DOCTOR
    Doctor = DoctorManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
        super().save(*args, **kwargs)






class PatientManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.PATIENT)


class Patient(User):

    base_role = User.Role.PATIENT

    patient = PatientManager()

    class Meta:
        proxy = True

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
        super().save(*args, **kwargs)





class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.user.username

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username

class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments',null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments',null=True)
    date = models.DateField(default=timezone.now)
    # time = models.TimeField(default=datetime.now().time)
    reason = models.TextField(default="No reason provided")


    def __str__(self):
        return f"{self.date} - {self.time} - Dr. {self.doctor.user.username} - {self.patient.user.username}"
