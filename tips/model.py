# tips/models.py
# Responsibility: Dhruv Patel - Sharing recycling tips & Displaying recycling tips
# Responsibility: Dharmik Patel - Saving favorite Tip & History management using session/cookie

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class TipCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Tip Categories'
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class RecyclingTip(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField()
    category = models.ForeignKey(TipCategory, on_delete=models.CASCADE, related_name='tips')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tips')
    image = models.ImageField(upload_to='tips/%Y/%m/%d/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['category']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while RecyclingTip.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    
    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])

class FavoriteTip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_tips')
    tip = models.ForeignKey(RecyclingTip, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'tip')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.tip.title}"