from django.urls import path, re_path, reverse_lazy
from django.contrib.auth import views as auth_views
from accounts import views

app_name = 'accounts'

urlpatterns = [
    re_path(r'^login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('change_password/',
         auth_views.PasswordChangeView.as_view(template_name='accounts/password_change_form.html',
                                               success_url=reverse_lazy('index')),
            name='change_password'),
    path('reset_password/', views.MyPasswordResetView.as_view(), name='reset_password'),
    path('reset_password/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done_form.html'),
        name='reset_password_done'),
    re_path(r'^reset_password/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',
        auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html',
                                                    success_url=reverse_lazy('accounts:reset_password_success')),
        name='reset_password_confirm'),
    path('reset_password/success/', views.PasswordResetSuccessView.as_view(), name='reset_password_success'),
    path('change_email/', views.change_email, name='change_email'),
    path('signup', views.sign_up, name='signup'),
]