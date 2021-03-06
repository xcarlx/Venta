from django import forms

from ..models import Menu


class MenuHijoForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = "__all__"

    def __init__(self,*args, **kwargs):
        super(MenuHijoForm, self).__init__(*args, **kwargs)
        for i, (fname, field) in enumerate(self.fields.iteritems()):
            field.widget.attrs['class'] = 'form-control'
        self.fields['url'].required = True
        self.fields['icono'].required = True
        self.fields['menu_padre'].required = True
        self.fields['menu_padre'].queryset = Menu.objects.filter(menu_padre=None)
        # self.fields['menu_padre'].widget = forms.HiddenInput()

class MenuPadreForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ["nombre", "orden", 'icono']

    def __init__(self,*args, **kwargs):
        super(MenuPadreForm, self).__init__(*args, **kwargs)
        for i, (fname, field) in enumerate(self.fields.iteritems()):
            field.widget.attrs['class'] = 'form-control'




