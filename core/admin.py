from django.contrib import admin
from .models import Bolsista, SessaoTrabalho

class SessaoTrabalhoInLine(admin.TabularInline):
    model = SessaoTrabalho
    extra = 0
    fields = ['entrada', 'saida', 'mostra_diferenca']
    readonly_fields = ['entrada', 'saida', 'mostra_diferenca']
    can_delete = False

@admin.register(Bolsista)
class BolsistaAdmin(admin.ModelAdmin):
    list_display = ['nome']
    search_fields = ['nome']
    inlines = [SessaoTrabalhoInLine]

@admin.register(SessaoTrabalho)
class SessaoTrabalhoAdmin(admin.ModelAdmin):
    list_display = ['bolsista', 'entrada', 'saida', 'mostra_diferenca']
    list_filter = ['bolsista']
    readonly_fields = ['entrada', 'saida', 'mostra_diferenca']