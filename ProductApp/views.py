from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework import status
from .serializers import ProductSerializer
from .models import Product
from django.utils import timezone
from datetime import datetime
from .tasks import update_variant


@api_view(['POST'])
def create_product(request):
    serializer = ProductSerializer(data=request.data, many=isinstance(request.data, list))
    if serializer.is_valid():
        products = serializer.save()

        for product in products:
            for variant in product.variants.all():
                active_time = variant.active_time

                # Validasi active_time tidak lebih kecil dari waktu sekarang
                if active_time and active_time < timezone.now():
                    return JsonResponse({
                        'status': 'error',
                        'message': 'active_time cannot be in the past'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # Jadwalkan update_variant sesuai dengan active_time (optional)
                if active_time and active_time > timezone.now():
                    update_variant.apply_async(args=[variant.id], eta=active_time)

        if isinstance(products, list):
            num_products = len(products)
            num_variants = sum(len(product.variants.all()) for product in products)
        else:
            num_products = 1
            num_variants = len(products.variants.all())
        return JsonResponse({
            'status': 'success',
            'message': f'success create {num_products} product(s) with {num_variants} variant(s)'
        })
    
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_products(request):
    from django.db import connection
    created_from = request.GET.get('created_from')
    created_to = request.GET.get('created_to')
    limit = request.GET.get('limit')

    # products = Product.objects.all()

    # to optimize the query, use select_related
    products = Product.objects.prefetch_related('variants')

    if created_from:
        created_from_date = datetime.strptime(created_from, '%Y-%m-%d').date()
        products = products.filter(created_at__gte=timezone.make_aware(datetime.combine(created_from_date, datetime.min.time())))

    if created_to:
        created_to_date = datetime.strptime(created_to, '%Y-%m-%d').date()
        products = products.filter(created_at__lte=timezone.make_aware(datetime.combine(created_to_date, datetime.max.time())))

    if limit:
        products = products[:int(limit)]
        
    print(connection.queries)
    serializer = ProductSerializer(products, many=True)
    
    return JsonResponse({
        'status': 'ok',
        'products': serializer.data
    })
