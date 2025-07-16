from django import forms

class ArchivoCargaForm(forms.Form):
    archivo = forms.FileField(
        label="Archivo (.csv o .xlsx)",
        help_text="Seleccione un archivo Excel o CSV"
    )

    def clean_archivo(self):
        archivo = self.cleaned_data.get('archivo')
        if not archivo.name.endswith(('.xlsx', '.csv')):
            raise forms.ValidationError("Solo se permiten archivos .xlsx o .csv")
        return archivo