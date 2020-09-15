from rest_framework                import status
from rest_framework.response       import Response
from rest_framework.decorators     import api_view, permission_classes
from rest_framework.permissions    import IsAuthenticated
from account.models                import Account
from publisher.models              import Publisher, Imprint
from publisher.api.serializers     import PublisherCreateSerializer, PublisherSerializer, PublisherUpdateSerializer
from rest_framework.pagination     import PageNumberPagination
from rest_framework.generics       import ListAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters        import SearchFilter, OrderingFilter

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def api_create_publisher_view(request):

	user = request.user
	if user.is_superuser != True:
		return Response({"response" : "You don't have access to add this"})
		
	if request.method == 'POST':

		data = request.data
		serializer = PublisherCreateSerializer(data=data)

		data = {}
		if serializer.is_valid():
			publisher = serializer.save()
			data['response'] = "Successfully created publisher"
			data['id'] = publisher.id
			data['name'] = publisher.name
			data['alt_id'] = publisher.alt_id
			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_detail_publisher_view(request, pk):
	try:
		publisher = Publisher.objects.get(pk=pk)
	except Publisher.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	if request.method == "GET":
		serializer = PublisherSerializer(publisher)
		return Response(serializer.data)

@api_view(['PUT',])
@permission_classes((IsAuthenticated,))
def api_update_publisher_view(request, pk):

	try:
		publisher = Publisher.objects.get(pk=pk)
	except Publisher.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	user = request.user
	if user.is_superuser != True:
		return Response({"response" : "You don't have access to update this"})
		
	if request.method == 'PUT':
		serializer = PublisherUpdateSerializer(publisher, data=request.data, partial=True)
		data = {}
		if serializer.is_valid():
			serializer.save()
			data['response'] = "Successfully updated publisher"
			data['id'] = publisher.id
			data['name'] = publisher.name
			data['alt_id'] = publisher.alt_id
			return Response(data=data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE', ])
@permission_classes((IsAuthenticated,))
def api_delete_publisher_view(request, pk):
	try:
		publisher = Publisher.objects.get(pk=pk)
	except Publisher.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	user = request.user
	if user.is_superuser != True:
		return Response({"response" : "You don't have access to delete this"})

	if request.method == "DELETE":
		operation = publisher.delete()
		data = {}
		if operation:
			data["success"] = "Successfully deleted publisher"
		else:
			data["failure"] = "Failed to delete publisher"
		return Response(data=data)

class APIPublisherListView(ListAPIView):
	queryset = Publisher.objects.all()
	serializer_class = PublisherSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)
	pagination_class = PageNumberPagination
	filter_backends = (SearchFilter, OrderingFilter)
	search_fields = ('name',)