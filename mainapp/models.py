from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
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


class LatestProductsManager:

	@staticmethod
	def get_products_for_main_page(*args, **kwargs):
		with_respect_to = kwargs.get('with_respect_to')
		products = []
		ct_models = ContentType.objects.filter(model__in=args)
		for ct_model in ct_models:
			model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
			products.extend(model_products)
		if with_respect_to:
			ct_model = ContentType.objects.filter(model=with_respect_to)
			if ct_model.exists():
				if with_respect_to in args:
					return sorted(
						products,
						key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to),
						reverse=True)
		return products



class LatestProducts:

	objects = LatestProductsManager()


class Category(models.Model):

	name = models.CharField(max_length=255, verbose_name="Имя категории")
	slug = models.SlugField(unique=True)

# this for admin part
	def __str__(self):
		return self.name


class Product(models.Model):

	class Meta:
		abstract = True

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

class NoteBook(Product):

	diagonal = models.CharField(max_length=255, verbose_name='Диагональ')
	display_type = models.CharField(max_length=255, verbose_name='Тип дисплея')
	processor_freq = models.CharField(max_length=255, verbose_name='Частота процессора')
	ram = models.CharField(max_length=255, verbose_name='Оперативная память')
	video = models.CharField(max_length=255, verbose_name='Видеокарта')
	time_without_charge = models.CharField(max_length=255, verbose_name='Заряд батареи')

# this for admin part
	def __str__(self):
		return "{} {}".format(self.category.name, self.title)


class Smartphone(Product):

	diagonal = models.CharField(max_length=255, verbose_name='Диагональ')
	display_type = models.CharField(max_length=255, verbose_name='Тип дисплея')
	resolution = models.CharField(max_length=255, verbose_name='Разрешение экрана')
	accum_volume = models.CharField(max_length=255, verbose_name='Объем батареи')
	ram = models.CharField(max_length=255, verbose_name='Оперативная память')
	sd = models.BooleanField(default=True)
	cd_volume_max = models.CharField(max_length=255, verbose_name='Максимальный объем CD карты')
	main_cam_mp = models.CharField(max_length=255, verbose_name='Главная камера')
	frontal_cam_mp = models.CharField(max_length=255, verbose_name='Фронтальная камера')

# this for admin part
	def __str__(self):
		return "{} {}".format(self.category.name, self.title)


class CartProduct(models.Model):

	user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
	# next fielf with option related_name, we can do query set:
	# cartpduct.related_cart.all()
	cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_product')
	# we don't need line bellow and alter it for next tree lines
	# product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')
# example of SQL queryset create new obj of CartProduct
# p = NotebookProduct.objects.get(pk=1)
# cp = CartProduct.objects.create(content_type=p)
# in example above we got instance of Product and create new inst CatrProduct for curent Product
# GenericForeignKey will take correct model and put as ForeignKey
	qty = models.PositiveIntegerField(default=1)
	final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')

# this for admin part
	def __str__(self):
		return "Продукт: {0} (для корзины)".format(self.product.title)


class Cart(models.Model):

	owner = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
	# next fielf with option related_name, we can do query set:
	# cart.related_product.all()
	products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
	total_products = models.PositiveIntegerField(default=0)
	final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')

# this for admin part
	def __str__(self):
		return self.id


class Customer(models.Model):

	user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
	phone = models.CharField(max_length=20, verbose_name='Номер телефона')
	address = models.CharField(max_length=255, verbose_name='Адрес')

# this for admin part
	def __str__(self):
		return "{} {}".format(self.user.first_name, self.user.last_name)



