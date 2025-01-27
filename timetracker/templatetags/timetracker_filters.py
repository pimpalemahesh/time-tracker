from django import template
from datetime import timedelta

register = template.Library()

@register.filter
def format_duration(td):
    if not isinstance(td, timedelta):
        return ""
    
    total_seconds = int(td.total_seconds())
    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0 or not parts:  # include seconds if it's the only non-zero value
        parts.append(f"{seconds}s")
    
    return " ".join(parts)

@register.filter
def total_hours_today(time_entries):
    from django.utils import timezone
    import pytz
    
    today = timezone.now().date()
    total_duration = timedelta()
    
    for entry in time_entries:
        if entry.start_time.date() == today:
            end_time = entry.end_time if entry.end_time else timezone.now()
            total_duration += end_time - entry.start_time
    
    hours = total_duration.total_seconds() / 3600
    return f"{hours:.1f}h" 