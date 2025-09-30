from django.urls import path
from . import views 

urlpatterns = [
    path("notes/",views.notes,name="notes"),
    path("notes/add/", views.note_add, name="note_add"),
]