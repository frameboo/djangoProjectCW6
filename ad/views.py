import datetime

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ad.filters import AdFilter
from ad.models import Ad, Comment
from ad.permissions import IsOwnerOrAdmin
from ad.serializers import AdListSerializer, AdCreateSerializer, AdUpdateSerializer, AdDestroySerializer, \
	AdDetailSerializer, CommentSerializer, AdSerializer


class AdViewSet(ModelViewSet):
	filter_backends = (DjangoFilterBackend,)
	filterset_class = AdFilter

	queryset = Ad.objects.all()
	serializer_class = AdSerializer
	serializer_action_classes = {
		'list': AdListSerializer,
		'retrieve': AdDetailSerializer,
		'create': AdCreateSerializer,
		'partial_update': AdUpdateSerializer,
		'destroy': AdDestroySerializer
	}

	def get_serializer_class(self):
		try:
			return self.serializer_action_classes[self.action]
		except (KeyError, AttributeError):
			return super().get_serializer_class()

	def perform_create(self, serializer):
		serializer.save(
			author=self.request.user,
			created_at=datetime.datetime.now(),
		)

	def perform_update(self, serializer):
		serializer.save(author=self.request.user)

	def get_permissions(self):
		if self.action in {'create', 'retrieve'}:
			self.permission_classes = [IsAuthenticated]
		elif self.action in {'partial-update', 'delete'}:
			self.permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
		return super().get_permissions()


class MyAdsView(ListAPIView):
	queryset = Ad.objects.all()
	serializer_class = AdListSerializer

	def list(self, request, *args, **kwargs):
		user_id = self.request.user.id
		self.queryset = Ad.objects.filter(author=user_id)
		return super().list(request, *args, **kwargs)


class CommentViewSet(ModelViewSet):
	queryset = Comment.objects.all()
	serializer_class = CommentSerializer

	def get_queryset(self):
		return Comment.objects.filter(ad=self.kwargs['ad_pk'])

	def perform_create(self, serializer):
		serializer.save(
			author=self.request.user,
			created_at=datetime.datetime.now(),
			ad_id=self.kwargs['ad_pk']
		)

	def perform_update(self, serializer):
		serializer.save(
			author=self.request.user,
			ad_id=self.kwargs['ad_pk']
		)
