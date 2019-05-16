from django import  forms
from OeBVAdmin.models import Club
from django.contrib.auth.models import User

class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['club_nr', 'name', 'shortname']

    proceed = forms.CharField(max_length=4, initial='list')


class ClubUpdateForm(forms.ModelForm):
    club_nr = forms.IntegerField(disabled=True)

    class Meta:
        model = Club
        fields = ['club_nr', 'name', 'shortname']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['club_nr'].label = 'Nummer'
        self.fields['shortname'].label = 'Abkürzung'


class CreateClubAdmin(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        data = self.cleaned_data.get('email')

        if data in User.objects.values_list('email', flat=True):
            raise forms.ValidationError('Die Mailadresse ist bereits im System vorhanden')

        return data


class RemoveClubAdmin(forms.Form):
    pass


class PlayersUploadForm(forms.Form):
    players_file = forms.FileField(required=True, label='Spielerdatei', allow_empty_file=False)


class RemoveRegUser(forms.Form):
    pass