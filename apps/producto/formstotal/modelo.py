from django import forms
from ..models import Modelo

class ModeloForm(forms.ModelForm):
    class Meta:
        model = Modelo
        fields = ["marca", "nombre"]

    def __init__(self, *args, **kwargs):
        super(ModeloForm, self).__init__(*args, **kwargs)
        for i, (fname, field) in enumerate(self.fields.iteritems()):
            field.widget.attrs['class'] = 'form-control'