from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.contrib import messages
from .utils import get_db_handle
from bson.objectid import ObjectId
import datetime

# Get MongoDB handle
db, client = get_db_handle()
notices_collection = db['notices']

@login_required
def home(request):
    category = request.GET.get('category')
    search = request.GET.get('search')
    
    filter_query = {}
    if category:
        filter_query['category'] = category
    
    if search:
        # Simple regex search
        filter_query['$or'] = [
            {'title': {'$regex': search, '$options': 'i'}},
            {'description': {'$regex': search, '$options': 'i'}}
        ]
        
    # MongoDB cursor to list
    notices_cursor = notices_collection.find(filter_query).sort('date_posted', -1)
    notices = []
    
    for n in notices_cursor:
        n['pk'] = str(n['_id']) # Manual mapping of _id to pk for templates
        notices.append(n)
        
    context = {
        'notices': notices,
        'category': category
    }
    return render(request, 'notices/home.html', context)

@login_required
def notice_detail(request, pk):
    try:
        notice = notices_collection.find_one({'_id': ObjectId(pk)})
    except:
        raise Http404("Invalid Notice ID")
        
    if not notice:
        raise Http404("Notice not found")
        
    notice['pk'] = str(notice['_id'])
    return render(request, 'notices/detail.html', {'notice': notice})

@login_required
def dashboard(request):
    # Admin/Faculty dashboard
    # Filter by username (posted_by is stored as username string or ID)
    # We'll store posted_by as username for simplicity in PyMongo
    
    notices_cursor = notices_collection.find({'posted_by': request.user.username}).sort('date_posted', -1)
    notices = []
    for n in notices_cursor:
        n['pk'] = str(n['_id'])
        notices.append(n)
        
    return render(request, 'notices/dashboard.html', {'notices': notices})

@login_required
def add_notice(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category = request.POST.get('category')
        
        if title and description and category:
            notice_data = {
                'title': title,
                'description': description,
                'category': category,
                'posted_by': request.user.username,
                'date_posted': datetime.datetime.now()
            }
            notices_collection.insert_one(notice_data)
            messages.success(request, 'Notice posted successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please fill all fields.')
            
    return render(request, 'notices/add_notice.html')

@login_required
def edit_notice(request, pk):
    try:
        notice = notices_collection.find_one({'_id': ObjectId(pk)})
    except:
        messages.error(request, 'Invalid Notice ID')
        return redirect('dashboard')

    if not notice:
        messages.error(request, 'Notice not found')
        return redirect('dashboard')
    
    # Check permissions
    if notice['posted_by'] != request.user.username and not request.user.is_superuser:
        messages.error(request, 'You do not have permission to edit this notice.')
        return redirect('dashboard')
        
    if request.method == 'POST':
        update_data = {
            'title': request.POST.get('title'),
            'description': request.POST.get('description'),
            'category': request.POST.get('category')
        }
        notices_collection.update_one({'_id': ObjectId(pk)}, {'$set': update_data})
        messages.success(request, 'Notice updated successfully!')
        return redirect('dashboard')
        
    notice['pk'] = str(notice['_id'])
    return render(request, 'notices/edit_notice.html', {'notice': notice})

@login_required
def delete_notice(request, pk):
    try:
        notice = notices_collection.find_one({'_id': ObjectId(pk)})
    except:
        messages.error(request, 'Invalid ID')
        return redirect('dashboard')

    if notice:
        if notice['posted_by'] == request.user.username or request.user.is_superuser:
            notices_collection.delete_one({'_id': ObjectId(pk)})
            messages.success(request, 'Notice deleted successfully!')
        else:
            messages.error(request, 'Permission denied.')
            
    return redirect('dashboard')

from .chatbot import get_chat_response

@login_required
def chatbot_api(request):
    query = request.GET.get('query', '')
    if query:
        results = get_chat_response(query)
        return JsonResponse({'results': results, 'status': 'success'})
    return JsonResponse({'results': [], 'status': 'no_query'})
