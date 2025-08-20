from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from api.models import (
    Category, Project, News, Publication, Resource, 
    TeamMember, Partner, ContactForm, PartnershipForm
)

class Command(BaseCommand):
    help = 'Peuple la base de données avec des données d\'exemple pour MOCESS'

    def handle(self, *args, **options):
        self.stdout.write('Création des données d\'exemple...')
        
        # Créer des catégories
        categories = self.create_categories()
        
        # Créer des projets
        self.create_projects(categories)
        
        # Créer des actualités
        self.create_news()
        
        # Créer des publications
        self.create_publications()
        
        # Créer des ressources
        self.create_resources(categories)
        
        # Créer des membres de l'équipe
        self.create_team_members()
        
        # Créer des partenaires
        self.create_partners()
        
        # Créer des formulaires de contact d'exemple
        self.create_sample_forms()
        
        self.stdout.write(
            self.style.SUCCESS('Données d\'exemple créées avec succès!')
        )

    def create_categories(self):
        categories_data = [
            {'name': 'Développement Durable', 'slug': 'developpement-durable'},
            {'name': 'Gestion de l\'Eau', 'slug': 'gestion-eau'},
            {'name': 'Agriculture Durable', 'slug': 'agriculture-durable'},
            {'name': 'Énergie Renouvelable', 'slug': 'energie-renouvelable'},
            {'name': 'Biodiversité', 'slug': 'biodiversite'},
        ]
        
        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={
                    'name': cat_data['name'],
                    'description': f'Catégorie pour {cat_data["name"]}'
                }
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Catégorie créée: {category.name}')
        
        return categories

    def create_projects(self, categories):
        projects_data = [
            {
                'title': 'WomATLAS',
                'slug': 'womatlas',
                'description': 'Projet d\'autonomisation des femmes dans le Haut Atlas',
                'theme': 'Autonomisation des femmes, développement économique local, égalité de genre',
                'objectives': [
                    'Créer des opportunités d\'emploi pour les femmes rurales',
                    'Réduire les inégalités de genre dans les zones montagneuses',
                    'Encourager l\'inclusion économique'
                ],
                'partners': [
                    'Association Al Amal pour le Développement Durable',
                    'Ambassade du Canada au Maroc'
                ],
                'results': [
                    'Feuille de route définie pour la mise en œuvre',
                    'Lancement d\'activités professionnelles locales',
                    'Renforcement des capacités locales'
                ],
                'sdgs': [
                    {'id': 5, 'text': 'Égalité entre les sexes'},
                    {'id': 8, 'text': 'Travail décent et croissance économique'},
                    {'id': 10, 'text': 'Réduction des inégalités'}
                ],
                'status': 'en_cours',
                'start_date': datetime.now().date() - timedelta(days=180),
                'end_date': datetime.now().date() + timedelta(days=180),
                'location': 'Haut Atlas, Maroc',
                'is_featured': True
            },
            {
                'title': 'PEAR-HAOUZ',
                'slug': 'pear-haouz',
                'description': 'Projet de gestion intégrée de l\'eau dans la région du Haouz',
                'theme': 'Gestion intégrée de l\'eau, agriculture durable, transfert de technologies',
                'objectives': [
                    'Renforcer les capacités des agriculteurs',
                    'Promouvoir la réutilisation sûre des eaux usées',
                    'Favoriser les solutions basées sur la nature'
                ],
                'partners': [
                    'CNEREE – Université Cadi Ayyad',
                    'MOCESS',
                    'Ambassade de France au Maroc'
                ],
                'results': [
                    'Visite technique de la plateforme de traitement',
                    'Dialogue multi-acteurs',
                    'Transfert de savoirs sur les procédés écologiques'
                ],
                'sdgs': [
                    {'id': 6, 'text': 'Eau propre et assainissement'},
                    {'id': 12, 'text': 'Consommation et production responsables'},
                    {'id': 13, 'text': 'Lutte contre les changements climatiques'}
                ],
                'status': 'en_cours',
                'start_date': datetime.now().date() - timedelta(days=90),
                'end_date': datetime.now().date() + timedelta(days=270),
                'location': 'Région du Haouz, Marrakech',
                'is_featured': True
            }
        ]
        
        for proj_data in projects_data:
            project, created = Project.objects.get_or_create(
                slug=proj_data['slug'],
                defaults=proj_data
            )
            if created:
                self.stdout.write(f'Projet créé: {project.title}')

    def create_news(self):
        news_data = [
            {
                'title': 'Table Ronde Internationale – 16 mai 2024',
                'slug': 'table-ronde-internationale-16-mai-2024',
                'description': 'Science pilotée par la communauté – Habiliter les ONG et le secteur privé pour une recherche durable',
                'content': 'Organisée par le MOCESS en partenariat avec l\'Association Al Amal et le CNEREE de l\'Université Cadi Ayyad',
                'news_type': 'table_ronde',
                'event_date': datetime.now() - timedelta(days=30),
                'location': 'Marrakech, Maroc',
                'organizers': ['MOCESS', 'Association Al Amal', 'CNEREE'],
                'is_featured': True
            },
            {
                'title': 'Conférence Internationale – 25-27 septembre 2024',
                'slug': 'conference-internationale-25-27-septembre-2024',
                'description': 'Innovation dans le domaine de l\'eau et irrigation intelligente',
                'content': 'Organisée par le MOCESS en partenariat avec l\'Université Cadi Ayyad, le CNEREE et l\'Association Al Amal',
                'news_type': 'conference',
                'event_date': datetime.now() + timedelta(days=60),
                'location': 'Marrakech, Maroc',
                'organizers': ['MOCESS', 'Université Cadi Ayyad', 'CNEREE', 'Association Al Amal'],
                'is_featured': True
            }
        ]
        
        for news_data_item in news_data:
            news, created = News.objects.get_or_create(
                slug=news_data_item['slug'],
                defaults=news_data_item
            )
            if created:
                self.stdout.write(f'Actualité créée: {news.title}')

    def create_publications(self):
        publications_data = [
            {
                'title': 'Gestion durable des ressources hydriques au Maroc',
                'slug': 'gestion-durable-ressources-hydriques-maroc',
                'authors': ['Dr. Ahmed Benali', 'Dr. Fatima Zahra'],
                'abstract': 'Cette étude analyse les défis et opportunités pour une gestion durable de l\'eau au Maroc',
                'publication_type': 'article',
                'journal': 'Journal of Water Management',
                'publication_date': datetime.now().date() - timedelta(days=90),
                'keywords': ['eau', 'durabilité', 'Maroc', 'gestion']
            },
            {
                'title': 'Rapport sur l\'état de l\'environnement au Maroc 2024',
                'slug': 'rapport-environnement-maroc-2024',
                'authors': ['MOCESS', 'Ministère de l\'Environnement'],
                'abstract': 'Rapport complet sur l\'état de l\'environnement au Maroc en 2024',
                'publication_type': 'rapport',
                'journal': 'MOCESS Publications',
                'publication_date': datetime.now().date() - timedelta(days=30),
                'keywords': ['environnement', 'rapport', 'Maroc', '2024']
            }
        ]
        
        for pub_data in publications_data:
            publication, created = Publication.objects.get_or_create(
                slug=pub_data['slug'],
                defaults=pub_data
            )
            if created:
                self.stdout.write(f'Publication créée: {publication.title}')

    def create_resources(self, categories):
        resources_data = [
            {
                'title': 'Guide de bonnes pratiques environnementales',
                'slug': 'guide-bonnes-pratiques-environnementales',
                'description': 'Guide complet pour les bonnes pratiques environnementales',
                'resource_type': 'document',
                'category': categories[0] if categories else None
            },
            {
                'title': 'Vidéo: Techniques d\'irrigation durable',
                'slug': 'video-techniques-irrigation-durable',
                'description': 'Vidéo explicative sur les techniques d\'irrigation durable',
                'resource_type': 'video',
                'category': categories[1] if len(categories) > 1 else None
            }
        ]
        
        for res_data in resources_data:
            resource, created = Resource.objects.get_or_create(
                slug=res_data['slug'],
                defaults=res_data
            )
            if created:
                self.stdout.write(f'Ressource créée: {resource.title}')

    def create_team_members(self):
        team_data = [
            {
                'name': 'Dr. Ahmed Benali',
                'position': 'Directeur Général',
                'bio': 'Expert en développement durable avec plus de 15 ans d\'expérience',
                'email': 'ahmed.benali@mocess.ma',
                'order': 1
            },
            {
                'name': 'Dr. Fatima Zahra',
                'position': 'Directrice de la Recherche',
                'bio': 'Spécialiste en gestion des ressources hydriques',
                'email': 'fatima.zahra@mocess.ma',
                'order': 2
            }
        ]
        
        for member_data in team_data:
            member, created = TeamMember.objects.get_or_create(
                email=member_data['email'],
                defaults=member_data
            )
            if created:
                self.stdout.write(f'Membre d\'équipe créé: {member.name}')

    def create_partners(self):
        partners_data = [
            {
                'name': 'Université Cadi Ayyad',
                'logo': 'partners/uca.jpg',
                'website': 'https://www.uca.ma/',
                'partner_type': 'Université',
                'order': 1
            },
            {
                'name': 'Programme des Nations Unies pour l\'Environnement',
                'logo': 'partners/pnue.png',
                'website': 'https://www.unep.org/',
                'partner_type': 'Organisation Internationale',
                'order': 2
            },
            {
                'name': 'Organisation des Nations Unies pour l\'Alimentation',
                'logo': 'partners/fao.jpeg',
                'website': 'https://www.fao.org/',
                'partner_type': 'Organisation Internationale',
                'order': 3
            }
        ]
        
        for partner_data in partners_data:
            partner, created = Partner.objects.get_or_create(
                name=partner_data['name'],
                defaults=partner_data
            )
            if created:
                self.stdout.write(f'Partenaire créé: {partner.name}')

    def create_sample_forms(self):
        # Créer quelques formulaires de contact d'exemple
        contact_forms = [
            {
                'name': 'Mohammed Alami',
                'email': 'mohammed.alami@example.com',
                'subject': 'Demande d\'information sur les projets',
                'message': 'Bonjour, je souhaiterais obtenir plus d\'informations sur vos projets de développement durable.',
                'phone': '+212 6 12 34 56 78',
                'organization': 'Association Environnementale'
            }
        ]
        
        for form_data in contact_forms:
            form, created = ContactForm.objects.get_or_create(
                email=form_data['email'],
                subject=form_data['subject'],
                defaults=form_data
            )
            if created:
                self.stdout.write(f'Formulaire de contact créé: {form.name}')
        
        # Créer quelques formulaires de partenariat d'exemple
        partnership_forms = [
            {
                'name': 'Sarah Johnson',
                'email': 'sarah.johnson@example.org',
                'organization': 'Green Development Initiative',
                'position': 'Directrice des Projets',
                'partnership_type': 'Collaboration de recherche',
                'message': 'Nous souhaitons collaborer sur des projets de développement durable.'
            }
        ]
        
        for form_data in partnership_forms:
            form, created = PartnershipForm.objects.get_or_create(
                email=form_data['email'],
                organization=form_data['organization'],
                defaults=form_data
            )
            if created:
                self.stdout.write(f'Formulaire de partenariat créé: {form.name}') 