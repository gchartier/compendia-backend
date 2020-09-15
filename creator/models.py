from django.db import models

class Creator(models.Model):
	name   = models.CharField(max_length=50, null=False, blank=False)
	alt_id = models.CharField(max_length=100, null=False, blank=True)

class ComicCreator(models.Model):
	comic        = models.ForeignKey("comic.Comic", on_delete=models.CASCADE)
	creator      = models.ForeignKey(Creator, on_delete=models.CASCADE)
	creator_type = models.CharField(max_length=200, null=False, blank=True)