import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from core.models import *
from django.contrib.auth.models import User

print("=== ALL USERS ===")
for u in User.objects.all():
    has_worker = hasattr(u, 'worker')
    print(f"  User {u.id}: {u.username}, is_staff={u.is_staff}, has_worker={has_worker}")

print("\n=== ALL WORKERS ===")
for w in Worker.objects.all():
    stage_names = list(w.stages.values_list('id', 'name', 'product__name'))
    print(f"  Worker {w.id}: user={w.user.username}, stages={stage_names}")

print("\n=== ALL STAGES ===")
for s in Stage.objects.all():
    print(f"  Stage {s.id}: {s.name} (product={s.product.name}, order={s.order})")

print("\n=== ACTIVE ITEM STAGES ===")
for ist in ItemStage.objects.filter(status='active'):
    print(f"  ItemStage {ist.id}: stage_id={ist.stage.id} ({ist.stage.name}), order #{ist.item.order.id}")
