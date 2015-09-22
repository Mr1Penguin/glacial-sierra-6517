from django import forms

class LoginForm(forms.Form):
	your_email = forms.EmailField(label="Email",widget=forms.TextInput(attrs={'placeholder': ''}))
	password = forms.CharField(widget=forms.PasswordInput,widget=forms.TextInput(attrs={'placeholder': ''}))
	widgets = {
            'password': forms.PasswordInput(),
    }