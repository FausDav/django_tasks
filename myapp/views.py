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
        form = UserCreationForm()
    else:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
    form.fields['username'].widget.attrs['class'] = "outline-none bg-lime-800 border-solid border-b-4 border-amber-200 rounded-lg px-4"
    form.fields['password1'].widget.attrs['class'] = "outline-none bg-lime-800 border-solid border-b-4 border-amber-200 rounded-lg px-4"
    form.fields['password2'].widget.attrs['class'] = "outline-none bg-lime-800 border-solid border-b-4 border-amber-200 rounded-lg px-4"

    form.fields['username'].widget.attrs['title'] = form.fields['username'].help_text
    form.fields['password1'].widget.attrs['title'] = form.fields['password1'].help_text.replace('<ul>','').replace('</ul>','').replace('<li>','').replace('</li>','\n')
    form.fields['password2'].widget.attrs['title'] = form.fields['password2'].help_text       
    return render(request,'signup.html',{"form":form})

def login_form(request):
    form = AuthenticationForm(request)
    form.fields['username'].widget.attrs['class'] = "outline-none bg-lime-800 border-solid border-b-4 border-amber-200 rounded-lg px-4"
    form.fields['password'].widget.attrs['class'] = "outline-none bg-lime-800 border-solid border-b-4 border-amber-200 rounded-lg px-4"
    if(request.method == 'GET'):
        return render(request,'login.html',{"form":form})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request,'login.html',{"form":form, "error":"Invalid username or password"})
        else:
            login(request,user)
            return redirect('/projects',{"form":NewProjectForm})

def logout_form(request):
    logout(request)
    return redirect('index')

def projects(request):
    if(request.method == 'GET'):
        form = NewProjectForm()
        form.fields['name'].widget.attrs['class'] = "outline-none bg-lime-800 border-solid border-b-4 border-amber-200 rounded-lg px-4"

        projects_list = Project.objects.filter(user_id=request.user.id)
        return render(request,'projects.html', {
            "projects": projects_list,
            "form":form,
        })
    else:
        Project.objects.create(name=request.POST['name'],user_id=request.user.id)
        return redirect('/projects')

def project_detail(request, project_id):
    if (request.method == 'GET'):
        try:
            form = NewTaskForm()
            form.fields['title'].widget.attrs['class'] = "outline-none bg-lime-800 border-solid border-b-4 border-amber-200 rounded-lg px-4 mb-4"
            form.fields['description'].widget.attrs['class'] = "outline-none bg-lime-800 border-solid border-b-4  border-s-4 border-amber-200 rounded-lg px-4 w-full text-lg"

            project = Project.objects.get(id=project_id, user_id = request.user.id)
            tasks_list = project.task_set.all().order_by("-id")
            return render(request,'project_detail.html', {
                "project":project,
                "tasks":tasks_list,
                "form":form,
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
        # return redirect('projects',project_id=project_id)
        return redirect(f'/projects/{project_id}#{project_id}-{task_id}')
    except (Project.DoesNotExist,Task.DoesNotExist):
        return redirect('projects',project_id=project_id)

def task_delete(request, project_id,task_id):
    try:
        Project.objects.get(pk=project_id, user_id=request.user.id)
        task = Task.objects.get(pk=task_id)
        task.delete()
        return redirect('projects',project_id=project_id)
    except (Project.DoesNotExist,Task.DoesNotExist):
        return redirect('projects',project_id=project_id)

def task_detail(request, project_id,task_id):
    task = None
    form = None
    if (request.method == 'GET'):
        try:
            Project.objects.get(pk=project_id, user_id=request.user.id)
            task = Task.objects.get(pk=task_id,project_id=project_id)
            form = TaskForm(instance=task)
        except (Project.DoesNotExist,Task.DoesNotExist):
            return redirect('projects',project_id=project_id)
    else:
        task = Task.objects.get(pk=task_id)
        form = TaskForm(request.POST, instance=task)
        form.save()

    
    form.fields['title'].widget.attrs['class'] = "outline-none bg-lime-800 border-solid border-b-4 border-amber-200 rounded-lg px-4 mb-4"
    form.fields['description'].widget.attrs['class'] = "outline-none bg-lime-800 border-solid border-b-4  border-s-4 border-amber-200 rounded-lg px-4 w-full text-lg"
    if(request.method=='GET'):
        return render(request,'task_detail.html',{"task":task, "project_id":project_id, "form":form})
    else:
        return redirect('projects',project_id=project_id)