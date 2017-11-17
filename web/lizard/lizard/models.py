from django.utils.translation import ugettext_lazy as _
from django.contrib.gis.db import models


class UserModel(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)


class Organisation(models.Model):
    name = models.CharField(max_length=100)


class Manhole(models.Model):
    """Manhole (Put or Knoop in Dutch).
    Units:
    - water_consumption (drinkwaterverbruik): l/s
    - drainage_area_sloping (hellend afvoerend oppervlak): m2
    - drainage_area_flat (vlak afvoerend oppervlak): m2
    - drainage_area_stretched (vlak uitgestrekt afvoerend oppervlak): m2
    """
    organisation_id = models.IntegerField(null=True)
    created = models.DateTimeField()
    code = models.CharField(
        _("code"),
        max_length=50,
        blank=False,
        null=True,
        default=None
    )
    surface_level = models.FloatField(_("surface level"), null=True)
    drainage_area = models.IntegerField(_("drainage area"), null=True)
    material = models.CharField(_("material"), max_length=4)
    width = models.FloatField(_("width"), null=True)
    length = models.FloatField(_("length"), null=True)
    shape = models.CharField(_("shape"), max_length=4)
    bottom_level = models.FloatField(_("bottom level"), null=True)
    image_url = models.CharField(max_length=255)
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    num_timeseries = models.IntegerField(default=0)
    water_consumption = models.FloatField(
        _("water consumption"), null=True)
    geometry = models.PointField(_("geometry"), srid=4326, dim=3, null=True)
