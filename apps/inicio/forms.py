from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.db.models import Q
from django.utils.text import capfirst

from ..personas.models import Ubigeo
from ..personas import models

class AuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'class':'form-control'}))
    password = forms.CharField(label=("Password"), widget=forms.PasswordInput(attrs={'class':'form-control'}))

    error_messages = {
        'invalid_login': ("Please enter a correct %(username)s and password. "
                           "Note that both fields may be case-sensitive."),
        'inactive': ("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)

        # Set the label for the "username" field.
        UserModel = get_user_model()
        self.username_field = UserModel._meta.get_field(UserModel.USERNAME_FIELD)
        if self.fields['username'].label is None:
            self.fields['username'].label = capfirst(self.username_field.verbose_name)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

class PersonaInicioForm(forms.ModelForm):
    departamento=forms.ModelChoiceField(queryset=None)
    provincia=forms.ModelChoiceField(queryset=None)
    distrito=forms.ModelChoiceField(queryset=None)
    class Meta:
        model = models.Persona
        fields = '__all__'
    def __init__(self,nro,*args, **kwargs):
        super(PersonaInicioForm, self).__init__(*args, **kwargs)
        for i, (fname, field) in enumerate(self.fields.iteritems()):
            field.widget.attrs['class'] = 'form-control'
        self.fields['ubigeo'].widget = forms.HiddenInput()
        self.fields['departamento'].queryset = Ubigeo.objects.filter(cod_pro='00',cod_dis='00')
        self.fields['provincia'].queryset = Ubigeo.objects.filter(cod_dis='00').exclude(cod_pro='00')
        self.fields['distrito'].queryset = Ubigeo.objects.filter().exclude(cod_pro='00',cod_dis='00')

        if int(nro>0):
            ids = Ubigeo.objects.get(pk=nro)
            self.fields['provincia'].queryset = Ubigeo.objects.filter(Q(coddpto=ids.cod_dep)  & Q(coddist='00') & ~Q(codprov='00'))
            self.fields['distrito'].queryset = Ubigeo.objects.filter(Q(coddpto=ids.cod_dep) & Q(codprov=ids.cod_pro) & ~Q(coddist='00'))

