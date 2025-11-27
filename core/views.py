from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from items.models import Item, Category
from centers.models import RecyclingCenter

def home(request):
    featured_items = Item.objects.filter(status=Item.STATUS_AVAILABLE)[:3]
    featured_tips = [] #Tip.objects.filter()[:3]
    recent_tips = []  # Add: Tip.objects.all().order_by('-created_at')[:3] when tips model exists
    context = {
        'featured_items': featured_items,
        'featured_tips': featured_tips,
        'recent_tips': recent_tips,
        'item_categories': Category.objects.count(),
        'total_items': Item.objects.filter(status=Item.STATUS_AVAILABLE).count(),
        'total_tips': 20, #Tip.objects.count() 
        'total_centers': RecyclingCenter.objects.count(),
    }
    return render(request, 'core/home.html', context)

@login_required 
def dashboard(request):    
    user_items = Item.objects.filter(owner=request.user).order_by('-created_at')[:5]
    context = {
        'user_items': user_items,
        'user_tips': ['Tips-1', 'Tips-2'],
        'favorite_tips': ['Favorite-Tips-1', 'Favorite-Tips-2'],
        'total_user_items': Item.objects.filter(owner=request.user).count(),
        'total_user_tips': 10,
        'total_favorites': 6,
    }
    return render(request, 'core/dashboard.html', context)

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')

def tips(request):
    return render(request, 'core/contact.html')