from rest_framework import viewsets, views, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from .models import StageTemplate, Product, Stage, Worker, OrderTemplate, Order, OrderItem, ItemStage
from .serializers import (
    StageTemplateSerializer, ProductSerializer, WorkerSerializer, OrderTemplateSerializer, 
    OrderSerializer, OrderItemSerializer, ItemStageSerializer, UserSerializer
)

class AuthView(views.APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        if 'login' in request.path:
            username = request.data.get('username')
            password = request.data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                is_admin = user.is_superuser or user.is_staff
                return Response({'token': token.key, 'is_admin': is_admin, 'user_id': user.id})
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        elif 'logout' in request.path:
            if request.user.is_authenticated:
                request.user.auth_token.delete()
            return Response({'success': 'Logged out'})

class MeView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'is_admin': user.is_superuser or user.is_staff
        }
        if hasattr(user, 'worker'):
            data['worker_id'] = user.worker.id
            data['stages'] = [{'id': s.id, 'name': s.name} for s in user.worker.stages.all()]
        return Response(data)

class StageTemplateViewSet(viewsets.ModelViewSet):
    queryset = StageTemplate.objects.all()
    serializer_class = StageTemplateSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        # Allow creating product and its stages simultaneously
        stages_data = request.data.pop('stages', [])
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        for idx, stage_name in enumerate(stages_data):
            Stage.objects.create(product=product, name=stage_name, order=idx+1)
        headers = self.get_success_headers(serializer.data)
        return Response(self.get_serializer(product).data, status=status.HTTP_201_CREATED, headers=headers)

