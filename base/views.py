from django.shortcuts import render, redirect

# используем class-based view
from django.views.generic.list import ListView

# этот класс позволяет получать детальную инфо из модели
from django.views.generic.detail import DetailView
# для регистрации нет встроенного класса - модифицируем FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from base.models import Task

from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
# ограничивает доступ незалогиненным пользователям
from django.contrib.auth.mixins import LoginRequiredMixin
# метод для создания юзера
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        # когда форма сохранена, возвращаемое значение будет user
        user = form.save()
        # когда user создан и залогинен, он перенаправляется на task list
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    # authenticated user не должен видеть форму регистрации, а перенаправляется на task list
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    # переопределяем success url
    def get_success_url(self):
        return reverse_lazy('tasks')


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    # объединяет данные контекста всех род. классов с данными текущего (**kwargs - именованные агрументы (kyeword))
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # залогиненный user будет получать только свои tasks
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        # посчитать завершенные задачи
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            # title__contains
            context['tasks'] = context['tasks'].filter(title__startswith=search_input)

        context['search_input'] = search_input

        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'


# создание формы с полями, соответствующими полям модели
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    # fields = '__all__'
    fields = ['title', 'description', 'complete']
    # в случае успешного создания task возвращаемся в список задач (tasks)
    success_url = reverse_lazy('tasks')

    # переопределяем, чтобы назначать задачи только себе
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    # fields = '__all__'
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')


class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')

