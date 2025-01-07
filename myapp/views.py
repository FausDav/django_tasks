from django.http import HttpResponse
from .models import Project, Task
from django.shortcuts import render, redirect
from .forms import NewTaskForm, NewProjectForm, TaskForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout, authenticate
# Create your views here.

def index(request):
    return render(request, 'index.html')

def hello(request, username):
    return HttpResponse(f"<h1>Hello {username}!</h1>")

def about(request):
    return render(request,'about.html')

def signup_form(request):
    if (request.method == 'GET'):
        return render(request,'signup.html',{"form":UserCreationForm})
    else:
        if (request.POST['password1']!=request.POST['password2']):
            return render(request,'signup.html',{"form":UserCreationForm, "error":"Password confirmation do not match"})
        try:
            user = User.objects.get(username=request.POST['username'])
            return render(request,'signup.html',{"form":UserCreationForm, "error":"User already exists"})
        except User.DoesNotExist:
            user = User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
            return redirect('/login',{"form":AuthenticationForm})


def login_form(request):
    if(request.method == 'GET'):
        return render(request,'login.html',{"form":AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request,'login.html',{"form":AuthenticationForm, "error":"Invalid username or password"})
        else:
            login(request,user)
            return redirect('/projects',{"form":NewProjectForm})

def logout_form(request):
    logout(request)
    return redirect('index')

def projects(request):
    if(request.method == 'GET'):
        projects_list = Project.objects.filter(user_id=request.user.id)
        return render(request,'projects.html', {
            "projects": projects_list,
            "form":NewProjectForm,
        })
    else:
        Project.objects.create(name=request.POST['name'],user_id=request.user.id)
        return redirect('/projects')

def project_detail(request, project_id):
    if (request.method == 'GET'):
        try:
            project = Project.objects.get(id=project_id, user_id = request.user.id)
            tasks_list = project.task_set.all()
            return render(request,'project_detail.html', {
                "project":project,
                "tasks":tasks_list,
                "form":NewTaskForm(),
            })
        except Project.DoesNotExist:
            return redirect('/projects')
    else:
        Task.objects.create(title=request.POST['title'], description=request.POST['description'],project_id=project_id)
        return redirect('projects',project_id=project_id)

def task_check(request, project_id,task_id):
    try:
        Project.objects.get(pk=project_id, user_id=request.user.id)
        task = Task.objects.get(pk=task_id)
        task.done = not task.done
        task.save()
        return redirect('projects',project_id=project_id)
    except (Project.DoesNotExist,Task.DoesNotExist):
        return redirect('projects',project_id=project_id)
    
def task_detail(request, project_id,task_id):
    if (request.method == 'GET'):
        try:
            Project.objects.get(pk=project_id, user_id=request.user.id)
            task = Task.objects.get(pk=task_id,project_id=project_id)
            return render(request,'task_detail.html',{"task":task, "form":TaskForm(instance=task)})
        except (Project.DoesNotExist,Task.DoesNotExist):
            return redirect('projects',project_id=project_id)
    else:
        task = Task.objects.get(pk=task_id)
        form = TaskForm(request.POST, instance=task)
        form.save()
        return redirect('projects',project_id=project_id)
