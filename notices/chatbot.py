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
    
    # Category based filtering with synonyms
    category_matched = False
    if any(word in query for word in ['exam', 'test', 'midterm', 'final', 'results']):
        notices = notices.filter(category__iexact='Exam')
        category_matched = True
    elif any(word in query for word in ['event', 'festival', 'fest', 'sports', 'cultural']):
        notices = notices.filter(category__iexact='Event')
        category_matched = True
    elif any(word in query for word in ['placement', 'job', 'interview', 'tcs', 'infosys', 'wipro', 'campus', 'drive']):
        notices = notices.filter(category__iexact='Placement')
        category_matched = True
    elif any(word in query for word in ['general', 'holiday', 'fee', 'schedule']):
        notices = notices.filter(category__iexact='General')
        category_matched = True
        
    # Date based filtering (simplistic)
    if 'today' in query:
        now = timezone.now()
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + datetime.timedelta(days=1)
        notices = notices.filter(date_posted__gte=start, date_posted__lt=end)
        
    # Full text search fallback if no strict category matched
    if not category_matched and query:
        stop_words = ['what', 'is', 'the', 'when', 'how', 'show', 'me', 'notices', 'about', 'some', 'any', 'a', 'an']
        words = [w for w in query.split() if w not in stop_words]
        if words:
            query_filter = Q()
            for word in words:
                query_filter |= Q(title__icontains=word) | Q(description__icontains=word)
            notices = notices.filter(query_filter).distinct()
            
    notices = notices.order_by('-date_posted')[:5]
    
    response_data = []
    for n in notices:
        response_data.append({
            'title': n.title,
            'date': n.date_posted.strftime("%Y-%m-%d"),
            'url': f"/notice/{n.pk}/"
        })
    
    return response_data
