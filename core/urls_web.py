from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.pagina_ponto, name='pagina_ponto'),
]