from django import forms
from .models import Complaint


class ComplaintForm(forms.ModelForm):
    """Complaint Submission Form"""
    
    class Meta:
        model = Complaint
        fields = ['category', 'subject', 'description']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter complaint subject'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your complaint in detail'
            }),
        }


class ComplaintUpdateForm(forms.ModelForm):
    """Admin Complaint Update Form"""
    
    class Meta:
        model = Complaint
        fields = ['status', 'admin_remarks']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'admin_remarks': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Add remarks or resolution details'
            }),
        }


class ComplaintFilterForm(forms.Form):
    """Complaint Filter Form"""
    
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by ID, subject...'
        })
    )
    category = forms.ChoiceField(
        choices=[('', 'All Categories')] + list(Complaint.CATEGORY_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    status = forms.ChoiceField(
        choices=[('', 'All Status')] + list(Complaint.STATUS_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
