from django.contrib import admin
from .models import (
    Service, PriceCategory, Price, GalleryImage, 
    FAQ, Testimonial, ContactMessage, SiteConfiguration, News, CustomerProfile
)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']
    ordering = ['order', 'title']


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description']
    list_editable = ['order', 'is_active']
    ordering = ['order', '-created_at']


class PriceInline(admin.TabularInline):
    model = Price
    extra = 1
    fields = ['item_name', 'description', 'amount', 'is_free', 'order', 'is_active']


@admin.register(PriceCategory)
class PriceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    inlines = [PriceInline]


@admin.register(Price)
class PriceAdmin(admin.ModelAdmin):
    list_display = ['item_name', 'category', 'amount', 'is_free', 'is_active', 'updated_at']
    list_filter = ['category', 'is_active', 'is_free']
    search_fields = ['item_name', 'description']
    list_editable = ['amount', 'is_free', 'is_active']


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active', 'uploaded_at']
    list_filter = ['is_active', 'uploaded_at']
    search_fields = ['title', 'description', 'alt_text']
    list_editable = ['order', 'is_active']
    readonly_fields = ['uploaded_at']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'order', 'is_active', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['question', 'answer']
    list_editable = ['order', 'is_active']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'is_featured', 'is_active', 'created_at']
    list_filter = ['rating', 'is_featured', 'is_active', 'created_at']
    search_fields = ['name', 'text']
    list_editable = ['rating', 'is_featured', 'is_active']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['full_name', 'email', 'phone', 'message']
    list_editable = ['is_read']
    readonly_fields = ['created_at']
    
    def has_add_permission(self, request):
        return False


@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Información General', {
            'fields': ('site_name', 'tagline', 'hero_image')
        }),
        ('Contacto', {
            'fields': ('phone', 'email', 'address', 'opening_hours')
        }),
        ('Redes Sociales', {
            'fields': ('instagram_url', 'facebook_url')
        }),
        ('Alertas', {
            'fields': ('special_alert', 'is_alert_active')
        }),
    )
    
    def has_add_permission(self, request):
        # Only one configuration allowed
        return not SiteConfiguration.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'birth_date', 'dni', 'phone', 'created_at']
    search_fields = ['user__username', 'user__email', 'dni', 'phone']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']
