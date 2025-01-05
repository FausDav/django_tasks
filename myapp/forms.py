from django import forms
from .models import Project,Task

class NewTaskForm(forms.Form):
    title = forms.CharField(label="Título de tarea", max_length=200,required=True, widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))
    description = forms.CharField(widget=forms.Textarea,label="Descripción de la tarea",required=False)

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title','description','done']

class NewProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name']
        widgets = {
            "name": forms.TextInput(attrs={'autofocus': 'autofocus'}),
        }