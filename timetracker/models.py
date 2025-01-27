from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.

class Company(models.Model):
    name = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Companies"

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=20, default='#6366f1')
    
    def __str__(self):
        return self.name

class TimeEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    
    def clean(self):
        # Check if there's an active time entry for this project and company combination
        if not self.end_time:  # If this is an active entry
            active_entry = TimeEntry.objects.filter(
                project=self.project,
                company=self.company,  # Add company to the filter
                end_time__isnull=True
            ).exclude(id=self.id).first()
            
            if active_entry:
                raise ValidationError(
                    f'There is already an active time entry for project "{self.project.name}" '
                    f'with company "{self.company.name}". '
                    f'Please stop the current timer before starting a new one.'
                )
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
    def duration(self):
        if self.end_time:
            return self.end_time - self.start_time
        return timezone.now() - self.start_time
    
    class Meta:
        verbose_name_plural = "Time entries"
