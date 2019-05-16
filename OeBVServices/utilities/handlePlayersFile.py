import pandas as pd
from OeBVAdmin import models
from OeBVServices.utilities.sluggenerator import create_random_slug

def handle_players_upload(request, file):
    club_dict = {}
    for club in models.Club.objects.all():
        club_dict[club.club_nr] = club

    df = pd.read_excel(file, 'SpoXls')
    oebv_nr_arr = []

    for pos, d in df.iterrows():
        oebv_nr_arr.append(d['NR'])
        player, created = models.Player.objects.get_or_create(oebv_nr=d["NR"])
        if created:
            player.slug = create_random_slug()

        player.last_name = str(d['NAME']).strip().title()
        player.first_name = str(d['VNAME']).strip().title()

        if d['STCLUB'] in club_dict:
            player.club = club_dict[d['STCLUB']]

        player.master_points = d['MPGES']
        player.setrank()
        player.oebv_member = True

        player.save()

#    deactivate players who cancelled their membership
    for player in models.Player.objects.exclude(oebv_nr__in=oebv_nr_arr):
        player.oebv_member = False
        if player.reg_user:
            user = player.reg_user
            player.reg_user = None
            user.delete()
        player.save()

