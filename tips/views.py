# tips/views.py
# Responsibility: Dhruv Patel - Sharing recycling tips & Displaying recycling tips
# Responsibility: Dharmik Patel - Saving favorite Tip & History management using session/cookie

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.http import JsonResponse
from .models import RecyclingTip, TipCategory, FavoriteTip
from .forms import RecyclingTipForm

class TipListView(ListView):
    model = RecyclingTip
    template_name = 'tips/tip_list.html'
    context_object_name = 'tips'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = RecyclingTip.objects.all().select_related('category', 'author')
        
        # Search by keyword
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query)
            )
        
        # Filter by category
        category_slug = self.request.GET.get('category', '')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = TipCategory.objects.all()
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_category'] = self.request.GET.get('category', '')
        context['featured_tips'] = RecyclingTip.objects.filter(is_featured=True)[:3]
        
        # Get user's favorite tips if logged in
        if self.request.user.is_authenticated:
            favorite_tip_ids = FavoriteTip.objects.filter(
                user=self.request.user
            ).values_list('tip_id', flat=True)
            context['favorite_tip_ids'] = list(favorite_tip_ids)
        else:
            context['favorite_tip_ids'] = []
        
        # Get recently viewed tips from session
        recently_viewed = self.request.session.get('recently_viewed_tips', [])
        if recently_viewed:
            context['recently_viewed_tips'] = RecyclingTip.objects.filter(
                id__in=recently_viewed
            )[:5]
        
        return context

class TipDetailView(DetailView):
    model = RecyclingTip
    template_name = 'tips/tip_detail.html'
    context_object_name = 'tip'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_object(self):
        obj = super().get_object()
        # Track view count
        if not self.request.user == obj.author:
            obj.increment_views()
        
        # Add to recently viewed in session
        recently_viewed = self.request.session.get('recently_viewed_tips', [])
        if obj.id in recently_viewed:
            recently_viewed.remove(obj.id)
        recently_viewed.insert(0, obj.id)
        self.request.session['recently_viewed_tips'] = recently_viewed[:10]
        self.request.session.modified = True
        
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_tips'] = RecyclingTip.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:4]
        
        # Check if user has favorited this tip
        if self.request.user.is_authenticated:
            context['is_favorited'] = FavoriteTip.objects.filter(
                user=self.request.user,
                tip=self.object
            ).exists()
        else:
            context['is_favorited'] = False
        
        return context

class TipCreateView(LoginRequiredMixin, CreateView):
    model = RecyclingTip
    form_class = RecyclingTipForm
    template_name = 'tips/tip_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Recycling tip created successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('tips:tip_detail', kwargs={'slug': self.object.slug})

class TipUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = RecyclingTip
    form_class = RecyclingTipForm
    template_name = 'tips/tip_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def test_func(self):
        return self.get_object().author == self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Recycling tip updated successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('tips:tip_detail', kwargs={'slug': self.object.slug})

class TipDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = RecyclingTip
    template_name = 'tips/tip_confirm_delete.html'
    success_url = reverse_lazy('core:dashboard')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def test_func(self):
        return self.get_object().author == self.request.user
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Recycling tip deleted successfully!')
        return super().delete(request, *args, **kwargs)

@login_required
def toggle_favorite(request, slug):
    tip = get_object_or_404(RecyclingTip, slug=slug)
    favorite, created = FavoriteTip.objects.get_or_create(user=request.user, tip=tip)
    
    if not created:
        favorite.delete()
        is_favorited = False
        message = 'Tip removed from favorites'
    else:
        is_favorited = True
        message = 'Tip added to favorites'
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'is_favorited': is_favorited,
            'message': message
        })
    else:
        messages.success(request, message)
        return redirect('tips:tip_detail', slug=slug)

@login_required
def my_tips(request):
    tips = RecyclingTip.objects.filter(author=request.user).select_related('category')
    return render(request, 'tips/my_tips.html', {'tips': tips})

@login_required
def favorite_tips(request):
    favorites = FavoriteTip.objects.filter(user=request.user).select_related('tip__category', 'tip__author')
    return render(request, 'tips/favorite_tips.html', {'favorites': favorites})

def clear_tip_history(request):
    request.session['recently_viewed_tips'] = []
    messages.success(request, 'Tip viewing history cleared!')
    return redirect('tips:tip_list')
