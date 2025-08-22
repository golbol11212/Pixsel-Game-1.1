from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Max
from .models import GameScore, GameComment
import json

def home(request):
    """Главная страница игр"""
    # Get top scores for each game
    top_scores = {}
    games = [choice[0] for choice in GameScore.GAME_CHOICES]
    
    for game in games:
        top_score = GameScore.objects.filter(game_name=game).order_by('-score').first()
        if top_score:
            top_scores[game] = top_score
    
    context = {
        'top_scores': top_scores
    }
    return render(request, 'games/home.html', context)

@login_required
@csrf_exempt
def save_score(request):
    """Save game score via AJAX"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            game_name = data.get('game_name')
            score = int(data.get('score', 0))
            level = int(data.get('level', 1))
            
            if game_name and score >= 0:
                GameScore.objects.create(
                    user=request.user,
                    game_name=game_name,
                    score=score,
                    level=level
                )
                return JsonResponse({'status': 'success', 'message': 'Score saved!'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid data'})
                
        except (ValueError, json.JSONDecodeError):
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required
@csrf_exempt
def save_comment(request):
    """Save game comment via AJAX"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            game_name = data.get('game_name')
            content = data.get('content', '').strip()
            
            if game_name and content:
                if len(content) > 500:
                    return JsonResponse({'status': 'error', 'message': 'Comment too long (max 500 characters)'})
                
                comment = GameComment.objects.create(
                    user=request.user,
                    game_name=game_name,
                    content=content
                )
                
                return JsonResponse({
                    'status': 'success', 
                    'message': 'Comment saved!',
                    'comment': {
                        'id': comment.id,
                        'username': comment.user.username,
                        'content': comment.content,
                        'created_at': comment.created_at.strftime('%d.%m.%Y %H:%M')
                    }
                })
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid data'})
                
        except (ValueError, json.JSONDecodeError):
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def get_comments(request, game_name):
    """Get comments for a specific game"""
    if request.method == 'GET':
        comments = GameComment.objects.filter(game_name=game_name).select_related('user')[:50]
        comments_data = []
        
        for comment in comments:
            comments_data.append({
                'id': comment.id,
                'username': comment.user.username,
                'content': comment.content,
                'created_at': comment.created_at.strftime('%d.%m.%Y %H:%M')
            })
        
        return JsonResponse({'comments': comments_data})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def leaderboard(request, game_name=None):
    """Display leaderboard for specific game or all games"""
    if game_name:
        scores = GameScore.objects.filter(game_name=game_name).select_related('user')[:10]
        game_title = dict(GameScore.GAME_CHOICES).get(game_name, game_name)
    else:
        # Get top 10 scores for each game
        scores = {}
        for game_code, game_title in GameScore.GAME_CHOICES:
            scores[game_title] = GameScore.objects.filter(
                game_name=game_code
            ).select_related('user')[:10]
    
    context = {
        'scores': scores,
        'game_name': game_name,
        'game_title': game_title if game_name else None
    }
    return render(request, 'games/leaderboard.html', context)

def user_stats(request):
    """Display user statistics"""
    if not request.user.is_authenticated:
        return redirect('users:login')
    
    user_scores = GameScore.objects.filter(user=request.user)
    
    # Get best score for each game
    best_scores = {}
    for game_code, game_title in GameScore.GAME_CHOICES:
        best_score = user_scores.filter(game_name=game_code).order_by('-score').first()
        if best_score:
            best_scores[game_title] = best_score
    
    # Get total games played
    total_games = user_scores.count()
    
    # Get overall best score
    overall_best = user_scores.order_by('-score').first()
    
    context = {
        'best_scores': best_scores,
        'total_games': total_games,
        'overall_best': overall_best,
        'recent_scores': user_scores[:10]
    }
    return render(request, 'games/user_stats.html', context)

def arkanoid(request):
    """Арканоид игра"""
    comments = GameComment.objects.filter(game_name='arkanoid').select_related('user')[:20]
    top_scores = GameScore.objects.filter(game_name='arkanoid').select_related('user').order_by('-score')[:5]
    return render(request, 'games/arkanoyd.html', {'comments': comments, 'top_scores': top_scores})

