from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
import datetime
from OeBVAdmin.models import Player
from ClubAdmin.models import Tournament
from TournRegister.models import Participant, TournPlayer
from TournRegister import forms
from django.contrib import messages
import re

# Create your views here.
players = Group.objects.get(name='Players')

def check_player(user):
    return players in user.groups.all()


def isolate_oebv_nr(data):
    match = re.match(r'^(?P<name>[- \w]+) \((?P<oebv_nr>\d+)\)$', data)
    if match:
        return match.group('oebv_nr')
    else:
        return -1


@user_passes_test(check_player)
def player_tourn_list(request, slug):
    player = get_object_or_404(Player, slug=slug)

    qs_player_reg = player.tourn_participations.filter(
        participant__tournament__date__gte=datetime.date.today()).order_by(
        'participant__tournament__date')

    tour_list = qs_player_reg.values_list('participant__tournament__slug', flat=True)

    qs_player_not_reg = Tournament.objects.filter(date__gte=datetime.date.today(), registration_open=True).exclude(
        slug__in=list(tour_list)).order_by('date')

    context = {
        'player':player,
        'qs_player_reg':qs_player_reg,
        'qs_player_not_reg':qs_player_not_reg
    }

    return render(request, 'TournRegister/tournament_list.html', context)


@user_passes_test(check_player)
def show_pair(request, slug):
    try:
        pair = Participant.objects.get(slug=slug)
    except:
        messages.error(request, 'Die Meldung wurde in der Zwischenzeit zurückgezogen')
        return redirect(reverse('TournRegister:tournament_list', kwargs={'slug':request.user.player.slug}))

    if request.user.player.oebv_nr not in pair.players.all().values_list('player__oebv_nr', flat=True):
        messages.error(request, 'Dein Partner hat die Meldung geändert')
        return redirect(reverse('TournRegister:tournament_list', kwargs={'slug':request.user.player.slug}))

    return render(request, 'TournRegister/show_pair.html', {'pair':pair})


@user_passes_test(check_player)
def show_indiv(request, slug):
    try:
        participant = Participant.objects.get(slug=slug)
    except:
        messages.error(request, 'Die Meldung wurde in der Zwischenzeit zurückgezogen')
        return redirect(reverse('TournRegister:tournament_list', kwargs={'slug':request.user.player.slug}))

    return render(request, 'TournRegister/show_indiv.html', {'part':participant})


@user_passes_test(check_player)
def show_team(request, slug):
    try:
        team = Participant.objects.get(slug=slug)
    except:
        messages.error(request, 'Die Meldung wurde in der Zwischenzeit zurückgezogen')
        return redirect(reverse('TournRegister:tournament_list', kwargs={'slug':request.user.player.slug}))

    if request.user.player.oebv_nr not in team.players.all().values_list('player__oebv_nr', flat=True):
        messages.error(request, 'Ein anderes Teammitglied hat die Meldung geändert')
        return redirect(reverse('TournRegister:tournament_list', kwargs={'slug':request.user.player.slug}))

    return render(request, 'TournRegister/show_team.html', {'team':team})


@user_passes_test(check_player)
def delete_participant(request, slug):
    try:
        participant = Participant.objects.get(slug=slug)
    except:
        messages.error(request, 'Die Meldung wurde bereits zurückgezogen')
        return redirect(reverse('TournRegister:tournament_list', kwargs={'slug':request.user.player.slug}))

    if request.method == 'POST':
        tour_name = participant.tournament.name
        participant.delete()
        messages.success(request, 'Du hast dich vom {} abgemeldet'.format(tour_name))
        return redirect(reverse('TournRegister:tournament_list', kwargs={'slug':request.user.player.slug}))

    return render(request, 'TournRegister/participation_cofirm_delete.html', {'participant':participant})


@user_passes_test(check_player)
def register_pair_combo(request, slug):
    player = request.user.player
    try:
        tournament = Tournament.objects.get(slug=slug)
    except:
        messages.error(request, 'Das Turnier wurde mittlerweile gelöscht')
        return redirect(reverse('TournRegister:tournament_list', kwargs={'slug':player.slug}))

    if not tournament.registration_open:
        messages.error(request, 'Der Veranstalter hat das Turnier für Anmeldungen geschlossen')
        return redirect(reverse('TournRegister:tournament_list', kwargs={'slug':player.slug}))

    if slug in player.tourn_participations.all().values_list('participant__tournament__slug', flat=True):
        messages.error(request, 'Du bist schon angemeldet')
        return redirect(reverse('TournRegister:tournament_list', kwargs={'slug':player.slug}))

    qs = Player.objects.filter(oebv_member=True).exclude(slug=player.slug).exclude(
        slug__in=TournPlayer.objects.filter(participant__tournament__slug=tournament.slug).values_list(
            'player__slug', flat=True
        )
    ).order_by('last_name', 'first_name')

    choices =[]
    for pl in qs:
        choices.append('{} {} ({})'.format(pl.last_name, pl.first_name, pl.oebv_nr))

    if request.method == "POST":
        form = forms.PairComboForm(request.POST, own_oebv_nr=player.oebv_nr)

        if form.is_valid():
            partner_nr = isolate_oebv_nr(form.cleaned_data.get('partner'))
            try:
                partner = Player.objects.get(oebv_nr=partner_nr)
            except:
                messages.error(request, 'Dein Partner wurde mittlerweile gelöscht')
                return redirect(reverse('TournRegister:tournament_list', kwargs={'slug':player.slug}))

            if partner.slug in player.tourn_participations.all().values_list('participant__tournament__slug',
                                                                             flat=True):
                messages.error(request, 'Dein Partner ist schon angemeldet')
                return redirect(reverse('TournRegister:tournament_list', kwargs={'slug':player.slug}))

            participant = Participant(tournament=tournament)
            participant.save()
            pl1 = TournPlayer(participant=participant, player=player)
            pl1.save()
            pl2 = TournPlayer(participant=participant, player=partner)
            pl2.save()
            messages.success(request, 'Du bist für {} gemeldet'.format(tournament.name))
            return redirect(reverse('TournRegister:tournament_list', kwargs={'slug':player.slug}))


    else:
        form = forms.PairComboForm()

    context = {
        'form': form,
        'tournament': tournament,
        'choices': choices
    }

    return render(request, 'TournRegister/register_pair_combo.html', context)


