from django.db                import models
from django.conf              import settings
from comic.models             import Comic
from django.db.models.signals import post_save
from django.core.exceptions   import ValidationError

class Collection(models.Model):
	user = models.OneToOneField("account.Account", on_delete=models.CASCADE)

	@classmethod
	def initialize_comic_boxes(self, collection):
		ComicBox(name="Favorites", collection=collection).save()
		ComicBox(name="Read", collection=collection).save()
		ComicBox(name="Want", collection=collection).save()


class CollectedComic(models.Model):

	def validate_grade(value):
		if value > 10.0 or value < 0.0:
			raise ValidationError('Ensure the comic grade is between 1.0 and 10.0')
		else:
			return value

	collection     = models.ForeignKey(Collection, on_delete=models.CASCADE, null=False, blank=False)
	comic          = models.ForeignKey("comic.Comic", on_delete=models.CASCADE, null=False, blank=False, related_name='comics')
	date_collected = models.DateTimeField(null=False, blank=True)
	purchase_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
	bought_at      = models.CharField(null=True, blank=True, max_length=50)
	condition      = models.CharField(null=True, blank=True, max_length=50)
	is_slabbed     = models.BooleanField(default=False, blank=True, null=False)
	certification  = models.CharField(null=True, blank=True, max_length=50)
	grade          = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True, validators=[validate_grade])
	quantity       = models.PositiveSmallIntegerField(null=False, blank=True)

class ComicBox(models.Model):
	name       = models.CharField(null=False, blank=False, max_length=50)
	comics     = models.ManyToManyField("comic.Comic", blank=True)
	collection = models.ForeignKey(Collection, on_delete=models.CASCADE, null=False, blank=False)