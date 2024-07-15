from django. forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
from django_recaptcha.fields import ReCaptchaField



class empleadoform(ModelForm):
    captcha = ReCaptchaField()
    class Meta:
        model = Empleado
        fields = '__all__'


class tipoempleadoform(ModelForm):
    captcha = ReCaptchaField()
    class Meta:
        model = tipoempleado
        fields = '__all__'

class CustomUserCreationForm(UserCreationForm):
    captcha = ReCaptchaField()

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class productoform(ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = Producto
        fields = '__all__'
