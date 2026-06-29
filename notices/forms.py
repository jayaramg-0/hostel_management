from django import forms
from .models import Notice


class NoticeForm(forms.ModelForm):
    """Notice Create/Update Form"""
    
    class Meta:
        model = Notice
        fields = ['title', 'description', 'priority', 'attachment', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Notice Title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Enter Notice Content'
            }),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'attachment': forms.FileInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
