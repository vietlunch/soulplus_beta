from django.conf.urls import url, include
from django.views.generic import TemplateView


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="index.html")),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
