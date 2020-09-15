from django.db import models

class Publisher(models.Model):
	name   = models.CharField(max_length=50, null=False, blank=False)
	alt_id = models.CharField(max_length=100, null=True, blank=True)

class Imprint(models.Model):
	name = models.CharField(max_length=50, null=False, blank=False)
	alt_id = models.CharField(max_length=100, null=True, blank=True)
	publisher = models.ForeignKey(Publisher, null=False, on_delete=models.CASCADE)