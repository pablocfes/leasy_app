from django import forms
from django.contrib.auth.forms import UserCreationForm

from usuarios.models import Usuario

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Usuario
        fields = ("email", "nombres", "apellidos", "password1", "password2")

    def clean(self):
        email = self.cleaned_data.get("email")
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe un usuario con este correo electrónico.")
        if not email:
            raise forms.ValidationError("El correo electrónico es obligatorio.")

        return super().clean()