from django.urls import path, include
from rest_framework import routers, urlpatterns
from api_app.views import (
    UserViewSet,
    DocumentRequestListAPIView,
    DocumentRequestCreateAPIView,
    SentDocumentRequestListAPIView,
    ReceivedDocumentRequestListCreateAPIView,
    RepliedDocumentRequestListAPIView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf.urls.static import static
from django.conf import settings
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)


router = routers.DefaultRouter()
router.register(r"users", UserViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls")),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("documentrequest/", DocumentRequestListAPIView.as_view(), name="all_request"),
    path(
        "documentrequest/send/",
        DocumentRequestCreateAPIView.as_view(),
        name="send_request",
    ),
    path(
        "documentrequest/sent/",
        SentDocumentRequestListAPIView.as_view(),
        name="sent_requests",
    ),
    path(
        "documentrequest/replied/",
        RepliedDocumentRequestListAPIView.as_view(),
        name="replied_requests",
    ),
    path(
        "documentrequest/received/",
        ReceivedDocumentRequestListCreateAPIView.as_view(),
        name="received_requests",
    ),
    # drf-spectacular
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
