from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Todo
from django.http import HttpResponseRedirect

# updated code
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('todos:index')
    else:
        form = UserCreationForm()
    return render(request, 'todos/signup.html', {'form': form})


@csrf_protect
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('todos:index')
    else:
        form = AuthenticationForm()
    return render(request, 'todos/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')

from django.contrib.auth.mixins import LoginRequiredMixin

class IndexView(LoginRequiredMixin, generic.ListView):
    login_url = 'login'  # name of your login route
    redirect_field_name = 'redirect_to'  # optional, for customizing redirect query param

    template_name = 'todos/index.html'
    context_object_name = 'todo_list'

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user).order_by('-created_at')

# previous code to add todo

# class IndexView(generic.ListView):
#     template_name = 'todos/index.html'
#     context_object_name = 'todo_list'

    # def get_queryset(self):
    #     """Return all the latest todos."""
    #     return Todo.objects.order_by('-created_at')
    # def get_queryset(self):
    #     return Todo.objects.filter(user=self.request.user).order_by('-created_at')

# def add(request):
#     title = request.POST['title']
#     Todo.objects.create(title=title)

#     return redirect('todos:index')

# def delete(request, todo_id):
#     todo = get_object_or_404(Todo, pk=todo_id)
#     todo.delete()

#     return redirect('todos:index')

# def update(request, todo_id):
    # todo = get_object_or_404(Todo, pk=todo_id)
    # isCompleted = request.POST.get('isCompleted', False)
    # if isCompleted == 'on':
    #     isCompleted = True
    
    # todo.isCompleted = isCompleted

    # todo.save()
    # return redirect('todos:index')

@login_required
def add(request):
    title = request.POST['title']
    Todo.objects.create(title=title, user=request.user)
    return redirect('todos:index')

@login_required
def delete(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id, user=request.user)
    todo.delete()
    return redirect('todos:index')

@login_required
def update(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id, user=request.user)
    todo.isCompleted = request.POST.get('isCompleted') == 'on'
    todo.save()
    return redirect('todos:index')
