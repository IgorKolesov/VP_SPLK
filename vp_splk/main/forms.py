from datetime import datetime, date

from django import forms
from .models import Supply, Cargo, SupplyChain, UploadFiles
from .models.comment import Comment

min_length = 5


class AddNewSupply(forms.ModelForm):
    deadline = forms.DateField(
        widget=forms.SelectDateWidget(attrs={'class': 'date_select'}),
        initial=date.today(),
        label='Крайний срок',

    )

    class Meta:
        model = Supply
        # fields = '__all__'
        exclude = ['employee', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form_input'}),
            'start_point_address': forms.Textarea(attrs={'class': 'form_input form_textarea'}),
            'end_point_address': forms.Textarea(attrs={'class': 'form_input form_textarea'}),
        }


class AddNewCargo(forms.ModelForm):
    class Meta:
        model = Cargo
        fields = '__all__'
        exclude = ['supply']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form_input'}),
            'description': forms.Textarea(attrs={'class': 'form_input form_textarea'}),
        }


class AddNewSupplyChain(forms.ModelForm):
    deadline = forms.DateField(
        widget=forms.SelectDateWidget(attrs={'class': 'date_select'}),
        initial=date.today(),
        label='Крайний срок',
    )

    class Meta:
        model = SupplyChain
        fields = '__all__'
        exclude = ['supply', 'serial_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form_input'}),
            'start_point_address': forms.Textarea(attrs={'class': 'form_input form_textarea'}),
            'end_point_address': forms.Textarea(attrs={'class': 'form_input form_textarea'}),
        }


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadFiles
        fields = ['file']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']
        widgets = {
            'comment_text': forms.Textarea(attrs={'class': 'form_input form_textarea'}),
        }