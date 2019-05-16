from django.shortcuts import render, redirect
from django.contrib.auth import models
from django.urls import reverse
from django.views.generic import TemplateView

def index(request):
    oebv_admins = models.Group.objects.get(name='OeBVAdmins')
    club_admins = models.Group.objects.get(name='ClubAdmins')
    players = models.Group.objects.get(name='Players')

    if request.user.is_authenticated:
        # redirect users depending on the group they belong to
        if oebv_admins in request.user.groups.all():
            return redirect(reverse('OeBVAdmin:club_list'))
        elif club_admins in request.user.groups.all():
            return redirect(reverse('ClubAdmin:tournament_list',kwargs={'slug':request.user.club.slug}))
        elif players in request.user.groups.all():
            return redirect(reverse('TournRegister:tournament_list', kwargs={'slug':request.user.player.slug}))

    return render(request, 'index.html')


class AboutView (TemplateView):
    template_name = 'about.html'