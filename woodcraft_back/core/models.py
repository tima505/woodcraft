from django.db import models
from django.contrib.auth.models import User

class StageTemplate(models.Model):
    """Global stage template that can be reused across products."""
    name = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Stage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stages')
    name = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=1)
    
    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.product.name} - {self.name}"

class Worker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stages = models.ManyToManyField(StageTemplate, blank=True)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class OrderTemplate(models.Model):
    name = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    cost_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    sale_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS = [('new','new'),('in_progress','in_progress'),('done','done'),('defect','defect')]
    client_name = models.CharField(max_length=200)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    description = models.TextField(blank=True)
    quantity = models.PositiveIntegerField(default=1)
    cost_price = models.DecimalField(max_digits=12, decimal_places=2)
    sale_price = models.DecimalField(max_digits=12, decimal_places=2)
    note = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='new')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.pk} - {self.client_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    number = models.PositiveIntegerField()

    def __str__(self):
        return f"Item {self.number} (Order {self.order.pk})"

class ItemStage(models.Model):
    STATUS = [('pending','pending'),('active','active'),('done','done'),('issue','issue')]
    item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='stages')
    stage = models.ForeignKey(Stage, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    assigned_worker = models.ForeignKey(Worker, null=True, blank=True, on_delete=models.SET_NULL)
    deadline = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    returned_at = models.DateTimeField(null=True, blank=True)
    returned_by = models.ForeignKey(Worker, null=True, blank=True, on_delete=models.SET_NULL, related_name='returned_stages')
    note = models.TextField(blank=True)

    def __str__(self):
        return f"{self.item} - {self.stage.name}"
