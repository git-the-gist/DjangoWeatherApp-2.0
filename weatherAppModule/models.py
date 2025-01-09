
from django.db import models
from django.utils.translation import gettext as _

class Cities(models.Model):
    id = models.BigIntegerField(primary_key=True, default='id', blank=True, null=False)
    country = models.CharField(_("country"), blank=True, null=True, max_length=255)
    state = models.CharField(_("state"), blank=True, null=True, max_length=255)
    county = models.CharField(_("county"), blank=True, null=True, max_length=255)
    name = models.CharField(_("name"), blank=True, null=True, max_length=255)
    normalized_name = models.CharField(_("normalized_name"), blank=True, null=True, max_length=255)
    lat = models.FloatField(_("lat"), blank=True, null=False, max_length=255)
    lng = models.FloatField(_("lng"), blank=True, null=True, max_length=255)