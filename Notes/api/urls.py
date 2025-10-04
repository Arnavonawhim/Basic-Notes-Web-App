from django.urls import path
from .views import RegisterView, LoginView, NoteListCreateView, NoteDetailView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    openapi.Info(
        title="Notes API",
        default_version='v1',
        description="API for managing user notes with authentication",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@notes.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='api_register'),
    path('login/', LoginView.as_view(), name='api_login'),
    path('notes/', NoteListCreateView.as_view(), name='api_notes'),
    path('notes/<int:pk>/', NoteDetailView.as_view(), name='api_note_detail'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='api_docs'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='api_redoc'),
]