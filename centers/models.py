from django.db import models

# Create your models here.
# centers/models.py
# Responsibility: Sakshi Patel - Searching based on keyword & Searching recycling center

from django.db import models
from django.utils.text import slugify


class RecyclingCenter(models.Model):
    MATERIAL_CHOICES = [
        ('paper', 'Paper'),
        ('plastic', 'Plastic'),
        ('glass', 'Glass'),
        ('metal', 'Metal'),
        ('electronics', 'Electronics'),
        ('batteries', 'Batteries'),
        ('textiles', 'Textiles'),
        ('organic', 'Organic Waste'),
        ('hazardous', 'Hazardous Materials'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='Canada')
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    # Operating hours
    monday_hours = models.CharField(max_length=50, blank=True, default='Closed')
    tuesday_hours = models.CharField(max_length=50, blank=True, default='Closed')
    wednesday_hours = models.CharField(max_length=50, blank=True, default='Closed')
    thursday_hours = models.CharField(max_length=50, blank=True, default='Closed')
    friday_hours = models.CharField(max_length=50, blank=True, default='Closed')
    saturday_hours = models.CharField(max_length=50, blank=True, default='Closed')
    sunday_hours = models.CharField(max_length=50, blank=True, default='Closed')

    # Features
    accepts_dropoff = models.BooleanField(default=True)
    offers_pickup = models.BooleanField(default=False)
    accepts_donations = models.BooleanField(default=False)

    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['city', 'name']
        indexes = [
            models.Index(fields=['city']),
            models.Index(fields=['state']),
            models.Index(fields=['zipcode']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while RecyclingCenter.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} - {self.city}"

    def get_full_address(self):
        return f"{self.address}, {self.city}, {self.state} {self.zipcode}"


class AcceptedMaterial(models.Model):
    center = models.ForeignKey(RecyclingCenter, on_delete=models.CASCADE, related_name='materials')
    material_type = models.CharField(max_length=50, choices=RecyclingCenter.MATERIAL_CHOICES)
    notes = models.TextField(blank=True, help_text='Special requirements or notes')

    class Meta:
        unique_together = ('center', 'material_type')

    def __str__(self):
        return f"{self.center.name} - {self.get_material_type_display()}"