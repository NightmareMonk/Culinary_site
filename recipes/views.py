from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Recipe
from .forms import RecipeForm


def recipe_list(request):
    """Список всех рецептов с возможностью поиска и фильтрации"""
    recipes = Recipe.objects.all()
    
    # Поиск
    search_query = request.GET.get('search')
    if search_query:
        recipes = recipes.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(ingredients__icontains=search_query)
        )
    
    # Фильтрация по категории
    category = request.GET.get('category')
    if category:
        recipes = recipes.filter(category=category)
    
    # Фильтрация по сложности
    difficulty = request.GET.get('difficulty')
    if difficulty:
        recipes = recipes.filter(difficulty=difficulty)
    
    # Пагинация
    paginator = Paginator(recipes, 6)  # 6 рецептов на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'category': category,
        'difficulty': difficulty,
        'category_choices': Recipe._meta.get_field('category').choices,
        'difficulty_choices': Recipe._meta.get_field('difficulty').choices,
    }
    return render(request, 'recipes/recipe_list.html', context)


def recipe_detail(request, pk):
    """Детальная страница рецепта"""
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})


@login_required
def recipe_create(request):
    """Создание нового рецепта"""
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            messages.success(request, 'Рецепт успешно создан!')
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm()
    
    return render(request, 'recipes/recipe_form.html', {
        'form': form,
        'title': 'Создать новый рецепт'
    })


@login_required
def recipe_update(request, pk):
    """Редактирование рецепта"""
    recipe = get_object_or_404(Recipe, pk=pk)
    
    # Проверяем, что пользователь является автором рецепта
    if recipe.author != request.user:
        messages.error(request, 'Вы можете редактировать только свои рецепты!')
        return redirect('recipe_detail', pk=pk)
    
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            messages.success(request, 'Рецепт успешно обновлен!')
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm(instance=recipe)
    
    return render(request, 'recipes/recipe_form.html', {
        'form': form,
        'title': 'Редактировать рецепт',
        'recipe': recipe
    })


@login_required
def recipe_delete(request, pk):
    """Удаление рецепта"""
    recipe = get_object_or_404(Recipe, pk=pk)
    
    # Проверяем, что пользователь является автором рецепта
    if recipe.author != request.user:
        messages.error(request, 'Вы можете удалять только свои рецепты!')
        return redirect('recipe_detail', pk=pk)
    
    if request.method == 'POST':
        recipe.delete()
        messages.success(request, 'Рецепт успешно удален!')
        return redirect('recipe_list')
    
    return render(request, 'recipes/recipe_confirm_delete.html', {'recipe': recipe})


def home(request):
    """Главная страница с последними рецептами"""
    latest_recipes = Recipe.objects.all()[:6]  # Последние 6 рецептов
    return render(request, 'recipes/home.html', {'latest_recipes': latest_recipes})
