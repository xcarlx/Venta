from django import forms
from ..models import Producto, Marca, Modelo


class ProductoForm(forms.ModelForm):
    marca = forms.ModelChoiceField(queryset=Marca.objects.all(), required=True)
    class Meta:
        model = Producto
        fields = ['codigo','descripcion','categoria','marca','modelo','precio','imagen']

    def __init__(self, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)
        for i, (fname, field) in enumerate(self.fields.iteritems()):
            field.widget.attrs['class'] = 'form-control'

        self.fields["modelo"].queryset = Modelo.objects.filter(id = -1)
        self.fields["modelo"].required = True
        self.fields["codigo"].widget.attrs['readonly'] = None

        if len(kwargs) > 0:
            if kwargs['initial']['marca'] != -1:
                marca = Marca.objects.get(id=kwargs['initial']['marca'])
                self.fields["modelo"].queryset = Modelo.objects.filter(marca_id = marca)

        if len(args) > 0:
            marca = Marca.objects.get(id=int(args[0]['marca']))
            self.fields["modelo"].queryset = Modelo.objects.filter(marca_id=marca)