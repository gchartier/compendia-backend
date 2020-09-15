from rest_framework import serializers
from review.models  import Review
from comic.models   import Comic
from account.models import Account

class ReviewSerializer(serializers.ModelSerializer):

	class Meta:
		model  = Review
		fields = ['pk', 'title', 'body', 'rating', 'author', 'comic',]

class ReviewUpdateSerializer(serializers.ModelSerializer):

	class Meta:
		model  = Review

		fields = ['title', 'body', 'rating',]

	def validate(self, review):
		try:
			title  = review['title']
			body   = review['body']
			rating = review['rating']

		except KeyError:
			pass
		return review

class ReviewCreateSerializer(serializers.ModelSerializer):
	comic  = serializers.PrimaryKeyRelatedField(many=False, queryset=Comic.objects)

	class Meta:
		model = Review
		fields = ['title', 'body', 'rating', 'comic',]

	def save(self):
		try:
			title  = self.validated_data['title']
			body   = self.validated_data['body']
			rating = self.validated_data['rating']
			comic  = self.validated_data['comic']
			
			# Create new review unless one already exists for this comic by this user
			try:
				previously_reviewed = Review.objects.get(author__id=self.context['request'].user.id, comic__id=comic.id)
				if previously_reviewed:
					raise serializers.ValidationError({"response": "You've already rated/reviewed this.",
						"review": ReviewSerializer(previously_reviewed).data})
			except Review.DoesNotExist:
				review = Review(title=title, body=body, rating=rating, author=self.context['request'].user, comic=comic)
				review.save()
				return review

		except KeyError as e:
			raise serializers.ValidationError({"response": "Please include all required fields"})