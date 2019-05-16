from django.urls import path, re_path
from TournRegister import views

app_name = 'TournRegister'

urlpatterns = [
    re_path(r'^list/(?P<slug>\w+)/$', views.player_tourn_list, name='tournament_list'),
    re_path(r'^pair/(?P<slug>\w+)/show/$', views.show_pair, name='show_pair'),
    re_path(r'^participant/(?P<slug>\w+)/delete/$', views.delete_participant, name='delete_participant'),
    re_path(r'^register_pair/(?P<slug>\w+)/$', views.register_pair_combo, name='register_pair'),
    re_path(r'^team/(?P<slug>\w+)/show/$', views.show_team, name='show_team'),
    re_path(r'^register_team/(?P<slug>\w+)/$', views.register_team_combo, name='register_team'),
    re_path(r'^indiv/(?P<slug>\w+)/show/$', views.show_indiv, name='show_indiv'),
    re_path(r'^register_indiv/(?P<slug>\w+)/$', views.register_indiv, name='register_indiv'),
]