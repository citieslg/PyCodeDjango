from django.urls import path
from .views import testview

urlpatterns = [
	path('', testview, name='base')

]
