from rest_framework                import status
from rest_framework.response       import Response
from rest_framework.decorators     import api_view, permission_classes
from rest_framework.permissions    import IsAuthenticated
from account.models                import Account
from collection.models             import Collection, ComicBox, CollectedComic
from comic.models                  import Comic
from collection.api.serializers    import (
	ComicBoxUpdateSerializer, ComicBoxSerializer, ComicBoxCreateSerializer, CollectionSerializer,
	CollectedComicAddSerializer, CollectedComicSerializer, CollectedComicUpdateSerializer )
from comic.api.serializers         import ComicSerializer
from rest_framework.pagination     import PageNumberPagination
from rest_framework.generics       import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters        import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

# Collection Views

@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_detail_collection_view(request):
	try:
		collection = Collection.objects.get(user=request.user)
	except Collection.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == "GET":
		serializer = CollectionSerializer(collection)
		return Response(serializer.data)


# Collected Comic Views

@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_detail_collected_comic_view(request, pk):
	try:
		collected_comic = CollectedComic.objects.get(comic__pk=pk, collection__user=request.user)
	except CollectedComic.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == "GET":
		serializer = ComicSerializer(collected_comic.comic, context={'request': request})
		return Response(serializer.data)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_add_collected_comic_view(request, pk):

	if request.method == 'POST':
		try:
			comic = Comic.objects.get(pk=pk)
		except Comic.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

		data = request.data
		serializer = CollectedComicAddSerializer(data=data, context={'request': request, 'comic': comic})

		data = {}
		if serializer.is_valid():
			collected_comic = serializer.save()

			data['response']       = "Successfully added comic to collection"
			data['id']             = collected_comic.id
			data['comic_id']       = collected_comic.comic.id
			data['collection_id']  = collected_comic.collection.id
			data['date_collected'] = collected_comic.date_collected
			data['purchase_price'] = collected_comic.purchase_price
			data['bought_at']      = collected_comic.bought_at
			data['condition']      = collected_comic.condition
			data['is_slabbed']     = collected_comic.is_slabbed
			data['certification']  = collected_comic.certification
			data['grade']          = collected_comic.grade
			data['quantity']       = collected_comic.quantity

			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def api_update_collected_comic_view(request, pk):

	try:
		collected_comic = CollectedComic.objects.get(comic__pk=pk, collection__user=request.user)
	except CollectedComic.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
		
	if request.method == 'PUT':
		serializer = CollectedComicUpdateSerializer(collected_comic, data=request.data, partial=True)
		data = {}
		if serializer.is_valid():
			serializer.save()

			data['response']       = "Successfully updated comic collection details"
			data['id']             = collected_comic.pk
			data['comic_id']       = collected_comic.comic.pk
			data['date_collected'] = collected_comic.date_collected
			data['purchase_price'] = collected_comic.purchase_price
			data['bought_at']      = collected_comic.bought_at
			data['condition']      = collected_comic.condition
			data['is_slabbed']     = collected_comic.is_slabbed
			data['certification']  = collected_comic.certification
			data['grade']          = collected_comic.grade
			data['quantity']       = collected_comic.quantity

			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def api_remove_collected_comic_view(request, pk):
	try:
		collected_comic = CollectedComic.objects.get(comic__pk=pk, collection__user=request.user)
	except CollectedComic.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == "DELETE":
		operation = collected_comic.delete()
		data = {}
		if operation:
			data["response"] = "Successfully removed comic from your collection"
		else:
			data["response"] = "Failed to remove comic from your collection"
		return Response(data=data)

class APICollectedComicListView(ListAPIView):
	serializer_class = ComicSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	pagination_class = PageNumberPagination
	filter_backends = [DjangoFilterBackend, SearchFilter]
	filterset_fields = ['comic__publisher__id', 'comic__series__id', 'comic__imprint__id', 'comic__version_of__id']
	search_fields = ('title',)

	def get_queryset(self):
		collected_comics = Comic.objects.filter(id__in=CollectedComic.objects.filter(collection=self.request.user.collection))
		return collected_comics


# Comic Box Views

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_create_comic_box_view(request):

	if request.method == 'POST':

		data = request.data
		serializer = ComicBoxCreateSerializer(data=data, context={'request': request})

		data = {}
		if serializer.is_valid():
			comic_box = serializer.save()

			data['response'] = "Successfully created comic box"
			data['id']       = comic_box.id
			data['name']     = comic_box.name

			if request.data.get('initial_comic', "") != "":
				try:
					existing_comic = comic_box.comics.get(pk=request.data['initial_comic'])
					data['initial_comic_response']  = "This comic is already in this box."
				except Comic.DoesNotExist:
					comic_box.comics.add(request.data['initial_comic'])
					data['initial_comic_response'] = "Successfully added comic to new box."

			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_detail_comic_box_view(request, pk):
	paginator = PageNumberPagination()
	try:
		comic_box = ComicBox.objects.get(pk=pk)
	except ComicBox.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == "GET":
		serializer = ComicBoxSerializer(comic_box)
		return Response(serializer.data)


class APIComicBoxComicsListView(ListAPIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	pagination_class = PageNumberPagination
	serializer_class = ComicSerializer

	def get_queryset(self):
		try:
			comic_box = ComicBox.objects.get(pk=self.kwargs['pk'])
			serializer_class = ComicSerializer
			return comic_box.comics.all()
		except ComicBox.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)

class APIComicBoxListView(ListAPIView):
	serializer_class = ComicBoxSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	pagination_class = PageNumberPagination
	filter_backends = [DjangoFilterBackend, SearchFilter]
	search_fields = ('name',)

	def get_queryset(self):
		comic_boxes = ComicBox.objects.filter(collection_id=self.request.user.collection.pk)
		return comic_boxes

@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def api_update_comic_box_view(request, pk):

	try:
		comic_box = ComicBox.objects.get(pk=pk, collection__user=request.user)
	except ComicBox.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
		
	if request.method == 'PUT':
		serializer = ComicBoxUpdateSerializer(comic_box, data=request.data, partial=True)
		data = {}
		if serializer.is_valid():
			serializer.save()

			data['response']  = "Successfully updated comic box"
			data['id']        = comic_box.id
			data['name']      = comic_box.name
			if request.data.get('add_comic', "") != "":
				try:
					existing_comic = comic_box.comics.get(pk=request.data['add_comic'])
					data['add_comic_response']  = "This comic is already in this box."
				except Comic.DoesNotExist:
					comic_box.comics.add(request.data['add_comic'])
					data['add_comic_response'] = "Successfully added comic to box."

			if request.data.get('remove_comic', "")  != "":
				try:
					existing_comic = comic_box.comics.get(pk=request.data['remove_comic'])
					comic_box.comics.remove(existing_comic)
					data['remove_comic_response'] = "Comic successfully removed from box."
					
				except Comic.DoesNotExist:
					data['remove_comic_response'] = "This comic is not in this box."

			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def api_delete_comic_box_view(request, pk):
	try:
		comic_box = ComicBox.objects.get(pk=pk, collection__user=request.user)
	except ComicBox.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == "DELETE":
		operation = comic_box.delete()
		data = {}
		if operation:
			data["response"] = "Successfully deleted comic box"
		else:
			data["response"] = "Failed to delete comic box"
		return Response(data=data)