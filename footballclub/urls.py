from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from club.views import *
from footballclub import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', start_page, name='start_page'),
    path('news/', news_page, name='news_page'),
    path('news/<int:new_id>/', new_page, name='new_page'),
    path('future-mathes/', future_matches_page, name='future_page'),
    path('past-mathes/', past_matches_page, name='past_page'),
    path('matches/', all_matches_page, name='matches'),
    path('main_team/', main_team_page, name='main_team'),
    path('academy_team/', academy_team_page, name='academy_team'),
    path('player/<int:player_id>/', player_page, name='player_page'),
    path('shop/', shop_page, name='shop_page'),
    path('supercategory/<int:categ_id>/', supercateg_page, name='supercategory_page'),
    path('category/<int:categ_id>/', categ_page, name='categ_page'),
    path('item/<int:item_id>/', item_page, name='item_page'),
    path('cart/', cart_page, name='cart_page'),
    path('orders/', orders_page, name='orders_page')
]

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)

