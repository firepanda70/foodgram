from django.contrib.auth import get_user_model
from django.db import models

from .validators import CookingTimeValidator, HEXCodeValidator

User = get_user_model()

MEASURE_CHOICES = [
    ('KG', 'кг'),
    ('G', 'г'),
    ('ML', 'мл.'),
    ('L', 'л.'),
    ('AN', 'по вкусу'),
    ('UN', 'шт.'),
    ('MS', 'ч. л.'),
    ('BS', 'ст. л.'),
    ('PN', 'щепотка')
]


class Tag(models.Model):
    name = models.CharField(
        'Тэг',
        unique=True,
        max_length=200,
        help_text='Категория рецепта'
    )
    color = models.CharField(
        'HEX-код',
        unique=True,
        validators=(HEXCodeValidator(),),
        help_text='Цветовой HEX-код (например, #49B64E)',
        max_length=7
    )
    slug = models.SlugField(
        'Адрес',
        unique=True,
        help_text='Адрес тэга',
        max_length=200
    )

    class Meta:
        ordering = ('name', )
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        'Название',
        unique=True,
        max_length=32,
        help_text='Название ингредиента'
    )
    measurement_unit = models.CharField(
        'Единица измерения',
        help_text='Единица измерения игредиента',
        choices=MEASURE_CHOICES,
        max_length=3
    )

    class Meta:
        ordering = ('name', )
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='recipes',
        help_text='Автор рецепта'
    )
    name = models.CharField(
        'Название',
        max_length=64,
        help_text='Название рецепта'
    )
    image = models.ImageField(
        'Изображение',
        upload_to='images/recipes/',
        help_text='Изображения блюда',
    )
    text = models.TextField(
        'Текст',
        help_text='Описание рецепта'
        )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe',
        verbose_name='Ингредиенты',
        help_text='Список ингредиентов'
    )
    tags = models.ManyToManyField(
        Tag,
        through='TagRecipe',
        verbose_name='Тэги',
        help_text='Список тэгов'
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
        validators=(CookingTimeValidator(),),
        help_text='Время приготовления в минутах'
    )

    class Meta:
        ordering = ('-id', )
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='related_ingredient'
    )
    amount = models.PositiveIntegerField(
        'Количество',
        validators=(CookingTimeValidator(),),
        help_text='Количество игредиента'
    )


class TagRecipe(models.Model):
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='favorites',
        help_text='Владелец списка избранного'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Избранные рецепты',
        on_delete=models.CASCADE,
        related_name='users_favorites',
        help_text='Избранные рецепты'
    )

    class Meta:
        ordering = ('recipe', )
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorite'
                ),
        )
        verbose_name = 'Избранный'
        verbose_name_plural = 'Избранные'

    def __str__(self):
        res = "{username}'s favorite list recipe {recipe}"
        return res.format(username=self.user.username, recipe=self.recipe.name)


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='shopping_list',
        help_text='Владелец списка покупок'
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт в списке покупок',
        on_delete=models.CASCADE,
        related_name='users_carts',
        help_text='Корзины пользователей'
    )

    class Meta:
        ordering = ('recipe', )
        verbose_name = 'Элемент списка покупок'
        verbose_name_plural = 'Элементы списка покупок'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_cart_item'
                ),
        )

    def __str__(self) -> str:
        res = "{username}'s shopping list recipe {recipe}"
        return res.format(username=self.user.username, recipe=self.recipe.name)
