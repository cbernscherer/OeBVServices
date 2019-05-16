from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from accounts.forms import ChangeEmailForm, MyUserCreateForm
from OeBVAdmin.models import Player
from django.contrib.auth.models import Group, User
from django.contrib.auth import login
from django.contrib import messages
from django.core.mail import send_mail

players = Group.objects.get(name='Players')

# Create your views here.

class MyPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset_form.html'
    # success_url = '/accounts/reset_password/done'
    success_url = reverse_lazy('accounts:reset_password_done')
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_header.txt'


class PasswordResetSuccessView(TemplateView):
    template_name = 'accounts/password_reset_success..html'


@login_required
def change_email(request):
    if request.method == 'POST':
        form = ChangeEmailForm(request.POST)

        if form.is_valid():
            try:
                user = request.user
                user.email = form.cleaned_data['email']
                user.save()

                if form.cleaned_data['send_test_mail']:
                    subject = 'Neue Mailadresse'
                    message = 'Die Änderung war erfolgreich!'
                    from_email = 'cbernscherer@gmail.com'
                    to_email = [user.email]
                    send_mail(subject, message, from_email, to_email)
            except:
                messages.error(request, 'Es ist ein Fehler aufgetreten!')

            return redirect(reverse_lazy('index'))

    else:
        form = ChangeEmailForm(instance=request.user)

    return render(request, 'accounts/change_email.html', {'form':form})


def sign_up(request):
    if request.method == "POST":
        form = MyUserCreateForm(request.POST)

        if form.is_valid():
            user = form.save()

            oebv_nr = form.cleaned_data.get('ver_oebv_nr')
            player = Player.objects.get(oebv_nr=oebv_nr)
            user.last_name = player.last_name
            user.first_name = player.first_name
            user.groups.add(players)
            user.save()

            player.reg_user = user
            player.save()

            login(request, user)
            return redirect(reverse_lazy('index'))

    else:
        form = MyUserCreateForm()

    return render(request, 'accounts/signup.html', {'form':form})