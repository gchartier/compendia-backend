from rest_framework import serializers
from creator.models import Creator, ComicCreator
from comic.models   import Comic
from account.models import Account

class CreatorSerializer(serializers.ModelSerializer):

	class Meta:
		model  = Creator
		fields = ['pk', 'name', 'alt_id',]

class ComicCreatorSerializer(serializers.HyperlinkedModelSerializer):
	creator_id = serializers.ReadOnlyField(source='creator.id')
	name       = serializers.ReadOnlyField(source='creator.name')

	class Meta:
		model  = ComicCreator
		fields = ['pk', 'creator_id', 'name', 'creator_type']

class CreatorUpdateSerializer(serializers.ModelSerializer):

	class Meta:
		model  = Creator

		fields = ['name', 'alt_id',]

	def validate(self, creator):
		name = ""
		try:
			name   = creator['name']
			alt_id = creator['alt_id']

		except KeyError:
			pass

		try:
			existing_creator = Creator.objects.get(name=name)
			if existing_creator:
				raise serializers.ValidationError({"response": "There's already a creator with that name",
					"creator": CreatorSerializer(existing_creator).data})
		except Creator.DoesNotExist:
			return creator

class CreatorCreateSerializer(serializers.ModelSerializer):

	class Meta:
		model = Creator
		fields = ['name', 'alt_id',]

	def save(self):
		try:
			name   = self.validated_data['name']
			alt_id = self.validated_data['alt_id']

			try:
				existing_creator = Creator.objects.get(name=name)
				if existing_creator:
					raise serializers.ValidationError({"response": "There's already a creator with that name",
						"creator": CreatorSerializer(existing_creator).data})
			except Creator.DoesNotExist:
				creator = Creator(name=name, alt_id=alt_id,)
				creator.save()
				return creator

		except KeyError:
			raise serializers.ValidationError({"response": "Please include all required fields"})

# Probably don't need this stuff

# class ComicCreatorCreateSerializer(serializers.ModelSerializer):

# 	class Meta:
# 		model = ComicCreator
# 		fields = ['comic', 'creator', 'creator_type', 'alt_id', 'name',]

# 	def save(self):
# 		try:
# 			comic        = self.validated_data['comic']
# 			creator      = self.validated_data['creator']
# 			creator_type = self.validated_data['creator_type']
# 			alt_id       = self.context['request'].data['alt_id']
# 			name         = self.context['request'].data['name']

# 			# Validate alt_id and name fields
# 			if !alt_id:
# 				raise serializers.ValidationError({"response": "alt_id is a required parameter"})
# 			if !name:
# 				raise serializers.ValidationError({"response": "name is a required parameter"})

# 			# Create a new creator if one does not already exist
# 			try:
# 				existing_creator = Creator.objects.get(name=name, alt_id=alt_id)
# 			except Creator.DoesNotExist:
# 				creator = Creator(name=name, alt_id=alt_id,)
# 				creator.save()

# 			# Create a new comic creator only if one does not already exist for the given comic/creator
# 			try:
# 				existing_comic_creator = ComicCreator.objects.get(comic__id=comic.id, creator__id=creator.id)
# 				if existing_comic_creator:
# 					raise serializers.ValidationError({"response": "This creator is already associated with this comic",
# 						"comic_creator": ComicCreatorSerializer(existing_comic_creator).data})
# 			except ComicCreator.DoesNotExist:
# 				comic_creator = ComicCreator(comic=comic, creator=creator, creator_type=creator_type,)
# 				comic_creator.save()
# 				return comic_creator

# 		except KeyError:
# 			raise serializers.ValidationError({"response": "Please include all required fields"})

# class ComicCreatorUpdateSerializer(serializers.ModelSerializer):

# 	class Meta:
# 		model  = ComicCreator

# 		fields = ['creator_type',]

# 	def validate(self, comic_creator):
# 		try:
# 			creator_type = comic_creator['creator_type']

# 		except KeyError:
# 			raise serializers.ValidationError({"response": "Please include all required fields"})
# 		return comic_creator