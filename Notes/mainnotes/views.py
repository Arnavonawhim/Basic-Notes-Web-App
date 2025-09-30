from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Note



@login_required(login_url='login_page')
def notes(request):
    person_notes = Note.objects.filter(user=request.user)
    context = {'notes': person_notes}
    return render(request, 'notes.html', context)

@login_required(login_url='login_page')
def note_add(request):
    title = request.POST.get('title')
    content = request.POST.get('content')
        
    if not title or not content:
        messages.error(request, "Notes Can't be empty")
        return render(request, 'note_add.html')
        
    Note.objects.create(user=request.user,title=title,content=content)
    messages.success(request, "Note Was Added")
    return redirect('notes')

@login_required(login_url='login_page')
def note_delete(request, note_id):
    current_note = get_object_or_404(Note, id=note_id, user=request.user)
    if request.method == 'POST':
        current_note.delete()
        messages.success(request, "Note Deleted")
        return redirect('notes')