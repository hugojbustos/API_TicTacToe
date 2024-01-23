from django.urls import path
from .views import CreateGameView, SubmitPlayView, GameListView, \
                   SingleGameView, DeleteGameView

urlpatterns = [
    path('create_game/', CreateGameView.as_view(), name='create_game'),
    path('submit_play/', SubmitPlayView.as_view(), name='submit_play'),
    path('games/', GameListView.as_view(), name='game_list'),
    path('games/<str:option>/<int:limit>/', GameListView.as_view(),
         name='game_list_with_option_and_limit'),
    path('games/<str:option>/', GameListView.as_view(),
         name='game_list_with_option'),
    path('game/<int:game_id>/', SingleGameView.as_view(), name='single_game'),
    path('game/<int:game_id>/delete/', DeleteGameView.as_view(),
         name='delete_game'),
]
