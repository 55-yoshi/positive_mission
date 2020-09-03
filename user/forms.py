from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

from django.forms import EmailField


# class UserCreateForm(UserCreationForm):
#     pass


class UserCreateForm(UserCreationForm):
    email = EmailField(label='メールアドレス', required=True, help_text='Required.')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            "kubun", "exp_total"
        )

# KUBUN_CHOICES = (
#    ('1', '経営者'),
#    ('2', '従業員'),
# )


# class ProfileForm(forms.Form, forms.ModelForm):
#    kubun = forms.ChoiceField(
#        label='区分',
#        widget=forms.Select,
#        choices=KUBUN_CHOICES,
#        required=True,
#    )

#    exp_total = forms.IntegerField(
#        label='経験値',
#        required=True,
#        initial='10',
#        widget=forms.TextInput(
#            attrs={
#                'readonly': 'readonly',
#            }
#        ),
#    )
