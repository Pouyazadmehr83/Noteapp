from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import NoteForm
from .models import Note

PAGE_SIZE = 10


@login_required
def read_data(request):
    query = request.GET.get("q", "").strip()
    notes = Note.objects.filter(User=request.user)
    if query:
        notes = notes.filter(Q(title__icontains=query) | Q(content__icontains=query))
    paginator = Paginator(notes, PAGE_SIZE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj, "query": query}
    return render(request, "notes/home.html", context)


@login_required
def detail_data(request, pk):
    note = get_object_or_404(Note, pk=pk, User=request.user)
    return render(request, "notes/detail.html", {"note": note})


@login_required
def create_data(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.User = request.user
            note.save()
            messages.success(request, "Note created successfully.")
            return redirect("notes:detail", pk=note.pk)
        messages.error(request, "Please fix the errors below.")
    else:
        form = NoteForm()
    return render(request, "notes/create.html", {"form": form})


@login_required
def update_data(request, pk):
    note = get_object_or_404(Note, pk=pk, User=request.user)
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, "Note updated successfully.")
            return redirect("notes:detail", pk=note.pk)
        messages.error(request, "Please fix the errors below.")
    else:
        form = NoteForm(instance=note)
    context = {"form": form, "note": note}
    return render(request, "notes/edit.html", context)


@login_required
@require_http_methods(["GET", "POST"])
def delete_data(request, pk):
    note = get_object_or_404(Note, pk=pk, User=request.user)
    if request.method == "POST":
        note.delete()
        messages.success(request, "Note deleted successfully.")
        return redirect("notes:read")
    return render(request, "notes/delete.html", {"note": note})
