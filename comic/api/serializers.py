from rest_framework             import serializers
from django.db.models           import Avg
from comic.models               import Comic
from publisher.models           import Publisher, Imprint
from series.models              import Series
from creator.models             import ComicCreator, Creator
from creator.api.serializers    import ComicCreatorSerializer, CreatorSerializer
from publisher.api.serializers  import PublisherSerializer
from series.api.serializers     import SeriesSerializer
from collection.models          import CollectedComic, ComicBox
from review.models              import Review
from django.conf                import settings
from django.core.files.storage  import default_storage
from django.core.files.storage  import FileSystemStorage
from comic.utils                import is_cover_aspect_ratio_valid, is_cover_size_valid

import os
IMAGE_SIZE_MAX_BYTES = 1024 * 1024 * 2 # 2MB
MIN_TITLE_LENGTH = 5
MIN_BODY_LENGTH = 50

class ComicSerializer(serializers.ModelSerializer):

	cover              = serializers.SerializerMethodField('format_cover_url')
	number_of_reviews  = serializers.SerializerMethodField('get_number_of_reviews')
	avg_rating         = serializers.SerializerMethodField('get_avg_rating')
	imprint            = serializers.PrimaryKeyRelatedField(many=False, queryset=Imprint.objects)
	creators           = ComicCreatorSerializer(source='comiccreator_set', many=True)
	version_of         = serializers.PrimaryKeyRelatedField(many=False, queryset=Comic.objects)
	collection_details = serializers.SerializerMethodField()
	is_read            = serializers.SerializerMethodField()
	is_favorited       = serializers.SerializerMethodField()
	is_wanted          = serializers.SerializerMethodField()
	user_rating        = serializers.SerializerMethodField()

	class Meta:
		model = Comic
		depth = 1
		fields = ['id', 'alt_id', 'diamond_id', 'title', 'item_number', 'release_date',
		'cover_price', 'cover', 'description', 'page_count', 'publisher', 'series', 'imprint',
		'creators', 'barcode', 'printing', 'format_type', 'date_added', 'date_updated',
		'solicit_date', 'is_mature', 'version_of', 'versions', 'variant_code', 'total_wanted',
		'total_favorited', 'total_owned', 'total_read', 'avg_rating', 'number_of_reviews',
		'collection_details', 'is_read', 'is_favorited', 'is_wanted', 'user_rating']

	def format_cover_url(self, comic):
		if comic.cover:
			cover = comic.cover
			new_url = cover.url
			if "?" in new_url:
				new_url = cover.url[:cover.url.rfind("?")]
			return new_url
		else:
			return ""

	def get_avg_rating(self, comic):
		return comic.get_avg_rating()

	def get_number_of_reviews(self, comic):
		return comic.get_number_of_reviews()

	def get_collection_details(self, object):
		try:
			collected_comic = object.comics.get(collection=self.context['request'].user.collection)

			collected_data = {}

			collected_data['id']              = collected_comic.id
			collected_data['date_collected']  = collected_comic.date_collected
			collected_data['purchase_price']  = collected_comic.purchase_price
			collected_data['bought_at']       = collected_comic.bought_at
			collected_data['condition']       = collected_comic.condition
			collected_data['is_slabbed']      = collected_comic.is_slabbed
			collected_data['certification']   = collected_comic.certification
			collected_data['grade']           = collected_comic.grade
			collected_data['quantity']        = collected_comic.quantity

			return collected_data

		except CollectedComic.DoesNotExist:
			return None

	def get_publisher(self, object):
		return Publisher.objects.get(pk=object.publisher_id)

	def get_series(self, object):
		return Publisher.objects.get(pk=object.series_id)

	def get_is_read(self, object):
		try:
			ComicBox.objects.get(collection=self.context['request'].user.collection, name='Read').comics.get(id=object.id)
			return True
		except Comic.DoesNotExist:
			return False

	def get_is_favorited(self, object):
		try:
			ComicBox.objects.get(collection=self.context['request'].user.collection, name='Favorites').comics.get(id=object.id)
			return True
		except Comic.DoesNotExist:
			return False

	def get_is_wanted(self, object):
		try:
			ComicBox.objects.get(collection=self.context['request'].user.collection, name='Want').comics.get(id=object.id)
			return True
		except Comic.DoesNotExist:
			return False

	def get_user_rating(self, comic):
		try:
			return Review.objects.get(author = self.context['request'].user, comic = comic).rating
		except Review.DoesNotExist:
			return 0.0

class ComicCoverSerializer(serializers.ModelSerializer):

	cover = serializers.SerializerMethodField('format_cover_url')

	class Meta:
		model = Comic
		fields = ['id', 'cover',]

	def format_cover_url(self, comic):
		if comic.cover:
			cover = comic.cover
			new_url = cover.url
			if "?" in new_url:
				new_url = cover.url[:cover.url.rfind("?")]
			return new_url
		else:
			return ""

