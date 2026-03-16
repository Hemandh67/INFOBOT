from .utils import get_db_handle
from django.utils import timezone
import datetime

db, client = get_db_handle()
notices_collection = db['notices']

def get_chat_response(query):
    """
    Process user query and return matching notices using PyMongo.
    """
    query = query.lower().strip()
    
    filter_query = {}
    
    # Category based filtering
    if 'exam' in query:
        filter_query['category'] = 'Exam'
    elif 'event' in query:
        filter_query['category'] = 'Event'
    elif 'placement' in query:
        filter_query['category'] = 'Placement'
    elif 'general' in query:
        filter_query['category'] = 'General'
        
    # Date based filtering (simplistic)
    # Storing date as datetime object in Mongo
    if 'today' in query:
        now = datetime.datetime.now()
        start = datetime.datetime(now.year, now.month, now.day)
        end = start + datetime.timedelta(days=1)
        filter_query['date_posted'] = {'$gte': start, '$lt': end}
        
    # Search logic if no category/date found? 
    # Or maybe text search if query is specific?
    # For now, if no filters, return top 5 latest
    
    cursor = notices_collection.find(filter_query).sort('date_posted', -1).limit(5)
    
    response_data = []
    for n in cursor:
        response_data.append({
            'title': n['title'],
            'date': n['date_posted'].strftime("%Y-%m-%d"),
            'url': f"/notice/{str(n['_id'])}/"
        })
    
    return response_data
