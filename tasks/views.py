from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    now = timezone.now()  # Hora atual
    return render(request, 'tasks/task_list.html', {'tasks': tasks, 'now': now})

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)  # Usando o formulário
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  # Vinculando a tarefa ao usuário logado
            task.save()

            # Verifica se a tarefa foi marcada como atrasada
            if task.is_delayed:
                messages.warning(request, "A tarefa está atrasada!")
            else:
                messages.success(request, "Tarefa criada com sucesso!")

            return redirect('task_list')  # Redirecionando para a lista de tarefas
    else:
        form = TaskForm()
    return render(request, 'tasks/create_task.html', {'form': form})

@login_required
def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        due_date = request.POST.get('due_date')
        completed = request.POST.get('completed')  # Verificando o status de concluída

        # Atualizando os campos
        task.title = title
        task.description = description
        if due_date:
            task.due_date = due_date

        # Atualizando o campo de conclusão
        if completed == 'on':  # Se o checkbox estiver marcado
            task.completed = True
        else:
            task.completed = False

        task.save()  # Salvando a tarefa

        # Verifica se a tarefa foi marcada como atrasada
        if task.is_delayed:
            messages.warning(request, "A tarefa está atrasada!")
        else:
            messages.success(request, "Tarefa atualizada com sucesso!")

        return redirect('task_list')
    return render(request, 'tasks/update_task.html', {'task': task})

@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':  # Para confirmar a exclusão
        task.delete()  # Excluindo a tarefa
        return redirect('task_list')  # Redireciona para a lista de tarefas
    return render(request, 'tasks/delete_task.html', {'task': task})
