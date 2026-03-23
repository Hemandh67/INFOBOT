import re
from .models import Notice
import datetime
from django.utils import timezone
from django.db.models import Q

def get_chat_response(query):
    """
    Process user query and return matching notices using Django ORM.
    Returns a dict with 'message' and 'results' (optional).
    """
    if not query or not query.strip():
        return {"message": "Please enter a question or keywords to search for notices."}
        
    # 1. Normalize input: lowercase and remove basic punctuation
    query = query.lower()
    query = re.sub(r'[^\w\s]', '', query).strip()
    
    if not query:
        return {"message": "Please enter a valid search query."}

    notices = Notice.objects.all()
    
    # 2. Intelligent Keyword Mapping
    category_matched = False
    category_name = None
    
    exam_keywords = ['exam', 'test', 'midterm', 'final', 'results', 'schedule']
    event_keywords = ['event', 'festival', 'fest', 'sports', 'cultural', 'competition']
    placement_keywords = ['placement', 'job', 'interview', 'tcs', 'infosys', 'wipro', 'campus', 'drive', 'hiring']
    general_keywords = ['general', 'holiday', 'fee', 'deadline', 'urgent']
    
    words = query.split()
    
    if any(word in words for word in exam_keywords):
        notices = notices.filter(category__iexact='Exam')
        category_matched = True
        category_name = "Exam"
    elif any(word in words for word in event_keywords):
        notices = notices.filter(category__iexact='Event')
        category_matched = True
        category_name = "Event"
    elif any(word in words for word in placement_keywords):
        notices = notices.filter(category__iexact='Placement')
        category_matched = True
        category_name = "Placement"
    elif any(word in words for word in general_keywords):
        notices = notices.filter(category__iexact='General')
        category_matched = True
        category_name = "General"
        
    # Date based filtering
    date_matched = False
    if 'today' in words:
        now = timezone.now()
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + datetime.timedelta(days=1)
        notices = notices.filter(date_posted__gte=start, date_posted__lt=end)
        date_matched = True
    elif 'week' in words or 'this week' in query:
        now = timezone.now()
        start = now - datetime.timedelta(days=now.weekday()) # Monday
        start = start.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + datetime.timedelta(days=7)
        notices = notices.filter(date_posted__gte=start, date_posted__lt=end)
        date_matched = True

    # 3. Database Search with Q objects for remaining words
    stop_words = {'what', 'is', 'the', 'when', 'how', 'show', 'me', 'notices', 'about', 'some', 'any', 'a', 'an', 'are', 'there', 'for', 'in', 'on', 'at', 'today', 'week', 'this', 'find', 'get', 'give', 'list'}
    search_words = [w for w in words if w not in stop_words and w not in exam_keywords + event_keywords + placement_keywords + general_keywords]
    
    if search_words:
        query_filter = Q()
        for word in search_words:
            # Flexible search across title, description, and category
            query_filter |= Q(title__icontains=word) | Q(description__icontains=word) | Q(category__icontains=word)
        notices = notices.filter(query_filter).distinct()
        
    # 4. Sort and limit to top 5
    notices = notices.order_by('-date_posted')[:5]
    
    if not notices.exists():
        # Fallback to latest notices if no strict match
        latest_notices = Notice.objects.all().order_by('-date_posted')[:3]
        if latest_notices.exists():
            results = []
            for n in latest_notices:
                results.append({
                    'title': n.title,
                    'description': (n.description[:100] + '...') if len(n.description) > 100 else n.description,
                    'date': n.date_posted.strftime("%Y-%m-%d"),
                    'category': n.category,
                    'url': f"/notice/{n.pk}/"
                })
            return {
                "message": "No matching notices found. Here are the latest notices instead:",
                "results": results
            }
        return {"message": "No matching notices found."}
        
    # Prepare successful response
    results = []
    for n in notices:
        results.append({
            'title': n.title,
            'description': (n.description[:100] + '...') if len(n.description) > 100 else n.description,
            'date': n.date_posted.strftime("%Y-%m-%d"),
            'category': n.category,
            'url': f"/notice/{n.pk}/"
        })
        
    # Construct an intelligent message
    if category_name and date_matched:
        msg = f"Here are the {category_name} notices for the requested timeframe:"
    elif category_name:
        msg = f"Here are the {category_name} notices:"
    elif date_matched:
        msg = "Here are the notices for the requested timeframe:"
    elif search_words:
        msg = f"Here are the notices matching '{' '.join(search_words)}':"
    else:
        msg = "Here are the latest notices:"

    return {
        "message": msg,
        "results": results
    }
