from rest_framework import serializers
from .models import Bolsista, SessaoTrabalho, MINUTOS_ESPERADOS

class SessaoTrabalhoSerializer(serializers.ModelSerializer):
    mostra_diferenca = serializers.SerializerMethodField()

    class Meta:
        model = SessaoTrabalho
        fields = ['id', 'entrada', 'saida', 'min_trabalhados', 'diferenca_min', 'mostra_diferenca',]

    def get_mostra_diferenca(self, obj):
        if obj.diferenca_min is None:
            return None
        sinal = '+' if obj.diferenca_min >= 0 else '-'
        total = abs(obj.diferenca_min)
        horas = total // 60
        minutos = total % 60
        return f'{sinal}{horas}h{minutos:02d}m'
        
class BolsistaSerializer(serializers.ModelSerializer):
    sessao_aberta = serializers.SerializerMethodField()
    sessoes_recentes = serializers.SerializerMethodField()

    class Meta:
        model = Bolsista
        fields = ['id', 'nome', 'sessao_aberta', 'sessoes_recentes',]
    
    def get_sessao_aberta(self, obj):
        sessao = obj.sessao_aberta()
        return SessaoTrabalhoSerializer(sessao).data if sessao else None
    
    def get_sessoes_recentes(self, obj):
        sessoes = obj.sessaotrabalho_set.all()[:5]
        return SessaoTrabalhoSerializer(sessoes, many=True).data