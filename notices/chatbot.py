from .models import Notice
import datetime
from django.utils import timezone
from django.db.models import Q

def get_chat_response(query):
    """
    Process user query and return matching notices using Django ORM.
    """
    query = query.lower().strip()
    
    notices = Notice.objects.all()
    
    # Category based filtering
    if 'exam' in query:
        notices = notices.filter(category__iexact='Exam')
    elif 'event' in query:
        notices = notices.filter(category__iexact='Event')
    elif 'placement' in query:
        notices = notices.filter(category__iexact='Placement')
    elif 'general' in query:
        notices = notices.filter(category__iexact='General')
        
    # Date based filtering (simplistic)
    if 'today' in query:
        now = timezone.now()
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + datetime.timedelta(days=1)
        notices = notices.filter(date_posted__gte=start, date_posted__lt=end)
        
    notices = notices.order_by('-date_posted')[:5]
    
    response_data = []
    for n in notices:
        response_data.append({
            'title': n.title,
            'date': n.date_posted.strftime("%Y-%m-%d"),
            'url': f"/notice/{n.pk}/"
        })
    
    return response_data
