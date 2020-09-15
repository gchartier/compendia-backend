from rest_framework                import status
from rest_framework.response       import Response
from rest_framework.decorators     import api_view, permission_classes
from rest_framework.permissions    import IsAuthenticated
from account.models                import Account
from comic.models                  import Comic
from publisher.models              import Publisher, Imprint
from series.models                 import Series
#from character.models              import Character, ComicCharacter
from creator.models                import Creator, ComicCreator
from collection.models             import Collection, CollectedComic
from comic.api.serializers         import ComicUpdateSerializer, ComicCreateSerializer, ComicCoverSerializer, ComicSerializer
from rest_framework.pagination     import PageNumberPagination
from rest_framework.generics       import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters        import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from datetime                      import timedelta, datetime
from django.utils                  import timezone
import pytz

@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_detail_comic_view(request, pk):
	try:
		comic = Comic.objects.get(pk=pk)
	except Comic.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == "GET":
		serializer = ComicSerializer(comic, context={'request': request})
		return Response(serializer.data)

@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def api_update_comic_view(request, pk):

	try:
		comic = Comic.objects.get(pk=pk)
	except Comic.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	user = request.user
	if user.is_superuser != True:
		return Response({"response" : "You don't have access to update this"})
		
	if request.method == 'PUT':
		serializer = ComicUpdateSerializer(comic, data=request.data, partial=True)
		data = {}
		if serializer.is_valid():
			serializer.save()
			data['response']          = "Successfully updated comic"
			data['id']                = comic.id
			data['alt_id']            = comic.alt_id
			data['diamond_id']        = comic.diamond_id
			data['title']             = comic.title
			data['page_count']        = comic.page_count
			data['publisher_id']      = comic.publisher.id
			data['publisher_name']    = comic.publisher.name
			data['series_id']         = comic.series.id
			data['series_name']       = comic.series.name
			data['barcode']           = comic.barcode
			data['printing']          = comic.printing
			data['format_type']       = comic.format_type
			data['date_added']        = comic.date_added
			data['date_updated']      = comic.date_updated
			data['solicit_date']      = comic.solicit_date
			data['release_date']      = comic.release_date
			data['is_mature']         = comic.is_mature
			if comic.version_of:
				data['version_of_id'] = comic.version_of.id
			data['versions']          = comic.versions
			data['variant_code']      = comic.variant_code
			data['total_wanted']      = comic.total_wanted
			data['total_favorited']   = comic.total_favorited
			data['total_owned']       = comic.total_owned
			data['total_read']        = comic.total_read
			data['avg_rating']        = comic.get_avg_rating()
			data['number_of_reviews'] = comic.get_number_of_reviews()

			if comic.cover:
				cover_url = str(request.build_absolute_uri(comic.cover.url))
				if "?" in cover_url:
					cover_url = cover_url[:cover_url.rfind("?")]
				data['cover'] = cover_url

			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def api_delete_comic_view(request, pk):
	try:
		comic = Comic.objects.get(pk=pk)
	except Comic.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	user = request.user
	if user.is_superuser != True:
		return Response({"response" : "You don't have access to delete this."})

	if request.method == "DELETE":
		operation = comic.delete()
		data = {}
		if operation:
			data["success"] = "Successfully deleted comic"
		else:
			data["failure"] = "Failed to delete comic"
		return Response(data=data)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_create_comic_view(request):

	user = request.user
	if user.is_superuser != True:
		return Response({"response" : "You don't have access to add this"})
		
	if request.method == 'POST':

		data = request.data
		serializer = ComicCreateSerializer(data=data)

		data = {}
		if serializer.is_valid():
			comic = serializer.save()
			data['response']       = "Successfully created comic"
			data['id']             = comic.id
			data['alt_id']         = comic.alt_id
			data['diamond_id']     = comic.diamond_id
			data['title']          = comic.title
			data['page_count']     = comic.page_count
			data['publisher_id']   = comic.publisher.id
			data['publisher_name'] = comic.publisher.name
			data['series_id']      = comic.series.id
			data['series_name']    = comic.series.name
			data['barcode']        = comic.barcode
			data['printing']       = comic.printing
			data['format_type']    = comic.format_type
			data['date_added']     = comic.date_added
			data['date_updated']   = comic.date_updated
			data['solicit_date']   = comic.solicit_date
			data['is_mature']      = comic.is_mature
			if comic.version_of:
				data['version_of_id'] = comic.version_of.id
			data['variant_code'] = comic.variant_code

			if comic.cover:
				cover_url = str(request.build_absolute_uri(comic.cover.url))
				if "?" in cover_url:
					cover_url = cover_url[:cover_url.rfind("?")]
				data['cover'] = cover_url

			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class APIComicListView(ListAPIView):
	queryset = Comic.objects.all()
	serializer_class = ComicSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	pagination_class = PageNumberPagination
	filter_backends = [DjangoFilterBackend, SearchFilter]
	filterset_fields = ['publisher__id', 'series__id', 'imprint__id', 'version_of__id']
	search_fields = ('title',)

class APIComicNewReleasesListView(ListAPIView):
	def get_new_releases_day():
		today       = timezone.now()
		offset      = (today.weekday() - 2) % 7
		release_day = today - timedelta(days=offset)
		return release_day

	release_day            = get_new_releases_day()
	queryset               = Comic.objects.filter(release_date=datetime(release_day.year, release_day.month, release_day.day, tzinfo=pytz.UTC))
	serializer_class       = ComicSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes     = (IsAuthenticated,)
	pagination_class       = PageNumberPagination
	filter_backends        = [DjangoFilterBackend, SearchFilter]
	filterset_fields       = ['publisher__id', 'series__id', 'imprint__id', 'version_of__id']
	search_fields          = ('title',)

class APIComicNewReleasesCoversListView(ListAPIView):
	def get_new_releases_day():
		today       = timezone.now()
		offset      = (today.weekday() - 2) % 7
		release_day = today - timedelta(days=offset)
		return release_day

	release_day            = get_new_releases_day()
	queryset               = Comic.objects.filter(release_date=datetime(release_day.year, release_day.month, release_day.day, tzinfo=pytz.UTC))
	serializer_class       = ComicCoverSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes     = (IsAuthenticated,)
	pagination_class       = PageNumberPagination
	filter_backends        = [DjangoFilterBackend, SearchFilter]
	filterset_fields       = []
	search_fields          = ()