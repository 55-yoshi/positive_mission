from django import forms
from mission.models import Mission

    
class ApprovalForm(forms.ModelForm):
    class Meta:
        model = Mission
        fields = [
            'success_exp', 
        ]