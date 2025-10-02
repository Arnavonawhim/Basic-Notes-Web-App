from django.urls import path
from .views import RegisterView, LoginView, NoteListCreateView, NoteDetailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='api_register'),
    path('login/', LoginView.as_view(), name='api_login'),
    path('notes/', NoteListCreateView.as_view(), name='api_notes'),
    path('notes/<int:pk>/', NoteDetailView.as_view(), name='api_note_detail'),
]