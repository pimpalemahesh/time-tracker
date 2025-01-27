from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Company, Project, TimeEntry, Tag
from .forms import TimeEntryForm, ProjectForm, CompanyForm
from datetime import datetime, timedelta
from django.db.models import Q
from django.http import JsonResponse

# Create your views here.

def dashboard(request):
    companies = Company.objects.all()
    projects = Project.objects.all()
    tags = Tag.objects.all()
    selected_company = request.GET.get('company')
    
    if selected_company:
        time_entries = TimeEntry.objects.filter(
            company_id=selected_company,
        ).order_by('-start_time')
    else:
        time_entries = TimeEntry.objects.all().order_by('-start_time')
    
    context = {
        'companies': companies,
        'projects': projects,
        'tags': tags,
        'selected_company': selected_company,
        'time_entries': time_entries,
        'form': TimeEntryForm(),
        'project_form': ProjectForm(),
        'company_form': CompanyForm(),
    }
    return render(request, 'timetracker/dashboard.html', context)

def start_timer(request):
    if request.method == 'POST':
        form = TimeEntryForm(request.POST)
        if form.is_valid():
            try:
                time_entry = TimeEntry.objects.create(
                    company=form.cleaned_data['company'],
                    project=form.cleaned_data['project'],
                    description=form.cleaned_data['description'],
                    start_time=timezone.now()
                )
                # Add tags
                time_entry.tags.set(form.cleaned_data['tags'])
                messages.success(request, 'Timer started successfully!')
            except Exception as e:
                messages.error(request, str(e))
        else:
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
        try:
            project = Project.objects.create(
                name=request.POST.get('name'),
                description=request.POST.get('description', '')
            )
            return JsonResponse({
                'status': 'success',
                'id': project.id,
                'name': project.name
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    return redirect('dashboard')

def add_company(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        try:
            company = Company.objects.create(name=name)
            # Return JSON response for AJAX request
            return JsonResponse({
                'status': 'success',
                'id': company.id,
                'name': company.name
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    return redirect('dashboard')

def add_tag(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        color = request.POST.get('color', '#6366f1')
        try:
            tag = Tag.objects.create(name=name, color=color)
            # Return JSON response for AJAX request
            return JsonResponse({
                'status': 'success',
                'id': tag.id,
                'name': tag.name
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    return redirect('dashboard')

def delete_entry(request, entry_id):
    try:
        entry = TimeEntry.objects.get(id=entry_id)
        entry.delete()
        messages.success(request, 'Time entry deleted successfully.')
    except TimeEntry.DoesNotExist:
        messages.error(request, 'Time entry not found.')
    return redirect('dashboard')

def clear_entries(request):
    TimeEntry.objects.all().delete()
    messages.success(request, 'All time entries have been cleared.')
    return redirect('dashboard')

def get_company_projects(request):
    company_id = request.GET.get('company_id')
    if company_id:
        projects = Project.objects.filter(company_id=company_id).values('id', 'name')
        return JsonResponse(list(projects), safe=False)
    return JsonResponse([], safe=False)
