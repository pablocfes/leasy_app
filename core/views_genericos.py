from django.views.generic import TemplateView, View
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

# local imports
from core.mixins import LoginRequiredMixin

class ModeloDinamicoListView(LoginRequiredMixin, TemplateView):
    """
    Vista Base para listar Modelos y sus valores de manera dinamica
    """
    template_name = 'base_list.html'
    model = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        queryset = self.model.objects.all()
        campos_excluidos = ['usuario_creacion_id', 'usuario_modificacion_id', 'fecha_modificacion']

        campos_visibles = [
            field for field in self.model._meta.fields
            if field.name not in campos_excluidos
        ]

        columnas_verbose = [field.verbose_name.title() for field in campos_visibles]
        columnas_names = [field.name for field in campos_visibles]

        filas = list(queryset.values(*columnas_names))

        context['titulo'] = self.model._meta.verbose_name_plural.title()
        context['columnas'] = columnas_verbose
        context['filas'] = filas
        return context




class ModeloDinamicoUpdateView(LoginRequiredMixin, View):
    model = None
    success_url = '/'

    def post(self, request, id):
        instance = get_object_or_404(self.model, pk=id)

        for field in self.model._meta.fields:
            name = field.name
            if name in request.POST and name != 'id':
                setattr(instance, name, request.POST.get(name))

        instance.save()
        messages.success(request, 'Registro actualizado correctamente.')
        return redirect(self.success_url)