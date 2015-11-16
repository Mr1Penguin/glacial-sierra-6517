from django import forms


class LoginForm(forms.Form):
    your_email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput)
    widgets = {
        'password': forms.PasswordInput(),
    }
    new_user = forms.BooleanField(label="New user", widget=forms.CheckboxInput(attrs={'onclick': 'toggled();'}))
    
#class LogoutForm(forms.Form):
#    user_id = forms.CharField(label="user_id")
