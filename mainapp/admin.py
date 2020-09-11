from django.forms import ModelChoiceField, ModelForm, ValidationError
from django.contrib import admin
# the import bellow creates from python str-> html
from django.utils.safestring import mark_safe

from .models import *
from PIL import Image

# Register your models here.
class NoteBookAdminForm(ModelForm):


	MIN_RESOLUTION = (400,400)
	MAX_RESOLUTION = (1500, 1100)


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['image'].help_text = \
		'Загружайте изображение с минимальным расширением {}X{} и не более {}X{}'.\
		format(*self.MIN_RESOLUTION, *self.MAX_RESOLUTION)
		self.fields['slug'].help_text = \
		mark_safe('<span style="color: green; font-size:14px;">Введите 123. Slug переименуется title.lower()</span>')

# all the methods works only with a forms(which we see in admin) not with DB instances
	def clean_image(self):
		image = self.cleaned_data['image']
		img = Image.open(image)
		img_size = (img.width, img.height)
		if image.size > Product.MAX_IMG_SIZE:
			raise ValidationError('Размер изображение больше {} байт'\
				.format(Product.MAX_IMG_SIZE))
		if self.MIN_RESOLUTION > img_size:
			raise ValidationError('Изображение меньше {}X{}'\
				.format(*Product.NOTEBOOK_MIN_RESOLUTION))
		elif self.MAX_RESOLUTION < img_size:
			raise ValidationError('Изображение больше {}X{}'.\
				format(*Product.NOTEBOOK_MAX_RESOLUTION))
		else:
			return image

	# def clean_title(self):
	# 	print('clean_name')
	# 	name = self.cleaned_data['title'].lower()
	# 	return name

	def clean_slug(self):
		slug = self.cleaned_data['title'].lower()
		newslug = ''
		for i in slug:
			if i in '@#$%^&:!/\\;., ':
				i = '_'
			newslug+=i
		return newslug

class NoteBookAdmin(admin.ModelAdmin):

	form = NoteBookAdminForm

	# next method works when in admin panel we try to choose category, Admin part shows for us only category == 'notebooks'
	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		print("db_field = ", db_field.name)
		if db_field.name == 'category':
			return ModelChoiceField(Category.objects.filter(slug='notebooks'))
		return super().formfield_for_foreignkey(db_field, request, **kwargs)


class SmartphoneAdmin(admin.ModelAdmin):
	# next method works when in admin panel we try to choose category, Admin part shows for us only category == 'notebooks'
	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		print("db_field = ", db_field.name)
		# db_field its an object of ForeignKey and its has atribute name
		if db_field.name == 'category':
			print("SmartPhones")
			a = Category.objects.filter(slug='smartphones')
			print(a)
			return ModelChoiceField(Category.objects.filter(slug='smartphones'))
		print("SmartPhones 2")
		return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(NoteBook, NoteBookAdmin)
admin.site.register(Smartphone, SmartphoneAdmin)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)


