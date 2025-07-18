from django import forms
from django.contrib.auth.forms import UserCreationForm

from usuarios.models import Usuario

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Usuario
        fields = ("email", "nombres", "apellidos", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].help_text = 'Tu contraseña debe tener al menos 8 caracteres y no puede ser completamente numérica.'
        self.fields['password2'].help_text = 'Ingresa la misma contraseña para verificación.'

    def clean_email(self):
        email = self.cleaned_data.get("email").lower().strip()
        if not email:
            raise forms.ValidationError("El correo electrónico es obligatorio.")
        if Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe un usuario con este correo electrónico.")
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1:
            # Validaciones personalizadas en español
            if len(password1) < 8:
                raise forms.ValidationError("Esta contraseña es demasiado corta. Debe contener al menos 8 caracteres.")
            if password1.isdigit():
                raise forms.ValidationError("Esta contraseña es completamente numérica.")
            if password1.lower() in ['password', '12345678', 'contraseña']:
                raise forms.ValidationError("Esta contraseña es demasiado común.")
        return password1

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2