from django import forms
from OeBVAdmin.models import Player
import re

class IndivForm(forms.Form):
    pass

def check_player_selection(data, own_oebv_nr=-1):
    match = re.match(r'^(?P<name>[- \w]+) \((?P<oebv_nr>\d+)\)$', data)
    if match:
        try:
            player = Player.objects.get(oebv_nr=match.group('oebv_nr'))
        except:
            return None
        else:
            player_name = '{} {}'.format(player.last_name, player.first_name)
            if match.group('name') != player_name:
                return None

            if player.oebv_nr == own_oebv_nr:
                return None

            return player.oebv_nr
    else:
        return None


class PairComboForm(forms.Form):
    partner = forms.CharField(max_length=128)

    def __init__(self, *args, own_oebv_nr=-1, **kwargs):
        super().__init__(*args, **kwargs)
        self.own_oebv_nr = own_oebv_nr

    def clean_partner(self):
        data = self.cleaned_data.get('partner')

        check = check_player_selection(data, own_oebv_nr=self.own_oebv_nr)
        if check == None:
            raise forms.ValidationError('Bitte wähle einen Spieler aus der Liste')
        else:
            return data


class TeamComboForm(forms.Form):
    name = forms.CharField(max_length=64)
    player2 = forms.CharField(max_length=128, required=False)
    player3 = forms.CharField(max_length=128, required=False)
    player4 = forms.CharField(max_length=128, required=False)
    player5 = forms.CharField(max_length=128, required=False)
    player6 = forms.CharField(max_length=128, required=False)
    player7 = forms.CharField(max_length=128, required=False)
    player8 = forms.CharField(max_length=128, required=False)

    def __init__(self, *args, own_oebv_nr=-1, **kwargs):
        super().__init__(*args, **kwargs)
        self.own_oebv_nr = own_oebv_nr
        self.player_list = []

    def clean_player2(self):
        data = self.cleaned_data.get('player2')

        if data == '':
            return data

        check = check_player_selection(data, self.own_oebv_nr)
        if check == None:
            raise forms.ValidationError('Bitte wähle einen Spieler aus der Liste')
        else:
            for pl in self.player_list:
                if check == pl:
                    raise forms.ValidationError('Spieler nicht mehrfach eintragen')

            self.player_list.append(check)
            return data

    def clean_player3(self):
        data = self.cleaned_data.get('player3')

        if data == '':
            return data

        check = check_player_selection(data, self.own_oebv_nr)
        if check == None:
            raise forms.ValidationError('Bitte wähle einen Spieler aus der Liste')
        else:
            for pl in self.player_list:
                if check == pl:
                    raise forms.ValidationError('Spieler nicht mehrfach eintragen')

            self.player_list.append(check)
            return data

    def clean_player4(self):
        data = self.cleaned_data.get('player4')

        if data == '':
            return data

        check = check_player_selection(data, self.own_oebv_nr)
        if check == None:
            raise forms.ValidationError('Bitte wähle einen Spieler aus der Liste')
        else:
            for pl in self.player_list:
                if check == pl:
                    raise forms.ValidationError('Spieler nicht mehrfach eintragen')

            self.player_list.append(check)
            return data

    def clean_player5(self):
        data = self.cleaned_data.get('player5')

        if data == '':
            return data

        check = check_player_selection(data, self.own_oebv_nr)
        if check == None:
            raise forms.ValidationError('Bitte wähle einen Spieler aus der Liste')
        else:
            for pl in self.player_list:
                if check == pl:
                    raise forms.ValidationError('Spieler nicht mehrfach eintragen')

            self.player_list.append(check)
            return data

    def clean_player6(self):
        data = self.cleaned_data.get('player6')

        if data == '':
            return data

        check = check_player_selection(data, self.own_oebv_nr)
        if check == None:
            raise forms.ValidationError('Bitte wähle einen Spieler aus der Liste')
        else:
            for pl in self.player_list:
                if check == pl:
                    raise forms.ValidationError('Spieler nicht mehrfach eintragen')

            self.player_list.append(check)
            return data

    def clean_player7(self):
        data = self.cleaned_data.get('player7')

        if data == '':
            return data

        check = check_player_selection(data, self.own_oebv_nr)
        if check == None:
            raise forms.ValidationError('Bitte wähle einen Spieler aus der Liste')
        else:
            for pl in self.player_list:
                if check == pl:
                    raise forms.ValidationError('Spieler nicht mehrfach eintragen')

            self.player_list.append(check)
            return data

    def clean_player8(self):
        data = self.cleaned_data.get('player8')

        if data == '':
            return data

        check = check_player_selection(data, self.own_oebv_nr)
        if check == None:
            raise forms.ValidationError('Bitte wähle einen Spieler aus der Liste')
        else:
            for pl in self.player_list:
                if check == pl:
                    raise forms.ValidationError('Spieler nicht mehrfach eintragen')

            self.player_list.append(check)
            return data
