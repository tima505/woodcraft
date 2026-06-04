from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Product, Stage, Worker, Order, OrderItem, ItemStage, OrderTemplate
from django.utils import timezone
import datetime

class Command(BaseCommand):
    help = 'Loads initial data for WoodCraft ERP'

    def handle(self, *args, **kwargs):
        self.stdout.write("Loading initial data...")

        # 1. Admin
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin')
            self.stdout.write("Created admin user.")

        # 2. Products and Stages
        if not Product.objects.exists():
            door = Product.objects.create(name='Дверь межкомнатная "Классика"', description='Массив сосны, 2000x800')
            door_stages = ['Заготовка', 'Фрезеровка', 'Шлифовка', 'Покраска', 'Сборка', 'Контроль']
            for i, name in enumerate(door_stages):
                Stage.objects.create(product=door, name=name, order=i+1)

            cabinet = Product.objects.create(name='Шкаф-купе', description='МДФ, зеркало, 2200x1500')
            cabinet_stages = ['Распил МДФ', 'Кромление', 'Сборка каркаса', 'Установка фасадов']
            for i, name in enumerate(cabinet_stages):
                Stage.objects.create(product=cabinet, name=name, order=i+1)

            self.stdout.write("Created products and stages.")
        else:
            door = Product.objects.get(name='Дверь межкомнатная "Классика"')
            cabinet = Product.objects.get(name='Шкаф-купе')

        # 3. Workers
        if not Worker.objects.exists():
            w1_user = User.objects.create_user(username='worker1', password='password123', first_name='Иван')
            w1 = Worker.objects.create(user=w1_user)
            # Assign first 3 stages of door, and first 2 of cabinet
            w1.stages.set(list(door.stages.all()[:3]) + list(cabinet.stages.all()[:2]))

            w2_user = User.objects.create_user(username='worker2', password='password123', first_name='Петр')
            w2 = Worker.objects.create(user=w2_user)
            # Assign remaining stages
            w2.stages.set(list(door.stages.all()[3:]) + list(cabinet.stages.all()[2:]))

            self.stdout.write("Created workers.")

        # 4. Templates
        if not OrderTemplate.objects.exists():
            OrderTemplate.objects.create(
                name='Стандартная дверь (Сосна)',
                product=door,
                description='2000x800, петли слева',
                cost_price=15000,
                sale_price=35000
            )

        # 5. Orders
        if not Order.objects.exists():
            now = timezone.now()
            
            # Order 1 (In Progress, with some passed stages and one near deadline)
            o1 = Order.objects.create(
                client_name='ООО СтройИнвест',
                product=door,
                quantity=2,
                cost_price=30000,
                sale_price=70000,
                status='in_progress'
            )
            for i in range(1, o1.quantity + 1):
                item = OrderItem.objects.create(order=o1, number=i)
                stages = list(o1.product.stages.all())
                for idx, stage in enumerate(stages):
                    status_val = 'pending'
                    deadline = None
                    if idx == 0:
                        status_val = 'done'
                    elif idx == 1:
                        status_val = 'active'
                        deadline = now + datetime.timedelta(hours=20) # Near deadline
                    ItemStage.objects.create(item=item, stage=stage, status=status_val, deadline=deadline)

            # Order 2 (New, just created)
            o2 = Order.objects.create(
                client_name='Иванов И.И.',
                product=cabinet,
                quantity=1,
                cost_price=45000,
                sale_price=95000,
                status='new'
            )
            item2 = OrderItem.objects.create(order=o2, number=1)
            for idx, stage in enumerate(cabinet.stages.all()):
                status_val = 'active' if idx == 0 else 'pending'
                ItemStage.objects.create(item=item2, stage=stage, status=status_val, deadline=now + datetime.timedelta(days=3))

            # Order 3 (With Overdue)
            o3 = Order.objects.create(
                client_name='ЖК Горизонт',
                product=door,
                quantity=1,
                cost_price=15000,
                sale_price=35000,
                status='in_progress'
            )
            item3 = OrderItem.objects.create(order=o3, number=1)
            for idx, stage in enumerate(door.stages.all()):
                status_val = 'pending'
                deadline = None
                if idx == 0:
                    status_val = 'active'
                    deadline = now - datetime.timedelta(hours=5) # Overdue
                ItemStage.objects.create(item=item3, stage=stage, status=status_val, deadline=deadline)
            
            self.stdout.write("Created sample orders.")

        self.stdout.write(self.style.SUCCESS('Successfully loaded initial data'))