@user_passes_test(check_player)
def register_team_combo(request, slug):
    player = request.user.player
    try:
        tournament = Tournament.objects.get(slug=slug)
    except:
        messages.error(request, 'Das Turnier wurde mittlerweile gelöscht')
        return redirect(reverse('TournRegister:tournament_list', kwargs={'slug':player.slug}))

    if not tournament.registration_open:
        messages.error(request, 'Der Veranstalter hat das Turnier für Anmeldungen geschlossen')
        return redirect(reverse('TournRegister:tournament_list', kwargs={'slug':player.slug}))

    if slug in player.tourn_participations.all().values_list('participant__tournament__slug', flat=True):
        messages.error(request, 'Du bist schon angemeldet')
        return redirect(reverse('TournRegister:tournament_list', kwargs={'slug':player.slug}))

    qs = Player.objects.filter(oebv_member=True).exclude(slug=player.slug).exclude(
        slug__in=TournPlayer.objects.filter(participant__tournament__slug=tournament.slug).values_list(
            'player__slug', flat=True
        )
    ).order_by('last_name', 'first_name')

    choices =[]
    for pl in qs:
        choices.append('{} {} ({})'.format(pl.last_name, pl.first_name, pl.oebv_nr))

    context = {}

    if request.method == "POST":
        form = forms.TeamComboForm(request.POST, own_oebv_nr=player.oebv_nr)

        if form.is_valid():
            members_list = [player]

            for i in range(2, 9):
                partner_nr = isolate_oebv_nr(form.cleaned_data.get('player{}'.format(i)))
                if partner_nr == -1:
                    continue
                try:
                    partner = Player.objects.get(oebv_nr=partner_nr)
                except:
                    messages.error(request, 'Dein Partner wurde mittlerweile gelöscht')
                    return redirect(reverse('TournRegister:tournament_list', kwargs={'slug': player.slug}))

                if partner.slug in player.tourn_participations.all().values_list('participant__tournament__slug',
                                                                                 flat=True):
                    messages.error(request, 'Dein Partner ist schon angemeldet')
                    return redirect(reverse('TournRegister:tournament_list', kwargs={'slug': player.slug}))

                members_list.append(partner)

            if len(members_list) > tournament.max_team_members:
                messages.error(request, 'Du hast zu viele Spieler gemeldet')
                return redirect(reverse('TournRegister:tournament_list', kwargs={'slug': player.slug}))



            participant = Participant(tournament=tournament, name=form.cleaned_data.get('name'))
            participant.save()

            for member in members_list:
                m = TournPlayer(participant=participant, player=member)
                m.save()

            messages.success(request, 'Du bist für {} gemeldet'.format(tournament.name))

            if len(members_list) < 4:
                messages.warning(request, 'Das Team besteht aus weniger als vier Spielern')

            return redirect(reverse('TournRegister:tournament_list', kwargs={'slug':player.slug}))

        else:
            context['team_name'] = form.cleaned_data.get('name')
            for i in range(2,9):
                pl_field = form.cleaned_data.get('player{}'.format(i))
                if pl_field:
                    context['pl_{}'.format(i)] = pl_field


    else:
        form = forms.TeamComboForm()

    context['form'] = form
    context['tournament'] = tournament
    context['choices'] = choices

    return render(request, 'TournRegister/register_team _combo.html', context)


@user_passes_test(check_player)
def register_indiv(request, slug):
    player = request.user.player
    try:
        tournament = Tournament.objects.get(slug=slug)
    except:
        messages.error(request, 'Das Turnier wurde mittlerweile gelöscht')
        return redirect(reverse('TournRegister:tournament_list', kwargs={'slug':player.slug}))

    if not tournament.registration_open:
        messages.error(request, 'Der Veranstalter hat das Turnier für Anmeldungen geschlossen')
        return redirect(reverse('TournRegister:tournament_list', kwargs={'slug':player.slug}))

    if slug in player.tourn_participations.all().values_list('participant__tournament__slug', flat=True):
        messages.error(request, 'Du bist schon angemeldet')
        return redirect(reverse('TournRegister:tournament_list', kwargs={'slug':player.slug}))

    if request.method == "POST":
        form = forms.IndivForm(request.POST)

        if form.is_valid():
            participant = Participant(tournament=tournament)
            participant.save()
            pl1 = TournPlayer(participant=participant, player=player)
            pl1.save()
            messages.success(request, 'Du bist für {} gemeldet'.format(tournament.name))
            return redirect(reverse('TournRegister:tournament_list', kwargs={'slug':player.slug}))


    else:
        form = forms.IndivForm()

    context = {
        'form': form,
        'tournament': tournament,
    }

    return render(request, 'TournRegister/register_indiv.html', context)