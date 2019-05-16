from django.db import models
from OeBVAdmin.models import Club
from OeBVServices.utilities.sluggenerator import create_random_slug
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Tournament(models.Model):
    tourn_type_choices = [
        ("P", "Paarturnier"),
        ("T", "Teamturnier"),
        ("I", "Individualturnier")
    ]

    name = models.CharField(max_length=256)
    date = models.DateField()
    organizer = models.ForeignKey(to=Club, on_delete=models.CASCADE, related_name='tournaments')
    tourn_type = models.CharField(max_length=1, default="P", choices=tourn_type_choices)
    registration_open = models.BooleanField(default=True)
    slug = models.SlugField(max_length=16, db_index=True, unique=True, default=create_random_slug)
    info = models.URLField(blank=True, null=True)
    max_team_members = models.PositiveSmallIntegerField(default=6,
                                                        validators=[
                                                            MinValueValidator(4),
                                                            MaxValueValidator(8)
                                                        ])

    class Meta:
        ordering = ['date']

    def __str__(self):
        return "{date} {name} ({type}, Veranstalter: {club}".format(
            date = self.date.strftime("%d.%m.%Y"),
            name = self.name,
            type = self.tourn_type,
            club = self.organizer.name
        )