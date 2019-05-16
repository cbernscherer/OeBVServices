from django.urls import path, re_path, reverse_lazy
from OeBVAdmin import views

app_name = 'OeBVAdmin'

urlpatterns = [
    path('', views.ClubListView.as_view(), name='club_list'),
    path('club/new/', views.create_club, name='club_create'),
    re_path(r'^club/(?P<slug>\w+)/$', views.ClubDetailView.as_view(), name='club_detail'),
    re_path(r'^club/(?P<slug>\w+)/update/$', views.ClubUpdateView.as_view(), name='club_update'),
    re_path(r'^club/(?P<slug>\w+)/delete/$', views.ClubDeleteView.as_view(), name='club_delete'),
    re_path(r'^club/delete_admin/(?P<pk>\d+)/$', views.del_club_admin, name='del_club_admin'),
    re_path(r'^club/create_admin/(?P<slug>\w+)/$', views.create_club_admin, name='create_club_admin'),
    re_path(r'^club/remove_admin/(?P<slug>\w+)/$', views.remove_club_admin, name='remove_club_admin'),
    path('players/upload/', views.player_upload, name='players_upload'),
    path('players/reg_user/', views.RegUsersList.as_view(), name='reguser_list'),
    re_path(r'^players/reg_user/(?P<slug>\w+)/$', views.RegUserDetail.as_view(), name='reguser_detail'),
    re_path(r'^players/reg_user/(?P<slug>\w+)/remove/$', views.remove_reg_user, name='reguser_remove'),
    path('players/not_members/', views.NotMembersist.as_view(), name='not_member_list'),
]