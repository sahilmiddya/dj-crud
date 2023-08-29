from typing import Any, Dict
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from .models import Task
from .forms import TaskForm
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView


class TaskListView(ListView):
    template_name = "tasks/task_list.html"
    context_object_name = 'tasks'
    model = Task
    # queryset = Task.objects.all()


class TaskDetailView(DetailView):
    template_name = "tasks/task_detail.html"
    model = Task
    context_object_name = 'task'
    pk_url_kwarg = 'pk'


class TaskCreateView(CreateView):
    template_name = "tasks/task_form.html"
    # model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks:task_list')

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Task'
        return context



class TaskUpdateView(UpdateView):
    template_name = "tasks/task_form.html"
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks:task_list')

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Task'
        return context



def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            print("asfnijnljibln", redirect(reverse("tasks:task_list")))
            return redirect(reverse("tasks:task_list"))
    else:
        form = TaskForm()

    return render(request, "tasks/task_form.html", {"form": form, })


# get task list
# def task_list(request):
#     tasks = Task.objects.all()
#     return render(request, , {"tasks": tasks, })


# get a single task
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk)
    return render(request, "tasks/task_detail.html", {"task": task, })


# Update a single task
def task_update(request, pk):
    template_name = "tasks/task_form.html"

    task_obj = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(instance=task_obj, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("tasks:task_detail", args=[pk,]))
    else:
        form = TaskForm(instance=task_obj)

    context = {"form": form, "object": task_obj}

    return render(request, template_name, context)


# Delete a single task
def task_delete(request, pk):
    task_obj = get_object_or_404(Task, pk=pk)
    task_obj.delete()
    return redirect(reverse("tasks:task_list"))
