from rest_framework import routers, views

router = routers.DefaultRouter()
router.register(r'car_brand', views.CarBrandViewSet)

urlpatterns = router.urls