from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, Category
from .forms import TaskForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count


CATEGORY_EMOJIS_COLORS = {
    "Uncategorized": {"emoji": "❓", "color": "#000000"},
    "Urgent": {"emoji": "⚠️", "color": "#ff0000"},
    "Hobbies": {"emoji": "🎨", "color": "#ff9800"},
    "Family": {"emoji": "👨‍👩‍👧‍👦", "color": "#4a154b"},
    "Travel": {"emoji": "✈️", "color": "#36c5f0"},
    "Education": {"emoji": "📘", "color": "#ecb22e"},
    "Shopping": {"emoji": "🛒", "color": "#8bc34a"},
    "Finance": {"emoji": "💰", "color": "#2e7d32"},
    "Health": {"emoji": "❤️", "color": "#e01e5a"},
    "Personal": {"emoji": "🏡", "color": "#6d4c41"},
    "Work": {"emoji": "💼", "color": "#2eb67d"},
}

# Lista de tarefas
# Lista de tarefas
@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user).select_related('category')  # Otimiza carregamento
    categories = Category.objects.annotate(task_count=Count('task'))  # Adiciona contagem de tarefas por categoria

    # Adicionar emojis e cores às tarefas
    for task in tasks:
        if task.category:  # Verifica se a tarefa tem uma categoria
            category_name = task.category.name
        else:
            category_name = "Uncategorized"

        # Garante que emoji e cor sempre sejam atribuídos
        category_name = task.category.name if task.category else "Uncategorized"
        task.emoji = CATEGORY_EMOJIS_COLORS.get(category_name, {}).get("emoji", "❓")
        task.color = CATEGORY_EMOJIS_COLORS.get(category_name, {}).get("color", "#000000")

        # Debug no terminal
        print(f"Tarefa: {task.title}, Categoria: {category_name}, Emoji: {task.emoji}, Cor: {task.color}")

    # Filtros e ordenação (mantém sua lógica anterior)
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

    sort = request.GET.get('sort', 'due_date')
    if sort in ['due_date', '-due_date', 'title', '-title']:
        tasks = tasks.order_by(sort)

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



# Criar tarefa
@login_required
def create_task(request):
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

@login_required
def update_task(request, pk):
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
        'task': task  # Certifique-se de passar o objeto `task` para o template
    })


# Deletar tarefa
@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        messages.success(request, "Tarefa excluída com sucesso!")
        return redirect('task_list')
    return render(request, 'tasks/delete_task.html', {'task': task})
