from django.urls import path, include
from django.conf.urls.static import static
from .views import JobViewSets, UserViewSets, CompanyViewSets
from rest_framework import routers

# create a router
router = routers.DefaultRouter()
router.register(r'jobs', JobViewSets)
router.register(r'user', UserViewSets)
router.register(r'company', CompanyViewSets)
print(router.urls)

urlpatterns = [
    path('', include(router.urls), name="Default")
]