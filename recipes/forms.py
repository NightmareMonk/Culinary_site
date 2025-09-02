from django import forms
from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title', 'description', 'ingredients', 'instructions',
            'cooking_time', 'servings', 'difficulty', 'category', 'image'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название рецепта'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Краткое описание блюда'
            }),
            'ingredients': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Список ингредиентов (каждый с новой строки)'
            }),
            'instructions': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 8,
                'placeholder': 'Пошаговые инструкции по приготовлению'
            }),
            'cooking_time': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Время в минутах'
            }),
            'servings': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Количество порций'
            }),
            'difficulty': forms.Select(attrs={
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
        labels = {
            'title': 'Название рецепта',
            'description': 'Описание',
            'ingredients': 'Ингредиенты',
            'instructions': 'Инструкции по приготовлению',
            'cooking_time': 'Время приготовления (минуты)',
            'servings': 'Количество порций',
            'difficulty': 'Сложность',
            'category': 'Категория',
            'image': 'Изображение блюда'
        }

    def clean_cooking_time(self):
        cooking_time = self.cleaned_data.get('cooking_time')
        if cooking_time and cooking_time <= 0:
            raise forms.ValidationError('Время приготовления должно быть больше 0')
        return cooking_time

    def clean_servings(self):
        servings = self.cleaned_data.get('servings')
        if servings and servings <= 0:
            raise forms.ValidationError('Количество порций должно быть больше 0')
        return servings
