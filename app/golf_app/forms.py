from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ModelMultipleChoiceField

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'handicap', 'contact_email', 'bio']

class GameForm(forms.ModelForm):
    players = forms.ModelMultipleChoiceField(
        queryset=Player.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Game
        fields = ['date', 'course_name', 'players']

    def save(self, commit=True):
        game = super().save(commit=False)
        if commit:
            game.save()
        new_player_name = self.cleaned_data.get('new_player_name')
        if new_player_name:
            player, created = Player.objects.get_or_create(name=new_player_name)
            game.players.add(player)
        self.save_m2m()
        return game

class PlayerGameScoreForm(forms.ModelForm):
    scores = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = PlayerGameScore
        fields = ['player', 'game', 'scores']

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance

class PlayerScoreForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(PlayerScoreForm, self).__init__(*args, **kwargs)
        for i in range(1, 19):
            self.fields[f'score_{i}'] = forms.CharField(required=False, widget=forms.TextInput(attrs={'size': '2'}))


class LoginForm(AuthenticationForm):  # Assuming LoginForm is a model-based form
    class Meta:
        model = CustomUser  # Use your custom user model
        fields = ['username', 'password']  # Update with your desired fields

class RegistrationForm(forms.ModelForm):  # Assuming RegistrationForm is a model-based form
    class Meta:
        model = CustomUser  # Use your custom user model
        fields = ['username', 'password', 'email']  # Update with your desired fields
