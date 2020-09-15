from rest_framework                import status
from rest_framework.response       import Response
from rest_framework.decorators     import api_view, permission_classes
from rest_framework.permissions    import IsAuthenticated
from account.models                import Account
from review.models                 import Review
from review.api.serializers        import ReviewCreateSerializer, ReviewSerializer, ReviewUpdateSerializer
from rest_framework.pagination     import PageNumberPagination
from rest_framework.generics       import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters        import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_create_review_view(request):

	if request.method == 'POST':

		data = request.data
		serializer = ReviewCreateSerializer(data=data, context={'request': request})

		data = {}
		if serializer.is_valid():
			review = serializer.save()

			data['response']        = "Successfully created review"
			data['id']              = review.id
			data['title']           = review.title
			data['body']            = review.body
			data['rating']          = review.rating
			data['comic_id']        = review.comic.id
			data['comic_title']     = review.comic.title
			data['author_username'] = request.user.username

			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_detail_review_view(request, pk):
	try:
		review = Review.objects.get(pk=pk)
	except Review.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == "GET":
		serializer = ReviewSerializer(review)
		return Response(serializer.data)

@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def api_update_review_view(request, pk):

	try:
		review = Review.objects.get(pk=pk)
	except Review.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	user = request.user
	if user.id != review.author.id:
		return Response({"response" : "You don't have access to update this"})
		
	if request.method == 'PUT':
		serializer = ReviewUpdateSerializer(review, data=request.data, partial=True)
		data = {}
		if serializer.is_valid():
			serializer.save()

			data['response']        = "Successfully updated review"
			data['id']              = review.id
			data['title']           = review.title
			data['body']            = review.body
			data['rating']          = review.rating
			data['comic_id']        = review.comic.id
			data['comic_title']     = review.comic.title
			data['author_id']       = review.author.id
			data['author_username'] = review.author.username

			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def api_delete_review_view(request, pk):
	try:
		review = Review.objects.get(pk=pk)
	except Review.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	user = request.user
	if user.id != review.author.id:
		return Response({"response" : "You don't have access to delete this"})

	if request.method == "DELETE":
		operation = review.delete()
		data = {}
		if operation:
			data["success"] = "Successfully deleted review"
		else:
			data["failure"] = "Failed to delete review"
		return Response(data=data)

class APIReviewListView(ListAPIView):
	queryset               = Review.objects.all()
	serializer_class       = ReviewSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes     = (IsAuthenticated,)
	pagination_class       = PageNumberPagination
	filter_backends        = [DjangoFilterBackend, SearchFilter]
	filterset_fields       = ['comic__id', 'author__id']
	search_fields          = ('title', 'body',)

class APIComicReviewsListView(ListAPIView):
	serializer_class       = ReviewSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes     = (IsAuthenticated,)
	pagination_class       = PageNumberPagination
	filter_backends        = [DjangoFilterBackend, SearchFilter]
	filterset_fields       = ['comic__id', 'author__id']
	search_fields          = ('title', 'body',)

	def get_queryset(self):
		return Review.objects.filter(comic__pk=self.kwargs['pk'])