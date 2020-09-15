from django.db import models
from publisher.models import Publisher, Imprint

class Series(models.Model):
	name              = models.CharField(max_length=50, null=False, blank=False)
	alt_id            = models.CharField(max_length=100, null=True, blank=True)
	publisher         = models.ForeignKey(Publisher, null=False, on_delete=models.CASCADE)
	imprint           = models.ForeignKey(Imprint, null=True, on_delete=models.CASCADE)
	genre             = models.CharField(max_length=50, null=True, blank=True)
	years             = models.CharField(max_length=100, null=True, blank=True)
	is_one_shot       = models.BooleanField(default=False)
	is_mini_series    = models.BooleanField(default=False)
	mini_series_limit = models.PositiveSmallIntegerField(null=True)