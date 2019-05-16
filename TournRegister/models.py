from django.db import models
from OeBVAdmin.models import Club, Player
from ClubAdmin.models import Tournament
from OeBVServices.utilities.sluggenerator import create_random_slug

# Create your models here.

class Participant(models.Model):
    # diese Tabelle ist entweder ein Team oder ein Paar

    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='participants')
    name = models.CharField(max_length=64, null=True, blank=True) # für Teamturniere
    slug = models.SlugField(max_length=16, db_index=True, unique=True, default=create_random_slug)

    def __str__(self):
        return '{}: {}'.format(self.tournament.name, self.name)



class TournPlayer(models.Model):
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE, related_name='players')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='tourn_participations')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['participant', 'player'], name='PlayerUnique')
        ]

    def __str__(self):
        return '{}: {}. {}'.format(self.participant.tournament.name,
                                   self.player.first_name[0],
                                   self.player.last_name)
