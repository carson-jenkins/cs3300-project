from django import forms
from .models import Player, Game
from django.forms import modelformset_factory, ModelForm
from django.shortcuts import get_object_or_404

class PlayerForm(ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'handicap']


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['date_played', 'course_name', 'players']
        widgets = {
            'date_played': forms.DateInput(attrs={'type': 'date'}),
            'course_name': forms.TextInput(),
            'players': forms.CheckboxSelectMultiple(),
        }

def hole_score_entry(request, game_id, hole_number):
    game = get_object_or_404(Game, pk=game_id)
    HoleFormSet = modelformset_factory(Score, fields=('par', 'strokes'), extra=game.players.count())
    
    if request.method == 'POST':
        formset = HoleFormSet(request.POST)
        if formset.is_valid():
            # Save the scores and redirect to the next hole or finish the game
            instances = formset.save(commit=False)
            for instance in instances:
                instance.game = game
                instance.hole.number = hole_number
                instance.save()
            if hole_number < 18:
                return redirect('hole_score_entry', game_id=game.pk, hole_number=hole_number+1)
            else:
                # Redirect to game summary or wherever you wish to go after the last hole
                return redirect('game_summary', game_id=game.pk)
    else:
        formset = HoleFormSet(queryset=Score.objects.none())
    
    return render(request, 'hole_score_form.html', {'formset': formset})

# Note: You'll need to create a 'hole_score_form.html' template for the formset.
