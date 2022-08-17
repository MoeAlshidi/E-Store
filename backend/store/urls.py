
from django.urls import path
from rest_framework_nested import routers
from . import views

router=routers.DefaultRouter()
router.register('product',views.ProductViewSet, basename='product')
router.register('collection',views.CollectionViewSet)
product_router=routers.NestedDefaultRouter(router, 'product',lookup='product')
product_router.register('reviews',views.ReviewViewSet, basename='product_reviews')




urlpatterns=router.urls + product_router.urls
