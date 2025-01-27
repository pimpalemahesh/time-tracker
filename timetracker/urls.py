from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('start/', views.start_timer, name='start_timer'),
    path('stop/<int:entry_id>/', views.stop_timer, name='stop_timer'),
    path('add-project/', views.add_project, name='add_project'),
    path('add-company/', views.add_company, name='add_company'),
    path('add-tag/', views.add_tag, name='add_tag'),
    path('delete-entry/<int:entry_id>/', views.delete_entry, name='delete_entry'),
    path('clear-entries/', views.clear_entries, name='clear_entries'),
    path('get-company-projects/', views.get_company_projects, name='get_company_projects'),
    path('summary/', views.summary, name='summary'),
] 