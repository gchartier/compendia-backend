from rest_framework import serializers
from series.models import Series
from comic.models import Comic
from publisher.models import Publisher, Imprint

class SeriesSerializer(serializers.ModelSerializer):

	number_of_entries = serializers.SerializerMethodField('get_number_of_entries')

	class Meta:
		model  = Series
		fields = ['pk', 'name', 'alt_id', 'publisher', 'imprint', 'genre', 'years', 'number_of_entries', 'is_one_shot', 'is_mini_series', 'mini_series_limit']

	def get_number_of_entries(self, series):
		return series.comic_set.count()

class SeriesUpdateSerializer(serializers.ModelSerializer):

	class Meta:
		model  = Series

		fields = ['name', 'alt_id', 'publisher', 'imprint', 'genre', 'years', 'is_one_shot', 'is_mini_series', 'mini_series_limit']

	def validate(self, series):
		try:
			name              = series['name']
			alt_id            = series['alt_id']
			publisher         = series['publisher']
			imprint           = series['imprint']
			genre             = series['genre']
			years             = series['years']
			is_one_shot       = series['is_one_shot']
			is_mini_series    = series['is_mini_series']
			mini_series_limit = series['mini_series_limit']

		except KeyError:
			pass
		return series

class SeriesCreateSerializer(serializers.ModelSerializer):
	publisher = serializers.PrimaryKeyRelatedField(many=False, queryset=Publisher.objects)
	imprint = serializers.PrimaryKeyRelatedField(many=False, allow_null=True, queryset=Imprint.objects)

	class Meta:
		model = Series
		fields = ['name', 'alt_id', 'publisher', 'imprint', 'genre', 'years', 'is_one_shot', 'is_mini_series', 'mini_series_limit']


	def save(self):
		name              = self.validated_data['name']
		alt_id            = self.validated_data['alt_id']
		publisher         = self.validated_data['publisher']
		imprint           = self.validated_data['imprint']
		genre             = self.validated_data['genre']
		years             = self.validated_data['years']
		is_one_shot       = self.validated_data['is_one_shot']
		is_mini_series    = self.validated_data['is_mini_series']
		mini_series_limit = self.validated_data['mini_series_limit']
		series = Series(alt_id=alt_id, name=name, publisher=publisher, imprint=imprint, genre=genre, years=years, is_one_shot=is_one_shot,
			is_mini_series=is_mini_series, mini_series_limit=mini_series_limit)
		series.save()

		return series