from django.forms import ModelChoiceField
from django.contrib import admin

from .models import *

# Register your models here.
class NoteBookAdmin(admin.ModelAdmin):
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


