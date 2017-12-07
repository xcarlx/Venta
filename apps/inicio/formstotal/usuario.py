from django import forms
from apps.inicio.models import Usuario


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = "__all__"

    def __init__(self,*args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        for i, (fname, field) in enumerate(self.fields.iteritems()):
            field.widget.attrs['class'] = 'form-control'