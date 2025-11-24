from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from .models import RecyclingCenter,CANADIAN_PROVINCES


class RecyclingCenterListView(LoginRequiredMixin, ListView):
    login_url = 'accounts:login'
    model = RecyclingCenter
    template_name = 'centers/center_list.html'
    context_object_name = 'centers'
    paginate_by = 15

    def get_queryset(self):
        queryset = RecyclingCenter.objects.all()

        # Search by keyword (name, city, address)
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(city__icontains=search_query) |
                Q(address__icontains=search_query) |
                Q(state__icontains=search_query) |
                Q(description__icontains=search_query)
            )

        # Filter by city
        city = self.request.GET.get('city', '')
        if city:
            queryset = queryset.filter(city__icontains=city)

        # Filter by state (now using abbreviation)
        state = self.request.GET.get('state', '')
        if state:
            # State is now stored as abbreviation, so direct match
            queryset = queryset.filter(state=state.upper())

        # Filter by zipcode
        zipcode = self.request.GET.get('zipcode', '')
        if zipcode:
            queryset = queryset.filter(zipcode__icontains=zipcode)

        # Filter by features
        if self.request.GET.get('dropoff') == 'on':
            queryset = queryset.filter(accepts_dropoff=True)
        if self.request.GET.get('pickup') == 'on':
            queryset = queryset.filter(offers_pickup=True)
        if self.request.GET.get('donations') == 'on':
            queryset = queryset.filter(accepts_donations=True)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['selected_city'] = self.request.GET.get('city', '')
        context['selected_state'] = self.request.GET.get('state', '')
        context['selected_zipcode'] = self.request.GET.get('zipcode', '')
        context['material_choices'] = RecyclingCenter.MATERIAL_CHOICES
        context['canadian_provinces'] = CANADIAN_PROVINCES

        # Get unique cities for filters
        all_centers = RecyclingCenter.objects.all()
        context['cities'] = all_centers.values_list('city', flat=True).distinct().order_by('city')

        return context


class RecyclingCenterDetailView(LoginRequiredMixin, DetailView):
    login_url = 'accounts:login'
    model = RecyclingCenter
    template_name = 'centers/center_detail.html'
    context_object_name = 'center'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['operating_hours'] = [
            ('Monday', self.object.monday_hours),
            ('Tuesday', self.object.tuesday_hours),
            ('Wednesday', self.object.wednesday_hours),
            ('Thursday', self.object.thursday_hours),
            ('Friday', self.object.friday_hours),
            ('Saturday', self.object.saturday_hours),
            ('Sunday', self.object.sunday_hours),
        ]

        # Get nearby centers (same city)
        context['nearby_centers'] = RecyclingCenter.objects.filter(
            city=self.object.city
        ).exclude(id=self.object.id)[:3]

        return context


@login_required(login_url='accounts:login')
def center_search(request):
    """Enhanced search view for recycling centers with state filter"""
    query = request.GET.get('q', '')
    location = request.GET.get('location', '')
    state = request.GET.get('state', '')

    centers = RecyclingCenter.objects.all()

    if query:
        centers = centers.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(city__icontains=query)
        )

    if location:
        centers = centers.filter(
            Q(city__icontains=location) |
            Q(zipcode__icontains=location)
        )

    if state:
        # State is now stored as abbreviation, so direct match
        centers = centers.filter(state=state.upper())

    #centers = centers.prefetch_related('materials')[:20]

    context = {
        'centers': centers,
        'query': query,
        'location': location,
        'selected_state': state,
        'canadian_provinces': CANADIAN_PROVINCES,
    }

    return render(request, 'centers/search_results.html', context)