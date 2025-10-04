from django.contrib import admin
from .models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at', 'user']
    search_fields = ['title', 'content', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Note Information', {'fields': ('user', 'title', 'content', 'image')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'),'classes': ('collapse',)}),)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user')