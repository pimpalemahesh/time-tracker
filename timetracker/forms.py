from django import forms
from .models import TimeEntry, Project, Company, Tag

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'company', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter project name'}),
            'company': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Project description'}),
        }

class TimeEntryForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select select2',
            'data-placeholder': 'Select tags'
        }),
        required=False
    )

    class Meta:
        model = TimeEntry
        fields = ['project', 'description', 'tags']
        widgets = {
            'project': forms.Select(attrs={
                'class': 'form-select select2',
                'data-placeholder': 'Select a project'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'What are you working on?'
            }),
        }

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter company name'
            })
        } 