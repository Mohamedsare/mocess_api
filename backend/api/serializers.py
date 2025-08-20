from rest_framework import serializers
from .models import (
    Category, Project, ProjectImage, News, NewsImage, Publication, 
    Resource, ContactForm, PartnershipForm, NewsletterSubscription,
    TeamMember, Partner, EventRegistration, ExternalLink
)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImage
        fields = ['id', 'image', 'caption', 'order']

class ProjectSerializer(serializers.ModelSerializer):
    images = ProjectImageSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Project
        fields = '__all__'

class NewsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsImage
        fields = ['id', 'image', 'caption', 'order']

class NewsSerializer(serializers.ModelSerializer):
    images = NewsImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = News
        fields = '__all__'

class PublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = '__all__'

class ResourceSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Resource
        fields = '__all__'

class ContactFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactForm
        fields = '__all__'
        read_only_fields = ['is_read', 'created_at']

class PartnershipFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnershipForm
        fields = '__all__'
        read_only_fields = ['is_processed', 'created_at']

class NewsletterSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscription
        fields = '__all__'
        read_only_fields = ['is_active', 'subscribed_at', 'unsubscribed_at']

class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = '__all__'

class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = '__all__'

class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRegistration
        fields = '__all__'
        read_only_fields = ['created_at']



class ExternalLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExternalLink
        fields = ['id', 'title', 'url', 'description', 'category', 'icon', 'order']

# Sérialiseurs pour les formulaires de soumission
class ContactFormSubmitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactForm
        fields = ['name', 'email', 'subject', 'message', 'phone', 'organization']

class PartnershipFormSubmitSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartnershipForm
        fields = ['name', 'email', 'organization', 'position', 'phone', 'website', 'partnership_type', 'message']

class NewsletterSubscriptionSubmitSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsletterSubscription
        fields = ['email'] 