from django import forms

class LoginForm(forms.Form):
	your_email = forms.EmailField(label="Email")
	password = forms.CharField(widget=forms.PasswordInput)
	widgets = {
            'password': forms.PasswordInput(),
    }