from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
######Main Models#####
#1. Category
#2. Product
#3. CartProduct
#4. Cart
#5. Order
######Other Models####
# 6. Customer
# 7. Specification
######################
# Create your models here.

User = get_user_model() # the line takes django model User

class Category(models.Model):

	name = models.CharField(max_length=255, verbose_name="Имя категории")
	slug = models.SlugField(unique=True)

# this for admin part
	def __str__(self):
		return self.name

class Product(models.Model):

	# next line ForeignKey shows link to table with Categoties to curent Caregory for example: notebook, smartphone etc
	# on_delete is requered option to shows what to do of delete obj
	category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
	title = models.CharField(max_length=255, verbose_name="Наименование")
	slug = models.SlugField(unique=True)
	image = models.ImageField(verbose_name='Изображение')
	# null=True means that field can be empty
	description = models.TextField(verbose_name='Описание', null=True)
	# max_digits- max length of number, decimal_places - how many numbers after point
	price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')

# this for admin part
	def __str__(self):
		return self.title

class CartProduct(models.Model):

	user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
	# next fielf with option related_name, we can do query set:
	# cartpduct.related_cart.all()
	cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_product')
	product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
	qty = models.PositiveIntegerField(default=1)
	final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')

	def __str__(self):
		return "Продукт: {0} (для корзины)".format(self.product.title)


class Cart(models.Model):

	owner = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
	# next fielf with option related_name, we can do query set:
	# cart.related_product.all()
	products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
	total_products = models.PositiveIntegerField(default=0)
	final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')

	def __str__(self):
		return self.id

class Customer(models.Model):

	user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
	phone = models.CharField(max_length=20, verbose_name='Номер телефона')
	address = models.CharField(max_length=255, verbose_name='Адрес')

	def __str__(self):
		return "{} {}".format(self.user.first_name, self.user.last_name)

class Specification(models.Model):

	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	name = models.CharField(max_length=255, verbose_name='Имя товара для характеристик')

	def __str___(self):
		return "Характеристики для товара :{}".format(self.name)
