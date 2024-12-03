from django.contrib import admin
from .models import Task, Category

# Registrar o modelo Category com configurações adicionais
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Exibe o nome da categoria na lista
    search_fields = ('name',)  # Adiciona um campo de busca no admin

# Registrar o modelo Task com configurações adicionais
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'due_date', 'completed', 'category', 'user')  # Adiciona informações na lista
    list_filter = ('completed', 'category')  # Filtros laterais no admin
    search_fields = ('title', 'description')  # Adiciona campo de busca no admin
