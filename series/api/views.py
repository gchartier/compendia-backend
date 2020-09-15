from rest_framework                import status
from rest_framework.response       import Response
from rest_framework.decorators     import api_view, permission_classes
from rest_framework.permissions    import IsAuthenticated
from account.models                import Account
from series.models                 import Series
from series.api.serializers        import SeriesCreateSerializer, SeriesSerializer, SeriesUpdateSerializer
from rest_framework.pagination     import PageNumberPagination
from rest_framework.generics       import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters        import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_create_series_view(request):

	user = request.user
	if user.is_superuser != True:
		return Response({"response" : "You don't have access to add this"})
		
	if request.method == 'POST':

		data = request.data
		serializer = SeriesCreateSerializer(data=data)

		data = {}
		if serializer.is_valid():
			series = serializer.save()

			data['response']          = "Successfully created series"
			data['id']                = series.id
			data['name']              = series.name
			data['alt_id']            = series.alt_id
			data['publisher_name']    = series.publisher.name
			data['publisher_id']      = series.publisher.id
			data['imprint_name']      = series.imprint.name
			data['imprint_id']        = series.imprint.id
			data['genre']             = series.genre
			data['years']             = series.years
			data['is_one_shot']       = series.is_one_shot
			data['is_mini_series']    = series.is_mini_series
			data['mini_series_limit'] = series.mini_series_limit

			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_detail_series_view(request, pk):
	try:
		series = Series.objects.get(pk=pk)
	except Series.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == "GET":
		serializer = SeriesSerializer(series)
		return Response(serializer.data)

@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def api_update_series_view(request, pk):

	try:
		series = Series.objects.get(pk=pk)
	except Series.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	user = request.user
	if user.is_superuser != True:
		return Response({"response" : "You don't have access to update this"})
		
	if request.method == 'PUT':
		serializer = SeriesUpdateSerializer(series, data=request.data, partial=True)
		data = {}
		if serializer.is_valid():
			serializer.save()

			data['response']          = "Successfully updated series"
			data['id']                = series.id
			data['name']              = series.name
			data['alt_id']            = series.alt_id

			if series.publisher != None:
				data['publisher_name']    = series.publisher.name
				data['publisher_id']      = series.publisher.id
			else:
				data['publisher_name']    = None
				data['publisher_id']      = None

			if series.imprint != None:
				data['imprint_name']      = series.imprint.name
				data['imprint_id']        = series.imprint.id
			else:
				data['imprint_name']      = None
				data['imprint_id']        = None

			data['genre']             = series.genre
			data['years']             = series.years
			data['is_one_shot']       = series.is_one_shot
			data['is_mini_series']    = series.is_mini_series
			data['mini_series_limit'] = series.mini_series_limit

			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def api_delete_series_view(request, pk):
	try:
		series = Series.objects.get(pk=pk)
	except Series.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	user = request.user
	if user.is_superuser != True:
		return Response({"response" : "You don't have access to delete this"})

	if request.method == "DELETE":
		operation = series.delete()
		data = {}
		if operation:
			data["success"] = "Successfully deleted series"
		else:
			data["failure"] = "Failed to delete series"
		return Response(data=data)

class APISeriesListView(ListAPIView):
	queryset = Series.objects.all()
	serializer_class = SeriesSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	pagination_class = PageNumberPagination
	filter_backends = [DjangoFilterBackend, SearchFilter]
	filterset_fields = ['publisher__id', 'imprint__id']
	search_fields = ('name',)