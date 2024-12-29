from django.db import models
from django.contrib.auth.models import User
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Название категории")
    description = models.TextField(blank=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Категория")
    name = models.CharField(max_length=200, verbose_name="Название товара")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to='products/', blank=True, verbose_name="Изображение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        ordering = ['name']

    def __str__(self):
        return self.name
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    products = models.ManyToManyField('Product', verbose_name="Продукты", related_name='orders')  # Связь с продуктами
    full_name = models.CharField(max_length=200, verbose_name="ФИО")
    address = models.TextField(verbose_name="Адрес доставки")
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Итоговая сумма")
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Ожидается'),
            ('in_progress', 'В обработке'),
            ('completed', 'Завершён'),
            ('cancelled', 'Отменён'),
        ],
        default='pending',
        verbose_name="Статус"
    )

    def __str__(self):
        return f"Заказ №{self.id} от {self.user.username}"