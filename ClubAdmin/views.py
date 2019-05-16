from django.shortcuts import get_object_or_404, redirect
from django.http import FileResponse, HttpResponse
from django.urls import reverse
from django.views.generic import ListView, DeleteView, DetailView, UpdateView, CreateView, TemplateView
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import UserPassesTestMixin
from ClubAdmin.models import Tournament
from ClubAdmin import forms
from OeBVAdmin.models import Club
from django.contrib.auth.models import Group
import pandas as pd
import os
from OeBVServices.settings import BASE_DIR
from django.contrib import messages

# Create your views here.
clubadmins = Group.objects.get(name='ClubAdmins')

def check_club_admin(user):
    return clubadmins in user.groups.all()

class TournamentListView(UserPassesTestMixin, ListView):
    def test_func(self):
        return clubadmins in self.request.user.groups.all()

    model = Tournament
    template_name = 'ClubAdmin/tournament_list.html'

    def get_queryset(self):
        club = get_object_or_404(Club, slug=self.kwargs.get('slug'))
        return club.tournaments.order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        club = get_object_or_404(Club, slug=self.kwargs.get('slug'))
        context['club'] = club
        return context


class TournamentCreateView(UserPassesTestMixin, CreateView):
    def test_func(self):
        return clubadmins in self.request.user.groups.all()

    model = Tournament
    template_name = 'ClubAdmin/tournament_form.html'
    form_class = forms.TournamentForm

    def get_success_url(self):
        return reverse('ClubAdmin:tournament_list', kwargs={'slug':self.kwargs.get('slug')})

    def get_initial(self):
        organizer = get_object_or_404(Club, slug=self.kwargs.get('slug'))
        return {'organizer':organizer}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        club = get_object_or_404(Club, slug=self.kwargs.get('slug'))
        context['club'] = club
        context['new'] = True
        return context


class TournamentDetailView(UserPassesTestMixin, DetailView):
    def test_func(self):
        return clubadmins in self.request.user.groups.all()

    model = Tournament
    template_name = 'ClubAdmin/tournament_detail.html'


class TournamentDeleteView(UserPassesTestMixin, DeleteView):
    def test_func(self):
        return clubadmins in self.request.user.groups.all()

    model = Tournament
    template_name = 'ClubAdmin/tournament_confirm_delete.html'

    def get_success_url(self):
        return reverse('ClubAdmin:tournament_list', kwargs={'slug':self.request.user.club.slug})


class ToutnamentUpdateView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        return clubadmins in self.request.user.groups.all()

    model = Tournament
    template_name = 'ClubAdmin/tournament_form.html'
    form_class = forms.TournamentUpdateForm

    def get_success_url(self):
        return reverse('ClubAdmin:tournament_detail', kwargs={'slug':self.kwargs.get('slug')})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tournament = get_object_or_404(Tournament, slug=self.kwargs.get('slug'))
        context['club'] = tournament.organizer
        context['new'] = False
        return context


class DownloadView(UserPassesTestMixin, TemplateView):
    def test_func(self):
        return clubadmins in self.request.user.groups.all()

    template_name = 'ClubAdmin/tournament_download.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tournament = get_object_or_404(Tournament, slug=self.kwargs.get('slug'))
        context['tournament'] = tournament
        return context


@user_passes_test(check_club_admin)
def download_excel(request, slug):
    tournament = get_object_or_404(Tournament, slug=slug)
    filename = str(tournament.organizer.club_nr) + '.xlsx'
    fullpath = os.path.join(BASE_DIR, 'media/generated', filename)

    if tournament.participants.count() == 0:
        messages.error(request, 'Keine Teilnehmer gemeldet')
        return redirect(reverse('ClubAdmin:tournament_detail', kwargs={'slug':slug}))

    participants = []
    for participant in tournament.participants.all():
        line = []
        if tournament.tourn_type == 'T':
            line.append(participant.name)

        for player in participant.players.all():
            line.append(player.player.last_name + ' ' + player.player.first_name)

        if tournament.tourn_type == 'T':
            for i in range(participant.players.count(), tournament.max_team_members):
                line.append('')

        participants.append(line)

    df = pd.DataFrame(participants)

    with pd.ExcelWriter(fullpath) as writer:
        if tournament.tourn_type == 'P':
            headers = ['Spieler 1', 'Spieler 2']
        elif tournament.tourn_type == 'I':
            headers = ['Spieler']
        elif tournament.tourn_type =='T':
            headers = ['Team', 'Spieler 1', 'Spieler 2', 'Spieler 3', 'Spieler 4']
            for i in range(5, tournament.max_team_members + 1):
                headers.append('Spieler ' + str(i))

        df.to_excel(writer,index=False, header=headers)

    return FileResponse(open(fullpath, 'rb'), as_attachment=True)
