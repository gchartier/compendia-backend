from django.db                import models
from django.db.models.signals import post_delete
from django.conf              import settings
from django.dispatch          import receiver
from review.models            import Review
from django.db.models         import Avg, Q

def upload_location(instance, filename, **kwargs):
	file_path = 'comic/{id}'.format(id=str(instance.pk), filename=filename)
	return file_path

class Comic(models.Model):
	alt_id            = models.CharField(max_length=100, null=True, blank=True)
	diamond_id        = models.CharField(max_length=100, null=False, blank=True)
	title             = models.CharField(max_length=100, null=False, blank=False)
	item_number       = models.CharField(max_length=50, blank=True, null=False)
	release_date      = models.DateTimeField(null=False, blank=False)
	cover_price       = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
	cover             = models.ImageField(upload_to=upload_location, null=False, blank=True)
	description       = models.TextField(null=False, blank=True, default="No Description")
	page_count        = models.PositiveSmallIntegerField(null=True, blank=True)
	publisher         = models.ForeignKey("publisher.Publisher", null=False, blank=False, on_delete=models.CASCADE)
	series            = models.ForeignKey("series.Series", blank=False, null=False, on_delete=models.CASCADE)
	imprint           = models.ForeignKey("publisher.Imprint", null=True, blank=True, on_delete=models.CASCADE)
	creators          = models.ManyToManyField("creator.Creator", blank=True, through="creator.ComicCreator")
	barcode           = models.CharField(max_length=200, null=False, blank=True)
	printing          = models.PositiveSmallIntegerField(default=1, null=False, blank=True)
	format_type       = models.CharField(max_length=50, null=False, blank=True)
	date_added        = models.DateTimeField(auto_now_add=True)
	date_updated      = models.DateTimeField(auto_now=True)
	solicit_date      = models.DateTimeField(null=True, blank=True)
	is_mature         = models.BooleanField(default=False, blank=True, null=False)
	is_standard_issue = models.BooleanField(default=False, blank=True, null=False)
	version_of        = models.ForeignKey("self", blank=True, null=True, on_delete=models.CASCADE)
	versions          = models.PositiveSmallIntegerField(default=0, blank=True, null=False)
	variant_code      = models.CharField(max_length=100, null=False, blank=True)
	total_wanted      = models.PositiveIntegerField(default=0, blank=True, null=False)
	total_favorited   = models.PositiveIntegerField(default=0, blank=True, null=False)
	total_owned       = models.PositiveIntegerField(default=0, blank=True, null=False)
	total_read        = models.PositiveIntegerField(default=0, blank=True, null=False)

	def get_avg_rating(self):
		reviews = Review.objects.filter(comic__id=self.id)
		if reviews:
			return reviews.aggregate(average=Avg("rating"))["average"]
		else:
			return "No Ratings"

	def get_number_of_reviews(self):
		return Review.objects.filter(Q(comic__id=self.id) & ~Q(title="")).count()

	def save(self, *args, **kwargs):
		if self.pk is None:
			saved_cover = self.cover
			self.cover = None
			super(Comic, self).save(*args, **kwargs)
			self.cover = saved_cover

		super(Comic, self).save(*args, **kwargs)

@receiver(post_delete, sender=Comic)
def submission_delete(sender, instance, **kwargs):
	instance.cover.delete(False)
