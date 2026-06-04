import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import Product, StageTemplate, Worker, Order, OrderTemplate

print("Deleting Orders...")
Order.objects.all().delete()
print("Deleting Products and Templates...")
Product.objects.all().delete()
OrderTemplate.objects.all().delete()
print("Deleting Workers...")
Worker.objects.all().delete()
print("Deleting Stage Templates...")
StageTemplate.objects.all().delete()

print("All product/stage data cleared. Admin user is kept.")
