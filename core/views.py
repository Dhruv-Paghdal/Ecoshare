from django.shortcuts import render

def home(request):
    context = {
        'featured_items': ['Featured-Items-1', 'Featured-Items-2'],
        'featured_tips': ['Featured-Tips-1', 'Featured-Tips-2'],
        'recent_tips': ['Recent-Tips-1', 'Recent-Tips-2'],
        'item_categories': 5,
        'total_items': 25,
        'total_tips': 20,
        'total_centers': 10,
    }
    return render(request, 'core/home.html', context)

def dashboard(request):    
    context = {
        'user_items': ['Items-1', 'Itmes-2'],
        'user_tips': ['Tips-1', 'Tips-2'],
        'favorite_tips': ['Favorite-Tips-1', 'Favorite-Tips-2'],
        'recently_viewed_items': ['Viewed-Items-1', 'Viewed-Items-2'],
        'recently_viewed_tips': ['Viewed-Tips-1', 'Viewed-Tips-2'],
        'total_user_items': 15,
        'total_user_tips': 10,
        'total_favorites': 6,
    }
    return render(request, 'core/dashboard.html', context)

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')