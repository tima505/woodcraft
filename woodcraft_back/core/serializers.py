from rest_framework import serializers
from .models import StageTemplate, Product, Stage, Worker, OrderTemplate, Order, OrderItem, ItemStage
from django.contrib.auth.models import User

class StageTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StageTemplate
        fields = ['id', 'name', 'created_at']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']

class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = ['id', 'name', 'order']

class ProductSerializer(serializers.ModelSerializer):
    stages = StageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'created_at', 'stages']

class WorkerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    stages = StageTemplateSerializer(many=True, read_only=True)
    stage_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=StageTemplate.objects.all(), source='stages', write_only=True
    )
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Worker
        fields = ['id', 'user', 'stages', 'stage_ids', 'username', 'password', 'first_name']

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        first_name = validated_data.pop('first_name', '')
        stages = validated_data.pop('stages', [])
        
        user = User.objects.create_user(username=username, password=password, first_name=first_name)
        worker = Worker.objects.create(user=user)
        worker.stages.set(stages)
        return worker

class OrderTemplateSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = OrderTemplate
        fields = ['id', 'name', 'product', 'product_details', 'description', 'cost_price', 'sale_price']

class ItemStageSerializer(serializers.ModelSerializer):
    stage = StageSerializer(read_only=True)
    assigned_worker = WorkerSerializer(read_only=True)

    class Meta:
        model = ItemStage
        fields = ['id', 'item', 'stage', 'status', 'assigned_worker', 'deadline', 'started_at', 'completed_at', 'returned_at', 'returned_by', 'note']

class OrderItemSerializer(serializers.ModelSerializer):
    stages = ItemStageSerializer(many=True, read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'number', 'stages']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    product_details = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'client_name', 'product', 'product_details', 'description', 'quantity', 'cost_price', 'sale_price', 'note', 'status', 'created_at', 'items']
