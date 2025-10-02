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
    image = request.FILES.get('image')
    if not title or not content:
        messages.error(request, "Notes Can't be empty")
        return render(request, 'note_add.html')
        
    Note.objects.create(user=request.user,title=title,content=content,image=image)
    if not image:
        messages.success(request, "Note Was Added")
        return redirect('notes')
    else:
        messages.success(request,'Note Was Added Along With Image')
        return redirect('notes')

@login_required(login_url='login_page')
def note_delete(request, note_id):
    current_note = get_object_or_404(Note,id=note_id,user=request.user)
    if request.method == 'POST':
        current_note.delete()
        messages.success(request, "Note Deleted")
        return redirect('notes')
    
@login_required(login_url='login_page')
def note_edit(request,note_id):
    current_note= get_object_or_404(Note,id=note_id,user=request.user)
    new_title=request.POST.get('title')
    new_content=request.POST.get('content')
    new_image=request.FILES.get('image')

    if not new_title or not new_content :
        messages.error(request,"Update Something")
        return render(request, 'note_edit.html', {'note': current_note})
    else:
        current_note.title=new_title
        current_note.content=new_content
        current_note.image=new_image
        current_note.save()
        messages.success(request,"Note was updated")
        return redirect('notes')