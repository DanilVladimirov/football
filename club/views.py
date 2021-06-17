from django.shortcuts import render, redirect
from .models import *
from datetime import date


# def age(birth_date):
#     today = date.today()
#     y = today.year - birth_date.year
#     if today.month < birth_date.month or today.month == birth_date.month and today.day < birth_date.day:
#         y -= 1
#     return y


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


def shop_page(request):
    data = {}
    data.update({'supercategs': SuperCategory.objects.all()})
    return render(request, 'shop-page.html', data)


def supercateg_page(request, categ_id):
    data = {}
    data.update({'supercateg': SuperCategory.objects.get(id=categ_id)})
    return render(request, 'supercateg-page.html', data)


def categ_page(request, categ_id):
    data = {}
    items = Category.objects.get(id=categ_id).items.all()

    data.update({'items': items, 'category': Category.objects.get(id=categ_id)})
    return render(request, 'category-page.html', data)


def item_page(request, item_id):
    data = {}
    item = Item.objects.get(id=item_id)
    recommend_items = item.category_set.filter()[0].items.order_by('-id').exclude(id=item.id)[:5]
    data.update({'item': item, 'items': recommend_items})
    cart = request.session.get('cart', {})

    if request.POST:
        item_cart = request.POST.get('item_id')
        if len(cart) == 0:
            request.session['cart'] = cart
            item = [{'item': int(item_cart),
                     'quantity': int(request.POST.get('quantity'))}]
            request.session['cart'] = item
            request.session.modified = True
        else:
            cart.append({'item': int(item_cart),
                         'quantity': int(request.POST.get('quantity'))})
            request.session.modified = True
    return render(request, 'item-page.html', data)


def cart_page(request):
    cart = request.session.get('cart', {})
    action = request.POST.get('action')

    if request.POST and action == 'del':
        for item in cart:
            if int(request.POST.get('item_id')) == item.get('item'):
                del cart[cart.index(item)]
        request.session['cart'] = cart
        request.session.modified = True

    cart = request.session.get('cart', {})
    cart_user = []
    for item in cart:
        cart_user.append({'item': Item.objects.get(id=item.get('item')),
                          'quantity': item.get('quantity')})
    data = {'cart': cart_user}

    if request.POST and action == 'order':
        telephone = request.POST.get('tel')
        f_name = request.POST.get('f_name')
        l_name = request.POST.get('l_name')
        address = request.POST.get('address')
        wish = request.POST.get('wish')
        if wish is None:
            wish = " "
        order_items = []
        for item in cart_user:
            new_order_item = OrderItem.objects.create(item=item.get('item'),
                                                      quantity=item.get('quantity'))
            new_order_item.save()
            order_items.append(new_order_item)
        new_order = Order.objects.create(telephone=telephone,
                                         first_name=f_name,
                                         last_name=l_name,
                                         address=address,
                                         wishtext=wish)
        for item in order_items:
            new_order.items.add(item)
        new_order.save()
        request.session['cart'] = {}
        request.session.modified = True

        cart = request.session.get('cart', {})
        cart_user = []
        for item in cart:
            cart_user.append({'item': Item.objects.get(id=item.get('item')),
                              'quantity': item.get('quantity')})
        data = {'cart': cart_user, 'good': True}

    return render(request, 'cart-page.html', data)


def orders_page(request):
    data = {}
    if not request.user.is_superuser:
        return redirect('start_page')
    if request.POST:
        order = Order.objects.get(id=request.POST.get('order_id'))
        order.delete()
    orders = Order.objects.all()
    data.update({'orders': orders})

    return render(request, 'orders-page.html', data)
