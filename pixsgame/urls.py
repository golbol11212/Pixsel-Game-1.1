from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('game.urls')),
    path('games/', include(('games.urls', 'games'), namespace='games')),
    path('users/', include('users.urls')),
]
