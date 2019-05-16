from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import Group, User
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from OeBVAdmin import models, forms
from django.contrib import messages
from OeBVServices.utilities.sluggenerator import create_random_slug
from OeBVServices.utilities.handlePlayersFile import handle_players_upload
from django.core.mail import send_mail

# Create your views here.
oebv_admins = Group.objects.get(name='OeBVAdmins')
club_admins = Group.objects.get(name='ClubAdmins')

# function for the decorator
def check_group(user):
    return oebv_admins in user.groups.all()

class ClubListView(UserPassesTestMixin, ListView):
    def test_func(self):
        return oebv_admins in self.request.user.groups.all()

    template_name = 'OeBVAdmin/club_list.html'
    model = models.Club


class ClubDetailView(UserPassesTestMixin, DetailView):
    def test_func(self):
        return oebv_admins in self.request.user.groups.all()

    template_name = 'OeBVAdmin/club_detail.html'
    model = models.Club


class ClubUpdateView(UserPassesTestMixin, UpdateView):
    def test_func(self):
        return oebv_admins in self.request.user.groups.all()

    def get_success_url(self):
        return reverse_lazy('OeBVAdmin:club_detail', kwargs={'slug':self.kwargs.get('slug')})

    template_name = 'OeBVAdmin/club_update_form.html'
    model = models.Club
    form_class = forms.ClubUpdateForm


class ClubDeleteView(UserPassesTestMixin, DeleteView):
    def test_func(self):
        return oebv_admins in self.request.user.groups.all()

    def get_success_url(self):
        club = get_object_or_404(models.Club, slug=self.kwargs.get('slug'))
        if club.club_admin:
            return reverse_lazy('OeBVAdmin:del_club_admin', kwargs={'pk':club.club_admin.pk})
        else:
            return reverse_lazy('OeBVAdmin:club_list')


    model = models.Club


@user_passes_test(check_group)
def create_club(request):
    if request.method == 'POST':
        form = forms.ClubForm(request.POST)

        if form.is_valid():
            try:
                club = form.save()
            except:
                messages.error(request, 'Beim Speichern ist ein Fehler aufgetreten!')
                form = forms.ClubForm()
            else:
                messages.success(request, club.name + ' gespeichert')

                if form.cleaned_data['proceed'] == 'new':
                    form = forms.ClubForm()
                else:
                    return redirect(reverse_lazy('OeBVAdmin:club_list'))
        else:
            messages.error(request, 'Beim Speichern ist ein Fehler aufgetreten!')

    else:
        form = forms.ClubForm()

    return render(request, 'OeBVAdmin/club_form.html', {'form':form, 'new':True})


@user_passes_test(check_group)
def del_club_admin(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return redirect(reverse_lazy('OeBVAdmin:club_list'))


@user_passes_test(check_group)
def remove_club_admin(request, slug):
    club = get_object_or_404(models.Club, slug=slug)

    if request.method == 'POST':
        form = forms.RemoveClubAdmin(request.POST)

        if form.is_valid():
            try:
                user = club.club_admin
                user.delete()
            except:
                pass

            return redirect(reverse_lazy('OeBVAdmin:club_detail', kwargs={'slug':slug}))

    else:
        form = forms.RemoveClubAdmin()

    context = {
        'form':form,
        'clubname':club.name,
        'slug':slug
    }
    return render(request, 'OeBVAdmin/remove_club_admin.html', context)



@user_passes_test(check_group)
def create_club_admin(request, slug):
    club = get_object_or_404(models.Club, slug=slug)

    if request.method == 'POST':
        form = forms.CreateClubAdmin(request.POST)

        if form.is_valid():
            try:
                user = User()
                user.username = 'club_' + str(club.club_nr)
                user.set_password(create_random_slug(10))
                user.email = form.cleaned_data['email']
                user.save()

                user.groups.add(club_admins)

                user.save()

                club.club_admin = user
                club.save()

            #     generate email
                subject = 'Admin für ' + club.name
                message = 'Wie gewünscht haben wir den Admin für ' + club.name + ' angelegt. '
                message += 'Dein Benutzername lautet ' + user.username + '.\n'
                message += 'Aus Sicherheitsgründen wurde ein zufälliges Passwort generiert, das niemandem bekannt ist '
                message += 'und auch nicht eingesehen werden kann. Klicke bitte im Login-Dialog auf Passwort vergessen '
                message += 'und folge den Anweisungen.'
                from_email = 'cbernscherer@gmail.com'
                to_email = [user.email]

                send_mail(subject, message, from_email, to_email)
            except:
                pass

            return redirect(reverse_lazy('OeBVAdmin:club_detail', kwargs={'slug':slug}))

    else:
        form = forms.CreateClubAdmin()

    context = {
        'form':form,
        'clubname':club.name,
        'slug':slug
    }
    return render(request, 'OeBVAdmin/create_club_admin.html', context)


@user_passes_test(check_group)
def player_upload(request):
    if request.method == "POST":
        form = forms.PlayersUploadForm(request.POST, request.FILES)

        if form.is_valid():
            if 'players_file' in request.FILES:
                try:
                    file = request.FILES['players_file']
                    handle_players_upload(request, file)
                except:
                    messages.error(request, 'Fehler beim Upload')
                else:
                    messages.success(request, 'Upload abgeschlossen')
                    return redirect(reverse_lazy('OeBVAdmin:not_member_list'))

            else:
                messages.error(request, 'Fehler beim Upload')

    else:
        form = forms.PlayersUploadForm()

    return render(request, 'OeBVAdmin/players_upload.html', {'form':form})


class RegUsersList(UserPassesTestMixin, ListView):
    def test_func(self):
        return oebv_admins in self.request.user.groups.all()

    template_name = 'OeBVAdmin/player_list.html'

    def get_queryset(self):
        return models.Player.objects.filter(reg_user__isnull=False).order_by('last_name', 'first_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reg_user'] = True
        return context


class NotMembersist(UserPassesTestMixin, ListView):
    def test_func(self):
        return oebv_admins in self.request.user.groups.all()

    template_name = 'OeBVAdmin/player_list.html'

    def get_queryset(self):
        return models.Player.objects.filter(oebv_member=False).order_by('last_name', 'first_name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_member'] = True
        return context


class RegUserDetail(UserPassesTestMixin,DetailView):
    def test_func(self):
        return oebv_admins in self.request.user.groups.all()

    template_name = 'OeBVAdmin/player_detail.html'
    model = models.Player

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reg_user'] = True
        return context


@user_passes_test(check_group)
def remove_reg_user(request, slug):
    player = get_object_or_404(models.Player, slug=slug)

    if request.method == 'POST':
        form = forms.RemoveRegUser(request.POST)

        if form.is_valid():
            try:
                user = player.reg_user
                user.delete()
            except:
                pass

            return redirect(reverse_lazy('OeBVAdmin:reguser_list'))

    else:
        form = forms.RemoveRegUser()

    context = {
        'form':form,
        'playername':'{0} {1}'.format(player.first_name, player.last_name),
        'slug':slug
    }
    return render(request, 'OeBVAdmin/remove_reg_user.html', context)