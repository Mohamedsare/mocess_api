from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator

class Category(models.Model):
    """Modèle pour les catégories (projets, actualités, etc.)"""
    name = models.CharField(max_length=100, verbose_name="Nom")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="Slug")
    description = models.TextField(blank=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ['name']

    def __str__(self):
        return self.name

class Project(models.Model):
    """Modèle pour les projets"""
    STATUS_CHOICES = [
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('planifie', 'Planifié'),
        ('suspendu', 'Suspendu'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Slug")
    description = models.TextField(verbose_name="Description")
    theme = models.CharField(max_length=300, verbose_name="Thème")
    objectives = models.JSONField(default=list, verbose_name="Objectifs")
    partners = models.JSONField(default=list, verbose_name="Partenaires")
    results = models.JSONField(default=list, verbose_name="Résultats")
    sdgs = models.JSONField(default=list, verbose_name="Objectifs de développement durable")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='en_cours', verbose_name="Statut")
    start_date = models.DateField(verbose_name="Date de début")
    end_date = models.DateField(null=True, blank=True, verbose_name="Date de fin")
    budget = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name="Budget")
    location = models.CharField(max_length=200, blank=True, verbose_name="Localisation")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Catégorie")
    is_featured = models.BooleanField(default=False, verbose_name="Projet en vedette")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Projet"
        verbose_name_plural = "Projets"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class ProjectImage(models.Model):
    """Modèle pour les images des projets"""
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE, verbose_name="Projet")
    image = models.ImageField(upload_to='projects/', verbose_name="Image")
    caption = models.CharField(max_length=200, blank=True, verbose_name="Légende")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Image de projet"
        verbose_name_plural = "Images de projets"
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"Image pour {self.project.title}"

class News(models.Model):
    """Modèle pour les actualités"""
    TYPE_CHOICES = [
        ('conference', 'Conférence'),
        ('lancement', 'Lancement'),
        ('symposium', 'Symposium'),
        ('table_ronde', 'Table ronde'),
        ('autre', 'Autre'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Slug")
    description = models.TextField(verbose_name="Description")
    content = models.TextField(verbose_name="Contenu détaillé")
    news_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='autre', verbose_name="Type d'actualité")
    event_date = models.DateTimeField(verbose_name="Date de l'événement")
    location = models.CharField(max_length=200, blank=True, verbose_name="Lieu")
    organizers = models.JSONField(default=list, verbose_name="Organisateurs")
    is_published = models.BooleanField(default=True, verbose_name="Publié")
    is_featured = models.BooleanField(default=False, verbose_name="En vedette")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Actualité"
        verbose_name_plural = "Actualités"
        ordering = ['-event_date']

    def __str__(self):
        return self.title

class NewsImage(models.Model):
    """Modèle pour les images des actualités"""
    news = models.ForeignKey(News, related_name='images', on_delete=models.CASCADE, verbose_name="Actualité")
    image = models.ImageField(upload_to='news/', verbose_name="Image")
    caption = models.CharField(max_length=200, blank=True, verbose_name="Légende")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Image d'actualité"
        verbose_name_plural = "Images d'actualités"
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"Image pour {self.news.title}"

class Publication(models.Model):
    """Modèle pour les publications"""
    TYPE_CHOICES = [
        ('article', 'Article scientifique'),
        ('rapport', 'Rapport'),
        ('livre', 'Livre'),
        ('these', 'Thèse'),
        ('autre', 'Autre'),
    ]
    
    title = models.CharField(max_length=300, verbose_name="Titre")
    slug = models.SlugField(max_length=300, unique=True, verbose_name="Slug")
    authors = models.JSONField(default=list, verbose_name="Auteurs")
    abstract = models.TextField(verbose_name="Résumé")
    content = models.TextField(blank=True, verbose_name="Contenu")
    publication_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='article', verbose_name="Type de publication")
    journal = models.CharField(max_length=200, blank=True, verbose_name="Journal/Éditeur")
    doi = models.CharField(max_length=100, blank=True, verbose_name="DOI")
    publication_date = models.DateField(verbose_name="Date de publication")
    keywords = models.JSONField(default=list, verbose_name="Mots-clés")
    file = models.FileField(upload_to='publications/', blank=True, verbose_name="Fichier PDF")
    is_published = models.BooleanField(default=True, verbose_name="Publié")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Publication"
        verbose_name_plural = "Publications"
        ordering = ['-publication_date']

    def __str__(self):
        return self.title

