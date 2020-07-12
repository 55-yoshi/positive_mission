from django import forms
from mission.models import Mission
from thanks.models import Thanks

    
class MissionApprovalForm(forms.ModelForm):
    class Meta:
        model = Mission
        fields = [
            'success_exp', 
        ]

class ThanksApprovalForm(forms.ModelForm):
    class Meta:
        model = Thanks
        fields = [
            'reward_exp', 
        ]
