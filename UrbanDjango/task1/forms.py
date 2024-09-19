from django import forms


class UserRegister(forms.Form):
    login = forms.CharField(max_length=30, label="Введите логин")
    password = forms.CharField(min_length=8, max_length=32, widget=forms.PasswordInput
                               , label="Введите пароль")
    repeat_password = forms.CharField(min_length=8, max_length=32, widget=forms.PasswordInput
                               , label="Повторите пароль")
    age = forms.CharField(max_length=3, widget=forms.NumberInput
                               , label="Введите возраст")