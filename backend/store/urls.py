from django.urls import path
from rest_framework.routers import SimpleRouter
from . import views

router=SimpleRouter()
router.register('product',views.ProductViewSet)
router.register('collection',views.CollectionViewSet)



urlpatterns=router.urls
