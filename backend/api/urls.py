from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, ProjectViewSet, ProjectImageViewSet,
    NewsViewSet, NewsImageViewSet, PublicationViewSet,
    ResourceViewSet, ContactFormViewSet, PartnershipFormViewSet,
    NewsletterSubscriptionViewSet, TeamMemberViewSet, PartnerViewSet,
    StatsViewSet, EventRegistrationViewSet, ExternalLinkViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'projects', ProjectViewSet)
router.register(r'project-images', ProjectImageViewSet)
router.register(r'news', NewsViewSet)
router.register(r'news-images', NewsImageViewSet)
router.register(r'publications', PublicationViewSet)
router.register(r'resources', ResourceViewSet)
router.register(r'contact', ContactFormViewSet)
router.register(r'partnership', PartnershipFormViewSet)
router.register(r'newsletter', NewsletterSubscriptionViewSet)
router.register(r'team', TeamMemberViewSet)
router.register(r'partners', PartnerViewSet)

router.register(r'stats', StatsViewSet, basename='stats')
router.register(r'event-registrations', EventRegistrationViewSet)
router.register(r'external-links', ExternalLinkViewSet)

urlpatterns = [
    path('', include(router.urls)),
] 