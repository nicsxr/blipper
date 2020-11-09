from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from account.models import Account

class RegistrationForm(UserCreationForm):
	#username = forms.CharField(max_length=60, help_text="Username")
	
	class Meta:
		model = Account
		fields = ("username", "email", "password1", "password2")
		widgets = {
			'username': forms.TextInput(attrs={'class': 'form-control'}),
			'email': forms.EmailInput(attrs={'class': 'form-control'}),
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['class'] = 'form-control'

class AccountAuthenticationForm(forms.ModelForm):
	#password = forms.CharField(label="Password", widget=forms.PasswordInput)

	class Meta:
		model = Account
		fields = ('username', 'password')
		widgets = {
			'username': forms.TextInput(attrs={'class': 'form-control'}),
			'password': forms.PasswordInput(attrs={'class': 'form-control'})
		}
	
	def clean(self):
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']
		if not authenticate(username=username, password=password):
			raise forms.ValidationError("Invalid login")

class AccountUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = Account
		fields = ['username', 'email']