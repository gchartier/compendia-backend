from rest_framework        import serializers
from collection.models     import Collection, CollectedComic, ComicBox
from comic.models          import Comic
from review.models         import Review
from publisher.models      import Publisher, Imprint
from comic.api.serializers import ComicSerializer
import datetime

# Collection Serializers

class CollectionSerializer(serializers.ModelSerializer):

	number_of_collected_comics = serializers.SerializerMethodField()
	number_of_read_comics      = serializers.SerializerMethodField()
	number_of_reviews          = serializers.SerializerMethodField()

	class Meta:
		model  = Collection
		fields = ['pk', 'number_of_read_comics', 'number_of_collected_comics', 'number_of_reviews']

	def get_number_of_read_comics(self, collection):
		return ComicBox.objects.get(collection=collection, name="Read").comics.count()

	def get_number_of_collected_comics(self, collection):
		return CollectedComic.objects.filter(collection=collection).count()

	def get_number_of_reviews(self, collection):
		return Review.objects.filter(author=collection.user).count()


# Collected Comic Serializers

class CollectedComicSerializer(serializers.ModelSerializer):
	comic = ComicSerializer(many=False, required=True)

	class Meta:
		model  = CollectedComic
		fields = ['pk', 'comic', 'date_collected', 'purchase_price', 'bought_at', 'condition', 'is_slabbed', 'certification', 'grade', 'quantity',]
		depth = 1

class CollectedComicAddSerializer(serializers.ModelSerializer):

	class Meta:
		model = CollectedComic
		fields = ['date_collected', 'purchase_price', 'bought_at', 'condition', 'is_slabbed', 'certification', 'grade', 'quantity',]

	def save(self):
		comic  = self.context['comic']
		if 'date_collected' in self.validated_data:
			date_collected = self.validated_data['date_collected']
		else:
			date_collected = str(datetime.datetime.now())

		if 'purchase_price' in self.validated_data:
			purchase_price = self.validated_data['purchase_price']
		else:
			purchase_price = None

		if 'bought_at' in self.validated_data:
			bought_at = self.validated_data['bought_at']
		else:
			bought_at = None

		if 'condition' in self.validated_data:
			condition = self.validated_data['condition']
		else:
			condition = None

		if 'is_slabbed' in self.validated_data:
			is_slabbed = self.validated_data['is_slabbed']
		else:
			is_slabbed = False

		if 'certification' in self.validated_data:
			certification = self.validated_data['certification']
		else:
			certification = None

		if 'grade' in self.validated_data:
			grade = self.validated_data['grade']
		else:
			grade = None

		if 'quantity' in self.validated_data:
			quantity = self.validated_data['quantity']
		else:
			quantity = 1

		# Add comic to collection unless it is already in the user's collection
		try:
			already_collected = CollectedComic.objects.get(collection=self.context['request'].user.collection, comic=comic)
			if already_collected:
				raise serializers.ValidationError({"response": "This comic is already in your collection."})
		except CollectedComic.DoesNotExist:
			collected_comic = CollectedComic(collection=self.context['request'].user.collection, comic=comic, date_collected=date_collected,
				purchase_price=purchase_price, bought_at=bought_at, condition=condition, is_slabbed=is_slabbed, certification=certification, grade=grade, quantity=quantity)
			collected_comic.save()
			return collected_comic

class CollectedComicUpdateSerializer(serializers.ModelSerializer):

	class Meta:
		model  = CollectedComic
		fields = ['date_collected', 'purchase_price', 'bought_at', 'condition', 'is_slabbed', 'certification', 'grade', 'quantity',]

	def validate(self, collected_comic):
		try:
			date_collected = collected_comic['date_collected']
			purchase_price = collected_comic['purchase_price']	
			bought_at      = collected_comic['bought_at']
			condition      = collected_comic['condition']
			is_slabbed     = collected_comic['is_slabbed']
			certification  = collected_comic['certification']
			grade          = collected_comic['grade']
			quantity       = collected_comic['quantity']

		except KeyError:
			pass
		return collected_comic


# Comic Box Serializers

class ComicBoxSerializer(serializers.ModelSerializer):

	number_of_entries = serializers.SerializerMethodField('get_number_of_entries')

	class Meta:
		model  = ComicBox
		fields = ['pk', 'name', 'number_of_entries',]

	def get_number_of_entries(self, comic_box):
		return comic_box.comics.count()

class ComicBoxComicsSerializer(serializers.ModelSerializer):

	comics = ComicSerializer(many=True)

	class Meta:
		model  = ComicBox
		fields = ['comics',]

class ComicBoxUpdateSerializer(serializers.ModelSerializer):
	add_comic    = serializers.PrimaryKeyRelatedField(many=False, required=False, queryset=Comic.objects)
	remove_comic = serializers.PrimaryKeyRelatedField(many=False, required=False, queryset=Comic.objects)

	class Meta:
		model  = ComicBox

		fields = ['name', 'add_comic', 'remove_comic',]

	def validate(self, comic_box):
		try:
			name         = comic_box['name']
			add_comic    = self.validated_data['add_comic']
			remove_comic = self.validated_data['remove_comic']

		except KeyError:
			pass
		return comic_box

class ComicBoxCreateSerializer(serializers.ModelSerializer):
	initial_comic = serializers.PrimaryKeyRelatedField(many=False, required=False, queryset=Comic.objects)

	class Meta:
		model = ComicBox
		fields = ['name', 'initial_comic',]

	def save(self):
		name = self.validated_data['name']
		if 'initial_comic' in self.validated_data:
			initial_comic = self.validated_data['initial_comic']

		comic_box = ComicBox(name=name, collection=self.context['request'].user.collection)
		comic_box.save()

		return comic_box