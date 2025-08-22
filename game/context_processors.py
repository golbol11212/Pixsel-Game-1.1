from .models import Header
from django.urls import reverse

def header_context(request):
    """Context processor to make header data available in all templates"""
    try:
        active_header = Header.objects.filter(is_active=True).first()
        if active_header:
            return {
                'header_data': active_header,
                'menu_items': active_header.menu_items.filter(is_active=True)
            }
    except:
        pass
    
    # Fallback to default values if no header is configured
    return {
        'header_data': {
            'site_name': 'PIXSGAME',
            'brand_color': '#ff00ff'
        },
        'menu_items': [
            {'title': 'СПИСОК ИГР', 'url': reverse('games:home'), 'css_class': ''},
            {'title': 'РЕГИСТРАЦИЯ', 'url': reverse('users:register'), 'css_class': ''},
            {'title': 'ВХОД', 'url': reverse('users:login'), 'css_class': ''},
        ]
    }
