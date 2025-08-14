from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, frontend_view, generate_post

router = DefaultRouter()
router.register(r"posts", PostViewSet)
router.register(r"comments", CommentViewSet)

urlpatterns = [
    path("", frontend_view),
    path("api/", include(router.urls)),
    path("api/generate_post/", generate_post),
]
