from django import forms

from ..models import Persona
from ..models import Usuario, Menu


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["persona", "tipo_usuario", "permisos"]

    def __init__(self,*args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        # print(kwargs)
        for i, (fname, field) in enumerate(self.fields.iteritems()):
            field.widget.attrs['class'] = 'form-control'
            field.required = True
        self.fields['permisos'].queryset = Menu.objects.exclude(menu_padre=None)
        if len(kwargs)>0:
            self.fields['persona'].queryset = Persona.objects.exclude(usuario__in=Usuario.objects.all().exclude(persona=kwargs['instance'].persona))
        else:
            self.fields['persona'].queryset = Persona.objects.exclude(usuario__in=Usuario.objects.all())