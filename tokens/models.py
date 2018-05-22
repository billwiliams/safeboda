from django.db import models
from django.core.urlresolvers import reverse


# Create your models here.
class Events(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=45, blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6)  # event location latitude
    lon = models.DecimalField(max_digits=9, decimal_places=6)  # event location longitude
    date = models.DateTimeField(auto_now=True)  # event date
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse("events")

    class Meta:
        db_table = 'event'
        managed = True


class PromoCode(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=45, blank=True, null=True, unique=True)
    active = models.BooleanField(default=False)
    radius = models.FloatField(default=10)  # radius from destination/origin default to 10km
    amount = models.FloatField(default=10)  # Amount worth of the promo code
    event = models.ForeignKey('Events', models.DO_NOTHING, null=False, related_name='Event')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.code)

    def get_absolute_url(self):
        return reverse("promo_code")

    class Meta:
        db_table = 'promo_code'
        managed = True
