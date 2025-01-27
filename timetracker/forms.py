from django import forms
from .models import TimeEntry, Project, Company, Tag

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter project name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter project description'
            })
        }

class TimeEntryForm(forms.ModelForm):
    company = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-select select2',
            'data-placeholder': 'Select a company'
        }),
        required=True
    )
    
    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-select select2',
            'data-placeholder': 'Select a project'
        }),
        required=True
    )

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
        fields = ['company', 'project', 'description', 'tags']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'What are you working on?'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initialize with all projects but filter in JavaScript
        self.fields['project'].queryset = Project.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        project = cleaned_data.get('project')
        company = cleaned_data.get('company')

        if project and company:
            # Check for active time entries with the same project and company
            active_entry = TimeEntry.objects.filter(
                project=project,
                company=company,
                end_time__isnull=True
            ).first()

            if active_entry:
                raise forms.ValidationError(
                    f'There is already an active time entry for project "{project.name}" '
                    f'with company "{company.name}". '
                    f'Please stop the current timer before starting a new one.'
                )

        return cleaned_data

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