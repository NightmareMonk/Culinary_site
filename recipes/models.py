from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Recipe(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    ingredients = models.TextField(verbose_name="Ингредиенты")
    instructions = models.TextField(verbose_name="Инструкции по приготовлению")
    cooking_time = models.PositiveIntegerField(verbose_name="Время приготовления (минуты)")
    servings = models.PositiveIntegerField(verbose_name="Количество порций")
    difficulty = models.CharField(
        max_length=20,
        choices=[
            ('easy', 'Легко'),
            ('medium', 'Средне'),
            ('hard', 'Сложно'),
        ],
        default='easy',
        verbose_name="Сложность"
    )
    category = models.CharField(
        max_length=50,
        choices=[
            ('breakfast', 'Завтрак'),
            ('lunch', 'Обед'),
            ('dinner', 'Ужин'),
            ('dessert', 'Десерт'),
            ('snack', 'Закуска'),
            ('drink', 'Напиток'),
        ],
        verbose_name="Категория"
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    image = models.ImageField(upload_to='recipe_images/', blank=True, null=True, verbose_name="Изображение")

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('recipe_detail', kwargs={'pk': self.pk})
