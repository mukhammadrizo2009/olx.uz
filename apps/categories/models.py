from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    name = models.CharField(max_length=128)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.ImageField(
        upload_to='categories/logos/',
        blank=True, null=True
        )
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    order_num = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return f"{self.name}"
    

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)