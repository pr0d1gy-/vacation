from django.conf.urls import url, include

from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from vacation_app import views


router = DefaultRouter()
router.register(r'users', views.EmployeeViewSet)
router.register(r'vacations', views.VacationViewSet)
router.register(r'mails', views.DeliveryViewSet)

urlpatterns = [
    url(r'user/(?P<id_user>[0-9]+)/vacation/$', views.VacationViewSet.as_view({
        'get': 'list',
    })),
    url(r'^', include(router.urls)),
    url(r'^api-token-auth/', obtain_auth_token),
]

#@urlpatterns = format_suffix_patterns(urlpatterns)
