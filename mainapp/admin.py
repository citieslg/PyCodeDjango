from django import forms
from django.contrib import admin

from .models import *

# Register your models here.
class NoteBookCategoryChoiceField(forms.ModelChoiceField):
	pass


class NoteBookAdmin(admin.ModelAdmin):
	# next method works when in admin panel we try to choose category, Admin part shows for us only category == 'notebooks'
	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		print("db_field = ", db_field)
		if db_field.name == 'category':
			return NoteBookCategoryChoiceField(Category.objects.filter(slug='notebooks'))
		return super().formfield_for_foreignkey(db_field, request, **kwargs)

class SmartphoneCategoryChoiceField(forms.ModelChoiceField):
	pass


class SmartphoneAdmin(admin.ModelAdmin):
	# next method works when in admin panel we try to choose category, Admin part shows for us only category == 'notebooks'
	def formfield_for_foreignkey(self, db_field, request, **kwargs):
		print("db_field = ", db_field)
		if db_field.name == 'category':
			return SmartphoneCategoryChoiceField(Category.objects.filter(slug='smartphone'))
		return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(NoteBook, NoteBookAdmin)
admin.site.register(Smartphone)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)


