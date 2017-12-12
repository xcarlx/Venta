from django import forms
from ..models import Marca

class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(MarcaForm, self).__init__(*args, **kwargs)
        for i, (fname, field) in enumerate(self.fields.iteritems()):
            field.widget.attrs['class'] = 'form-control'