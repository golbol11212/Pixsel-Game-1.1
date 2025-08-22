from django.db import models

class Header(models.Model):
    """Model for storing main header configuration"""
    site_name = models.CharField(max_length=50, default="PIXSGAME")
    brand_color = models.CharField(max_length=7, default="#ff00ff")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Header"
        verbose_name_plural = "Headers"

    def __str__(self):
        return f"{self.site_name} - {'Active' if self.is_active else 'Inactive'}"

class MenuItem(models.Model):
    """Model for storing navigation menu items"""
    header = models.ForeignKey(Header, on_delete=models.CASCADE, related_name='menu_items')
    title = models.CharField(max_length=50)
    url = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    css_class = models.CharField(max_length=50, blank=True, null=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = "Menu Item"
        verbose_name_plural = "Menu Items"

    def __str__(self):
        return f"{self.title} - {self.url}"
