from django import forms


class UserRegister(forms.Form):
    login = forms.CharField(max_length=30, label="Введите логин")
    password = forms.CharField(min_length=8, max_length=32, widget=forms.PasswordInput
                               , label="Введите пароль")
    repeat_password = forms.CharField(min_length=8, max_length=32, widget=forms.PasswordInput
                               , label="Повторите пароль")
    age = forms.CharField(max_length=3, widget=forms.NumberInput
                               , label="Введите возраст")

class NumberPage(forms.Form):
    class Meta:
        fields = [
            "number",
        ]
    def __init__(self, *args, **kwargs):
        MAX_ELEMENTS = [str(a+1) for a in range(10)]
        super(NumberPage, self).__init__(*args, **kwargs)
        self.fields['number'] = forms.ChoiceField(label="Отображаемых элементов",choices=([(element, element) for element in MAX_ELEMENTS]))
        # self.fieglds['1'] = forms.ChoiceField(choices=([(brand, brand) for brand in MAX_ELEMENTS]))
