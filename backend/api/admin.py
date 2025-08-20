from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Category, Project, ProjectImage, News, NewsImage, Publication, 
    Resource, ContactForm, PartnershipForm, NewsletterSubscription,
    TeamMember, Partner, EventRegistration, ExternalLink
)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ['image', 'caption', 'order']

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'start_date', 'end_date', 'is_featured', 'created_at']
    list_filter = ['status', 'is_featured', 'category', 'start_date', 'created_at']
    search_fields = ['title', 'description', 'theme']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline]
    filter_horizontal = []
    date_hierarchy = 'start_date'

@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ['project', 'caption', 'order', 'created_at']
    list_filter = ['project', 'created_at']
    search_fields = ['project__title', 'caption']

class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 1
    fields = ['image', 'caption', 'order']

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'news_type', 'event_date', 'is_published', 'is_featured', 'created_at']
    list_filter = ['news_type', 'is_published', 'is_featured', 'event_date', 'created_at']
    search_fields = ['title', 'description', 'content']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [NewsImageInline]
    date_hierarchy = 'event_date'

@admin.register(NewsImage)
class NewsImageAdmin(admin.ModelAdmin):
    list_display = ['news', 'caption', 'order', 'created_at']
    list_filter = ['news', 'created_at']
    search_fields = ['news__title', 'caption']

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ['title', 'publication_type', 'publication_date', 'is_published', 'created_at']
    list_filter = ['publication_type', 'is_published', 'publication_date', 'created_at']
    search_fields = ['title', 'abstract', 'authors', 'keywords']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publication_date'

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'resource_type', 'category', 'is_public', 'download_count', 'created_at']
    list_filter = ['resource_type', 'is_public', 'category', 'created_at']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at']
    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Marquer comme lu"

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = "Marquer comme non lu"

@admin.register(PartnershipForm)
class PartnershipFormAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'organization', 'is_processed', 'created_at']
    list_filter = ['is_processed', 'created_at']
    search_fields = ['name', 'email', 'organization', 'message']
    readonly_fields = ['created_at']
    actions = ['mark_as_processed', 'mark_as_unprocessed']

    def mark_as_processed(self, request, queryset):
        queryset.update(is_processed=True)
    mark_as_processed.short_description = "Marquer comme traité"

    def mark_as_unprocessed(self, request, queryset):
        queryset.update(is_processed=False)
    mark_as_unprocessed.short_description = "Marquer comme non traité"

@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['email', 'is_active', 'subscribed_at', 'unsubscribed_at']
    list_filter = ['is_active', 'subscribed_at', 'unsubscribed_at']
    search_fields = ['email']
    readonly_fields = ['subscribed_at', 'unsubscribed_at']
    actions = ['activate_subscriptions', 'deactivate_subscriptions']

    def activate_subscriptions(self, request, queryset):
        queryset.update(is_active=True, unsubscribed_at=None)
    activate_subscriptions.short_description = "Activer les abonnements"

    def deactivate_subscriptions(self, request, queryset):
        from django.utils import timezone
        queryset.update(is_active=False, unsubscribed_at=timezone.now())
    deactivate_subscriptions.short_description = "Désactiver les abonnements"

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'is_active', 'order', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'position', 'bio']
    list_editable = ['order', 'is_active']

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'partner_type', 'is_active', 'order', 'created_at']
    list_filter = ['partner_type', 'is_active', 'created_at']
    search_fields = ['name', 'description']
    list_editable = ['order', 'is_active']

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'created_at']
    search_fields = ['name', 'email', 'phone', 'message']
    list_filter = ['created_at']
    readonly_fields = ['created_at']



@admin.register(ExternalLink)
class ExternalLinkAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'url', 'is_active', 'order', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'url']
    list_editable = ['order', 'is_active']
    ordering = ['order', 'title']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('title', 'url', 'description', 'category')
        }),
        ('Affichage', {
            'fields': ('icon', 'is_active', 'order')
        }),
    )

# Configuration de l'admin
admin.site.site_header = "Administration MOCESS"
admin.site.site_title = "MOCESS Admin"
admin.site.index_title = "Bienvenue dans l'administration MOCESS"
