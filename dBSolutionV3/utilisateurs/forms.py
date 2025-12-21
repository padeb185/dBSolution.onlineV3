from django import forms

class LoginTOTPForm(forms.Form):
    email_google = forms.EmailField(label="Email Google")
    password = forms.CharField(widget=forms.PasswordInput)
    totp_token = forms.CharField(label="Code Google Authenticator", max_length=6)
