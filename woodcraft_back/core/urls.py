from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AuthView, MeView, StageTemplateViewSet, ProductViewSet, WorkerViewSet,
    OrderTemplateViewSet, OrderViewSet, ItemStageViewSet,
    DashboardView, StageActionView, AnalyticsView
)

router = DefaultRouter()
router.register(r'stage-templates', StageTemplateViewSet, basename='stage-template')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'workers', WorkerViewSet, basename='worker')
router.register(r'templates', OrderTemplateViewSet, basename='template')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('auth/login/', AuthView.as_view(), name='login'),
    path('auth/logout/', AuthView.as_view(), name='logout'),
    path('me/', MeView.as_view(), name='me'),
    
    path('', include(router.urls)),
    
    # Custom route for item stages update (if needed, DRF router provides /orders/{id}/items/ inside OrderViewSet via @action)
    # The requirement asks for PATCH /api/orders/{id}/items/{item_id}/stages/{stage_id}/
    # So we expose ItemStage directly to allow PATCH
    path('item-stages/<int:pk>/', ItemStageViewSet.as_view({'patch': 'partial_update'}), name='itemstage-detail'),
    
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('analytics/', AnalyticsView.as_view(), name='analytics'),
    path('stage/<str:action_type>/', StageActionView.as_view(), name='stage-action'),
]
