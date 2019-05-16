from django.urls import path, re_path

from ClubAdmin import views

app_name = 'ClubAdmin'

urlpatterns = [
    re_path(r'^(?P<slug>\w+)/$', views.TournamentListView.as_view(), name='tournament_list'),
    re_path(r'^(?P<slug>\w+)/create/$', views.TournamentCreateView.as_view(), name='tournament_create'),
    re_path(r'^tournament/(?P<slug>\w+)/$', views.TournamentDetailView.as_view(), name='tournament_detail'),
    re_path(r'^tournament/(?P<slug>\w+)/delete/$', views.TournamentDeleteView.as_view(), name='tournament_delete'),
    re_path(r'^tournament/(?P<slug>\w+)/update/$', views.ToutnamentUpdateView.as_view(), name='tournament_update'),
    re_path(r'^tournament/(?P<slug>\w+)/download/$', views.DownloadView.as_view(), name='tournament_download'),
    re_path(r'^tournament/(?P<slug>\w+)/download/excel/$', views.download_excel, name='tournament_download_excel'),
]