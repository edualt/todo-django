from django.urls import path
from django.contrib.auth.views import LogoutView
from base.models import Task
from .views import TaskDetail, TaskList, CompletedTask, TaskCreate, TaskUpdate, DeleteView, CustomLoginView, RegisterPage

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),#Login
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),#logout
    path('register/', RegisterPage.as_view(), name='register'),

    path('', TaskList.as_view(), name='tasks'),#All created tasks
    path('completed/', CompletedTask.as_view(), name='completed-tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),#Specified task
    path('task-create/', TaskCreate.as_view(), name='task-create'),#Create task
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),#Update task
    path('task-delete/<int:pk>/', DeleteView.as_view(), name='task-delete'),#Delete task
]