class Resource(models.Model):
    """Modèle pour les ressources"""
    TYPE_CHOICES = [
        ('document', 'Document'),
        ('video', 'Vidéo'),
        ('audio', 'Audio'),
        ('lien', 'Lien externe'),
        ('autre', 'Autre'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="Slug")
    description = models.TextField(verbose_name="Description")
    resource_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='document', verbose_name="Type de ressource")
    file = models.FileField(upload_to='resources/', blank=True, verbose_name="Fichier")
    external_url = models.URLField(blank=True, verbose_name="URL externe")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Catégorie")
    is_public = models.BooleanField(default=True, verbose_name="Public")
    download_count = models.PositiveIntegerField(default=0, verbose_name="Nombre de téléchargements")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ressource"
        verbose_name_plural = "Ressources"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class ContactForm(models.Model):
    """Modèle pour le formulaire de contact"""
    name = models.CharField(max_length=100, verbose_name="Nom complet")
    email = models.EmailField(verbose_name="Email")
    subject = models.CharField(max_length=200, verbose_name="Sujet")
    message = models.TextField(verbose_name="Message")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    organization = models.CharField(max_length=200, blank=True, verbose_name="Organisation")
    is_read = models.BooleanField(default=False, verbose_name="Lu")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"
        ordering = ['-created_at']

    def __str__(self):
        return f"Message de {self.name} - {self.subject}"

class PartnershipForm(models.Model):
    """Modèle pour le formulaire de partenariat"""
    name = models.CharField(max_length=100, verbose_name="Nom complet")
    email = models.EmailField(verbose_name="Email")
    organization = models.CharField(max_length=200, verbose_name="Organisation")
    position = models.CharField(max_length=100, blank=True, verbose_name="Poste")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    website = models.URLField(blank=True, verbose_name="Site web")
    partnership_type = models.CharField(max_length=100, blank=True, verbose_name="Type de partenariat souhaité")
    message = models.TextField(verbose_name="Message")
    is_processed = models.BooleanField(default=False, verbose_name="Traité")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Demande de partenariat"
        verbose_name_plural = "Demandes de partenariat"
        ordering = ['-created_at']

    def __str__(self):
        return f"Partenariat de {self.name} - {self.organization}"

class NewsletterSubscription(models.Model):
    """Modèle pour les abonnements à la newsletter"""
    email = models.EmailField(unique=True, verbose_name="Email")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Abonnement newsletter"
        verbose_name_plural = "Abonnements newsletter"
        ordering = ['-subscribed_at']

    def __str__(self):
        return self.email

class TeamMember(models.Model):
    """Modèle pour les membres de l'équipe"""
    name = models.CharField(max_length=100, verbose_name="Nom complet")
    position = models.CharField(max_length=100, verbose_name="Poste")
    bio = models.TextField(verbose_name="Biographie")
    email = models.EmailField(blank=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    photo = models.ImageField(upload_to='team/', blank=True, verbose_name="Photo")
    linkedin = models.URLField(blank=True, verbose_name="LinkedIn")
    twitter = models.URLField(blank=True, verbose_name="Twitter")
    facebook = models.URLField(blank=True, verbose_name="Facebook")
    website = models.URLField(blank=True, verbose_name="Site web")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Membre de l'équipe"
        verbose_name_plural = "Membres de l'équipe"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

class Partner(models.Model):
    """Modèle pour les partenaires"""
    name = models.CharField(max_length=200, verbose_name="Nom")
    logo = models.ImageField(upload_to='partners/', verbose_name="Logo")
    website = models.URLField(blank=True, verbose_name="Site web")
    description = models.TextField(blank=True, verbose_name="Description")
    partner_type = models.CharField(max_length=100, blank=True, verbose_name="Type de partenaire")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Partenaire"
        verbose_name_plural = "Partenaires"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

class EventRegistration(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom complet")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    message = models.TextField(blank=True, verbose_name="Message")
    created_at = models.DateTimeField(auto_now_add=True)

     # 👉 Champs ajoutés pour le formulaire
    participation_mode = models.CharField(max_length=100, blank=True, verbose_name="Mode de participation")
    position = models.CharField(max_length=100, blank=True, verbose_name="Poste ou fonction")
    organization = models.CharField(max_length=200, blank=True, verbose_name="Organisation")
    interest_domain = models.CharField(max_length=200, blank=True, verbose_name="Domaine d’intérêt")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Inscription à un événement"
        verbose_name_plural = "Inscriptions aux événements"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.email}"



class ExternalLink(models.Model):
    """Modèle pour les liens externes des publications"""
    CATEGORY_CHOICES = [
        ('recherche', 'Recherche'),
        ('institutionnel', 'Institutionnel'),
        ('partenaire', 'Partenaire'),
        ('ressource', 'Ressource'),
        ('autre', 'Autre'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Titre")
    url = models.URLField(verbose_name="URL")
    description = models.TextField(blank=True, verbose_name="Description")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='autre', verbose_name="Catégorie")
    icon = models.CharField(max_length=50, blank=True, verbose_name="Icône (nom de classe)")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Lien externe"
        verbose_name_plural = "Liens externes"
        ordering = ['order', 'title']

    def __str__(self):
        return self.title
