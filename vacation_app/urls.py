from django.conf.urls import url, include

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from vacation_app.views import *
from vacation_app.views import authorization


router = DefaultRouter()
router.register(r'users', EmployeeViewSet)
router.register(r'vacations', VacationViewSet)
router.register(r'mails', DeliveryViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-token-auth/', authorization.TokenAuthWithIdNameGroup.as_view()),
]
