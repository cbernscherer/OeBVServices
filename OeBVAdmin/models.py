from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse_lazy

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from OeBVServices.utilities.sluggenerator import create_random_slug

# Create your models here.
class Club(models.Model):
    club_nr = models.PositiveIntegerField(primary_key=True)
    slug = models.SlugField(max_length=16, db_index=True, unique=True, default=create_random_slug)
    name = models.CharField(max_length=64)
    shortname = models.CharField(max_length=16, null= True, blank=True)
    club_admin = models.OneToOneField(to=User, on_delete=models.SET_NULL,
                                      related_name='club', default=None, null=True, blank=True)

    class Meta:
        ordering = ['club_nr']

    def __str__(self):
        clubstr = "{1}: {0}".format(self.name, self.club_nr)
        if self.shortname:
            clubstr += " ({0})".format(self.shortname)
        return clubstr

    def get_absolute_url(self):
        return reverse_lazy('OeBVAdmin:club_list')


class Player(models.Model):
    rank_choices = [
        ("GM", "Grandmaster"),
        ("JGM", "Junior Grandmaster"),
        ("SLM", "Senior Lifemaster"),
        ("LM", "Lifemaster"),
        ("P", "Pik"),
        ("H", "Herz"),
        ("K", "Karo"),
        ("T", "Treff"),
        ("A", "Anfänger")
    ]

    rank_limits = [
        ("GM", 600000),
        ("JGM", 300000),
        ("SLM", 150000),
        ("LM", 60000),
        ("P", 30000),
        ("H", 15000),
        ("K", 7000),
        ("T", 2500),
        ("A", 0)
    ]

    oebv_nr = models.PositiveIntegerField(primary_key=True)
    slug = models.SlugField(max_length=16, db_index=True, unique=True, default=create_random_slug)
    last_name = models.CharField(max_length=64)
    first_name = models.CharField(max_length=64)
    club = models.ForeignKey(Club, on_delete=models.SET_NULL, default=None, blank=True,
                             null=True, related_name='clubmembers')
    master_points = models.PositiveIntegerField(default=0)
    rank = models.CharField(max_length=3,default="A", choices=rank_choices)
    oebv_member = models.BooleanField(default=True)
    reg_user = models.OneToOneField(to=User, on_delete=models.SET_NULL,
                                    related_name='player', default=None, null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name', 'oebv_nr']

    def __str__(self):
        return "{0} {1}".format(self.last_name, self.first_name)

    def setrank(self):
        i = 0

        while True:
            rk, lim = self.rank_limits[i]

            if self.master_points >= lim:
                self.rank = rk
                break

            i += 1