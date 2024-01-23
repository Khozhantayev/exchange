from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import CurrencyRate
from .serializers import CurrencyRateSerializer
from .services import get_usd_to_rub_exchange_rate
from django.utils import timezone

class GetCurrentUSD(APIView):
    def get(self, request):
        usd_to_rub_rate = get_usd_to_rub_exchange_rate()

        if usd_to_rub_rate is None:
            return Response({'error': 'Не удалось получить курс валюты'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Провереряес время последнего запроса
        last_request_time = CurrencyRate.objects.last().time_rate

        if (timezone.now() - last_request_time).total_seconds() < 10:
            time_to_wait = 10 - (timezone.now() - last_request_time).total_seconds()
            return Response({'message': f'Подождите {int(time_to_wait)} секунд перед следующим запросом'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        
        else:
            
            # Сохраняем курс
            currency_rate = CurrencyRate(rate=usd_to_rub_rate)
            currency_rate.save()

            # сериализируем 10 последних запросов
            last_10_rates = CurrencyRate.objects.all().order_by('-time_rate')[:10]
            serializer = CurrencyRateSerializer(last_10_rates, many=True)
            return Response(serializer.data)
