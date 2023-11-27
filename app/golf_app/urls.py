from django.urls import path
from . import views

urlpatterns = [
    # Homepage
    path('', views.index, name='index'),

    # Player URLs
    path('players/', views.PlayerListView.as_view(), name='player-list'),
    path('players/<int:pk>/', views.PlayerDetailView.as_view(), name='player-detail'),
    path('players/new/', views.create_update_player, name='new-player'),
    path('players/<int:pk>/edit/', views.create_update_player, name='edit-player'),
    path('player/delete/<int:pk>/', views.PlayerDeleteView.as_view(), name='player-delete'),
    
    # Game URLs
    path('games/', views.GameListView.as_view(), name='game-list'),
    path('games/<int:pk>/', views.GameDetailView.as_view(), name='game-detail'),  # Handles game details and score entry
    path('games/new/', views.create_update_game, name='new-game'),  # For creating a new game
    path('games/<int:pk>/edit/', views.create_update_game, name='edit-game'),  # For editing an existing game
    path('game/delete/<int:pk>/', views.GameDeleteView.as_view(), name='game-delete'),

    # User URLs
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
]
