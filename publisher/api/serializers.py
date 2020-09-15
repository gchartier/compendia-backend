from rest_framework import serializers
from publisher.models import Imprint, Publisher

class PublisherSerializer(serializers.ModelSerializer):

	class Meta:
		model  = Publisher
		fields = ['pk', 'name', 'alt_id']

class PublisherUpdateSerializer(serializers.ModelSerializer):

	class Meta:
		model  = Publisher
		fields = ['alt_id', 'name']

	def validate(self, publisher):
		try:
			name   = publisher['name']
			alt_id = publisher['alt_id']

		except KeyError:
			pass
		return publisher

class PublisherCreateSerializer(serializers.ModelSerializer):


	class Meta:
		model = Publisher
		fields = ['alt_id', 'name']


	def save(self):
		
		try:
			name = self.validated_data['name']
			alt_id = self.validated_data['alt_id']		
			publisher = Publisher(alt_id=alt_id, name=name,)

			publisher.save()
			return publisher
		except KeyError:
			raise serializers.ValidationError({"response": "You must have a name"})