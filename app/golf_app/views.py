from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import *
from .forms import *
import random
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.views.generic.edit import DeleteView

class UserLoginView(LoginView):
    template_name = 'golf_app/login.html'
    authentication_form = AuthenticationForm
    next_page = '/'  # Redirect to the homepage after login

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('index')

class UserRegistrationView(CreateView):
    template_name = 'golf_app/registration.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # Save the form and create a new user
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return super().form_valid(form)

def index(request):
    sayings = [
        "Hit 'em straight!",
        "Play well!",
        "Fairways and greens!",
        "Keep it on the short grass!",
        "May the course be with you!",
        "Stay out of the bunkers!",
        "Best of luck on the links!",
        "Chase that little white ball!",
        "Enjoy the walk!",
        "Swing smooth!",
        "Drive for show, putt for dough!",
        "Tee it high and let it fly!",
        "Nothing but hole!",
        "It's a good day for a great game!",
        "Avoid the hazards!",
        "Swing with confidence!",
        "Here’s to a birdie kind of day!",
    ]
    chosen_saying = random.choice(sayings)

    game_list = Game.objects.all().order_by('-date')[:5]
    recent_games = game_list

    top_players = Player.objects.all().order_by('handicap')[:5]

    context = {
        'recent_games': recent_games,
        'top_players': top_players,
        'chosen_saying': chosen_saying,
    }
    return render(request, 'golf_app/index.html', context)

# Player views
class PlayerListView(generic.ListView):
    model = Player
    context_object_name = 'player_list'
    template_name = 'player_list.html'

class PlayerDetailView(generic.DetailView):
    model = Player
    template_name = 'golf_app/player_detail.html'

class PlayerDeleteView(DeleteView):
    model = Player
    success_url = reverse_lazy('player-list')

@login_required  # Restrict access to logged-in users
def create_update_player(request, pk=None):
    player = get_object_or_404(Player, pk=pk) if pk else None
    if request.method == 'POST':
        form = PlayerForm(request.POST, instance=player)
        if form.is_valid():
            form.save()
            return redirect('player-detail', pk=form.instance.pk)
    else:
        form = PlayerForm(instance=player)
    return render(request, 'golf_app/player_form.html', {'form': form})

# Game views
class GameListView(generic.ListView):
    model = Game
    context_object_name = 'game_list'
    template_name = 'game_list.html'

class GameDetailView(generic.DetailView):
    model = Game
    template_name = 'golf_app/game_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        game = self.get_object()  # Get the game object for the current view
        PlayerScoreFormSet = formset_factory(PlayerScoreForm, extra=0)

        formset_data = []
        for player_score in PlayerGameScore.objects.filter(game=game):
            form_data = {f'score_{i + 1}': player_score.get_score(i + 1) for i in range(18)}
            formset_data.append(form_data)

        context['formset'] = PlayerScoreFormSet(initial=formset_data)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Set the object for the current view
        game = self.object
        PlayerScoreFormSet = formset_factory(PlayerScoreForm, extra=0)
        formset = PlayerScoreFormSet(request.POST)

        if formset.is_valid():
            player_scores = PlayerGameScore.objects.filter(game=game)
            for form, player_score in zip(formset, player_scores):
                scores = [form.cleaned_data[f'score_{i + 1}'] for i in range(18)]
                player_score.scores = ','.join(scores)
                player_score.save()

            return redirect('game-detail', pk=game.pk)

        return self.render_to_response(self.get_context_data(formset=formset))

class GameDeleteView(DeleteView):
    model = Game
    success_url = reverse_lazy('game-list')  # Redirect to the game list after deletion

@login_required
def create_update_game(request, pk=None):
    game = get_object_or_404(Game, pk=pk) if pk else None

    if request.method == 'POST':
        form = GameForm(request.POST, instance=game)
        if form.is_valid():
            new_game = form.save()  # Save the game first

            # Handle new player creation
            new_player_name = form.cleaned_data.get('new_player_name')
            if new_player_name:
                player, created = Player.objects.get_or_create(name=new_player_name)
                new_game.players.add(player)

            # Redirect to the game detail page for score entry
            return redirect('game-detail', pk=new_game.pk)
    else:
        form = GameForm(instance=game)

    return render(request, 'golf_app/game_form.html', {'form': form})