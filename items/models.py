from django.db import models
from django.utils.text import slugify
from django.conf import settings


class Category(models.Model):
	name = models.CharField(max_length=100, unique=True)
	slug = models.SlugField(max_length=120, unique=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['name']

	def __str__(self):
		return self.name

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		super().save(*args, **kwargs)


class Item(models.Model):
	CONDITION_NEW = 'new'
	CONDITION_USED = 'used'
	CONDITION_REFURB = 'refurb'
	CONDITION_CHOICES = [
		(CONDITION_NEW, 'New'),
		(CONDITION_USED, 'Used'),
		(CONDITION_REFURB, 'Refurbished'),
	]

	STATUS_AVAILABLE = 'available'
	STATUS_RESERVED = 'reserved'
	STATUS_COMPLETED = 'completed'
	STATUS_CHOICES = [
		(STATUS_AVAILABLE, 'Available'),
		(STATUS_RESERVED, 'Reserved'),
		(STATUS_COMPLETED, 'Completed'),
	]

	title = models.CharField(max_length=200)
	slug = models.SlugField(max_length=220, unique=True)
	description = models.TextField(blank=True)
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='items')
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='items')
	location = models.CharField(max_length=150, blank=True)
	condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, default=CONDITION_USED)
	status = models.CharField(max_length=12, choices=STATUS_CHOICES, default=STATUS_AVAILABLE)
	is_free = models.BooleanField(default=True)
	views = models.PositiveIntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		if not self.slug:
			base = slugify(self.title)[:200]
			slug = base
			counter = 1
			while Item.objects.filter(slug=slug).exists():
				slug = f"{base}-{counter}"
				counter += 1
			self.slug = slug
		super().save(*args, **kwargs)


class ItemImage(models.Model):
	item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='images')
	image = models.ImageField(upload_to='items/%Y/%m/%d/')
	is_primary = models.BooleanField(default=False)
	uploaded_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-is_primary', '-uploaded_at']

	def __str__(self):
		return f"Image for {self.item.title}"

