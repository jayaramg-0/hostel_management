from django import forms
from .models import LeaveRequest


class LeaveRequestForm(forms.ModelForm):
    """Leave Request Submission Form"""
    
    class Meta:
        model = LeaveRequest
        fields = ['leave_type', 'reason', 'from_date', 'to_date', 'destination', 'contact_during_leave']
        widgets = {
            'leave_type': forms.Select(attrs={'class': 'form-select'}),
            'reason': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter reason for leave'
            }),
            'from_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'to_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'destination': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Where will you be going?'
            }),
            'contact_during_leave': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Contact number during leave'
            }),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        from_date = cleaned_data.get('from_date')
        to_date = cleaned_data.get('to_date')
        
        if from_date and to_date:
            if to_date < from_date:
                raise forms.ValidationError('To date cannot be before from date.')
        
        return cleaned_data


class LeaveApprovalForm(forms.ModelForm):
    """Admin Leave Approval Form"""
    
    class Meta:
        model = LeaveRequest
        fields = ['status', 'admin_remarks']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'admin_remarks': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Add remarks (optional)'
            }),
        }


class LeaveFilterForm(forms.Form):
    """Leave Request Filter Form"""
    
    status = forms.ChoiceField(
        choices=[('', 'All Status')] + list(LeaveRequest.STATUS_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    leave_type = forms.ChoiceField(
        choices=[('', 'All Types')] + list(LeaveRequest.LEAVE_TYPE_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
