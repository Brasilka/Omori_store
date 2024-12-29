from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    path('', views.index, name='index'),  # Главная страница
    path('category/<int:category_id>/', views.category_detail, name='category_detail'),  # Страница категории
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),  # Страница товара
    path('cart/', views.cart_detail, name='cart_detail'),  # Корзина
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),  # Добавление в корзину
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),  # Удаление из корзины
    path('cart/update/<int:product_id>/', views.cart_update, name='cart_update'),  # Новый маршрут
    path('login/', views.user_login, name='login'),  # Вход (с кастомной формой)
    path('order/create/', views.create_order, name='create_order'),  # Создание заказа
    path('logout/', views.user_logout, name='logout'),  # Выход
    path('register/', views.register, name='register'),  # Регистрация
    path('order/history/', views.order_history, name='order_history'),
    path('admin/', admin.site.urls),  # Админка
    path('order/history/', views.order_history, name='order_history'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
