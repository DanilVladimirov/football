from django.shortcuts import render
from .models import *
from datetime import date


def age(birth_date):
    today = date.today()
    y = today.year - birth_date.year
    if today.month < birth_date.month or today.month == birth_date.month and today.day < birth_date.day:
        y -= 1
    return y


def last_news_returner():
    last_news = News.objects.order_by('-id')[:3]
    return last_news


def last_matches_returner():
    last_matches = Match.objects.filter(future_match=False).order_by('-date')[:3]
    return last_matches


def start_page(request):
    data = {}
    last_news = last_news_returner()
    last_matches = last_matches_returner()
    sponsors = Sponsor.objects.all()
    data.update({'news': last_news,
                 'matches': last_matches,
                 'sponsors': sponsors})

    return render(request, 'start-page.html', data)


def news_page(request):
    data = {'news': News.objects.order_by('-id')}
    if request.POST:
        date = request.POST.get('date')
        print(date)
        news = News.objects.filter(time=date)
        data = {'news': news.order_by('-id')}
    return render(request, 'news-page.html', data)


def new_page(request, new_id):
    data = {}
    new = News.objects.get(id=new_id)
    data.update({'new': new})
    last_news = News.objects.exclude(id=new.id)
    last_news = last_news.order_by('-id')[:2]
    print(last_news)
    data.update({'news': last_news})
    return render(request, 'new-page.html', data)


def future_matches_page(request):
    matches = Match.objects.filter(future_match=True).order_by('-date')
    data = {'matches': matches}

    return render(request, 'matches-page.html', data)


def past_matches_page(request):
    matches = Match.objects.filter(future_match=False).order_by('-date')
    data = {'matches': matches}

    return render(request, 'matches-page.html', data)


def all_matches_page(request):
    matches = Match.objects.all()
    data = {'matches': matches}

    return render(request, 'matches-page.html', data)


def main_team_page(request):
    data = {}
    players = Player.objects.filter(team='M')

    goalkeepers = players.filter(role_player='goalkeeper')
    defenders = players.filter(role_player='defender')
    midfielder = players.filter(role_player='midfielder')
    attackers = players.filter(role_player='attackers')

    data.update({'goalkeepers': goalkeepers,
                 'defenders': defenders,
                 'midfielder': midfielder,
                 'attackers': attackers})

    return render(request, 'team-page.html', data)


def academy_team_page(request):
    data = {}
    players = Player.objects.filter(team='A')

    goalkeepers = players.filter(role_player='goalkeeper')
    defenders = players.filter(role_player='defender')
    midfielder = players.filter(role_player='midfielder')
    attackers = players.filter(role_player='attackers')

    data.update({'goalkeepers': goalkeepers,
                 'defenders': defenders,
                 'midfielder': midfielder,
                 'attackers': attackers})

    return render(request, 'team-page.html', data)


def player_page(request, player_id):
    data = {'player': Player.objects.get(id=player_id)}
    return render(request, 'player-page.html', data)
