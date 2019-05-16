from django import forms
from ClubAdmin import models

class TournamentForm(forms.ModelForm):

    class Meta:
        model = models.Tournament
        fields = ['organizer', 'name', 'date', 'tourn_type', 'max_team_members', 'info', 'registration_open']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['organizer'].label = 'Veranstalter'
        self.fields['organizer'].widget = forms.HiddenInput()
        self.fields['date'].label = 'Datum'
        self.fields['date'].widget = forms.SelectDateWidget()
        self.fields['tourn_type'].label = 'Turniertyp'
        self.fields['info'].label = 'Link zu den Turnierinformationen'
        self.fields['registration_open'].label = 'Anmeldung offen'
        self.fields['max_team_members'].label = 'Maximalanzahl Spieler pro Team'

class TournamentUpdateForm(TournamentForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['tourn_type'].disabled = True
        self.fields['max_team_members'].disabled = True