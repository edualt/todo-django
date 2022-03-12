from re import template
from django.urls import path
from django.contrib.auth.views import LogoutView
from base.models import Task
from .views import TaskDetail, TaskList, CompletedTask, IncompletedTask, TaskCreate, TaskUpdate, DeleteView, CustomLoginView, RegisterPage
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),#Login
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),#logout
    path('register/', RegisterPage.as_view(), name='register'),

    path('', TaskList.as_view(), name='tasks'),#All created tasks
    path('completed/', CompletedTask.as_view(), name='completed-tasks'),
    path('incompleted/', IncompletedTask.as_view(), name='incompleted-tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),#Specified task
    path('task-create/', TaskCreate.as_view(), name='task-create'),#Create task
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),#Update task
    path('task-delete/<int:pk>/', DeleteView.as_view(), name='task-delete'),#Delete task

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="base/password_reset.html"), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="base/password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="base/password_reset_form.html"), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="base/password_reset_complete.html"), name='password_reset_complete')
]
