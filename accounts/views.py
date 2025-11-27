from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import UserRegistrationForm, UserProfileForm, PasswordResetRequestForm
from django.contrib.auth.models import User
from items.models import Item
from tips.models import RecyclingTip

class RegisterView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Account created successfully! Please login.')
        return response

def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                next_url = request.GET.get('next', 'core:dashboard')
                return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('core:home')

def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data.get('identifier')
            # Store the identifier in session to use in the next step
            request.session['reset_identifier'] = identifier
            return redirect('accounts:password_reset_confirm')
    else:
        form = PasswordResetRequestForm()
    
    return render(request, 'accounts/password_reset.html', {'form': form})

def password_reset_confirm(request):
    identifier = request.session.get('reset_identifier')
    
    if not identifier:
        messages.error(request, 'Please enter your username or email first.')
        return redirect('accounts:password_reset')
    
    try:
        if '@' in identifier:
            user = User.objects.get(email=identifier)
        else:
            user = User.objects.get(username=identifier)
    except User.DoesNotExist:
        messages.error(request, 'No user found with that username or email.')
        del request.session['reset_identifier']
        return redirect('accounts:password_reset')
    
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            # Clear the session
            del request.session['reset_identifier']
            messages.success(request, 'Your password has been reset successfully! Please login with your new password.')
            return redirect('accounts:login')
    else:
        form = SetPasswordForm(user)
    
    return render(request, 'accounts/password_reset_confirm.html', {
        'form': form,
        'username': user.username
    })

@login_required
@login_required
def profile_view(request):
    
    recent_items = Item.objects.filter(owner=request.user).order_by('-created_at')[:5]
    recent_tips = RecyclingTip.objects.filter(author=request.user).order_by('-created_at')[:5]
    
    return render(request, 'accounts/profile.html', {
        'user': request.user,
        'recent_items': recent_items,
        'recent_tips': recent_tips
    })

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user.profile)
    
    return render(request, 'accounts/profile_edit.html', {'form': form})