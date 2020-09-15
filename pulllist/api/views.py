from rest_framework                import status
from rest_framework.response       import Response
from rest_framework.decorators     import api_view, permission_classes
from rest_framework.permissions    import IsAuthenticated
from account.models                import Account
from pulllist.models               import PullList, PullListSeries
from comic.models                  import Comic
from comic.api.serializers         import ComicSerializer
from pulllist.api.serializers      import PullListSeriesSubscribeSerializer, PullListSeriesUpdateSerializer	, PullListSeriesSerializer
from rest_framework.pagination     import PageNumberPagination
from rest_framework.generics       import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters        import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_detail_pull_list_series_view(request, pk):
	try:
		pull_list_series = PullListSeries.objects.get(pk=pk)
		if(pull_list_series.pull_list.collection.user != request.user):
			return Response({"response" : "You don't have access to this"}, status=status.HTTP_403_FORBIDDEN)
	except PullListSeries.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == "GET":
		serializer = PullListSeriesSerializer(pull_list_series)
		return Response(serializer.data)

class APIPullListSeriesListView(ListAPIView):
	serializer_class       = PullListSeriesSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes     = (IsAuthenticated,)
	pagination_class       = PageNumberPagination
	filter_backends        = [DjangoFilterBackend, SearchFilter]
	filterset_fields       = ['include_standard_issues', 'include_variants', 'include_TPB', 'include_all_collections', 'include_all', 'series__publisher__name', 'series__imprint__name']
	search_fields          = ('series__name',)

	def get_queryset(self):
		return PullListSeries.objects.filter(pull_list__collection__user=self.request.user)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_sub_series_pulllist_view(request):

	pull_list = PullList.objects.get(collection__user=request.user)
		
	if request.method == 'POST':

		data = request.data
		serializer = PullListSeriesSubscribeSerializer(data=data, context={'pull_list': pull_list, 'request': request})

		data = {}
		if serializer.is_valid():
			pull_list_series = serializer.save()

			data['response']                = "Successfully subscribed to series"
			data['id']                      = pull_list_series.id
			data['series_id']               = pull_list_series.series.id
			data['include_standard_issues'] = pull_list_series.include_standard_issues
			data['include_variants']        = pull_list_series.include_variants
			data['include_TPB']             = pull_list_series.include_TPB
			data['include_all_collections'] = pull_list_series.include_all_collections
			data['include_all']             = pull_list_series.include_all

			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def api_unsub_series_pulllist_view(request):

	user = request.user
	try:
		pull_list_series = PullListSeries.objects.get(series__id=request.data["series"])
		pull_list = pull_list_series.pull_list
		if user != pull_list.collection.user:
			return Response({"response" : "You don't have access to this"}, status=status.HTTP_403_FORBIDDEN)
	except PullListSeries.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == "DELETE":
		series    = pull_list_series.series
		operation = pull_list_series.delete()
		data      = {}
		if operation:
			if 'remove_comics' in request.data and request.data['remove_comics'] == "true":
				comics = pull_list.comics.filter(series=series)
				pull_list.comics.remove(*list(comics))
			data["response"] = "Successfully unsubscribed from series"
		else:
			data["response"] = "Failed to unsubscribe from series"
		return Response(data=data)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_add_comic_pulllist_view(request):

	pull_list = PullList.objects.get(collection__user=request.user)
		
	if "comic" in request.data:
		try:
			comic = pull_list.comics.get(pk=request.data["comic"])
			return Response({"response" : "Comic is already in your pull list"})
		except Comic.DoesNotExist:
			try:
				pull_list.comics.add(Comic.objects.get(pk=request.data["comic"]))
			except Comic.DoesNotExist:
				return Response({"response" : "Comic does not exist"}, status=status.HTTP_400_BAD_REQUEST)
			return Response({"response" : "Successfully added comic to your pull list"})
	else:
		return Response({"response" : "Comic parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes((IsAuthenticated,))
def api_remove_comic_pulllist_view(request):

	pull_list = PullList.objects.get(collection__user=request.user)
		
	if "comic" in request.data:
		try:
			comic = pull_list.comics.get(pk=request.data["comic"])
			pull_list.comics.remove(comic)
			return Response({"response" : "Successfully removed comic from your pull list"})
		except Comic.DoesNotExist:
			return Response({"response" : "This comic is not in your pull list"})
	else:
		return Response({"response" : "Comic parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def api_update_subbed_series_pulllist_view(request):

	try:
		if 'series' not in request.data:
			return Response(status=status.HTTP_400_BAD_REQUEST)
		pull_list_series = PullListSeries.objects.get(series__id=request.data['series'], pull_list__collection=request.user.collection)
	except PullListSeries.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
		
	if request.method == 'PUT':
		serializer = PullListSeriesUpdateSerializer(pull_list_series, data=request.data, partial=True, context={'pull_list_series_before_update' : pull_list_series})
		data = {}
		if serializer.is_valid():
			serializer.save()

			data['response']                = "Successfully updated pull list series"
			data['id']                      = pull_list_series.id
			data['series_id']               = pull_list_series.series.id
			data['include_standard_issues'] = pull_list_series.include_standard_issues
			data['include_variants']        = pull_list_series.include_variants
			data['include_TPB']             = pull_list_series.include_TPB
			data['include_all_collections'] = pull_list_series.include_all_collections
			data['include_all']             = pull_list_series.include_all

			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class APIPullListComicsListView(ListAPIView):
	serializer_class       = ComicSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes     = (IsAuthenticated,)
	pagination_class       = PageNumberPagination
	filter_backends        = [DjangoFilterBackend, SearchFilter]
	filterset_fields       = ['publisher__id', 'imprint__id', 'release_date']
	search_fields          = ('title',)

	def get_queryset(self):
		return PullList.objects.get(collection__user=self.request.user).comics