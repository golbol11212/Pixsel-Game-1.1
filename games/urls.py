from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('save-score/', views.save_score, name='save_score'),
    path('save-comment/', views.save_comment, name='save_comment'),
    path('get-comments/<str:game_name>/', views.get_comments, name='get_comments'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('leaderboard/<str:game_name>/', views.leaderboard, name='game_leaderboard'),
    path('user-stats/', views.user_stats, name='user_stats'),
    path('arkanoid/', views.arkanoid, name='arkanoid'),
    path('tetris/', views.tetris, name='tetris'),
    path('snake/', views.snake, name='snake'),
    path('space-shooter/', views.space_shooter, name='space_shooter'),
    path('flappy-bird/', views.flappy_bird, name='flappy_bird'),
    path('ping-pong/', views.ping_pong, name='ping_pong'),
    path('coinrunner/', views.coinrunner, name='coinrunner'),
    path('runner/', views.runner, name='runner'),
    path('labyrint/', views.labyrint, name='labyrint'),
    path('base-defender/', views.base_defender, name='base_defender'),
    path('full-leaderboard/', views.full_leaderboard, name='full_leaderboard'),
]
