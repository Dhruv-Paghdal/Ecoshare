# items/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Item, Category
from .forms import ItemForm, ItemImageFormSet

class ItemListView(ListView):
    model = Item
    template_name = 'items/item_list.html'
    context_object_name = 'items'
    paginate_by = 12

    def get_queryset(self):
        # Filter for available items by default
        queryset = Item.objects.filter(status=Item.STATUS_AVAILABLE).select_related('category', 'owner')
        
        # Search by keyword
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(location__icontains=search_query)
            )
        
        # Filter by category
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # Filter by condition
        condition = self.request.GET.get('condition')
        if condition:
            queryset = queryset.filter(condition=condition)

        # Filter by type (Free vs Trade)
        item_type = self.request.GET.get('type')
        if item_type == 'free':
            queryset = queryset.filter(is_free=True)
        elif item_type == 'trade':
            queryset = queryset.filter(is_free=False)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # 1. Pass Categories for the dropdown
        context['categories'] = Category.objects.all()
        
        # 2. Pass Condition Choices for the dropdown (THIS WAS MISSING)
        context['condition_choices'] = Item.CONDITION_CHOICES
        
        # 3. Preserve the user's search inputs so they don't disappear after clicking search
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_condition'] = self.request.GET.get('condition', '')
        context['selected_type'] = self.request.GET.get('type', '')
        
        return context

class ItemDetailView(DetailView):
    model = Item
    template_name = 'items/item_detail.html'
    context_object_name = 'item'
    
    def get_object(self):
        obj = super().get_object()
        # Increment view count
        if self.request.user != obj.owner:
            obj.views += 1
            obj.save(update_fields=['views'])
        return obj

class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'items/item_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = ItemImageFormSet(self.request.POST, self.request.FILES)
        else:
            context['image_formset'] = ItemImageFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']
        
        if image_formset.is_valid():
            form.instance.owner = self.request.user
            self.object = form.save()
            image_formset.instance = self.object
            image_formset.save()
            messages.success(self.request, 'Item listed successfully!')
            return redirect('items:item_detail', slug=self.object.slug)
        
        return self.render_to_response(self.get_context_data(form=form))

class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    form_class = ItemForm
    template_name = 'items/item_form.html'

    def test_func(self):
        return self.request.user == self.get_object().owner

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['image_formset'] = ItemImageFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['image_formset'] = ItemImageFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        image_formset = context['image_formset']
        
        if image_formset.is_valid():
            self.object = form.save()
            image_formset.save()
            messages.success(self.request, 'Item updated successfully!')
            return redirect('items:item_detail', slug=self.object.slug)
        
        return self.render_to_response(self.get_context_data(form=form))

class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item
    template_name = 'items/item_confirm_delete.html'
    success_url = reverse_lazy('items:my_items')

    def test_func(self):
        return self.request.user == self.get_object().owner

@login_required
def my_items(request):
    items = Item.objects.filter(owner=request.user)
    return render(request, 'items/my_items.html', {'items': items})