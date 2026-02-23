from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from .models import Bolsista, SessaoTrabalho, MINUTOS_ESPERADOS
from .serializers import BolsistaSerializer, SessaoTrabalhoSerializer

@api_view(['GET'])
def lista_bolsistas(request):
    bolsistas = Bolsista.objects.all()
    serializer = BolsistaSerializer(bolsistas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def busca_bolsista(request, pk):
    try:
        bolsista = Bolsista.objects.get(pk=pk)
    except Bolsista.DoesNotExist:
        return Response({'error': 'Bolsista não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = BolsistaSerializer(bolsista)
    return Response(serializer.data)

@api_view(['POST'])
def ponto_bolsista(request, pk):
    try:
        bolsista = Bolsista.objects.get(pk=pk)
    except Bolsista.DoesNotExist:
        return Response({'error': 'Bolsista não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    
    sessao_aberta = bolsista.sessao_aberta()

    if sessao_aberta is None:
        sessao = SessaoTrabalho.objects.create(bolsista=bolsista)
        return Response({
            'acao': 'entrada',
            'mensagem': 'Entrada registrada com sucesso!',
            'sessao': SessaoTrabalhoSerializer(sessao).data,
        }, status=status.HTTP_201_CREATED)
    else:
        agora = timezone.now()
        trabalhou = int((agora - sessao_aberta.entrada).total_seconds() / 60)
        sessao_aberta.saida = agora
        sessao_aberta.min_trabalhados = trabalhou
        sessao_aberta.diferenca_min = trabalhou - MINUTOS_ESPERADOS
        sessao_aberta.save()
        return Response({
            'acao': 'saida',
            'mensagem': 'Saída registrada com sucesso!',
            'sessao': SessaoTrabalhoSerializer(sessao_aberta).data,
        })
    
@api_view(['GET'])
def sessoes_bolsista(request, pk):
    try:
        bolsista = Bolsista.objects.get(pk=pk)
    except Bolsista.DoesNotExist:
        return Response({'error': 'Bolsista não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    
    sessoes = bolsista.sessaotrabalho_set.all()
    serializer = SessaoTrabalhoSerializer(sessoes, many=True)
    return Response(serializer.data)