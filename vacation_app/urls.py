from django.conf.urls import url, include

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
# from rest_framework.urlpatterns import format_suffix_patterns

from vacation_app.views.delivery import DeliveryViewSet
from vacation_app.views.vacation import VacationViewSet
from vacation_app.views.employee import EmployeeViewSet


router = DefaultRouter()
router.register(r'users', EmployeeViewSet)
router.register(r'vacations', VacationViewSet)
router.register(r'mails', DeliveryViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-token-auth/', obtain_auth_token),
]

# @urlpatterns = format_suffix_patterns(urlpatterns)
