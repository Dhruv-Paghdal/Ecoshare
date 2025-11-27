from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from items.models import Item, Category
from centers.models import RecyclingCenter
from tips.models import RecyclingTip, FavoriteTip

def home(request):
    featured_items = Item.objects.filter(status=Item.STATUS_AVAILABLE)[:3]
    featured_tips = RecyclingTip.objects.filter(is_featured=True)[:3]
    recent_tips = RecyclingTip.objects.all().order_by('-created_at')[:3]
    context = {
        'featured_items': featured_items,
        'featured_tips': featured_tips,
        'recent_tips': recent_tips,
        'item_categories': Category.objects.count(),
        'total_items': Item.objects.filter(status=Item.STATUS_AVAILABLE).count(),
        'total_tips': RecyclingTip.objects.count(),
        'total_centers': RecyclingCenter.objects.count(),
    }
    return render(request, 'core/home.html', context)

@login_required 
def dashboard(request):    
    user_items = Item.objects.filter(owner=request.user).order_by('-created_at')[:5]
    user_tips = RecyclingTip.objects.filter(author=request.user).order_by('-created_at')[:5]
    favorite_tips = FavoriteTip.objects.filter(user=request.user).select_related('tip').order_by('-created_at')[:5]

    context = {
        'user_items': user_items,
        'user_tips': user_tips,
        'favorite_tips': favorite_tips,
        'total_user_items': Item.objects.filter(owner=request.user).count(),
        'total_user_tips': RecyclingTip.objects.filter(author=request.user).count(),
        'total_favorites': FavoriteTip.objects.filter(user=request.user).count(),
    }
    return render(request, 'core/dashboard.html', context)

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')

def tips(request):
    return render(request, 'core/contact.html')