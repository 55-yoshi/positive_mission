from django import forms
from .models import Thanks
from user.models import Profile


# class ThanksCreateForm(forms.ModelForm):
#     recipients = forms.ModelMultipleChoiceField(
#         queryset = Profile.objects,
#         widget = forms.SelectMultiple
#         # widget = forms.CheckboxSelectMultiple
#     )
class ThanksCreateForm(forms.ModelForm):
    recipients = forms.ModelMultipleChoiceField(
        queryset = Profile.objects,
        widget = forms.CheckboxSelectMultiple
    )

        

    class Meta:
        model = Thanks
        fields = (
            'recipients', 'content',
        )