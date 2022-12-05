from django.urls import path, include
from rest_framework import routers

from ad import views
from ad.views import CommentViewSet

comments_router = routers.SimpleRouter()
comments_router.register('comments', CommentViewSet)

urlpatterns = [
	path('me/', views.MyAdsView.as_view(), name='my_ads'),
	path('<int:ad_pk>/', include(comments_router.urls), name='comments'),
]
