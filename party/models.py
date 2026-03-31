from django.db import models


class Pokemon(models.Model):
    LOCATION_PARTY = 'party'
    LOCATION_PC = 'pc'
    LOCATION_CHOICES = [
        (LOCATION_PARTY, 'Party'),
        (LOCATION_PC, 'PC Box'),
    ]

    pokeapi_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    image_url = models.URLField(max_length=500)
    types = models.JSONField(default=list)

    # Stats
    hp = models.IntegerField(default=0)
    attack = models.IntegerField(default=0)
    defense = models.IntegerField(default=0)
    special_attack = models.IntegerField(default=0)
    special_defense = models.IntegerField(default=0)
    speed = models.IntegerField(default=0)
    total_power = models.IntegerField(default=0)

    location = models.CharField(max_length=10, choices=LOCATION_CHOICES, default=LOCATION_PARTY)
    order = models.IntegerField(default=0)
    captured_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'captured_at']

    def __str__(self):
        return f"{self.name.capitalize()} (#{self.pokeapi_id})"

    def save(self, *args, **kwargs):
        self.total_power = self.hp + self.attack + self.defense + self.special_attack + self.special_defense + self.speed
        super().save(*args, **kwargs)

    @property
    def primary_type(self):
        if self.types:
            return self.types[0]
        return 'normal'
