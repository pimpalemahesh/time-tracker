from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Company, Project, TimeEntry, Tag
from .forms import TimeEntryForm, ProjectForm, CompanyForm

# Create your views here.

def dashboard(request):
    companies = Company.objects.all()
    selected_company = request.GET.get('company')
    
    if selected_company:
        time_entries = TimeEntry.objects.filter(
            project__company_id=selected_company,
        ).order_by('-start_time')
    else:
        time_entries = TimeEntry.objects.all().order_by('-start_time')
    
    # Keep the form data in case of errors
    form = TimeEntryForm(request.POST if request.method == 'POST' else None)
    
    context = {
        'companies': companies,
        'selected_company': selected_company,
        'time_entries': time_entries,
        'form': form,
        'project_form': ProjectForm(),
        'company_form': CompanyForm(),
    }
    return render(request, 'timetracker/dashboard.html', context)

def start_timer(request):
    if request.method == 'POST':
        form = TimeEntryForm(request.POST)
        if form.is_valid():
            try:
                time_entry = form.save(commit=False)
                time_entry.start_time = timezone.now()
                time_entry.save()
                form.save_m2m()  # Save tags
                messages.success(request, 'Timer started successfully!')
            except ValidationError as e:
                messages.error(request, str(e))
        else:
            # Show specific error messages for each field
            for field, errors in form.errors.items():
                field_name = field.replace('_', ' ').title()
                for error in errors:
                    messages.error(request, f"{field_name}: {error}")
    return redirect('dashboard')

def stop_timer(request, entry_id):
    try:
        time_entry = TimeEntry.objects.get(id=entry_id)
        if not time_entry.end_time:
            time_entry.end_time = timezone.now()
            time_entry.save()
            messages.success(request, 'Timer stopped successfully!')
        else:
            messages.warning(request, 'This timer was already stopped.')
    except TimeEntry.DoesNotExist:
        messages.error(request, 'Timer entry not found.')
    return redirect('dashboard')

def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            messages.success(request, f'Project "{project.name}" was created successfully!')
        else:
            for field, errors in form.errors.items():
                field_name = field.replace('_', ' ').title()
                for error in errors:
                    messages.error(request, f"{field_name}: {error}")
    return redirect('dashboard')

def add_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            company = form.save()
            messages.success(request, f'Company "{company.name}" was created successfully!')
        else:
            for field, errors in form.errors.items():
                field_name = field.replace('_', ' ').title()
                for error in errors:
                    messages.error(request, f"{field_name}: {error}")
    return redirect('dashboard')

def add_tag(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        color = request.POST.get('color')
        if name:
            try:
                tag = Tag.objects.create(name=name, color=color)
                messages.success(request, f'Tag "{tag.name}" was created successfully!')
            except Exception as e:
                messages.error(request, f'Error creating tag: {str(e)}')
        else:
            messages.error(request, 'Tag name is required.')
    return redirect('dashboard')
