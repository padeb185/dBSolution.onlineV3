from django import forms

class LoginTOTPForm(forms.Form):
    email_google = forms.EmailField(label="Email Google")
    password = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput(attrs={
            "autocomplete": "current-password"
        })
    )
    totp_token = forms.CharField(
        label="Code Google Authenticator",
        max_length=6,
        widget=forms.TextInput(attrs={
            "inputmode": "numeric",
            "pattern": "[0-9]{6}",
            "autocomplete": "one-time-code",
        })
    )
