from django.db import models
from django.contrib.auth.models import User

class GameScore(models.Model):
    """Model for storing game scores"""
    GAME_CHOICES = [
        ('arkanoid', 'Арканоїд'),
        ('tetris', 'Тетріс'),
        ('snake', 'Змійка'),
        ('space_shooter', 'Космічний шутер'),
        ('flappy_bird', 'Flappy Bird'),
        ('ping_pong', 'Пінг-понг'),
        ('coinrunner', 'Coin Runner'),
        ('runner', 'Бігун'),
        ('labyrint', 'Лабіринт'),
        ('base_defender', 'Захист бази'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_scores')
    game_name = models.CharField(max_length=20, choices=GAME_CHOICES)
    score = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    achieved_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-score', 'achieved_at']
        verbose_name = 'Game Score'
        verbose_name_plural = 'Game Scores'
    
    def __str__(self):
        return f"{self.user.username} - {self.get_game_name_display()}: {self.score}"


class GameComment(models.Model):
    """Model for storing game comments"""
    GAME_CHOICES = [
        ('arkanoid', 'Арканоїд'),
        ('tetris', 'Тетріс'),
        ('snake', 'Змійка'),
        ('space_shooter', 'Космічний шутер'),
        ('flappy_bird', 'Flappy Bird'),
        ('ping_pong', 'Пінг-понг'),
        ('coinrunner', 'Coin Runner'),
        ('runner', 'Бігун'),
        ('labyrint', 'Лабіринт'),
        ('base_defender', 'Захист бази'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='game_comments')
    game_name = models.CharField(max_length=20, choices=GAME_CHOICES)
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Game Comment'
        verbose_name_plural = 'Game Comments'
    
    def __str__(self):
        return f"{self.user.username} - {self.get_game_name_display()}: {self.content[:50]}..."
