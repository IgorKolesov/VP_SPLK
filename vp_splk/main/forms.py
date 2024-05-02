from django import forms
from .models import Supply, Cargo

min_length = 5


class AddNewSupply(forms.ModelForm):
    class Meta:
        model = Supply
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form_input'}),
            'start_point_address': forms.Textarea(attrs={'width': 200, 'height': 20 }),
            'end_point_address': forms.Textarea(attrs={'cols': 50, 'rows': 20}),
        }


class AddNewCargo(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form_input'}),
        }