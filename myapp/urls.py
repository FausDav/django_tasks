
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('hello/<str:username>',views.hello),
    path('about/',views.about, name='about'),
    path('projects/',views.projects, name='projects'),
    path('signup/',views.signup_form, name='signup'),
    path('login/',views.login_form, name='login'),
    path('logout/',views.logout_form, name='logout'),
    path('projects/<int:project_id>',views.project_detail, name='projects'),
    path('projects/<int:project_id>/task_check/<int:task_id>',views.task_check, name='task_check'),
    path('projects/<int:project_id>/task_delete/<int:task_id>',views.task_delete, name='task_delete'),
    path('projects/<int:project_id>/tasks/<int:task_id>',views.task_detail, name='task_detail'),
]