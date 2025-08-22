from django.core.management.base import BaseCommand
from django.urls import reverse
from game.models import Header, MenuItem

class Command(BaseCommand):
    help = 'Create initial header and menu items'

    def handle(self, *args, **options):
        # Create or get the main header
        header, created = Header.objects.get_or_create(
            site_name="PIXSGAME",
            defaults={
                'brand_color': '#ff00ff',
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('Created main header'))
        
        # Clear existing menu items to ensure a fresh start
        MenuItem.objects.filter(header=header).delete()
        self.stdout.write(self.style.SUCCESS('Cleared old menu items'))

        # Create menu items
        menu_items = [
            {'title': 'СПИСОК ИГР', 'url': reverse('games:home'), 'order': 1},
            {'title': 'РЕКОРДЫ', 'url': reverse('games:full_leaderboard'), 'order': 2},
            {'title': 'РЕГИСТРАЦИЯ', 'url': reverse('users:register'), 'order': 3},
            {'title': 'ВХОД', 'url': reverse('users:login'), 'order': 4},
        ]
        
        for item_data in menu_items:
            MenuItem.objects.create(
                header=header,
                title=item_data['title'],
                url=item_data['url'],
                order=item_data['order'],
                is_active=True
            )
        
        self.stdout.write(self.style.SUCCESS('Successfully created initial header and menu items'))
