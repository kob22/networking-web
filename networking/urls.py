from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path, reverse_lazy
from django.views.generic.base import RedirectView

urlpatterns = [
    # the 'api-root' from django rest-frameworks default router
    # http://www.django-rest-framework.org/api-guide/routers/#defaultrouter
    path("api/", include("friendship.urls", namespace="friendship")),
    re_path(r"^$", RedirectView.as_view(url=reverse_lazy("api-root"), permanent=False)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
