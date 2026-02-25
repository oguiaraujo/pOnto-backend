from django.db import models

MINUTOS_ESPERADOS = 240

class Bolsista(models.Model):
    nome = models.CharField("Nome", max_length=100)

    class Meta:
        verbose_name = 'Bolsista'
        verbose_name_plural = 'Bolsistas'
        ordering = ['nome']

    def __str__(self):
        return self.nome
    
    def sessao_aberta(self):
        # Retorna a seção aberta, se existir
        return self.sessaotrabalho_set.filter(saida__isnull=True).first()
    
class SessaoTrabalho(models.Model):
    bolsista = models.ForeignKey(Bolsista, on_delete=models.CASCADE, verbose_name='Bolsista')
    entrada = models.DateTimeField('Entrada', auto_now_add=True)
    saida = models.DateTimeField('Saída', null=True, blank=True)
    min_trabalhados = models.IntegerField('Minutos Trabalhados', null=True, blank=True)
    diferenca_min = models.IntegerField('Diferença (min)', null=True, blank=True)

    def mostra_diferenca(self):
        if self.diferenca_min is None:
            return None
        diferenca = min(self.diferenca_min, 120)
        sinal = '+' if diferenca >= 0 else '-'
        total = abs(diferenca)
        horas = total // 60
        minutos = total % 60
        return f'{sinal}{horas}h{minutos:02d}m'

    mostra_diferenca.short_description = 'Diferença'
    
    class Meta:
        verbose_name = 'Sessão'
        verbose_name_plural = 'Sessões'
        ordering = ['-entrada']

    def __str__(self):
        return f'{self.bolsista}'