from rest_framework         import serializers
from series.models          import Series
from pulllist.models        import PullList, PullListSeries
from series.api.serializers import SeriesSerializer
from comic.models           import Comic
from django.utils           import timezone
import datetime

class PullListSeriesSerializer(serializers.ModelSerializer):
	series = SeriesSerializer(many=False, required=True)

	class Meta:
		model  = PullListSeries
		fields = ['pk', 'series', 'include_standard_issues', 'include_variants', 'include_TPB', 'include_all_collections', 'include_all']
		depth = 1

class PullListSeriesUpdateSerializer(serializers.ModelSerializer):
	remove_comics = serializers.SerializerMethodField()

	class Meta:
		model  = PullListSeries

		fields = ['include_standard_issues', 'include_variants', 'include_TPB', 'include_all_collections', 'include_all', 'remove_comics']

	def validate(self, pull_list_series):
		try:
			include_standard_issues = pull_list_series['include_standard_issues']
			include_variants        = pull_list_series['include_variants']
			include_TPB             = pull_list_series['include_TPB']
			include_all_collections = pull_list_series['include_all_collections']
			include_all             = pull_list_series['include_all']
			remove_comics           = pull_list_series['remove_comics']

		except KeyError:
			pass

		return pull_list_series

	def save(self):
		pre_update = self.context['pull_list_series_before_update']
		pull_list  = pre_update.pull_list

		if 'include_standard_issues' in self.validated_data:
			include_standard_issues = self.validated_data['include_standard_issues']
		else:
			include_standard_issues = pre_update.include_standard_issues

		if 'include_variants' in self.validated_data:
			include_variants = self.validated_data['include_variants']
		else:
			include_variants = pre_update.include_variants

		if 'include_TPB' in self.validated_data:
			include_TPB = self.validated_data['include_TPB']
		else:
			include_TPB = pre_update.include_TPB

		if 'include_all_collections' in self.validated_data:
			include_all_collections = self.validated_data['include_all_collections']
		else:
			include_all_collections = pre_update.include_all_collections

		if 'include_all' in self.validated_data:
			include_all = self.validated_data['include_all']
		else:
			include_all = pre_update.include_all

		if 'remove_comics' in self.validated_data:
			remove_comics = self.validated_data['remove_comics']
		else:
			remove_comics = False

		# Get all the comics from the pull list that are in the series and remove the comics according to the request
		comics_in_series = pull_list.comics.filter(series=pre_update.series)
		if pre_update.include_all is True and include_all is False and remove_comics is True:
			pull_list.comics.remove(*list(comics_in_series))
		else:
			# Remove all standard issue comics in the series from the pull list
			if pre_update.include_standard_issues is True and include_standard_issues is False and remove_comics is True:
				pull_list.comics.remove(*list(comics_in_series.filter(is_standard_issue=True, format_type="Issue")))

			# Remove all variant comics in the series from the pull list
			if pre_update.include_variants is True and include_variants is False and remove_comics is True:
				pull_list.comics.remove(*list(comics_in_series.filter(is_standard_issue=False, format_type="Issue", variant_code__ne="")))

			# Remove all collected format comics in the series from the pull list
			if pre_update.include_all_collections is True and include_all_collections is False and remove_comics is True:
				pull_list.comics.remove(*list(comics_in_series.filter(format_type__in=["TPB","Hardcover","Compendium"])))

			# Remove all TPB format comics in the series from the pull list
			if pre_update.include_TPB is True and include_TPB is False and remove_comics is True:
				pull_list.comics.remove(*list(comics_in_series.filter(format_type="TPB")))
			
		# Add the unreleased comics to the pull list according to the request
		today = timezone.now()
		unreleased_comics = Comic.objects.filter(series=pre_update.series, release_date__gte=datetime.date(today.year, today.month, today.day))
		if pre_update.include_all is False and include_all is True:
			pull_list.comics.add(*list(unreleased_comics))
		else:
			if pre_update.include_standard_issues is False and include_standard_issues is True:
				pull_list.comics.add(*list(unreleased_comics.filter(is_standard_issue=True, format_type="Issue")))

			if pre_update.include_variants is False and include_variants is True:
				pull_list.comics.add(*list(unreleased_comics.filter(is_standard_issue=False, format_type="Issue", variant_code__ne="")))

			if pre_update.include_all_collections is False and include_all_collections is True:
				pull_list.comics.add(*list(unreleased_comics.filter(format_type__in=["TPB","Hardcover","Compendium"])))

			if pre_update.include_TPB is False and include_TPB is True:
				pull_list.comics.add(*list(unreleased_comics.filter(format_type="TPB")))

class PullListSeriesSubscribeSerializer(serializers.ModelSerializer):
	series = serializers.PrimaryKeyRelatedField(many=False, queryset=Series.objects)

	class Meta:
		model = PullListSeries
		fields = ['series', 'include_standard_issues', 'include_variants', 'include_TPB', 'include_all_collections', 'include_all',]


	def save(self):

		pull_list = self.context['pull_list']

		series = self.validated_data['series']

		if 'include_standard_issues' not in self.context['request'].data:
			include_standard_issues = True
		else:
			include_standard_issues = self.validated_data['include_standard_issues']
		include_variants        = self.validated_data['include_variants']
		include_TPB             = self.validated_data['include_TPB']
		include_all_collections = self.validated_data['include_all_collections']
		include_all             = self.validated_data['include_all']

		# Subscribe series to pull list unless it is already in the user's pull list
		try:
			already_subbed = PullListSeries.objects.get(pull_list=pull_list, series=series)
			if already_subbed:
				raise serializers.ValidationError({"response": "You've already subscribed to this series."})
		except PullListSeries.DoesNotExist:
			pull_list_series = PullListSeries(series=series, pull_list=pull_list, include_standard_issues=include_standard_issues,
				include_variants=include_variants, include_TPB=include_TPB, include_all_collections=include_all_collections, include_all=include_all)
			pull_list_series.save()

			today = timezone.now()

			unreleased_comics = Comic.objects.filter(series=series, release_date__gte=datetime.date(today.year, today.month, today.day))
			if include_all:
				pull_list.comics.add(*list(unreleased_comics))
			else:
				if include_standard_issues:
					pull_list.comics.add(*list(unreleased_comics.filter(is_standard_issue=True, format_type="Issue")))

				if include_variants:
					pull_list.comics.add(*list(unreleased_comics.filter(is_standard_issue=False, format_type="Issue", variant_code__ne="")))

				if include_all_collections:
					pull_list.comics.add(*list(unreleased_comics.filter(format_type__in=["TPB","Hardcover","Compendium"])))
				elif include_TPB:
					pull_list.comics.add(*list(unreleased_comics.filter(format_type="TPB")))

			return pull_list_series