from django.db    import models
from django.conf  import settings
from comic.models import Comic

class PullList(models.Model):
	collection        = models.OneToOneField("collection.Collection", on_delete=models.CASCADE)
	subscribed_series = models.ManyToManyField("series.Series", blank=True, through="pulllist.PullListSeries")
	comics            = models.ManyToManyField("comic.Comic", blank=True)

class PullListSeries(models.Model):
	series                  = models.ForeignKey("series.Series", on_delete=models.CASCADE)
	pull_list               = models.ForeignKey("pulllist.PullList", on_delete=models.CASCADE)
	include_standard_issues = models.BooleanField(default=True, null=False, blank=False)
	include_variants        = models.BooleanField(default=False, null=False, blank=False)
	include_TPB             = models.BooleanField(default=False, null=False, blank=False)
	include_all_collections = models.BooleanField(default=False, null=False, blank=False)
	include_all             = models.BooleanField(default=False, null=False, blank=False)