def tetris(request):
    """Тетрис игра"""
    comments = GameComment.objects.filter(game_name='tetris').select_related('user')[:20]
    top_scores = GameScore.objects.filter(game_name='tetris').select_related('user').order_by('-score')[:5]
    return render(request, 'games/tetris.html', {'comments': comments, 'top_scores': top_scores})

def snake(request):
    """Змейка игра"""
    comments = GameComment.objects.filter(game_name='snake').select_related('user')[:20]
    top_scores = GameScore.objects.filter(game_name='snake').select_related('user').order_by('-score')[:5]
    return render(request, 'games/zmeyka.html', {'comments': comments, 'top_scores': top_scores})

def space_shooter(request):
    """Космический шутер"""
    comments = GameComment.objects.filter(game_name='space_shooter').select_related('user')[:20]
    top_scores = GameScore.objects.filter(game_name='space_shooter').select_related('user').order_by('-score')[:5]
    return render(request, 'games/space_shooter.html', {'comments': comments, 'top_scores': top_scores})

def flappy_bird(request):
    """Flappy Bird игра"""
    comments = GameComment.objects.filter(game_name='flappy_bird').select_related('user')[:20]
    top_scores = GameScore.objects.filter(game_name='flappy_bird').select_related('user').order_by('-score')[:5]
    return render(request, 'games/flappy_bird.html', {'comments': comments, 'top_scores': top_scores})

def ping_pong(request):
    """Пинг-понг игра"""
    comments = GameComment.objects.filter(game_name='ping_pong').select_related('user')[:20]
    top_scores = GameScore.objects.filter(game_name='ping_pong').select_related('user').order_by('-score')[:5]
    return render(request, 'games/ping_pong.html', {'comments': comments, 'top_scores': top_scores})

def coinrunner(request):
    """Coin Runner игра"""
    comments = GameComment.objects.filter(game_name='coinrunner').select_related('user')[:20]
    top_scores = GameScore.objects.filter(game_name='coinrunner').select_related('user').order_by('-score')[:5]
    return render(request, 'games/coinrunner.html', {'comments': comments, 'top_scores': top_scores})

def runner(request):
    """Бегун игра"""
    comments = GameComment.objects.filter(game_name='runner').select_related('user')[:20]
    top_scores = GameScore.objects.filter(game_name='runner').select_related('user').order_by('-score')[:5]
    return render(request, 'games/runner.html', {'comments': comments, 'top_scores': top_scores})

def labyrint(request):
    """Лабиринт игра"""
    comments = GameComment.objects.filter(game_name='labyrint').select_related('user')[:20]
    top_scores = GameScore.objects.filter(game_name='labyrint').select_related('user').order_by('-score')[:5]
    return render(request, 'games/labyrint.html', {'comments': comments, 'top_scores': top_scores})

def base_defender(request):
    """Защита базы игра"""
    comments = GameComment.objects.filter(game_name='base_defender').select_related('user')[:20]
    top_scores = GameScore.objects.filter(game_name='base_defender').select_related('user').order_by('-score')[:5]
    return render(request, 'games/base_defender.html', {'comments': comments, 'top_scores': top_scores})

def full_leaderboard(request):
    """Display a full leaderboard with global scores and user's personal bests."""
    # Get top 10 scores for each game for all users
    global_scores = {}
    for game_code, game_title in GameScore.GAME_CHOICES:
        global_scores[game_title] = GameScore.objects.filter(
            game_name=game_code
        ).select_related('user').order_by('-score')[:10]

    # Get personal bests for the logged-in user
    personal_scores = {}
    if request.user.is_authenticated:
        user_scores = GameScore.objects.filter(user=request.user)
        for game_code, game_title in GameScore.GAME_CHOICES:
            best_score = user_scores.filter(game_name=game_code).order_by('-score').first()
            if best_score:
                personal_scores[game_title] = best_score

    context = {
        'global_scores': global_scores,
        'personal_scores': personal_scores,
    }
    return render(request, 'games/full_leaderboard.html', context)
