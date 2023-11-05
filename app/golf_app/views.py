from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import *
from .forms import GameForm, PlayerForm
from django.urls import reverse_lazy
import random

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

    # Pass the chosen saying to the template context
    return render(request, 'golf_app/index.html', {'chosen_saying': chosen_saying})

# Player Views
class PlayerListView(ListView):
    model = Player
    template_name = 'golf_app/player_list.html'
    context_object_name = 'players'

class PlayerDetailView(DetailView):
    model = Player
    template_name = 'golf_app/player_detail.html'


class PlayerCreateView(CreateView):
    model = Player
    form_class = PlayerForm
    template_name = 'golf_app/player_form.html'
    success_url = reverse_lazy('player_list')

class PlayerUpdateView(UpdateView):
    model = Player
    form_class = PlayerForm
    template_name = 'golf_app/player_form.html'
    success_url = reverse_lazy('player_list')

class PlayerDeleteView(DeleteView):
    model = Player
    template_name = 'golf_app/player_confirm_delete.html'
    success_url = reverse_lazy('player_list')

# Game Views
class GameListView(ListView):
    model = Game
    template_name = 'golf_app/game_list.html'
    context_object_name = 'games'

class GameDetailView(DetailView):
    model = Game
    template_name = 'golf_app/game_detail.html'

# This view is for creating a new game
class GameCreateView(CreateView):
    model = Game
    form_class = GameForm
    template_name = 'golf_app/new_game.html'
    success_url = reverse_lazy('game_list')

    def form_valid(self, form):
        game = form.save(commit=False)
        game.save()
        # Assuming you redirect to the score entry page for the first hole after creating a game
        return redirect('hole_score_entry', game_id=game.pk, hole_number=1)

# This function-based view is for entering scores for each hole
def hole_score_entry(request, game_id, hole_number):
    game = get_object_or_404(Game, pk=game_id)
    ScoreFormSet = modelformset_factory(Score, form=ScoreForm, formset=BaseScoreFormSet, extra=game.number_of_players)
    if request.method == 'POST':
        formset = ScoreFormSet(request.POST, request.FILES, queryset=Score.objects.none())
        if formset.is_valid():
            instances = formset.save(commit=False)
            for instance in instances:
                instance.game = game
                instance.hole_number = hole_number
                instance.save()
            if hole_number < 18:
                return redirect('hole_score_entry', game_id=game.pk, hole_number=hole_number+1)
            else:
                return redirect('game_detail', pk=game.pk)
    else:
        formset = ScoreFormSet(queryset=Score.objects.none())
    return render(request, 'hole_score_form.html', {'formset': formset, 'game': game, 'hole_number': hole_number})