class WorkerViewSet(viewsets.ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = instance.user
        instance.delete()
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class OrderTemplateViewSet(viewsets.ModelViewSet):
    queryset = OrderTemplate.objects.all()
    serializer_class = OrderTemplateSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        stage_deadlines = request.data.pop('stage_deadlines', {})
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        
        # 1. Create OrderItems
        for i in range(1, order.quantity + 1):
            item = OrderItem.objects.create(order=order, number=i)
            # 2. Create ItemStages for each item based on Product stages
            stages = order.product.stages.all()
            for idx, stage in enumerate(stages):
                status_val = 'active' if idx == 0 else 'pending'
                deadline = stage_deadlines.get(str(stage.id)) or stage_deadlines.get(stage.id)
                ItemStage.objects.create(
                    item=item,
                    stage=stage,
                    status=status_val,
                    deadline=deadline if deadline else None
                )
        headers = self.get_success_headers(serializer.data)
        # Fetch the complete order to return nested items
        return Response(self.get_serializer(order).data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        order = self.get_object()
        return Response(OrderItemSerializer(order.items.all(), many=True).data)

class ItemStageViewSet(viewsets.ModelViewSet):
    queryset = ItemStage.objects.all()
    serializer_class = ItemStageSerializer

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

class DashboardView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not hasattr(request.user, 'worker'):
            return Response([])
        worker = request.user.worker
        # Match tasks by stage names assigned to the worker
        # This way if a worker is assigned to "Заготовка" for one product,
        # they see "Заготовка" for all products.
        stage_names = worker.stages.values_list('name', flat=True)
        tasks = ItemStage.objects.filter(
            stage__name__in=stage_names,
            status__in=['active', 'issue'],
            item__order__status__in=['new', 'in_progress']
        ).select_related('item__order', 'stage', 'returned_by__user')
        serializer = ItemStageSerializer(tasks, many=True)
        
        # Add some extra data for dashboard cards easily
        data = serializer.data
        for t in data:
            db_task = tasks.get(id=t['id'])
            t['order_number'] = db_task.item.order.id
            t['client_name'] = db_task.item.order.client_name
            t['product_name'] = db_task.item.order.product.name
            t['item_number'] = db_task.item.number
            if db_task.returned_by:
                t['returned_by_name'] = db_task.returned_by.user.first_name or db_task.returned_by.user.username
        return Response(data)

class AnalyticsView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        today = timezone.localtime().date()
        from django.db.models import Count, Sum, F, Q
        from django.utils import timezone as dz_timezone
        from datetime import timedelta
        
        now = dz_timezone.now()
        
        # Helper to calculate revenue/profit
        def calc_finances(orders_qs):
            aggs = orders_qs.aggregate(
                revenue=Sum('sale_price'),
                cost=Sum('cost_price')
            )
            revenue = aggs['revenue'] or 0
            profit = revenue - (aggs['cost'] or 0)
            return revenue, profit

        # 1. Orders received today
        orders_received_today = Order.objects.filter(created_at__date=today).count()
        
        # 2. Stages completed today
        stages_completed_today = ItemStage.objects.filter(completed_at__date=today, status='done').count()
        
        # 3. Orders completed today/month & Finances
        orders_done_today = Order.objects.filter(status='done', items__stages__completed_at__date=today).distinct()
        orders_completed_today_count = orders_done_today.count()
        rev_today, prof_today = calc_finances(orders_done_today)
        
        this_month_start = today.replace(day=1)
        orders_done_month = Order.objects.filter(status='done', items__stages__completed_at__date__gte=this_month_start).distinct()
        rev_month, prof_month = calc_finances(orders_done_month)

        # 4. WIP summary
        orders_in_progress = Order.objects.filter(status='in_progress').count()
        orders_new = Order.objects.filter(status='new').count()

        # 5. Overdue stages
        overdue_stages_count = ItemStage.objects.filter(status='active', deadline__lt=now).count()

        # 6. Slowest stage / most delayed
        delayed_stages = ItemStage.objects.filter(
            Q(status='issue') | Q(status='active', deadline__lt=now)
        ).values('stage__name').annotate(count=Count('id')).order_by('-count')
        slowest_stage = delayed_stages.first()['stage__name'] if delayed_stages.exists() else 'Нет задержек'

        # 7. Worker Efficiency (Top 5 this week)
        week_start = today - timedelta(days=today.weekday())
        top_workers_qs = ItemStage.objects.filter(
            status='done', completed_at__date__gte=week_start, assigned_worker__isnull=False
        ).values(
            name=F('assigned_worker__user__first_name'),
            username=F('assigned_worker__user__username')
        ).annotate(stages_done=Count('id')).order_by('-stages_done')[:5]
        
        top_workers = []
        for w in top_workers_qs:
            top_workers.append({
                'name': w['name'] or w['username'],
                'stages_done': w['stages_done']
            })

        # 8. Trend data (Last 7 days)
        trend_data = []
        for i in range(6, -1, -1):
            d = today - timedelta(days=i)
            ods = Order.objects.filter(status='done', items__stages__completed_at__date=d).distinct()
            r, _ = calc_finances(ods)
            trend_data.append({
                'date': d.strftime('%d.%m'),
                'orders': ods.count(),
                'revenue': r
            })

        return Response({
            'orders_received_today': orders_received_today,
            'stages_completed_today': stages_completed_today,
            'orders_completed_today': orders_completed_today_count,
            'slowest_stage': slowest_stage,
            'revenue_today': rev_today,
            'profit_today': prof_today,
            'revenue_month': rev_month,
            'profit_month': prof_month,
            'orders_in_progress': orders_in_progress,
            'orders_new': orders_new,
            'overdue_stages_count': overdue_stages_count,
            'top_workers': top_workers,
            'trend_data': trend_data
        })

class StageActionView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, action_type):
        stage_id = request.data.get('item_stage_id')
        note = request.data.get('note', '')
        try:
            item_stage = ItemStage.objects.get(id=stage_id)
        except ItemStage.DoesNotExist:
            return Response({'error': 'Not found'}, status=404)

        worker = getattr(request.user, 'worker', None)

        if action_type == 'complete':
            item_stage.status = 'done'
            item_stage.completed_at = timezone.now()
            if worker:
                item_stage.assigned_worker = worker
            item_stage.save()

            order = item_stage.item.order

            # Move order to in_progress as soon as any stage is completed
            if order.status == 'new':
                order.status = 'in_progress'
                order.save()

            # Make next stage active
            next_stage = ItemStage.objects.filter(
                item=item_stage.item,
                stage__order__gt=item_stage.stage.order
            ).exclude(status='done').order_by('stage__order').first()

            if next_stage:
                next_stage.status = 'active'
                next_stage.save()
            else:
                # All stages done, check if order is done
                if not ItemStage.objects.filter(item__order=order).exclude(status='done').exists():
                    order.status = 'done'
                    order.save()

            return Response({'status': 'success'})

        elif action_type == 'return-back':
            # Previous stage
            prev_stage = ItemStage.objects.filter(
                item=item_stage.item,
                stage__order__lt=item_stage.stage.order
            ).order_by('-stage__order').first()

            if prev_stage:
                prev_stage.status = 'issue'
                prev_stage.note = note
                prev_stage.returned_at = timezone.now()
                if worker:
                    prev_stage.returned_by = worker
                prev_stage.save()
                
                item_stage.status = 'done'
                item_stage.completed_at = timezone.now()
                if worker:
                    item_stage.assigned_worker = worker
                item_stage.save()
            
            return Response({'status': 'returned'})
        
        return Response({'error': 'Invalid action'}, status=400)
