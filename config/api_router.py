from rest_framework.routers import DefaultRouter

from joinup.profiles import api_view as profiles_views


router = DefaultRouter()


router.register(r'profiles', profiles_views.ProfileUserViewSet, basename='profiles')

app_name = "api"
urlpatterns = router.urls