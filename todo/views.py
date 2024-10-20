from django.shortcuts import render, redirect
from .models import Todo
from .forms import TodoForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
#! profile_pic. için
from users.models import UserProfile



def home(request):
    todos = []
    priority_count = 0
    done_count = 0
    profile = None #! profile_pic. için
    
    if request.user.is_authenticated:
        if request.user.is_superuser:
            todos = Todo.objects.all().order_by('priority')
            priority_count = todos.filter(priority__gt=2).count()
            done_count = todos.filter(is_done=True).count()

            #! profile_pic. için
            try:
                profile = UserProfile.objects.get(user=request.user)
            except UserProfile.DoesNotExist:
                profile = None  # veya uygun bir default değer
        else:
            todos = Todo.objects.filter(user=request.user).order_by('priority')
            priority_count = todos.filter(user=request.user, priority__gt=2).count()
            done_count = todos.filter(is_done=True).count()

            #! profile_pic. için
            try:
                profile = UserProfile.objects.get(user=request.user)
            except UserProfile.DoesNotExist:
                profile = None  # veya uygun bir default değer
        
    form = TodoForm()
    
    context = {
        "todos" : todos,
        "form" : form,
        "priority_count" : priority_count,
        "done_count" : done_count,
        "profile" : profile #! profile_pic. için
    } 
    return render(request, 'todo/home.html', context)

@login_required(login_url = 'user_login')
def todo_create(request):
    form = TodoForm()
    
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            
            messages.success(request, 'Todo created successfully.')
            return redirect('home')
    
    context = {
        "form" : form
    }
    return render(request, 'todo/todo_add.html', context)

@login_required(login_url = 'user_login')
def todo_update(request, id):
    todo = Todo.objects.get(id=id)
    form = TodoForm(instance=todo)
    
    if request.method == 'POST':
        form = TodoForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Todo updated successfully')
            return redirect('home')
        
    context = {
        'todo' : todo, 
        'form' : form, 
    }
    return render(request, "todo/todo_update.html", context)

@login_required(login_url = 'user_login')
def todo_delete(request, id):
    todo = Todo.objects.get(id=id)
    
    if request.method == 'POST':
        todo.delete()
        messages.warning(request, 'Todo deleted!')
        return redirect('home')
    
    context = {
        'todo' : todo
    }
    return render(request, 'todo/todo_delete.html', context)


# def is_completed(request, id):
#     todo = Todo.objects.get(id=id)
#     todo.is_done = not(todo.is_done)
#     todo.save()
#     return redirect('home')

def is_completed(request, id):
    todo = Todo.objects.get(id=id)
    if request.user == todo.user:
        todo.is_done = not(todo.is_done)
        messages.success(request, 'Todo is done successfully')
    else:
        messages.warning(request, 'Not authorized for this Todo!')
    todo.save()
    return redirect('home')
    
    
    