from django import forms
from .models import Ubigeo, Persona


class PersonaInicioForm(forms.ModelForm):
    departamento=forms.ModelChoiceField(queryset=Ubigeo.objects.filter(cod_pro='00',cod_dis='00'),required=True)
    provincia=forms.ModelChoiceField(queryset=Ubigeo.objects.filter(id=-1), required=True)
    distrito=forms.ModelChoiceField(queryset=Ubigeo.objects.filter(id=-1),required=True)
    class Meta:
        model = Persona
        fields = ['nombre', 'paterno','materno','nacimiento','ubigeo','sexo']
    def __init__(self,*args, **kwargs):
        super(PersonaInicioForm, self).__init__(*args, **kwargs)
        for i, (fname, field) in enumerate(self.fields.iteritems()):
            field.widget.attrs['class'] = 'form-control'
        self.fields['nacimiento'].widget.attrs[' data-provide'] = "datepicker"
        self.fields['ubigeo'].widget = forms.HiddenInput()

        if len(kwargs)>0:
            departamento = Ubigeo.objects.get(id = kwargs['initial']['departamento'])
            provincia = Ubigeo.objects.get(id = kwargs['initial']['provincia'])
            distrito = Ubigeo.objects.get(id = kwargs['initial']['distrito'])
            self.fields['provincia'].queryset = Ubigeo.objects.filter(cod_dep=departamento.cod_dep, cod_dis='00').exclude(cod_pro='00')
            self.fields['distrito'].queryset = Ubigeo.objects.filter(cod_pro=provincia.cod_pro, cod_dep=distrito.cod_dep).exclude(cod_dis='00')

        if len(args)>0:
            departamento = Ubigeo.objects.get(id = int(args[0]['departamento']))
            provincia = Ubigeo.objects.get(id =int(args[0]['provincia']))
            distrito = Ubigeo.objects.get(id =int(args[0]['distrito']))
            self.fields['departamento'].queryset = Ubigeo.objects.filter(id = departamento.id)
            self.fields['provincia'].queryset = Ubigeo.objects.filter(cod_dep=departamento.cod_dep, cod_dis='00').exclude(cod_pro='00')
            self.fields['distrito'].queryset = Ubigeo.objects.filter(cod_pro=provincia.cod_pro, cod_dep=distrito.cod_dep).exclude(cod_dis='00')





