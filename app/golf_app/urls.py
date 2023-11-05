from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('games/', views.GameListView.as_view(), name='game_list'),
    path('games/<int:pk>/', views.GameDetailView.as_view(), name='game_detail'),
    path('games/new/', views.GameCreateView.as_view(), name='new_game'),
    path('games/<int:game_id>/hole/<int:hole_number>/', hole_score_entry, name='hole_score_entry'),
    path('players/', views.PlayerListView.as_view(), name='player_list'),
    path('players/<int:pk>/', views.PlayerDetailView.as_view(), name='player_detail'),
    path('players/add/', views.PlayerCreateView.as_view(), name='player_add'),
    path('players/<int:pk>/edit/', views.PlayerUpdateView.as_view(), name='player_edit'),
    path('players/<int:pk>/delete/', views.PlayerDeleteView.as_view(), name='player_delete'),
]
