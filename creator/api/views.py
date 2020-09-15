from rest_framework                import status
from rest_framework.response       import Response
from rest_framework.decorators     import api_view, permission_classes
from rest_framework.permissions    import IsAuthenticated
from account.models                import Account
from creator.models                import Creator, ComicCreator
from creator.api.serializers       import CreatorCreateSerializer, CreatorSerializer, CreatorUpdateSerializer
from rest_framework.pagination     import PageNumberPagination
from rest_framework.generics       import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters        import SearchFilter, OrderingFilter

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_create_creator_view(request):

	user = request.user
	if user.is_superuser != True:
		return Response({"response" : "You don't have access to add this"})

	if request.method == 'POST':

		data = request.data
		serializer = CreatorCreateSerializer(data=data)

		data = {}
		if serializer.is_valid():
			creator = serializer.save()

			data['response']     = "Successfully created creator"
			data['id']           = creator.id
			data['name']         = creator.name
			data['alt_id']       = creator.alt_id

			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_detail_creator_view(request, pk):
	try:
		creator = Creator.objects.get(pk=pk)
	except Creator.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	serializer = CreatorSerializer(creator)
	return Response(serializer.data)

@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def api_update_creator_view(request, pk):
	try:
		creator = Creator.objects.get(pk=pk)
	except Creator.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	user = request.user
	if user.is_superuser != True:
		return Response({"response" : "You don't have access to update this"})
		
	if request.method == 'PUT':
		serializer = CreatorUpdateSerializer(creator, data=request.data, partial=True)
		data = {}
		if serializer.is_valid():
			serializer.save()

			data['response'] = "Successfully updated creator"
			data['id']       = creator.id
			data['name']     = creator.name
			data['alt_id']   = creator.alt_id

			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def api_delete_creator_view(request, pk):
	try:
		creator = Creator.objects.get(pk=pk)
	except Creator.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	user = request.user
	if user.is_superuser != True:
		return Response({"response" : "You don't have access to delete this"})

	if request.method == "DELETE":
		operation = creator.delete()
		data = {}
		if operation:
			data["success"] = "Successfully deleted creator"
		else:
			data["failure"] = "Failed to delete creator"
		return Response(data=data)

class APICreatorListView(ListAPIView):
	queryset = Creator.objects.all()
	serializer_class = CreatorSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	pagination_class = PageNumberPagination
	filter_backends = (SearchFilter, OrderingFilter)
	search_fields = ('name',)