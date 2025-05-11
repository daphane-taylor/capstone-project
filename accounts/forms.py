from django import forms
from django.contrib.auth.models import User
from .models import Profile

class SignupForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	password_confirm = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ['first_name', 'last_name', 'email', 'username', 'password', 'password_confirm']


class UpdateProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['picture', 'phone_number', 'street', 'city', 'state', 'zip_code']