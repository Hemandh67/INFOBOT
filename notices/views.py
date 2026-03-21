from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, Http404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Notice
import datetime
from django.contrib.auth import logout

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. Welcome!')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

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

def notice_detail(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    return render(request, 'notices/detail.html', {'notice': notice})

def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff)

@user_passes_test(is_admin)
def dashboard(request):
    notices = Notice.objects.all().order_by('-date_posted')
    return render(request, 'notices/dashboard.html', {'notices': notices})

def is_admin(user):
    return user.is_authenticated and (user.is_superuser or user.is_staff)

@user_passes_test(is_admin)
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

@user_passes_test(is_admin)
def edit_notice(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    
    if request.method == 'POST':
        notice.title = request.POST.get('title')
        notice.description = request.POST.get('description')
        notice.category = request.POST.get('category')
        notice.save()
        messages.success(request, 'Notice updated successfully!')
        return redirect('dashboard')
        
    return render(request, 'notices/edit_notice.html', {'notice': notice})

@user_passes_test(is_admin)
def delete_notice(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    notice.delete()
    messages.success(request, 'Notice deleted successfully!')
            
    return redirect('dashboard')

from .chatbot import get_chat_response

def chatbot_api(request):
    query = request.GET.get('query', '')
    if query:
        results = get_chat_response(query)
        return JsonResponse({'results': results, 'status': 'success'})
    return JsonResponse({'results': [], 'status': 'no_query'})

def custom_logout(request):
    logout(request)
    messages.info(request, "You have been completely logged out.")
    return redirect('home')
