from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from OeBVAdmin.models import Player

class ChangeEmailForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields =['email']

    send_test_mail = forms.BooleanField(initial=False, widget=forms.CheckboxInput(),
                                        label='Testmail senden', required=False)


class MyUserCreateForm(UserCreationForm):

    class Meta:
        fields = ('username', 'email', 'password1', 'password2')
        model = User

    ver_oebv_nr = forms.IntegerField(required=True, label='Deine ÖBV-Nummer')
    ver_last_name = forms.CharField(max_length=64, required=True, label='Familienname')

    def clean_username(self):
        usern = self.cleaned_data['username']
        lower_username = str(usern).strip().lower()
        exceptions =['oebv', 'club']

        if lower_username[:4] in exceptions:
            raise forms.ValidationError('Benutzernamen dürfen nicht mit oebv oder club beginnen')
        else:
            return usern

    def clean(self):
        cleaned_data = super().clean()
        oebv_nr = cleaned_data.get('ver_oebv_nr')
        lastname = cleaned_data.get('ver_last_name')

        try:
            player = Player.objects.get(oebv_nr = oebv_nr)
        except:
            raise forms.ValidationError(str(oebv_nr) + ' existiert nicht in der Datenbank')
        else:
            if not player.oebv_member:
                raise forms.ValidationError('Du bist kein Mitglied')
            else:
                vergl1 = str(lastname).strip().lower()[:8]
                vergl2 = str(player.last_name).strip().lower()[:8]

                if vergl1 != vergl2:
                    raise forms.ValidationError('Der angegebene Name stimmt nicht mit dem gespeicherten überein')
                elif player.reg_user:
                    raise forms.ValidationError('Für diesen Spieler ist schon der Beutzer {0} hinterlegt'.format(
                        player.reg_user.username))

