from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Category
from .forms import TaskForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count

# Task List View
@login_required
def task_list(request):
    """
    Handles the display of the user's task list. Includes filters, sorting, and pagination.
    - Filters: Status, delay, category.
    - Sorting: Title, due date.
    - Pagination: Displays 6 tasks per page.
    """
    tasks = Task.objects.filter(user=request.user).select_related('category')  # Optimized query
    categories = Category.objects.annotate(task_count=Count('task'))  # Category task count

    # Apply filters based on GET parameters
    status = request.GET.get('status')
    if status == 'completed':
        tasks = tasks.filter(completed=True)
    elif status == 'pending':
        tasks = tasks.filter(completed=False)

    delay = request.GET.get('delay')
    if delay == 'delayed':
        tasks = tasks.filter(due_date__lt=timezone.now())

    selected_category = request.GET.get('category')
    if selected_category:
        tasks = tasks.filter(category_id=selected_category)

    # Sorting tasks
    sort = request.GET.get('sort', 'due_date')
    if sort in ['due_date', '-due_date', 'title', '-title']:
        tasks = tasks.order_by(sort)

    # Pagination
    paginator = Paginator(tasks, 6)
    page = request.GET.get('page')
    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)

    now = timezone.now()
    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'categories': categories,
        'selected_category': selected_category,
        'now': now,
    })

# Create Task View
@login_required
def create_task(request):
    """
    Handles the creation of a new task.
    - Displays a form for task details.
    - Saves the task and associates it with the logged-in user.
    - Displays appropriate messages for success or delays.
    """
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            if task.is_delayed:
                messages.warning(request, "A tarefa está atrasada!")
            else:
                messages.success(request, "Tarefa criada com sucesso!")
            return redirect('task_list')
    else:
        form = TaskForm()
    categories = Category.objects.all()
    return render(request, 'tasks/create_task.html', {'form': form, 'categories': categories})

# Update Task View
@login_required
def update_task(request, pk):
    """
    Handles the update of an existing task.
    - Prefills the form with existing task data.
    - Saves updates and displays appropriate messages for success or delays.
    """
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            if task.is_delayed:
                messages.warning(request, "A tarefa está atrasada!")
            else:
                messages.success(request, "Tarefa atualizada com sucesso!")
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    categories = Category.objects.all()
    return render(request, 'tasks/update_task.html', {
        'form': form,
        'categories': categories,
        'task': task
    })

# Delete Task View
@login_required
def delete_task(request, pk):
    """
    Handles the deletion of a task.
    - Confirms task deletion via a POST request.
    - Displays a success message upon deletion.
    """
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        messages.success(request, "Tarefa excluída com sucesso!")
        return redirect('task_list')
    return render(request, 'tasks/delete_task.html', {'task': task})
