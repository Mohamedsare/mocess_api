from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.utils import timezone
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import (
    Category, Project, ProjectImage, News, NewsImage, Publication, 
    Resource, ContactForm, PartnershipForm, NewsletterSubscription,
    TeamMember, Partner, EventRegistration, ExternalLink
)
from .serializers import (
    CategorySerializer, ProjectSerializer, ProjectImageSerializer,
    NewsSerializer, NewsImageSerializer, PublicationSerializer,
    ResourceSerializer, ContactFormSerializer, PartnershipFormSerializer,
    NewsletterSubscriptionSerializer, TeamMemberSerializer, PartnerSerializer,
    ContactFormSubmitSerializer, PartnershipFormSubmitSerializer,
    NewsletterSubscriptionSubmitSerializer, EventRegistrationSerializer,
    ExternalLinkSerializer
)

# Vue d'accueil simple
@csrf_exempt
def home_view(request):
    """Vue d'accueil pour la racine du site"""
    html_content = """
    <!DOCTYPE html>
    <html lang="fr">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>MOCESS - API Backend</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                margin: 0;
                padding: 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                min-height: 100vh;
            }
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: rgba(255, 255, 255, 0.1);
                padding: 30px;
                border-radius: 15px;
                backdrop-filter: blur(10px);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            }
            h1 {
                text-align: center;
                color: #fff;
                margin-bottom: 10px;
                font-size: 2.5em;
            }
            .subtitle {
                text-align: center;
                color: #e0e0e0;
                margin-bottom: 30px;
                font-size: 1.2em;
            }
            .section {
                margin-bottom: 30px;
                padding: 20px;
                background: rgba(255, 255, 255, 0.05);
                border-radius: 10px;
            }
            .section h2 {
                color: #4ade80;
                margin-bottom: 15px;
                border-bottom: 2px solid #4ade80;
                padding-bottom: 5px;
            }
            .endpoint {
                background: rgba(0, 0, 0, 0.2);
                padding: 10px;
                margin: 5px 0;
                border-radius: 5px;
                font-family: 'Courier New', monospace;
            }
            .link {
                color: #4ade80;
                text-decoration: none;
                font-weight: bold;
            }
            .link:hover {
                text-decoration: underline;
            }
            .warning {
                background: rgba(255, 193, 7, 0.2);
                border: 1px solid #ffc107;
                padding: 15px;
                border-radius: 5px;
                margin: 20px 0;
            }
            .success {
                background: rgba(40, 167, 69, 0.2);
                border: 1px solid #28a745;
                padding: 15px;
                border-radius: 5px;
                margin: 20px 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>MOCESS</h1>
            <p class="subtitle">Centre Marocain des Études et de Recherches sur le Développement Durable</p>
            
            <div class="success">
                <strong>✅ Backend Django opérationnel !</strong><br>
                L'API REST est prête à recevoir des requêtes.
            </div>
            
            <div class="section">
                <h2>🔗 Liens utiles</h2>
                <p><a href="/admin/" class="link">📊 Interface d'administration Django</a></p>
                <p><a href="/api/" class="link">🔌 API REST - Documentation</a></p>
                <p><a href="http://localhost:5173" class="link">🎨 Frontend React (démarrez avec npm run dev)</a></p>
            </div>
            
            <div class="section">
                <h2>📡 Endpoints API disponibles</h2>
                <div class="endpoint">GET /api/projects/</div>
                <div class="endpoint">GET /api/news/</div>
                <div class="endpoint">GET /api/publications/</div>
                <div class="endpoint">GET /api/resources/</div>
                <div class class="endpoint">GET /api/team/</div>
                <div class="endpoint">GET /api/partners/</div>
                <div class="endpoint">POST /api/contact/</div>
                <div class="endpoint">POST /api/partnership/</div>
                <div class="endpoint">POST /api/newsletter/</div>
                <div class="endpoint">POST /api/event-registrations/</div>
                <div class="endpoint">GET /api/stats/dashboard/</div>
            </div>
            
            <div class="warning">
                <strong>⚠️ Important :</strong><br>
                Pour accéder au site complet, démarrez aussi le frontend React :<br>
                <code>cd Frontend && npm run dev</code><br>
                Puis allez sur <a href="http://localhost:5173" class="link">http://localhost:5173</a>
            </div>
            
            <div class="section">
                <h2>📚 Documentation</h2>
                <p>Consultez le fichier README.md pour plus d'informations sur l'installation et l'utilisation.</p>
            </div>
        </div>
    </body>
    </html>
    """
    from django.http import HttpResponse
    return HttpResponse(html_content)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'description']

class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.filter(is_featured=True)
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'category', 'is_featured']
    search_fields = ['title', 'description', 'theme']

    def get_queryset(self):
        queryset = Project.objects.all()
        status_filter = self.request.query_params.get('status', None)
        category_filter = self.request.query_params.get('category', None)
        featured_filter = self.request.query_params.get('featured', None)
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if category_filter:
            queryset = queryset.filter(category__slug=category_filter)
        if featured_filter:
            queryset = queryset.filter(is_featured=True)
            
        return queryset

    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured_projects = self.queryset.filter(is_featured=True)
        serializer = self.get_serializer(featured_projects, many=True)
        return Response(serializer.data)

class ProjectImageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ProjectImage.objects.all()
    serializer_class = ProjectImageSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project']

class NewsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = News.objects.filter(is_published=True)
    serializer_class = NewsSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['news_type', 'is_featured', 'is_published']
    search_fields = ['title', 'description', 'content']

    def get_queryset(self):
        queryset = News.objects.filter(is_published=True)
        news_type = self.request.query_params.get('type', None)
        featured = self.request.query_params.get('featured', None)
        
        if news_type:
            queryset = queryset.filter(news_type=news_type)
        if featured:
            queryset = queryset.filter(is_featured=True)
            
        return queryset.order_by('-event_date')

    @action(detail=False, methods=['get'])
    def recent(self, request):
        recent_news = self.queryset.filter(
            event_date__gte=timezone.now() - timezone.timedelta(days=30)
        )[:5]
        serializer = self.get_serializer(recent_news, many=True)
        return Response(serializer.data)

class NewsImageViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NewsImage.objects.all()
    serializer_class = NewsImageSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['news']

class PublicationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Publication.objects.filter(is_published=True)
    serializer_class = PublicationSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['publication_type', 'is_published']
    search_fields = ['title', 'abstract', 'authors', 'keywords']

    def get_queryset(self):
        queryset = Publication.objects.filter(is_published=True)
        pub_type = self.request.query_params.get('type', None)
        
        if pub_type:
            queryset = queryset.filter(publication_type=pub_type)
            
        return queryset.order_by('-publication_date')

class ResourceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Resource.objects.filter(is_public=True)
    serializer_class = ResourceSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['resource_type', 'category', 'is_public']
    search_fields = ['title', 'description']

    def get_queryset(self):
        queryset = Resource.objects.filter(is_public=True)
        resource_type = self.request.query_params.get('type', None)
        category = self.request.query_params.get('category', None)
        
        if resource_type:
            queryset = queryset.filter(resource_type=resource_type)
        if category:
            queryset = queryset.filter(category__slug=category)
            
        return queryset

    @action(detail=True, methods=['post'])
    def download(self, request, pk=None):
        resource = self.get_object()
        resource.download_count += 1
        resource.save()
        return Response({'message': 'Download count updated'})

class ContactFormViewSet(viewsets.ModelViewSet):
    queryset = ContactForm.objects.all()
    serializer_class = ContactFormSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get', 'post', 'head', 'options']

    def get_serializer_class(self):
        if self.action == 'create':
            return ContactFormSubmitSerializer
        return ContactFormSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Votre message a été envoyé avec succès. Nous vous répondrons dans les plus brefs délais.'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PartnershipFormViewSet(viewsets.ModelViewSet):
    queryset = PartnershipForm.objects.all()
    serializer_class = PartnershipFormSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get', 'post', 'head', 'options']

    def get_serializer_class(self):
        if self.action == 'create':
            return PartnershipFormSubmitSerializer
        return PartnershipFormSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Votre demande de partenariat a été envoyée avec succès. Nous vous contacterons rapidement.'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NewsletterSubscriptionViewSet(viewsets.ModelViewSet):
    queryset = NewsletterSubscription.objects.all()
    serializer_class = NewsletterSubscriptionSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get', 'post', 'head', 'options']

    def get_serializer_class(self):
        if self.action == 'create':
            return NewsletterSubscriptionSubmitSerializer
        return NewsletterSubscriptionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            subscription, created = NewsletterSubscription.objects.get_or_create(
                email=email,
                defaults={'is_active': True}
            )
            if not created and not subscription.is_active:
                subscription.is_active = True
                subscription.unsubscribed_at = None
                subscription.save()
            
            return Response({
                'message': 'Vous avez été inscrit avec succès à notre newsletter !'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def unsubscribe(self, request):
        email = request.data.get('email')
        if email:
            try:
                subscription = NewsletterSubscription.objects.get(email=email)
                subscription.is_active = False
                subscription.unsubscribed_at = timezone.now()
                subscription.save()
                return Response({
                    'message': 'Vous avez été désinscrit de notre newsletter.'
                })
            except NewsletterSubscription.DoesNotExist:
                return Response({
                    'error': 'Email non trouvé.'
                }, status=status.HTTP_404_NOT_FOUND)
        return Response({
            'error': 'Email requis.'
        }, status=status.HTTP_400_BAD_REQUEST)

class TeamMemberViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TeamMember.objects.filter(is_active=True)
    serializer_class = TeamMemberSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'position', 'bio']

class PartnerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Partner.objects.filter(is_active=True)
    serializer_class = PartnerSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['partner_type']
    search_fields = ['name', 'description']

class EventRegistrationViewSet(viewsets.ModelViewSet):
    queryset = EventRegistration.objects.all()
    serializer_class = EventRegistrationSerializer
    permission_classes = [AllowAny]
    http_method_names = ['get', 'post', 'head', 'options']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': "Votre inscription a bien été enregistrée. Nous vous contacterons si besoin."
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Vues pour les statistiques
class StatsViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        total_projects = Project.objects.count()
        active_projects = Project.objects.filter(status='en_cours').count()
        total_news = News.objects.filter(is_published=True).count()
        total_publications = Publication.objects.filter(is_published=True).count()
        total_resources = Resource.objects.filter(is_public=True).count()
        total_team_members = TeamMember.objects.filter(is_active=True).count()
        total_partners = Partner.objects.filter(is_active=True).count()
        
        return Response({
            'total_projects': total_projects,
            'active_projects': active_projects,
            'total_news': total_news,
            'total_publications': total_publications,
            'total_resources': total_resources,
            'total_team_members': total_team_members,
            'total_partners': total_partners,
        })

class ExternalLinkViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ExternalLink.objects.filter(is_active=True)
    serializer_class = ExternalLinkSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']
    search_fields = ['title', 'description']
    ordering = ['order', 'title']

    def get_queryset(self):
        return ExternalLink.objects.filter(is_active=True).order_by('order', 'title')
