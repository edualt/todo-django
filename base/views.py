
from itertools import count
from turtle import title
from urllib import request
from venv import create
from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from .models import Task
from .forms import PostTask, CreateUserForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.urls import reverse_lazy
import os
from django.conf import settings
from django.db.models.functions import Lower
from django.core.mail import send_mail
from django.template.loader import render_to_string

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')

class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = CreateUserForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)

        username = user.username

        subject='Register Confirmed! Welcome ' + username + '!'
        message='Hey ' +username+ ' you are now successfully register with us!'
        to=user.email

        send_mail(
            subject,
            message,
            'TODOapp',
            [to],
            html_message=render_to_string('base/prueba.html', {'context':'values'})
        )

        return super(RegisterPage, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)

class TaskList(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        context['counttasks'] = context['tasks'].filter(user=self.request.user).count()

        search_input = self.request.GET.get('search-area')
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)
        
        context['search_input'] = search_input

        return context

    def get_ordering(self):
        ordering = self.request.GET.get('ordering')
        # validate ordering here
        if ordering == 'title':
            Task.objects.filter(title=title).order_by('title').query.__str__()
            ordering = [Lower('title')]

        if ordering == 'created':
            Task.objects.filter(title=title).order_by('created').query.__str__()
            
        return ordering


class CompletedTask(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = 'tasks'
    template_name='base/completed_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user, complete=True)
        context['countCompleted'] = context['tasks'].filter(complete=True).count()
        
        search_input = self.request.GET.get('search-area')
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input, complete=True)
        
        context['search_input'] = search_input

        return context

class IncompletedTask(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = 'tasks'
    template_name='base/incompleted_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user, complete=False)
        context['countCompleted'] = context['tasks'].filter(complete=False).count()
        
        search_input = self.request.GET.get('search-area')
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input, complete=False)
        
        context['search_input'] = search_input

        return context
    
    
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task_detail.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    form_class = PostTask
    #fields = ['title', 'description', 'complete' ]
    path = settings.MEDIA_ROOT
    img_list = os.listdir(path + '/myimage')
    context = {'image' : img_list}
    success_url = reverse_lazy('tasks')
    

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = PostTask
    #fields = ['title', 'description', 'complete' ]
    success_url = reverse_lazy('tasks')
    
class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
