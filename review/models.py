from django.db import models
from django.core.exceptions import ValidationError

def validate_rating(value):
	if value < 1 or value > 10:
		raise ValidationError(('Rating must be a number between 1 and 10'), params={'value': value},)

class Review(models.Model):
	title  = models.CharField(max_length=200, null=False, blank=True)
	body   = models.TextField(null=True, blank=True)
	rating = models.PositiveSmallIntegerField(null=True, validators=[validate_rating])
	comic  = models.ForeignKey("comic.Comic", on_delete=models.CASCADE, null=False)
	author = models.ForeignKey("account.Account", on_delete=models.CASCADE, null=False, blank=True)