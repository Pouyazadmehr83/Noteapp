from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "عنوان"}),
            "content": forms.Textarea(attrs={"placeholder": "متن نوت", "rows": 6}),
        }
