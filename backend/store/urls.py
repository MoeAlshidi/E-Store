
from django.urls import path
from rest_framework_nested import routers
from . import views

router=routers.DefaultRouter()
router.register('products',views.ProductViewSet, basename='products')
router.register('collections',views.CollectionViewSet)
router.register('carts',views.CartViewSet,basename='carts')

product_router=routers.NestedDefaultRouter(router, 'products',lookup='product')
product_router.register('reviews',views.ReviewViewSet, basename='products_reviews')

cart_items=routers.NestedDefaultRouter(router,'carts',lookup='cart')
cart_items.register('items',views.CartItemViewSet,basename='cart-items')




urlpatterns=router.urls + product_router.urls + cart_items.urls