class ComicUpdateSerializer(serializers.ModelSerializer):

	class Meta:
		model = Comic
		fields = ['alt_id', 'diamond_id', 'title', 'item_number', 'release_date',
		'cover_price', 'cover', 'description', 'page_count', 'publisher', 'series',
		'creators', 'barcode', 'printing', 'format_type', 'solicit_date', 'is_mature',
		'version_of', 'variant_code', ]

	def validate(self, comic):
		try:
			alt_id       = comic['alt_id']
			diamond_id   = comic['diamond_id']
			title        = comic['title']
			item_number  = comic['item_number']
			release_date = comic['release_date']
			cover_price  = comic['cover_price']
			cover        = comic['cover']
			description  = comic['description']
			page_count   = comic['page_count']
			publisher    = comic['publisher']
			series       = comic['series']
			creators     = comic['creators']
			barcode      = comic['barcode']
			printing     = comic['printing']
			format_type  = comic['format_type']
			solicit_date = comic['solicit_date']
			is_mature    = comic['is_mature']
			version_of   = comic['version_of']
			variant_code = comic['variant_code']
			
			url = os.path.join(settings.TEMP , str(cover))
			storage = FileSystemStorage(location=url)

			with storage.open('', 'wb+') as destination:
				for chunk in cover.chunks():
					destination.write(chunk)
				destination.close()

			# Check cover size
			if not is_cover_size_valid(url, IMAGE_SIZE_MAX_BYTES):
				os.remove(url)
				raise serializers.ValidationError({"response": "That cover is too large. Images must be less than 2 MB. Try a different cover."})

			# Check cover aspect ratio
			if not is_cover_aspect_ratio_valid(url):
				os.remove(url)
				raise serializers.ValidationError({"response": "Image height must not exceed cover width. Try a different cover."})

			os.remove(url)
		except KeyError:
			pass
		return comic

class ComicCreateSerializer(serializers.ModelSerializer):

	#cover      = serializers.SerializerMethodField('format_cover_url', required=False)
	publisher  = serializers.PrimaryKeyRelatedField(many=False, queryset=Publisher.objects)
	series     = serializers.PrimaryKeyRelatedField(many=False, queryset=Series.objects)
	creators   = serializers.SerializerMethodField(required=False)
	version_of = serializers.PrimaryKeyRelatedField(many=False, queryset=Comic.objects, required=False)

	class Meta:
		model = Comic
		fields = ['alt_id', 'diamond_id', 'title', 'item_number', 'release_date',
		'cover_price', 'cover', 'description', 'page_count', 'publisher', 'series',
		'creators', 'barcode', 'printing', 'format_type', 'solicit_date', 'is_mature',
		'version_of', 'variant_code',]

	def format_cover_url(self, comic):
		cover = comic.cover
		new_url = cover.url
		if "?" in new_url:
			new_url = cover.url[:cover.url.rfind("?")]
		return new_url


	def save(self):
		
		try:
			alt_id       = self.validated_data['alt_id']
			diamond_id   = self.validated_data['diamond_id']
			title        = self.validated_data['title']
			item_number  = self.validated_data['item_number']
			release_date = self.validated_data['release_date']
			cover_price  = self.validated_data['cover_price']
			#if 'cover' in self.validated_data:
			cover        = self.validated_data['cover']
			#else:
			#	cover = ""
			description  = self.validated_data['description']
			page_count   = self.validated_data['page_count']
			publisher    = self.validated_data['publisher']
			series       = self.validated_data['series']
			#creators     = self.validated_data['creators']
			barcode      = self.validated_data['barcode']
			printing     = self.validated_data['printing']
			format_type  = self.validated_data['format_type']
			solicit_date = self.validated_data['solicit_date']
			is_mature    = self.validated_data['is_mature']
			if 'version_of' in self.validated_data:
				version_of   = self.validated_data['version_of']
			else:
				version_of = None
			variant_code = self.validated_data['variant_code']
			
			comic = Comic(alt_id=alt_id, diamond_id=diamond_id, title=title, item_number=item_number,
				release_date=release_date, cover_price=cover_price, cover=cover, description=description,
				page_count=page_count, publisher=publisher, series=series, barcode=barcode, printing=printing,
				format_type=format_type, solicit_date=solicit_date, is_mature=is_mature, version_of=version_of,
				variant_code=variant_code)

			# if cover is not "":
			url = os.path.join(settings.TEMP , str(cover))
			storage = FileSystemStorage(location=url)

			with storage.open('', 'wb+') as destination:
				for chunk in cover.chunks():
					destination.write(chunk)
				destination.close()

			# 	# Check cover size
			# 	if not is_cover_size_valid(url, IMAGE_SIZE_MAX_BYTES):
			# 		os.remove(url)
			# 		raise serializers.ValidationError({"response": "That cover is too large. Images must be less than 2 MB. Try a different cover."})

			# 	# Check cover aspect ratio
			# 	if not is_cover_aspect_ratio_valid(url):
			# 		os.remove(url)
			# 		raise serializers.ValidationError({"response": "Cover height must not exceed cover width. Try a different cover."})

			os.remove(url)

			comic.save()
			#ComicCreator(comic=comic, creator=Creator.objects.get(pk=1), creator_type="Letterer").save()

			#if outcome:
			# for creator in creators:
			# 	print("creator " + creator)
			# 	if creator["id"] != None and creator["type"] != None and creator["action"] != None:
			# 		if creator["action"] is "add":
			# 			ComicCreator.objects.create(comic=comic, creator=Creator.objects.get(pk=creator["id"]), creator_type=creator["type"])

			return comic

		except KeyError as e:
			raise serializers.ValidationError({"response": e})