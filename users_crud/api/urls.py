from rest_framework.routers import DefaultRouter
from users_crud.api.views import DeviceTypeView, DeviceView, UserProfilView , LoginAPI


router = DefaultRouter()
router.register(r'users_profile', UserProfilView, basename='users_profile')
router.register(r'devices', DeviceView, basename='devices')
router.register(r'device_types', DeviceTypeView, basename='device_types')
urlpatterns = router.urls
