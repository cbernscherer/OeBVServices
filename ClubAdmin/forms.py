from django import forms
from ClubAdmin import models
import datetime

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

    def clean_date(self):
        data = self.cleaned_data.get('date')

        if data < datetime.date.today():
            raise forms.ValidationError('Das Datum liegt in der Vergangenheit')
        return data


class TournamentUpdateForm(TournamentForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['tourn_type'].disabled = True
        self.fields['max_team_members'].disabled = True

    def clean_date(self):
        data = self.cleaned_data.get('date')
        if 'date' in self.changed_data:
            if data < datetime.date.today():
                raise forms.ValidationError('Das Datum liegt in der Vergangenheit')

        return data