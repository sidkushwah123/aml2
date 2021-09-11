from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import  VsUsers



CHOICES=[('Performer','I AM A Performer'),('Voter','I AM A Voter')]
class SignUpForm(UserCreationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form-control","placeholder": "Username"}))
    password1 = forms.CharField(required=True, label="Password", widget=forms.PasswordInput(attrs={"class": "form-control","placeholder": "Password"}))
    password2 = forms.CharField(required=True, label="Confirm Password", widget=forms.PasswordInput(attrs={"class": "form-control","placeholder": "Confirm Password"}))
    email = forms.EmailField(max_length=254, help_text='Email.',widget=forms.TextInput(attrs={"class": "form-control","placeholder": "E-mail"}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )

    # def clean(self):
    #     cleaned_data = super(SignUpForm, self).clean()
    #     username = cleaned_data.get('username')
    #     if username and User.objects.filter(username__iexact=username).exists():
    #         self.add_error('username', 'A user with that username already exists.')
    #     return cleaned_data


class  VsUsersForm(forms.ModelForm):

    # Type = forms.CharField(label='Type', widget=forms.RadioSelect(choices=CHOICES))
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={"class": "form-control","placeholder": "Name"}))
    Contact_no = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={"class": "form-control","placeholder": "Phone No"}))
    Zip_Code = forms.IntegerField(required=True, widget=forms.NumberInput(attrs={"class": "form-control","placeholder": "Zipcode"}))
    class Meta:
        model = VsUsers
        fields = ('name', 'Contact_no', 'Zip_Code', )


