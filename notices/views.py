from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, Http404
from django.contrib import messages
from django.db.models import Q
from .models import Notice
import datetime

@login_required
def home(request):
    category = request.GET.get('category')
    search = request.GET.get('search')
    
    notices = Notice.objects.all()
    if category:
        notices = notices.filter(category=category)
    if search:
        notices = notices.filter(Q(title__icontains=search) | Q(description__icontains=search))
        
    notices = notices.order_by('-date_posted')
        
    context = {
        'notices': notices,
        'category': category
    }
    return render(request, 'notices/home.html', context)

@login_required
def notice_detail(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    return render(request, 'notices/detail.html', {'notice': notice})

@login_required
def dashboard(request):
    notices = Notice.objects.filter(posted_by=request.user.username).order_by('-date_posted')
    return render(request, 'notices/dashboard.html', {'notices': notices})

@login_required
def add_notice(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category = request.POST.get('category')
        
        if title and description and category:
            Notice.objects.create(
                title=title,
                description=description,
                category=category,
                posted_by=request.user.username
            )
            messages.success(request, 'Notice posted successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please fill all fields.')
            
    return render(request, 'notices/add_notice.html')

@login_required
def edit_notice(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    
    if notice.posted_by != request.user.username and not request.user.is_superuser:
        messages.error(request, 'You do not have permission to edit this notice.')
        return redirect('dashboard')
        
    if request.method == 'POST':
        notice.title = request.POST.get('title')
        notice.description = request.POST.get('description')
        notice.category = request.POST.get('category')
        notice.save()
        messages.success(request, 'Notice updated successfully!')
        return redirect('dashboard')
        
    return render(request, 'notices/edit_notice.html', {'notice': notice})

@login_required
def delete_notice(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    
    if notice.posted_by == request.user.username or request.user.is_superuser:
        notice.delete()
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
