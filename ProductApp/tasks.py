from celery import shared_task
from .models import Product
from django.utils import timezone

@shared_task
def update_variant(product_id):
    product = Product.objects.get(id=product_id)
    variants = product.variants.all()

    for variant in variants:
        variant.is_active = True
        variant.active_time = timezone.now()
        variant.save()